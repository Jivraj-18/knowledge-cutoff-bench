#!/usr/bin/env python3
"""Run benchmark tasks against Claude models via `claude -p` headless mode."""
import argparse
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS_DIR = ROOT / "tasks"
RESULTS_DIR = ROOT / "results"
ENVS_DIR = ROOT / "envs"

MODELS = ["claude-opus-4-6", "claude-opus-5-5"]
DEFAULT_EFFORT = "medium"
DEFAULT_SAMPLES = 1
DEFAULT_CONCURRENCY = 2
CLAUDE_TIMEOUT = 600
TEST_TIMEOUT = 120

CODE_BLOCK_RE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.DOTALL)

_jsonl_locks: dict[str, threading.Lock] = {}
_jsonl_locks_guard = threading.Lock()


def jsonl_lock(path: Path) -> threading.Lock:
    with _jsonl_locks_guard:
        return _jsonl_locks.setdefault(str(path), threading.Lock())


def extract_first_python(text: str) -> str | None:
    m = CODE_BLOCK_RE.search(text or "")
    return m.group(1) if m else None


def call_claude(prompt: str, model: str, effort: str) -> dict:
    """Run `claude -p` in a fresh empty temp dir outside the project."""
    with tempfile.TemporaryDirectory(prefix="claude-run-", dir="/tmp") as tmp:
        env = os.environ.copy()
        # --safe-mode disables user CLAUDE.md, hooks, plugins, MCP, skills, etc.
        # while keeping auth and model selection working normally.
        cmd = [
            "claude", "-p", prompt,
            "--model", model,
            "--output-format", "json",
            "--tools", "",
            "--effort", effort,
            "--permission-prompts", "none",
            "--setting-sources", "",
            "--safe-mode",
            "--no-session-persistence",
        ]
        proc = subprocess.run(
            cmd, cwd=tmp, env=env,
            capture_output=True, text=True, timeout=CLAUDE_TIMEOUT,
        )
    out = proc.stdout.strip()
    # Output is a single JSON object; strip anything after if present.
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        # Try to find the first {...} block
        start = out.find("{")
        if start >= 0:
            return json.loads(out[start:])
        raise RuntimeError(f"claude did not return JSON: stderr={proc.stderr[:400]}")


