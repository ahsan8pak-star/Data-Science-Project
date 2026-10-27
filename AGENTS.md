# AGENTS.md — root entrypoint

Markdown reference: [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)

---

The full instruction set lives in `agentic_models/AGENTS.md` (read it before
acting). This file is the compact version: only what an agent is likely to
miss. Rule 14 (context-first) applies in both Plan and Build mode.

## Commands

- .venv-win access: `(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& c:\Users\A.I.M\C.S\Data-Science-Project\.venv-win\Scripts\Activate.ps1)`
- .venv-wsl access: `source .venv-wsl/bin/activate`
- Windows interpreter: `.venv-win/Scripts/python.exe` (3.14.5).
- WSL/Linux interpreter: `.venv-wsl/bin/python` (3.12.3).
- Full suite: `.venv-win/Scripts/python.exe -m pytest` (2042 passed).
- WSL suite: `.venv-wsl/bin/python -m pytest` (2042 passed).
- One test file: `.venv-win/Scripts/python.exe -m pytest tests/test_scripts/test_repo_doc_numbers.py`
- Never use bare `python`/`python3` — it resolves to the system interpreter.
- Bare `pytest` works after activation; still prefer `python -m pytest` for reproducibility.
- `-ra` is in addopts, so skipped tests print their reason in the summary alongside other non-passing outcomes. Use `-W error` to turn warnings into failures when triaging.

## Architecture

- Python is primary. Java is checked statically from `university_courseworks/.../cs1op/coursework/ai_parity_cases.json`.
- `agentic_models/AGENTS.md` holds the rules, rotation tables and model ceilings. `agentic_models/TASK_MODEL_GUIDE.md` maps tasks to models and effort levels.
- `git_repo_progress/PROGRESSION.md` — session log (rule 13, append-only).
- `git_repo_progress/HISTORY_REVIEW.md` — WWW/EBI retrospective.
- Two venvs, named per platform: `.venv-win/` and `.venv-wsl/`. Both are ignored by git.

## Key rules

- **Rule 12** — conventional `type(scope):` commit subjects (every commit carries a scope naming the file or folder touched).
- **Rule 13** — a session-log row per session in `git_repo_progress/PROGRESSION.md`; historical rows append-only.
- **Rule 14** — read relevant context before acting (Plan and Build). Ask when the fit is suboptimal.
- Coverage: `branch = true`, `source = python`, 99% lines / 95% branch.
- Docs and guards must agree: test counts, coverage figures, README tree, file scores. A stale number must fail the suite.

## Model discipline — does the model interrupt to offer a better alternative?

**No.** An agent cannot switch models mid-session — model selection happens in the OpenCode console (`/models`), not from inside a conversation. What the agent *does* do:

- Before a long run, or when a model feels wrong, pause and **ask the user** whether to switch to a better free model. Do not silently continue on a suboptimal model.
- If the task is wrong for the current model (wrong window, wrong variant/effort level, logged route), **decline and recommend three ranked models, best first**, with a one-line reason each. Name what has *not* been done yet. Nothing is edited until A.I.M picks a model.
- Variants/effort levels (where a model offers them) run `low` → `medium` → `high` → `xhigh` → `max`. Pick the lowest level that solves the task; `max` on a trivial task is waste, not quality. Space Bunny offers the full range; most models in the rotation run at a fixed effort.
- For simple mechanical repo operations — `git status`, `git add`, `git commit`, `git push`, `git pull`, branch syncs, simple PR text, and sync scripts — prefer the smallest model that can do the job. The default is `Ling 3.1 Flash Free` or `Ling 3.0 Flash Fin Free`; use `MiMo-V2.6-Flash Free` for short commit-message drafting, and keep `Space Bunny`, `LongCat`, and the large reasoning models for the long-context or debugging tasks.

Check the model is correct, reasonable and efficient for the task: token cost, time, and variant/effort level. A larger window is not always better — a 256K model is the right tool for a single-file edit.

Verify route ceilings from the `models.dev` registry, not a model card: MiMo-V2.6-Flash is 200,000 on this route and 1,048,576 elsewhere.

Privacy: Space Bunny Free and LongCat 2.5 Preview Free are zero-retention. Everything else may train on data. Do not send personal data to a non-zero-retention route.

If a model is missing from the Zen `/models` list, treat it as a reason to pick the next-best row, not to force a removed route.

## Project rules (load-bearing, not optional)

- **The OOP lane is frozen.** `python/object_oriented_programming/` — specifically `decorator.py`, `generator.py`, `multitasking.py`, `dice.py` — must not be moved, renamed, or have imports rewritten.
- **Never commit `.env`** — it holds local credentials and is gitignored.
- **`transactions.py` saves `transactionv1.xlsx` to the current working directory** via a relative path. Do not "fix" it — tests encode this CWD-relative behaviour with `monkeypatch.chdir(tmp_path)`.
- **`qrcode_generator.py` saves PNGs relative to the CWD** — do not hardcode the script's own directory. Tests point it at `tmp_path`.
- **Entry points are content-named, not `def main()`.** Only `imperative_programming/fundamental_topics/main.py` keeps `def main()` by design.
- **Text files are LF**, enforced by `.gitattributes` (`* text=auto eol=lf`, with `.joblib` / `.xlsx` / `.pdf` marked binary).

## Commit conventions

- Standard prefixes: `feat`, `fix`, `docs`, `refactor`, `test`, `style`, `chore`, `ci`.
- Every commit carries a scope naming the file or folder touched: `fix(generator.py): resolve import error`, not `fix: resolve import error`.
- Non-standard prefixes like `file(...)` break commitlint, changelogs and Semantic Release.

## WWW / EBI (What Went Well / Evidence-Based Improvements)

The retrospective in `git_repo_progress/HISTORY_REVIEW.md` (554 lines) applies this framework to the whole 22-week record. Preserve its lessons:

- **What worked:** context-first rule 14, conventional commits (rule 12), pinned interpreters, guards that make stale numbers fail, branch coverage, two-tier weighting in `FILE_RANKING_GUIDE.md`.
- **What went wrong:** 123 scope-less commits in June against 2 in October; mass mechanical commits of 82–261 files; the `Python/` → `python/` case rename done as a two-hop; an 886-line README diff inside one path commit.
- **Evidence-based improvements:** `.mailmap` for identity, a guard that fails on being correct (fixed by checking internal consistency instead), the 14.7% test-asserting-the-repo tripwire, and a ratchet rather than a tripwire on coverage figures.
- A suite that only ever ran on one operating system was not cross-platform; platform limitations must be named in `skipif` reasons, not hidden.

## When updating docs

- Bump the suite count everywhere it is quoted (AGENTS.md, PROGRESSION.md, FILE_RANKING_GUIDE.md).
- Refresh coverage figures and their retrieval date together.
- Record whether a model was removed because it was discontinued or because it was unwanted — the distinction matters later.
