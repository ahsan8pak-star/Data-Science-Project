# AGENTS.md — root entrypoint

The full instruction set lives in `agentic_models/AGENTS.md` (read it before
acting). This file is the compact version: only what an agent is likely to
miss. Rule 14 (context-first) applies in both Plan and Build mode.

## Commands

- Windows interpreter: `.venv-win/Scripts/python.exe` (3.14.5).
- WSL/Linux interpreter: `.venv-wsl/bin/python` (3.12.3).
- Full suite: `.venv-win/Scripts/python.exe -m pytest` (1990 passed).
- WSL suite: `.venv-wsl/bin/python -m pytest` (1800 passed, 12 skipped).
- Never use bare `python`/`python3` — it resolves to the system interpreter.
- Bare `pytest` now works after activation (launchers were regenerated
  after the venv rename); still prefer `python -m pytest` for reproducibility.
- `-rs` is in addopts, so skipped tests print their reason. Warnings show by
  default; use `-W error` to turn them into failures when triaging.
- A moved .venv-wsl keeps working through `bin/python` while its console scripts
  fail; rewrite the shebangs and `VIRTUAL_ENV` lines after any move.

## Architecture

- Python is primary. Java is checked statically from
  `university_courseworks/.../cs1op/coursework/ai_parity_cases.json`.
- `agentic_models/AGENTS.md` holds the rules, rotation tables and model
  ceilings. `agentic_models/TASK_MODEL_GUIDE.md` maps tasks to models.
- `git_repo_progress/PROGRESSION.md` — session log (rule 13, append-only).
- `git_repo_progress/HISTORY_REVIEW.md` — WWW/EBI retrospective.
- Two venvs, named per platform: `.venv-win/` and `.venv-wsl/`. Both are ignored.

## Key rules

- **Rule 12** — conventional `type(scope):` commit subjects.
- **Rule 13** — a session-log row per session; historical rows append-only.
- **Rule 14** — read relevant context before acting (Plan and Build).
- Coverage: `branch = true`, `source = python`, 99% lines / 95% branch.
- Docs and guards must agree: test counts, coverage figures, README tree,
  file scores. A stale number must fail the suite.

## Model discipline

- The free rotation is twelve models; the registry now lists 44 zero-cost
  ones. The rotation is a shortlist, not a catalog.
- Before a long run, or when a model feels wrong, pause and ask the user
  whether to switch to a better free model. Do not silently continue on a
  suboptimal model.
- Check the model is correct, reasonable and efficient for the task: token
  cost, time, and the variant/effort level. A larger window is not always
  better; a 256K model is the right tool for a single-file edit.
- Verify route ceilings from the `models.dev` registry, not a model card:
  MiMo-V2.6-Flash is 200,000 on this route and 1,048,576 elsewhere.
- Privacy: Space Bunny Free and LongCat 2.5 Preview Free are zero-retention.
  Everything else may train on data. Do not send personal data to a
  non-zero-retention route.
- If a model is missing from the Zen `/models` list, treat it as a reason to
  pick the next-best row, not to force a removed route.

## WWW / EBI (What Went Well / Evidence-Based Improvements)

The retrospective in `git_repo_progress/HISTORY_REVIEW.md` (554 lines)
applies this framework to the whole 22-week record. Preserve its lessons:

- **What worked:** context-first rule 14, conventional commits (rule 12),
  pinned interpreters, guards that make stale numbers fail, the
  `run_script()` harness, branch coverage, the two-tier weighting in
  `FILE_RANKING_GUIDE.md`.
- **What went wrong:** 123 scope-less commits in June against 2 in October;
  mass mechanical commits of 82–261 files; the `Python/` → `python/` case
  rename done as a two-hop; an 886-line README diff inside one path commit.
- **Evidence-based improvements:** `.mailmap` for identity, a guard that
  fails on being correct (fixed by checking internal consistency instead),
  the 14.7% test-asserting-the-repo tripwire, and a ratchet rather than a
  tripwire on coverage figures.
- A suite that only ever ran on one operating system was not cross-platform;
  platform limitations must be named in `skipif` reasons, not hidden.

## When updating docs

- Bump the suite count everywhere it is quoted (AGENTS.md, PROGRESSION.md,
  FILE_RANKING_GUIDE.md).
- Refresh coverage figures and their retrieval date together.
- Record whether a model was removed because it was discontinued or because
  it was unwanted — the distinction matters later.
