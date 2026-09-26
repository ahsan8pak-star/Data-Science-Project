# AGENTS.md — Project Instructions for AI Agents and Collaborators

This file is the single source of truth for how this repository works. Any AI
agent (or future human) working on this project should read this first.

## Project Overview

- Personal data-science learning journey: Python (imperative → functional →
  object-oriented) → PostgreSQL → Machine Learning (visualisation, cleaning,
  modelling).
- Authored by a single developer whose public identity is the initials
  **A.I.M** (the hardcoded `name = "A.I.M"` in several scripts is that
  personal signature, not placeholder text). The whole repo is his public
  portfolio.
- Python 3.14 venv lives at `.venv/`. Always invoke it explicitly.
- All scripts live under `python/<paradigm>/<folder>/`. Tests live under
  `tests/<area>/` and mirror the source folders 1:1.
- `README.md` describes the full architecture; keep its tree and headers in
  sync when folders/files move.

## Year 2 Transition (2026/27)

- The personal data-science journey has moved into **Year 2 of the degree**
  (University of Reading, 2026/27): the repo's Python, PostgreSQL and ML work
  now feeds the taught modules below instead of standing alone.
- **Semester 1** (Mon 28 Sep 2026 – Thu 17 Dec 2026):
  `CS2DA` Data Structures and Algorithms, `CS2PP` Programming in Python,
  `CS2SE` Software Engineering & Professional Development.
- **Semester 2** (Mon 1 Feb 2027 – Fri 28 May 2027):
  `CS2AI` Artificial Intelligence, `CS2ON` Operating Systems and Computer
  Networking, `CS2SD` Software Systems Design.
- Full week-by-week plans and readiness gaps live in the standalone
  `university_courseworks/year2/YEAR2_SEMESTER1.md` and
  `university_courseworks/year2/YEAR2_SEMESTER2.md`; keep them in sync when the
  module briefings or term dates change.

## Career Direction

