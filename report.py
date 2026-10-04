#!/usr/bin/env python3
"""Summarize results produced by runner.py."""
import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
TASKS_DIR = ROOT / "tasks"

DIRECTIONS = ["legacy", "legacy_req", "legacy_edit", "latest"]


def load(model: str, effort: str) -> list[dict]:
    p = RESULTS_DIR / model / effort / "runs.jsonl"
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def pct(num: int, den: int) -> str:
    return f"{(100.0 * num / den):5.1f}%" if den else "   n/a"


def summarize(model: str, effort: str, runs: list[dict]) -> None:
    print(f"\n=== {model} / effort={effort} ({len(runs)} runs) ===")
    if not runs:
        print("  (no runs)")
        return

    by_dir = defaultdict(list)
    by_lib = defaultdict(list)
    for r in runs:
        by_dir[r["direction"]].append(r)
        by_lib[r["library"]].append(r)

    print("  Pass rate by direction:")
    ordered = [d for d in DIRECTIONS if d in by_dir] + \
              [d for d in sorted(by_dir) if d not in DIRECTIONS]
    for d in ordered:
        rs = by_dir[d]
        p = sum(1 for r in rs if r["passed"])
        print(f"    {d:12} {p:3}/{len(rs):3}  {pct(p, len(rs))}")

    print("  Pass rate by library:")
    for lib, rs in sorted(by_lib.items()):
        p = sum(1 for r in rs if r["passed"])
        print(f"    {lib:7} {p:3}/{len(rs):3}  {pct(p, len(rs))}")

    legacy_like = [r for r in runs if r["direction"].startswith("legacy")]
    leaks = sum(1 for r in legacy_like if r.get("failure_type") == "leak")
    print(f"  Leak rate on legacy*: {leaks}/{len(legacy_like)}  {pct(leaks, len(legacy_like))}")

    tot_in = sum(r.get("input_tokens", 0) for r in runs)
    tot_cc = sum(r.get("cache_creation_input_tokens", 0) for r in runs)
    tot_cr = sum(r.get("cache_read_input_tokens", 0) for r in runs)
    tot_out = sum(r.get("output_tokens", 0) for r in runs)
    tot_think = sum(r.get("thinking_tokens", 0) for r in runs)
    tot_cost = sum(r.get("cost_usd", 0.0) for r in runs)
    tot_in_all = tot_in + tot_cc + tot_cr
    print(f"  Input tokens: fresh={tot_in}  cache_create={tot_cc}  cache_read={tot_cr}  total_in={tot_in_all}")
    print(f"  Output tokens: {tot_out} (thinking={tot_think})")
    print(f"  Cost: ${tot_cost:.4f}")


def side_by_side(models: list[str], effort: str, all_runs: dict[str, list[dict]]) -> None:
    tasks = json.loads((TASKS_DIR / "manifest.json").read_text())
    print(f"\n=== Per-task comparison / effort={effort} ({' vs '.join(models)}) ===")
    hdr = f"  {'task':30} {'dir':12} " + " ".join(f"{m:>22}" for m in models)
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    for t in tasks:
        tid = t["id"]
        cells = []
        for m in models:
            rs = [r for r in all_runs[m] if r["task_id"] == tid]
            if not rs:
                cells.append(f"{'-':>22}")
                continue
            p = sum(1 for r in rs if r["passed"])
            leaks = sum(1 for r in rs if r.get("failure_type") == "leak")
            tag = f"{p}/{len(rs)}"
            if leaks:
                tag += f" leak={leaks}"
            cells.append(f"{tag:>22}")
        print(f"  {tid:30} {t['direction']:12} " + " ".join(cells))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--models", nargs="+",
                    default=["claude-opus-4-6", "claude-opus-5-5"])
    args = ap.parse_args()
    all_runs = {m: load(m, args.effort) for m in args.models}
    for m in args.models:
        summarize(m, args.effort, all_runs[m])
    if all(all_runs[m] for m in args.models):
        side_by_side(args.models, args.effort, all_runs)


if __name__ == "__main__":
    main()