def grade(code: str, task: dict) -> tuple[bool, str]:
    env_py = ENVS_DIR / task["env"] / "bin" / "python"
    task_dir = TASKS_DIR / task["id"]
    with tempfile.TemporaryDirectory(prefix="grade-", dir="/tmp") as tmp:
        tmpd = Path(tmp)
        (tmpd / "solution.py").write_text(code)
        shutil.copy(task_dir / "test_task.py", tmpd / "test_task.py")
        try:
            r = subprocess.run(
                [str(env_py), "test_task.py"],
                cwd=tmpd, capture_output=True, text=True, timeout=TEST_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            return False, "TIMEOUT"
        passed = r.returncode == 0 and "PASS" in r.stdout
        err_src = r.stderr.strip() or r.stdout.strip()
        last_err = (err_src.splitlines() or [""])[-1][:200]
        return passed, last_err


def classify_failure(passed: bool, code: str | None, task: dict) -> str | None:
    if passed:
        return None
    if code is None:
        return "no_code"
    if task["direction"] == "legacy":
        for marker in task.get("leak_markers", []):
            if marker in code:
                return "leak"
    return "other"


def run_one(task: dict, model: str, sample: int, effort: str, runs_path: Path,
            raw_dir: Path, code_dir: Path) -> dict | None:
    task_id = task["id"]
    tag = f"{task_id}__s{sample}"
    raw_path = raw_dir / f"{tag}.json"
    code_path = code_dir / f"{tag}.py"

    # Resume: skip if raw + runs line already exist for this (task, sample, model).
    if raw_path.exists() and _run_exists(runs_path, task_id, sample):
        return None

    prompt = (TASKS_DIR / task_id / "prompt.md").read_text()
    t0 = time.time()
    try:
        resp = call_claude(prompt, model, effort)
    except Exception as e:
        rec = {
            "task_id": task_id, "sample": sample, "direction": task["direction"],
            "library": task["library"], "model": model, "effort": effort,
            "passed": False, "failure_type": "other", "error": f"call_failed: {e}"[:200],
            "input_tokens": 0, "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0, "output_tokens": 0, "thinking_tokens": 0,
            "cost_usd": 0.0,
            "duration_ms": int((time.time() - t0) * 1000), "model_id_reported": None,
        }
        _append_jsonl(runs_path, rec)
        return rec

    raw_path.write_text(json.dumps(resp, indent=2))

    text = resp.get("result", "") or ""
    code = extract_first_python(text)
    if code is not None:
        code_path.write_text(code)

    if code is None:
        passed, err = False, "no_code"
    else:
        passed, err = grade(code, task)

    usage = resp.get("usage", {}) or {}
    model_usage = resp.get("modelUsage", {}) or {}
    reported_model = next(iter(model_usage.keys()), None)

    rec = {
        "task_id": task_id,
        "sample": sample,
        "direction": task["direction"],
        "library": task["library"],
        "model": model,
        "model_id_reported": reported_model,
        "effort": effort,
        "passed": passed,
        "failure_type": classify_failure(passed, code, task),
        "error": err,
        "input_tokens": usage.get("input_tokens", 0),
        "cache_creation_input_tokens": usage.get("cache_creation_input_tokens", 0),
        "cache_read_input_tokens": usage.get("cache_read_input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "thinking_tokens": (usage.get("output_tokens_details") or {}).get("thinking_tokens", 0),
        "cost_usd": resp.get("total_cost_usd", 0.0),
        "duration_ms": resp.get("duration_ms", int((time.time() - t0) * 1000)),
    }
    _append_jsonl(runs_path, rec)
    return rec


def _append_jsonl(path: Path, rec: dict) -> None:
    with jsonl_lock(path):
        with path.open("a") as f:
            f.write(json.dumps(rec) + "\n")


def _run_exists(path: Path, task_id: str, sample: int) -> bool:
    if not path.exists():
        return False
    with jsonl_lock(path):
        with path.open() as f:
            for line in f:
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if r.get("task_id") == task_id and r.get("sample") == sample:
                    return True
    return False


def model_dirs(model: str, effort: str) -> tuple[Path, Path, Path, Path]:
    base = RESULTS_DIR / model / effort
    raw = base / "raw"
    code = base / "code"
    runs = base / "runs.jsonl"
    for p in (base, raw, code):
        p.mkdir(parents=True, exist_ok=True)
    return base, raw, code, runs


def regrade_all(models: list[str]) -> int:
    tasks_by_id = {t["id"]: t for t in json.loads((TASKS_DIR / "manifest.json").read_text())}
    code_re = re.compile(r"^(?P<tid>.+)__s(?P<s>\d+)\.py$")
    for model in models:
        model_base = RESULTS_DIR / model
        if not model_base.exists():
            continue
        effort_dirs = [p for p in sorted(model_base.iterdir())
                       if p.is_dir() and (p / "runs.jsonl").exists()]
        if not effort_dirs:
            print(f"[{model}] no effort subdirs with runs.jsonl, skipping")
            continue
        for base in effort_dirs:
            _regrade_dir(base, tasks_by_id, code_re, label=f"{model}/{base.name}")
    return 0


def _regrade_dir(base: Path, tasks_by_id: dict, code_re: re.Pattern, label: str) -> None:
    runs_path = base / "runs.jsonl"
    code_dir = base / "code"
    records = [json.loads(l) for l in runs_path.read_text().splitlines() if l.strip()]
    by_key = {(r["task_id"], r["sample"]): r for r in records}
    print(f"=== regrade {label} ({len(records)} records) ===")
    for p in sorted(code_dir.glob("*.py")) if code_dir.exists() else []:
        m = code_re.match(p.name)
        if not m:
            continue
        tid, s = m["tid"], int(m["s"])
        task = tasks_by_id.get(tid)
        if task is None:
            print(f"  [skip] {p.name}: unknown task_id")
            continue
        rec = by_key.get((tid, s))
        if rec is None:
            print(f"  [skip] {p.name}: no runs.jsonl entry")
            continue
        code = p.read_text()
        passed, err = grade(code, task)
        rec["passed"] = passed
        rec["failure_type"] = classify_failure(passed, code, task)
        rec["error"] = "PASS" if passed else err
        print(f"  {tid:30} s{s} pass={passed!s:5} ft={rec['failure_type']}")
    with runs_path.open("w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print(f"  wrote {runs_path}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=DEFAULT_SAMPLES)
    ap.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY,
                    help="Threads per model.")
    ap.add_argument("--effort", default=DEFAULT_EFFORT)
    ap.add_argument("--models", nargs="+", default=MODELS)
    ap.add_argument("--tasks", nargs="*", default=None, help="Subset of task IDs.")
    ap.add_argument("--regrade", action="store_true",
                    help="Re-grade existing saved code against current test_task.py, "
                         "rewriting runs.jsonl. Does not call any model.")
    args = ap.parse_args()

    if args.regrade:
        return regrade_all(args.models)

    all_tasks = json.loads((TASKS_DIR / "manifest.json").read_text())
    if args.tasks:
        all_tasks = [t for t in all_tasks if t["id"] in set(args.tasks)]

    for model in args.models:
        base, raw, code, runs = model_dirs(model, args.effort)
        print(f"=== {model} (effort={args.effort}, N={args.samples}, "
              f"conc={args.concurrency}) -> {base} ===", flush=True)
        jobs = [(t, s) for t in all_tasks for s in range(1, args.samples + 1)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as ex:
            futs = {ex.submit(run_one, t, model, s, args.effort, runs, raw, code): (t["id"], s)
                    for t, s in jobs}
            for fut in concurrent.futures.as_completed(futs):
                tid, s = futs[fut]
                try:
                    rec = fut.result()
                except Exception as e:
                    print(f"  [ERROR] {tid} s{s}: {e}", flush=True)
                    continue
                if rec is None:
                    print(f"  [skip] {tid} s{s} (already done)", flush=True)
                else:
                    print(f"  {tid:30} s{s} pass={rec['passed']!s:5} "
                          f"ft={rec['failure_type']} dur={rec['duration_ms']}ms "
                          f"cost=${rec['cost_usd']:.4f}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