- Post-university ladder (owner's own plan): **Data Analyst -> Data Science
  -> ML / AI models & agentics**, exited on demonstrated capability rather
  than tenure (work experience is the main gap).
- Stage-by-stage exit criteria, the two risk habits (analyst plateau and
  maths depth) and a capability-based timeline are tracked in `NOTES.md`
  under `## Career Direction`.

## AI Collaboration Style

- **Level calibration:** the owner is early-intermediate — strong at writing
  standalone coursework-style scripts and following process, but test-infra
  internals (runpy, mocking, coverage) and metaprogramming are still being
  learned. Explain realistically; never overstate or condescend.
- **Explain "why" first, in plain English, then the code.** One concept per
  answer; if jargon is unavoidable, define it in one line. Simpler is better —
  no overcomplications or overengineering.
- **Multi-AI cross-auditing:** the owner uses Claude, Gemini and OpenCode
  together (same task and/or split by strength). Distinguish *fact* vs
  *heuristic* vs *opinion*, flag where other tools would plausibly disagree,
  and anchor every claim to repo ground truth (this file, the tests, and the
  results of the commands shown).
- **Verification culture:** show the exact command and its output for every
  change; always cite commands the owner can re-run themselves.
- **House style:** British English, SPaG-clean; comments explain *why* only
  (no new comments unless useful or explicitly requested), matching the
  one-line-statement-then-reason style already present. **Short vs block
  comments:** short comments use `#` (max 2 lines); longer explanations use
  `"""` blocks instead. **AI-authored comments** (anything the agent writes to
  explain its own fix, not A.I.M's notes) must start with a
  `[AI-authored fix]` marker inside a `"""` block so they are instantly
  distinguishable from the owner's own comments. **British Standard English
  ALWAYS:** every agent-written word (docs, comments, replies, commit
  messages) must use British spelling and phrasing - e.g. organise, colour,
  behaviour, analyse, labelled - never Americanised forms (organize, color,
  behavior, analyze, labeled).
- **Rules always win:** never break the Project Rules below (frozen OOP lane,
  coverage caps, `transactions.py` CWD quirk, no comment stripping, `.env`).

### Prompt Format (owner -> agent)

For tasks (not one-off questions), give the agent a compact block:

Goal: <the outcome, not the method>
Files: <explicit paths or "everything under python/">
Constraints: <rules that must not break, e.g. frozen OOP lane, caps>
Verify: <tests to run + command, or "full suite before committing">
Explain: <plain English, why first, one concept per answer> (optional)

Example that mirrors how this repo actually worked:

Goal: Speed up the test suite without touching any teaching script.
Files: tests/ (TestModules class especially)
Constraints: python/ scripts stay frozen; no new comments unless asked
Verify: .venv/Scripts/python.exe -m pytest -q

Capitalisation does not change how the agent reads the prompt - use
normal sentence case and reserve ALL-CAPS for one or two critical words
(e.g. a single NOT). Specificity reduces misreading; shouting does not.

Misspellings in prose (e.g. "accoridngly", "out pytest") do not matter -
the agent reads intent, not exact letters. What DOES matter is precision
on identifiers the agent must resolve: file names, module/function/test
names, command flags and expected output strings. Those should be exact.

### Tool-choice recommendations (owner's assessment)

The owner runs Claude, Gemini and OpenCode (Big Pickle) on the same
task. Use each where it is strongest:

- Big Pickle / OpenCode: strongest at plan -> execute -> verify in one
  loop over the repo (reads files, edits, runs the pinned interpreter).
  Best default for multi-file repo tasks given a Goal/Files/Constraints
  block. Concise by default - add "full detail" when you want depth.
- Claude: fantastic for code queries, small fixes and debugging issues -
  its unique attribute is coding and programming. Use it when the ask
  is code-specific; ask it to critique or patch, not to re-design.
- Gemini: has the capability but is more general use - more generative
  and broad than Claude's code focus. Use it for research sweeps,
  long-context reading and open-ended ideas; treat its specific
  line-level claims as candidates to verify, not ground truth.

Shared weak spot to guard: all three pattern-match open prompts like
"make it better" and over-reach without constraints. The
Goal/Files/Constraints block exists precisely because of that - it is
not a formality.

## Running Things

| Task | Command |
| --- | --- |
| Run the full test suite | `.venv/Scripts/python.exe -m pytest` |
| Run one test folder | `.venv/Scripts/python.exe -m pytest tests/test_imperative_programming/` |
| Run one test file | `.venv/Scripts/python.exe -m pytest tests/test_imperative_programming/test_unit_and_format_converters.py` |
| Coverage report (term + missing lines + branch) | `.venv/Scripts/python.exe -m pytest --cov --cov-report=term-missing` |
| Coverage scope limited to `python/` | `.venv/Scripts/python.exe -m pytest --cov=python` |
| Clickable HTML coverage report | `.venv/Scripts/python.exe -m pytest --cov=python --cov-report=html` (writes to ignored `htmlcov/`) |
| Interactive project tree + benchmark | `.venv/Scripts/python.exe scripts/execution_time.py` |
| Project tree in non-interactive `--all` mode | `.venv/Scripts/python.exe scripts/execution_time.py --all` |
| Repo hygiene guards (CWD artefacts stay ignored) | `.venv/Scripts/python.exe -m pytest tests/test_scripts/test_repo_hygiene.py` |

> Use the Windows venv python (`.venv/Scripts/python.exe`), NOT a plain `python`
> / `python3` — the repo is pinned to that interpreter.

## Project Rules (Do NOT break these)

1. **The OOP lane is frozen.** `python/object_oriented_programming/` —
   specifically `decorator.py`, `generator.py`, `multitasking.py`, `dice.py` —
   must not be moved, renamed, or have imports rewritten. (`classes.py` had a
   misspelled sibling import (`orienteded`) that was corrected, not rewritten.)
2. **No comments in code unless explicitly asked.** Coursework scripts are
   heavily commented; do NOT strip existing comments, but do not add new ones
   unless the user requests them.
3. **`transactions.py` filename bug is intentional.** It saves
   `transactionv1.xlsx` to the *current working directory* via a relative
   `wb.save(...)`. Do not "fix" it. Tests encode this CWD-relative behaviour
   with `monkeypatch.chdir(tmp_path)`.
4. **`qrcode_generator.py` saves PNGs relative to the CWD** (uses
   `os.getcwd()`), so tests can point it at `tmp_path`. Do not hardcode the
   script's own directory. Both of these outputs are `.gitignore`d at the
   repo root — running either script from the root, or the
   `execution_time.py` benchmark (which launches all files with the root as
   CWD), drops the artefact there. `tests/test_scripts/test_repo_hygiene.py`
   guards that, so a contributor cannot reintroduce the hazard.
5. **Keep the OOP lane frozen and the imperative lane clean** — files added to
   `python/imperative_programming/` should match their folder's theme exactly
   (`syntax_exercises`, `unit_and_format_converters`, `interactive_games`,
   `math_and_science_calculators`, `fundamental_topics`).
6. **Do not touch `.env`** — it holds local credentials, is gitignored, and is
   never committed.
7. **Keep README tree + `TREE_SKIP` in sync** when folders are added/removed.
   `TREE_SKIP` in `scripts/execution_time.py` excludes generated/vendored paths
   (`.git`, `.venv`, `.pytest_cache`, `__pycache__`, `.coverage`, `htmlcov`).
8. **Any file type may be staged and committed — `python/` included.**
   Agents follow the Conventional Commit table below for every commit
   (`feat`, `fix`, `docs`, `refactor`, `test`, `style`, `chore`, `ci`),
   scoped to the file when that reads better, e.g.
   `fix(login_status.py): catch the empty-answer IndexError`. The previous
   ring-fence on `python/` is lifted: those scripts are the owner's
   portfolio and practice material, **not** the assessed coursework, which
   lives in `university_courseworks/` (for example the marked CS1IP scripts
   are `university_courseworks/year1/cs1ip/coursework1/*.py`). Two
   consequences still apply: never commit `.env` (rule 6), and never
   rewrite a script's *behaviour* just to tidy it, because documented
   defects are pinned by tests on purpose (rule 11).
9. **Entry points are content-named, not `def main()`.** The lane-wide sweep
   replaced `def main()` with descriptive names (`launch_mp3_player`,
   `summarise_grades`, `generate_qrcode`, ...); only
   `imperative_programming/fundamental_topics/main.py` keeps `def main()` by
   design. Keep new scripts on named entry points, and never regress the
   renamed ones.
10. **Text files are LF, enforced by `.gitattributes`** (`* text=auto eol=lf`,
    with `.joblib` / `.xlsx` / `.pdf` marked binary). Do not reintroduce CRLF
    or mixed endings when editing or creating files.
11. **Documented source defects stay defective — unless the defect is a
    crash or a false result, which get fixed.** Coursework scripts under
    `python/` are not repaired for tidiness. Where a script's misbehaviour
    is the *point* of the exercise, a test pins it and its docstring names
    the defect, so the problem stays visible instead of being quietly
    deleted — the same treatment as rules 3 and 4. Fixing one means editing
    `python/` *and* rewriting the test that documents it, which erases the
    record; that is the owner's call, not a cleanup. Still on the list,
    with the test that pins each: the always-truthy
    `isdigit() != "r" or "p" or "s"` in `rock_paper_scissors.py`'s
    `play_round()`, the two predicates in `login_status.py`'s
    `check_access_status()` (truthiness used where a comparison to `"T"` is
    needed, so "Stop Lying" is unreachable and the `elif` ignores
    `is_new`), and `area_of_circle.py` (no `__main__` guard). `modules.py` is
    deliberately
    **not** on this list — the `e` shadowing is the "Module Conflict Example"
    the file exists to demonstrate. Two defects have been repaired rather
    than pinned, because both made the program lie or crash: the `:.2f` on
    an error string in `arithmetic_expressions.py`'s `format_result()`,
    which killed the results loop and reported bad input for valid numbers,
    and the uncaught `IndexError` on an empty answer in `login_status.py`.
    Full detail in
    `NOTES.md`.

## Term-Time Operating Cadence

- Term time (university) = **maintenance mode**. Daily loop when the owner
  passes through: Python recheck, README/`.md` upkeep and checks, Friday
  career sprint. Heavy learning and new roadmap phases run in holidays only.
- Each pass-through is logged as a dated row in `NOTES.md`'s maintenance log,
  using the week frame of `university_courseworks/year2/`; the row states the
  previous week(s) covered as of the logged day.
- `postgresql/` will gain **experimental folders during term**; they are
  learning scratch, full-pace work happens in Summer 2027 Block II. Never
  force experimental files into a commit.

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

- 92 imperative scripts, 21 functional, 41 OOP, plus `advanced_projects`
  (machine_learning notebooks, transactions xlsx pipeline, music player).
- 1350 passing tests, ~99% line coverage and 98% branch coverage (171 of the
  182 measured `python/` files at 100% lines, including both
  music-player GUIs; the one never-imported file is
  `imperative_programming/fundamental_topics/main.py`, and the 161
  non-`__init__.py` files are the number a docstring sweep covers). Branch
  coverage is
  enabled in `[tool.coverage.run]` because line coverage alone read 99%
  while 99 branch directions had never executed - `sine_rule.py` was at
  100% lines with 21 of its 92 branches unexercised. A 2026 audit closed
  49 of those arcs (38 tests); **53 remain open across 28 files**. An earlier
  draft split those into "10 in caps, 18 import guards, 22 assorted", but that
  arithmetic was never verifiable: coverage only names 16 of the 53 arcs (the
  other 37 carry no line numbers in the report), so any precise per-category
  split is a guess. What is solid: 21 of them are in the four documented
  dead-by-design caps (`conditions.py` 12, `dictionaries.py` 4,
  `variables.py` 3, `generator.py` 2), the largest single contributor being
  `conditions.py`, whose hardcoded `temperature = 25` makes most of its
  branches unreachable. The rest are spread thin, one or two per file. The two
  newest functional teaching files are `functools_module.py` (cache,
  lru_cache, partial, reduce, singledispatch, wraps) and
  `statistics_module.py` (12 core measures) - the latter sits in the
  functional lane because `imperative_programming/fundamental_topics/
  numbers.py` shadows the stdlib `numbers` module that `statistics`
  imports internally, so a copy there dies on a `decimal` circular
  import. `itertools_module.py` now demonstrates all 20 public names, and
  `numbers.py` / `dictionaries.py` gained a `bytes.hex` block and a
  `setdefault` block respectively. Full suite
  now runs in ~21s with 0 warnings (`TestModules` stubs
  `pkgutil.walk_packages`, so the `help("modules")` line in `modules.py`
  no longer scans every installed package - that scan cost ~20s and
  dragged in 12 third-party deprecation warnings). `conftest.py`
  per area
  provides `run_script()` which
  runs scripts via `runpy` with mocked `input()` / `time.sleep()` and
  optional `cwd` for file-writing tests.
- Coverage caps by design (do NOT "fix" the scripts to chase lines): the
  remaining 38 uncovered lines sit only in the eleven capped scripts -
  `variables.py` (8), `conditions.py` (6), `classes.py` (6),
  `generator.py` (5), `dictionaries.py` (4), `abstract_classes.py` (2),
  `device.py` (2), `drink_script_example.py` (2), and one each in
  `login_status.py`, `polymorphism.py` and `rock_paper_scissors.py`. The 8
  lines in `classes.py` and `drink_script_example.py` are the
  `except ImportError:` fallback bodies and the `sys.path` block added when
  those two files were made runnable outside pytest; they cannot execute under
  a test run, because `pythonpath = ["python"]` satisfies the first import
  before the fallback is ever reached. That is the deliberate price of two
  files that run at all - see the runnability audit in `NOTES.md`.
  `variables.py` (75%) has hardcoded booleans whose nested
  "Stop Lying"/"Accident or Intended?"/offline branches are unreachable
  without editing source; OOP `generator.py` (90%) has a dead
  `elif execution_time >= 3600` branch that can never fire after the
  earlier `>= 60` elif. Additional
  dead-by-design caps documented during the full-path sweep:
  `conditions.py` (92%) hardcodes `temperature = 25` / `name = "A.I.M"` so the
  hot/bit-cold/cold branches and the name-while-loop body can never run;
  `dictionaries.py` (88%) calls `capitals.clear()` before its keys()/values()/
  items() loops so those loop bodies are unreachable; `abstract_classes.py`
  (92%), `device.py` (96%) and `polymorphism.py` (97%) keep `pass` bodies
  inside abstract methods that can never be invoked; `login_status.py` (93%)
  compares a bound method to a string (`is_admin[0].upper == "T"`), which is
  never True.
- `scripts/execution_time.py`: interactive `tree /f`-style project map +
  per-folder benchmark report over five statuses - `PASS` (ran and exited
  cleanly), `INTERACTIVE` (stopped at an `input()` prompt, which is what 62 of
  the 183 files do), `TIMEOUT` (ran past 2s), `FAIL` (raised a real error, now
  only 2 files) and `ERROR` (the harness could not launch it). It benchmarks
  `sys.executable` rather than a bare `python`, so it measures the pinned venv
  interpreter, and derives `PROJECT_ROOT` from `__file__` rather than a baked
  absolute path.
- Postgres is planned (`psycopg2` installed, `postgresql/sandbox/aim.sql`
  reserved) but not started.

## References

External study/project resources tracked in `NOTES.md`, plus the local module
briefing documents under `university_courseworks/` (tracked in git; the
accompanying `.pdf` / `.txt` copies are local-only).
`university_courseworks/UNIVERSITY_MODULES.md`
is the rolling three-year reference (2025/26-2027/28) with academic dates,
module semester splits, briefing instructions/objectives and the official
University of Reading module-catalogue links for every module.

### Codedex Projects

| Resource | Purpose | URL |
| --- | --- | --- |
| 50 Terminal Project Ideas | Beginner CLI Python project list | <https://www.codedex.io/projects/50-terminal-project-ideas-using-python> |
| Roman Numeral Converter | Data-format conversion exercise | <https://www.codedex.io/projects/convert-roman-numerals-with-python> |
| Word Guessing Game | Game-loop state machine exercise | <https://www.codedex.io/projects/build-a-word-guessing-game-with-python> |
| Create a GIF | Pillow image generation | <https://www.codedex.io/projects/create-a-gif-with-python> |
| Generate a QR Code | qrcode image output | <https://www.codedex.io/projects/generate-a-qr-code-with-python> |
| Build Pong with PyGame | Real-time physics / collision engine | <https://www.codedex.io/projects/build-pong-with-pygame> |
| Web Scrape Amazon with Beautiful Soup | DOM parsing / HTTP extraction | <https://www.codedex.io/projects/web-scrape-amazon-with-beautiful-soup> |
| Build a Discord Bot | Async network event loops | <https://www.codedex.io/projects/build-a-discord-bot-with-python> |
| Automated Scheduling Alert System via SMTP | Email automation / background tasks | <https://www.codedex.io/projects/automate-secret-santa-emails-with-smtp> |
| Analyze Spreadsheet Data with Pandas & ChatGPT | DataFrames + LLM-driven EDA | <https://www.codedex.io/projects/analyze-spreadsheet-data-with-pandas-chatgpt> |
| Visualize YouTube Data with Plotly | Multi-variable time-series visualisation | <https://www.codedex.io/projects/visualize-youtube-data-with-plotly> |
| PostgreSQL Data Analysis | Relational database aggregates / `.groupby()` | <https://www.codedex.io/projects/analyze-twitch-data-with-sqlite> |
| Analyze Custom Library Data with SciPy | Scientific statistics / variance models | <https://www.codedex.io/projects/analyze-us-census-data-with-scipy> |
| Analyze Premier League / Baseball Stats (Pandas + Matplotlib) | Time-series wrangling / moving averages | <https://www.codedex.io/projects/analyze-baseball-stats-with-pandas-and-matplotlib> |
| Predict Home Prices with Linear Regression | Supervised predictive modelling | <https://www.codedex.io/projects/predict-home-prices-with-python-and-linear-regression> |
| Image Object Detection with Hugging Face | Computer vision / pre-trained transformers | <https://www.codedex.io/projects/detect-hotdog-with-hugging-face> |
| Custom Search Engine with Exa AI | Dense vector semantics / neural indexes | <https://www.codedex.io/projects/build-a-custom-search-engine-with-exa-ai> |
| Voice Virtual Assistant with ElevenLabs | Multimodal audio streaming | <https://www.codedex.io/projects/create-a-voice-virtual-assistant-with-elevenlabs> |

### Roadmaps & Learning Platforms

| Resource | Purpose | URL |
| --- | --- | --- |
| AI & Data Scientist Roadmap | Systems architecture guide | <https://roadmap.sh/ai-data-scientist> |
| Business Case Modelling Tracks | Production analytics portfolios | <https://learn.365datascience.com/projects/> |
| Enterprise GenAI Projects | LLM vector and application implementations | <https://www.projectpro.io/genai-projects> |
| Core Data Science Projects | Scaled production data-science implementations | <https://www.projectpro.io/projects/data-science-projects> |
| Applied ML Algorithms | Supervised/unsupervised ML frameworks | <https://www.projectpro.io/projects/data-science-projects/machine-learning-projects-in-python> |
| Neural Networks Projects | Deep learning production systems | <https://www.projectpro.io/projects/data-science-projects/deep-learning-projects> |

### University Module Briefings (local, non-code)

| Module | Purpose | File |
| --- | --- | --- |
| CS1AC | Applications of Computer Science (Year 1) | `university_courseworks/year1/CS1AC~0022~20256.html` |
| CS1CA | Computer Systems Architecture (Year 1) | `university_courseworks/year1/CS1CA~0022~20256.html` |
| CS1DB | Databases - group assessment (Year 1) | `university_courseworks/year1/CS1DB~0022~20256.html` |
| CS1IP | Imperative Programming (Year 1) | `university_courseworks/year1/CS1IP~0022~20256.html` |
| CS1MA | Mathematics and Computation (Year 1) | `university_courseworks/year1/CS1MA~0022~20256.html` |
| CS1OP | Object-Oriented Programming (Year 1) | `university_courseworks/year1/CS1OP~0022~20256.html` |
| CS2DA | Data Analytics (Year 2) | `university_courseworks/year2/CS2DA~0022~20267.htm` |
| CS2AI | Artificial Intelligence (Year 2) | `university_courseworks/year2/CS2AI~0022~20267.htm` |
| CS2ON | Operating Systems and Computer Networking (Year 2) | `university_courseworks/year2/CS2ON~0022~20267.htm` |
| CS2PP | Python Programming (Year 2) | `university_courseworks/year2/CS2PP~0022~20267.htm` |
| CS2SD | Software Systems Design (Year 2) | `university_courseworks/year2/CS2SD~0022~20267.htm` |
| CS2SE | Software Engineering (Year 2) | `university_courseworks/year2/CS2SE~0022~20267.htm` |
| CS3IP | Individual Project (Year 3) | `university_courseworks/year3/year3-briefing-2025.txt` |
| CS3AM | Artificial Intelligence and Machine Learning (Year 3) | `university_courseworks/year3/year3-briefing-2025.txt` |
| CS3 elective group | DV/VR (S1), BC/CS/IV/TM (S2) - Year 3 | `university_courseworks/year3/year3-briefing-2025.txt` |

### Assessed Coursework Scripts (marked work — handle with care)

| Module | Folder | What is in it |
| --- | --- | --- |
| CS1IP | `university_courseworks/year1/cs1ip/coursework1/` | The marked scripts: `average_grades.py`, `hello.py`, `ice_cream.py`, `seven_segment.py`, `volume.py`, each with a `.java` counterpart |
| CS1IP | `university_courseworks/year1/cs1ip/coursework2/` | `sort10.txt` and its sorting script |

These are the **submitted, marked** artefacts, so they carry a different
risk profile from the rest of the repo: behaviour that was correct on
submission day should not be changed casually, and nothing in `python/`
duplicates them (checked — only the filename `volume.py` coincides, as an
unrelated calculator script under `math_and_science_calculators/`). The
`python/` tree is the owner's own learning and portfolio material and is
covered by `tests/`; this folder is not, so there is no test safety net
here. Read the relevant briefing before editing anything in it.

> Dates, semester splits, briefing instructions/objectives and official
> University of Reading module-catalogue links for every module across all
> three years: see `university_courseworks/UNIVERSITY_MODULES.md`. Official BSc Computer Science
> (UCAS G400) course pages: 2025/26, 2026/27 and 2027/28 entry (the 2025 page
> redirects to 2026/27; the 2027 page is not live yet).
