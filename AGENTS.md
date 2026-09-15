# AGENTS.md — Project Instructions for AI Agents and Collaborators

This file is the single source of truth for how this repository works. Any AI
agent (or future human) working on this project should read this first.

## Project Overview

- Personal data-science learning journey: Python (imperative → functional →
  object-oriented) → PostgreSQL → Machine Learning (visualisation, cleaning,
  modelling).
- Python 3.14 venv lives at `.venv/`. Always invoke it explicitly.
- All scripts live under `python/<paradigm>/<folder>/`. Tests live under
  `tests/<area>/` and mirror the source folders 1:1.
- `README.md` describes the full architecture; keep its tree and headers in
  sync when folders/files move.

## Running Things

| Task | Command |
| --- | --- |
| Run the full test suite | `.venv/Scripts/python.exe -m pytest` |
| Run one test folder | `.venv/Scripts/python.exe -m pytest tests/test_imperative_programming/` |
| Run one test file | `.venv/Scripts/python.exe -m pytest tests/test_imperative_programming/test_unit_and_format_converters.py` |
| Coverage report (term + missing lines) | `.venv/Scripts/python.exe -m pytest --cov --cov-report=term-missing` |
| Interactive project tree + benchmark | `.venv/Scripts/python.exe scripts/execution_time.py` |
| Project tree in non-interactive `--all` mode | `.venv/Scripts/python.exe scripts/execution_time.py --all` |

> Use the Windows venv python (`.venv/Scripts/python.exe`), NOT a plain `python`
> / `python3` — the repo is pinned to that interpreter.

## Project Rules (Do NOT break these)

1. **The OOP lane is frozen.** `python/object_oriented_programming/` —
   specifically `decorator.py`, `generator.py`, `multitasking.py`, `dice.py` —
   must not be moved, renamed, or have imports rewritten. (Known typo in
   `classes.py:11` - `object_orienteded_programming` - is documented, not fixed.)
2. **No comments in code unless explicitly asked.** Coursework scripts are
   heavily commented; do NOT strip existing comments, but do not add new ones
   unless the user requests them.
3. **`transactions.py` filename bug is intentional.** It saves
   `transactionv1.xlsx` to the *current working directory* via a relative
   `wb.save(...)`. Do not "fix" it. Tests encode this CWD-relative behaviour
   with `monkeypatch.chdir(tmp_path)`.
4. **`qrcode_generator.py` saves PNGs relative to the CWD** (uses
   `os.getcwd()`), so tests can point it at `tmp_path`. Do not hardcode the
   script's own directory.
5. **Keep the OOP lane frozen and the imperative lane clean** — files added to
   `python/imperative_programming/` should match their folder's theme exactly
   (`syntax_exercises`, `unit_and_format_converters`, `interactive_games`,
   `math_and_science_calculators`, `fundamental_topics`).
6. **Do not touch `.env`** — it holds local credentials, is gitignored, and is
   never committed.
7. **Keep README tree + `TREE_SKIP` in sync** when folders are added/removed.
   `TREE_SKIP` in `scripts/execution_time.py` excludes generated/vendored paths
   (`.git`, `.venv`, `.pytest_cache`, `__pycache__`, `.coverage`, `htmlcov`).

## Commit Conventions (Conventional Commits)

Standard prefixes give automated tools (release pipelines, linters, changelogs)
structured history and keep the log scannable:

| Prefix | Usage | Example |
| --- | --- | --- |
| `feat` | New feature / new source file / new script | `feat: create generator.py script` |
| `fix` | Patches a bug or resolves a runtime error | `fix: resolve timing drift in clock loop` |
| `docs` | Documentation only (README, docstrings, notes) | `docs: update setup commands in README` |
| `refactor` | Restructure/move code without changing behaviour | `refactor: move alarm_clock.py to syntax_exercises` |
| `test` | Add or modify automated tests (pytest) | `test: add coverage for invalid period input` |
| `style` | Formatting only — no logic changes | `style: format imports and docstrings` |
| `chore` | Maintenance, deps, build config, `.gitignore` | `chore: update dependencies in requirements.txt` |
| `ci` | CI / pipeline workflow changes | `ci: add automated pytest execution workflow` |

### Rules of thumb

- **Creating a file** → primary `feat`; use `test` for a new test file, `docs`
  for documentation, `chore` for config like `.gitignore`.
  - `git add <file_path>` then `git commit -m "feat: create <file_name>"`
- **Running a file** → Git tracks changes, not local execution. Execution gets
  committed under `ci` (automated workflows) or `chore`.
- **Moving / relocating a file** → `refactor`.
  - `git mv <old_path> <new_path>` then
    `git commit -m "refactor: relocate <file_name>"`
- **Referencing a specific file** → use the file name as the *scope* inside
  parentheses, e.g. `refactor(alarm_clock.py): move to syntax_exercises`,
  `fix(generator.py): resolve import error`. This keeps the standard prefix
  (machine-readable) while keeping the file explicit (human-readable).
- **Avoid non-standard prefixes** like `file(...)`. They work for solo repos
  but break commit linters (`commitlint`), changelog generators, and Semantic
  Release, which only understand the standard types.

## Git Workflow — Status Message Meanings

| Command | Output | Meaning |
| --- | --- | --- |
| `git status` | `On branch main / up to date with 'origin/main'` | Working tree clean; local matches remote |
| `git status` | `Changes not staged for commit:` | Files modified locally, not yet `git add`ed |
| `git status` | `Untracked files:` | New files not yet tracked by Git |
| `git add .` | *(silent)* | Staged all changes for the next commit |
| `git commit -m "msg"` | `[main 1a2b3c4] feat: add module` | New snapshot created locally |
| `git push origin main` | `To github.com:... main -> main` | Local commit history uploaded to remote |
| `git push` | `[rejected] (fetch first)` | Remote has commits you lack; run `git pull` first |
| `git pull` | `Already up to date.` | Local is synced with remote |
| `git pull` | `Updating 1a2b3c4..5d6e7f8` | Fetched and merged remote changes |
| `git merge <branch>` | `CONFLICT (content): file.py` | Overlapping changes; resolve manually |

### Remote / mirror workflow

- There are **two remote namespaces** (`origin` and `github`), each carrying 4
  push URLs: GitHub Project, GitHub Backup, GitLab Project, GitLab Backup.
- Push once to `origin`, and all 4 mirrors update:
  `git push origin main`
- Never force-push to `main`.

## Feature Summary (what exists today)

- 92 imperative scripts, 19 functional, 41 OOP, plus `advanced_projects`
  (machine_learning notebooks, transactions xlsx pipeline, music player).
- 1112 passing tests, ~93% coverage. `conftest.py` per area provides
  `run_script()` which runs scripts via `runpy` with mocked `input()` /
  `time.sleep()` and optional `cwd` for file-writing tests.
- `scripts/execution_time.py`: interactive `tree /f`-style project map +
  per-folder benchmark report (`PASS`/`FAIL`/`TIMEOUT`/`ERROR`).
- Postgres is planned (`psycopg2` installed, `postgresql/sandbox/aim.sql`
  reserved) but not started.