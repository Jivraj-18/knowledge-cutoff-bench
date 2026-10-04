# Do newer models get confused by newer APIs? A small benchmark.

- **Repo:** https://github.com/Jivraj-18/knowledge-cutoff-bench
- **Site:** https://Jivraj-18.github.io/knowledge-cutoff-bench/

A 32-task benchmark that asks whether a model's published training cutoff
predicts what it actually knows, and whether a newer model leaks newer APIs
into code it is explicitly asked to write for a legacy version.

**Author:** Jivraj Shekhawat.
**Models compared:** Claude Opus 4.6 (training cutoff: August 2025) and
Claude Opus 5.5 (training cutoff: June 2026), both called through the Claude
Code CLI in headless mode (`claude -p`, tools disabled, fresh temp directory
per call, `--effort medium`).

## The question

Two things we hear a lot about model knowledge cutoffs:

1. "Older models can't know newer APIs" — so a model with an Aug 2025 cutoff
   should fail on an API shipped in June 2026.
2. "Newer models leak the latest APIs into older code" — a model with a June
   2026 cutoff, asked to write pandas 2.x code, will reach for pandas 3.0
   features it was trained on.

This benchmark tries to pressure-test both claims on real breaking changes.

## Setup

Each task is one of four kinds:

| direction      | what the task asks                                                                                            |
| -------------- | ------------------------------------------------------------------------------------------------------------- |
| `legacy`       | solve the problem on an older pinned version (e.g. pandas 2.3.3) — a newer-API answer fails.                  |
| `legacy_req`   | same, with an explicit "do not use the newer API" instruction in the prompt.                                  |
| `legacy_edit`  | same, but the prompt already contains legacy-style code to extend or clean, so the model follows the pattern. |
| `latest`       | solve the problem on the newer pinned version (e.g. Django 6.0) — a legacy-only answer fails.                 |

Breaking changes under test:

- pandas 2.3.3 → 3.0.6: `pd.col()`, new string dtype default, Copy-on-Write default.
- Django 5.2.17 → 6.0.6: built-in `ContentSecurityPolicyMiddleware`, template partials.
- pytest 8.4.2 → 9.0.3: built-in subtests.

Each task × model is run 5 times. Grading is deterministic: extract the first
```python fenced block, drop it next to the task's `test_task.py` in a fresh
temp directory, run it with the pinned env's Python, and check for `PASS` on
stdout and exit code 0. Every task was validated both ways before the run:
the reference solution passes and a solution written for the other version
fails (see `tasks/validation_log.txt`).

## Results

Pass rate by direction (5 samples × task):

| direction      | tasks | runs | Opus 4.6         | Opus 5.5         |
| -------------- | ----- | ---- | ---------------- | ---------------- |
| legacy         | 7     | 35   | 30/35 (85.7%)    | 35/35 (100.0%)   |
| legacy_req     | 7     | 35   | 30/35 (85.7%)    | 35/35 (100.0%)   |
| legacy_edit    | 8     | 40   | 40/40 (100.0%)   | 40/40 (100.0%)   |
| latest         | 10    | 50   | 26/50 (52.0%)    | 50/50 (100.0%)   |
| **total**      | 32    | 160  | **126/160 (78.8%)** | **160/160 (100.0%)** |

Pass rate by library:

| library | runs | Opus 4.6         | Opus 5.5         |
| ------- | ---- | ---------------- | ---------------- |
| django  | 70   | 40/70 (57.1%)    | 70/70 (100.0%)   |
| pandas  | 60   | 60/60 (100.0%)   | 60/60 (100.0%)   |
| pytest  | 30   | 26/30 (86.7%)    | 30/30 (100.0%)   |

Tokens and cost (160 runs per model):

|                        | Opus 4.6  | Opus 5.5                      |
| ---------------------- | --------- | ----------------------------- |
| input (fresh)          | 597,238   | 320                           |
| input (cache create)   | 0         | 56,857                        |
| input (cache read)     | 0         | 273,603                       |
| **total input**        | 597,238   | 330,780                       |
| output                 | 40,580    | 72,738                        |
| of which thinking      | 9,631     | 38,168                        |
| **cost (USD)**         | **$4.00** | **$1.97**                     |

Full per-task × per-sample numbers are in `results/<model>/medium/runs.jsonl`;
the raw model responses are in `results/<model>/medium/raw/` and the extracted
code is in `results/<model>/medium/code/`.

## Findings

Scoped strictly to what this run tested.

### 1. Zero newer-API leaks in 110 legacy runs per model

Across every `legacy`, `legacy_req` and `legacy_edit` run — 110 runs for each
of the two models — the saved code contained **zero** matches for the newer-API
leak markers listed in each task's `meta.json` (e.g. `pd.col(`,
`django.middleware.csp`, `SECURE_CSP`, `partialdef`). Opus 5.5's legacy
failures are not leaks; it just didn't produce passing code on a couple of
samples. Opus 4.6 failed the same way: wrong code, but not newer-API code.

On this task set, "the newer model will leak the new API into your legacy
code" was simply not observed.

### 2. Opus 4.6 fails every Django 6.0 task by inventing plausible APIs

Opus 4.6 scored **0/20** on the four Django 6.0 `latest` tasks
(`dj_N1_builtin_csp`, `dj_N2_builtin_csp_override`, `dj_N3_csp_nonce`,
`dj_N4_template_partials`). It did not refuse, and it did not say it was
unsure. It made up a settings schema that is close to a real third-party
library's — the `django-csp` package — rather than the actual built-in Django
6.0 API.

From `results/claude-opus-4-6/medium/code/dj_N1_builtin_csp__s1.py`:

```python
MIDDLEWARE_ENTRY = "django.middleware.security.SecurityMiddleware"

EXTRA_SETTINGS = {
    "CONTENT_SECURITY_POLICY": {
        "DIRECTIVES": {
            "default-src": ["'self'"],
            "img-src": ["'self'", "https:"],
        }
    }
}
```

Two inventions in six lines: it reused the long-standing `SecurityMiddleware`
(which doesn't set CSP headers), and it wrote a `CONTENT_SECURITY_POLICY` +
`DIRECTIVES` settings schema that matches the third-party `django-csp` package,
not Django 6.0's built-in — which uses `SECURE_CSP` and
`django.middleware.csp.ContentSecurityPolicyMiddleware`. The code is confident
and shaped like a real framework setting; it just isn't the one that exists.

### 3. Opus 4.6 used `pd.col` correctly, even though pandas 3.0 shipped after its cutoff

Both models scored 5/5 on both `pd.col` tasks (`pd_N1_col_expr` and
`pd_N1b_col_unnamed`).

`pd.col` landed on pandas' main branch on **2025-08-22** in
[PR #62103](https://github.com/pandas-dev/pandas/pull/62103)
([commit](https://github.com/pandas-dev/pandas/commit/188b2dae7df85a9c9945db39c5a23d23b1d4ce2e)) —
the same month as Opus 4.6's stated training cutoff, and months before pandas
3.0 shipped (Jan 2026). Opus 4.6 may have seen the PR, its discussion or the
merge, or inferred the API from Polars' `pl.col`; we can't tell which from
this experiment. Either way, release dates are a poor guide to what a model
knows.

### 4. Opus 5.5 was both more accurate and cheaper on this set

Opus 5.5 passed every one of the 160 runs (100%) for about **$1.97**. Opus
4.6 passed 126/160 (78.8%) for about **$4.00**. Opus 5.5's higher per-token
rate was more than offset by Opus Code's prompt-cache hits (273,603 cache-read
input tokens vs none for 4.6 in these runs) and shorter answers on the easy
tasks.

## Limitations

- **Scope:** one vendor, one model pair, 32 tasks, 5 samples per task × model.
  Not a generalizable benchmark; a probe.
- **Harness:** calls go through the Claude Code CLI in headless mode, so the
  Claude Code system prompt was in context on every call. The specific
  Content-Security-Policy string the Django 5.2 task asks for is also present
  in that system prompt text.
- **Thinking could not be matched.** At `--effort medium`, Opus 4.6 produced
  thinking tokens on only 8 of 160 runs (all on `dj_N4_template_partials` and
  `pd_N1b_col_unnamed`) — 9,631 thinking tokens in total. Opus 5.5 produced
  thinking on its runs throughout — 38,168 thinking tokens in total — and it
  could not be disabled in headless mode. So the pass-rate gap is partly a
  "allowed to think more" gap.
- **Grading flakes.** Two grading runs failed due to infrastructure errors
  (a numpy import failure and an interrupted process) and were re-executed;
  the model output was unchanged.
- **Third-party precursors.** Several of the "newer" APIs existed earlier as
  third-party packages (`django-csp`, `django-template-partials`, `django-tasks`,
  `pytest-subtests`); the tests require the built-in versions, so a
  reasonable-looking third-party pattern can score 0 as it did in finding 2.
- **No "obvious prior art" controls.** Some latest-direction features have
  obvious prior art in the ecosystem (e.g. Polars' `pl.col` resembles pandas'
  new `pd.col`), which makes "did it know the API?" and "did it generalise
  from a sibling library?" hard to separate — see finding 3.

## Reproduce

Prerequisites: Python 3.11+, `uv`, and a working `claude` CLI (Claude Code)
on `$PATH`.

```bash
# 1. Create the six pinned uv venvs (pandas 2/3, Django 5/6, pytest 8/9)
./setup_envs.sh

# 2. (Optional) Validate every task both ways: reference passes, wrong-version fails
python3 validate.py

# 3. Run the matrix. Default: both models × all tasks × 5 samples at --effort medium
python3 runner.py --samples 5 --concurrency 2

# 4. Summarise
python3 report.py --effort medium
```

`runner.py` saves one raw JSON per call under `results/<model>/<effort>/raw/`,
the extracted first python block under `.../code/`, and one line per run in
`.../runs.jsonl`. It skips runs it has already recorded, so you can resume
after an interruption. To re-execute grading against the saved code without
calling any model, run `python3 runner.py --regrade`.

### Adding a task

1. Create `tasks/<task_id>/` with `prompt.md`, `test_task.py`, a
   `reference_solution.py` that passes on the pinned env, and (recommended) a
   `wrong_version_solution.py` that fails on it.
2. Append a row to `tasks/manifest.json` with the task's `library`,
   `pinned_version`, `env`, `direction`, `change_id`, and any
   `leak_markers` (substrings of the newer API).
3. Re-run `python3 validate.py` to confirm the task discriminates.

### Adding a model

Pass it to the runner:

```bash
python3 runner.py --models claude-opus-4-6 claude-opus-5-5 claude-haiku-4-5 --samples 5
```

Any model name the local `claude` CLI accepts for `--model` will work.

## Credits & related reading

- [Microsoft Research, "Knowledge cutoff is a poor proxy for model capability"](https://www.microsoft.com/en-us/research/blog/evaluating-knowledge-cutoff-dates-is-trickier-than-it-looks/)
- Cheng et al., [*Dated Data: Tracing Knowledge Cutoffs in Large Language Models*](https://arxiv.org/abs/2403.12958)
- [LLMLagBench](https://github.com/mcevansayn/LLMLagBench)

## License

MIT. See [LICENSE](./LICENSE).
