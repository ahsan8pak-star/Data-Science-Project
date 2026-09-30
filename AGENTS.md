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
  comments — this is binding, not a preference.** Two lines is the absolute
  maximum for `#`. A run of three or more consecutive `#` lines is wrong and
  becomes a `"""` block instead, in this exact shape, with the quotes alone
  on their own lines:

  ```python
  """
  Summary sentence on its own line.

  Further explanation, wrapped to roughly 80 columns, separated from the
  summary by one blank line.
  """
  ```

  A `"""` block is only legal where it stands as its own statement: at the top
  of a module or function as the real docstring, or mid-function as an
  explanatory block. It never opens and closes on the same line as its text.
  **End of file: exactly two trailing newlines** — the last line of code, one
  empty line, then EOF. Three reads as an accidental blank page. LF only;
  `.gitattributes` pins `* text=auto eol=lf`. Both byte invariants are enforced
  by `tests/test_scripts/test_data_files.py`.
  Single-line `#` comments are fine and preferred for one-liners; the limit
  applies to *consecutive* `#` lines only, so `# note` followed by unrelated
  code is unaffected. Inline trailing comments (`x = 5  # why`) are unaffected
  too — the rule governs standalone comment blocks. The rule applies to **every
  tracked `.py` file in the repository**, not only to newly written ones; the
  two standing exemptions are the frozen OOP lane (rule 1) and the marked CS1IP
  coursework (rule 8), which are named in the guard rather than left implicit.
  **AI-authored comments**
  (anything the agent writes to explain its own fix, not A.I.M's notes) must
  start with a
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

### Free-tier model rotation (OpenCode)

The seven free OpenCode models rotated are: Big Pickle Free,
Space Bunny Free, Nemotron 3.5 Lightning Free, Nemotron 3 Ultra
Free, Ling 3.0 Flash Fin Free, Muse Spark 1.3 Free and MiMo
-V2.6-Flash Free. Rotation is selected in the OpenCode console,
not from inside a conversation — an agent cannot switch its own
model mid-session.

An agent cannot reliably self-identify which model is processing a
conversation — do not trust a claim of the form "I am model X" made by
the agent itself. The same discipline applies regardless of model: give a
Goal/Files/Constraints block, and treat any model's line-level claims as
candidates to verify against the repo rather than ground truth.

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
    A third defect was repaired after the audit:
    `fundamental_topics/numbers.py`'s `decimal` circular import,
    which killed the file ~60 lines in whenever run directly
    (the test harness hid it because the real stdlib `numbers`
    is already cached under pytest). Fixed by dropping the file's
    own folder from `sys.path` at the top; direct run now exits
    0, benchmark row FAIL -> PASS, suite unchanged at 1350.
    Full detail in
    `NOTES.md`.
12. **Every commit message carries a scope naming the file or folder it
    touched.** `fix(generator.py): resolve import error`, not
    `fix: resolve import error`. The Conventional Commits type still leads so
    linters and Semantic Release keep working; the parenthesised scope is what
    makes the history scannable in `git log --oneline`, where the subject is
    all you see. For a multi-file change, scope to the folder
    (`docs(university_courseworks/year2/): add holiday weekly tables`) or name
    the principal file. A commit with no scope at all is wrong even when the
    prefix is right - this was violated five times in a row during the 29 Sep
    2026 session and had to be promoted from a "rule of thumb" to a numbered
    rule to stop the drift.
13. **`PROGRESSION.md` is a living document and is updated every session.**
    The review is not a one-off write-up of the 16-week run; it is the running
    record of where the project has got to, and it is updated whenever the
    project moves. On any session that changes the project - new modules, new
    tests, a fixed bug, a new rule, a changed stage of learning - append a row
    to the session log in that file and refresh any figure it quotes. A session
    that ends with the document describing a state the repo has moved past is
    a failed session, even if every test passes. The figures are test-guarded by
    `tests/test_scripts/test_repo_doc_numbers.py`, so a stale number fails the
    suite; the log itself is the part only the agent can maintain, and a rule
    cannot enforce intent. Keep additions append-only where possible so the
    narrative still reads as a progression rather than a rewrite.

## Term-Time Operating Cadence

- Term time (university) = **maintenance mode**. Daily loop when the owner
  passes through: Python recheck, README/`.md` upkeep and checks, Friday
  career sprint. Heavy learning and new roadmap phases run in holidays only.
- **The owner's real contact hours govern scheduling** (confirmed Mon 28 Sep
  2026): Monday 11:00 AM - 4:00 PM (home 6:00 PM), Tuesday 2:00 PM - 6:00 PM
  (home 8:00 PM, tired), Wednesday **free**, Thursday 9:00 AM - 4:00 PM (home
  6:00 PM), Friday **free**. So Wednesday is the single deep-work day
  (~6 hrs in two blocks: 9 AM - noon, 2 PM - 5 PM), Monday and Thursday are
  2-hour late-evening maintenance slots (7 PM - 9 PM), Friday holds the career
  sprint plus a review block (2 PM - 4 PM and 7 PM - 9 PM), Tuesday takes a
  **morning block (8:30 AM - 10:30 AM)** before its late finish with the
  evening left as rest, and Saturday/Sunday are
  a fixed **7:00 PM - 9:00 PM** review slot that is the same in semester and
  holidays - only holiday weekdays expand (to the 9:00 AM - 9:00 PM Times Off
  window). Per-day tables live in `NOTES.md` and both
  `YEAR2_SEMESTER*.md` files; those are the authority, not this summary.
- Each pass-through is logged as a dated row in `NOTES.md`'s maintenance log,
  using the week frame of `university_courseworks/year2/`; the row states the
  previous week(s) covered as of the logged day. The log records what was
  done, not a quota - a Tuesday logged with only its morning block is a
  legitimate partial, and a rest evening is not a missed session.
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
- **Every commit message carries a scope naming the file or folder it
  touched** - this is mandatory, not a style preference. The Conventional
  Commits prefix still leads, with the name in parentheses straight after:
  `fix(generator.py): resolve import error`,
  `refactor(alarm_clock.py): move to syntax_exercises`,
  `test(test_ranking_docs.py): guard heading drift`,
  `docs(FILE_SCORES.md): align headings with table finals`. For a change
  spanning many files, scope to the folder or area instead
  (`docs(university_courseworks/year2/): add holiday weekly tables`) or, if
  that still reads badly, name the principal file. A commit with no scope at
  all is wrong even when the prefix is right. This keeps the type
  machine-readable for linters and Semantic Release while keeping the subject
  human-readable. **Merge commits are exempt**: the forge generates their
  subject from its own template, so no amount of discipline puts a scope on
  one, and since branch-and-PR is now the default correction path every
  correction would otherwise add a violation. The guard skips them by parent
  count rather than by matching the word "Merge", so a squash or rebase merge
  is covered too.
- **Sequence the work easiest-and-safest first, hardest-and-riskiest last.**
  Order steps so difficulty and risk rise together - a docstring, a guard
  test, a mechanical rename, a frozen-lane change, a history rewrite - rather
  than doing the delicate thing first and building on an unverified baseline.
  Each step leaves the suite green, so when the risky step runs there is
  already a known-good state to fall back to. State the ordering up front
  before touching anything, and re-verify between steps rather than batching.
  The point is that a mistake made at step 1 is caught by a cheap test, while
  the same mistake at step 5 is caught by a reviewer.
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
- **Never force-push `main`.** That history is the portfolio's public face and
  every mirror follows it, so rewriting it is the one destructive git action
  left here.
- **Force-pushing a branch is allowed**, with `git push --force-with-lease`
  rather than `--force` so a stale local ref cannot clobber someone else's
  work. This is the correction path: when a pushed commit is wrong, branch
  from `main`, amend or re-commit there, force-push the branch, and open a
  pull request rather than editing `main` in place. `--force-with-lease`
  refuses when the remote has moved since the last fetch, which is exactly the
  case a blind `--force` would destroy.
- This holds on **all four mirrors**, backups included. A branch that is
  rewritten on the GitHub Project but not on the GitLab Backup is a half-fixed
  correction, and the backups exist to be restorable, so they should get the
  same shape. `main` still carries the rule above on every mirror, backup
  namespaces not excepted.
- **Additions do not need per-instance approval.** New source files, new tests,
  new documentation sections, new folders, and new remotes or branches may be
  added and committed under the Conventional Commit table above without asking
  first. The two standing limits are unchanged: never commit `.env` (rule 6),
  and never repair a documented defect just to tidy it (rule 11). Everything
  else that would once have prompted a question — "may I add this file?", "may
  I create this branch?" — is pre-approved.

### Correcting something already pushed

**A mistake on `main` is corrected on a branch, never on `main` directly.**
The sequence is: open a branch, commit the fix there with a subject stating
both the change and the issue behind it, verify the fix properly, then
force-push the branch and open a pull request. `main` itself is never
force-pushed, so a bad commit is not erased - it is superseded.

The owner's wording, which is the rule: *"if a mistake is made on main, please
make a pull request, review it, investigate, check, and after creating a
branch to fix, stating the git commit fix and the issue behind it, force push
it in when all parts have been fixed - i.e. met the satisfied functions with
little to no bugs, especially when running and executing user inputs."*

That last clause is the part that matters most: the branch is not ready on
"the tests pass" alone. Before force-pushing, the fix has to be shown working
under the way a user actually meets the code:

- the **full suite green**, run more than once, not once;
- for a change to a script, the script **executed for real** with representative
  user input, not merely imported - `scripts/execution_time.py --all` when
  anything under `python/` changed, since that is the only harness that runs
  every file standalone;
- for a change to the CWD-relative writers (`transactions.py`,
  `qrcode_generator.py`), run them and confirm the artefact lands where the
  rule intends and that no stray file reaches the repo root;
- the behaviour that was wrong **reproduced before the fix** and shown absent
  after it, so the fix is demonstrated rather than asserted;
- any test added to prove it is confirmed to **fail against the old code**,
  otherwise it may be passing for an unrelated reason.

**When a follow-up commit is still the right answer.** A branch and a pull
request cost a review and a merge; that is worth it when the wrong content
must be *replaced* rather than merely countered. A one-line doc fix, a typo in
a comment, or a correction that a reader benefits from seeing in the log is
better served by an honest follow-up commit on `main` - the history then shows
the mistake *and* the correction, which is worth more to a reader than a tidy
log. The deciding question is whether the wrong state was ever useful to
anyone: if it was, keep it visible and correct it forward; if it was pure
noise, supersede it on a branch.

**Force-pushing the branch is expected** once the fix is verified, and
`--force-with-lease` is used rather than `--force` so a stale local ref cannot
clobber someone else's work. The same applies on all four mirrors: a branch
rewritten on the GitHub Project must get the same shape on the GitLab Backup,
or the correction is half-applied.

## Feature Summary (what exists today)

- 92 imperative scripts, 21 functional, 41 OOP, plus `advanced_projects`
  (machine_learning notebooks, transactions xlsx pipeline, music player).
- 1527 passing tests, ~99% line coverage and 95% branch coverage (148 of the
  159 measured `python/` files at 100% lines, including both
  music-player GUIs; the one never-imported file is
  `imperative_programming/fundamental_topics/main.py`, and the 161
  non-`__init__.py` files are the number a docstring sweep covers). The 159
  counts files that carry at least one statement. The coverage table prints
  182 rows because it also lists 22 files that have no statement - the empty
  `__init__.py` files - which report 100% without anything having run; `main.py`
  is excluded from
  the report entirely because its deliberate `IndentationError` stops it
  being parsed. Branch coverage is
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
  imports internally, so a copy placed there dies on
  `AttributeError: module 'numbers' has no attribute 'Number'`. That
  placement still stands even though `numbers.py` itself now runs clean
  standalone, because the shadowing - not the crash - is the problem.
  `itertools_module.py` now demonstrates all 20 public names, and
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
  the 182 files do), `TIMEOUT` (ran past 2s), `FAIL` (raised a real error, now
  only `main.py`, whose `IndentationError` is the deliberate teaching stub
  pinned by `test_fundamentals.py`) and `ERROR` (the harness could not launch
  it, currently none). It benchmarks
  `sys.executable` rather than a bare `python`, so it measures the pinned venv
  interpreter, and derives `PROJECT_ROOT` from `__file__` rather than a baked
  absolute path.
- `FILE_RANKING_GUIDE.md` and `FILE_SCORES.md`: a 0-100 scoring guide and the
  results for all 160 non-`__init__` Python files under `python/`, ranked across
  Fixability (40%), Readability (25%), Durability (20%) and Robustness (15%).
  Each entry carries a criterion-by-criterion breakdown and a sincere comment
  naming what works, what does not, why the score, and what would fix it.
  Overall average: 77.5/100 (band C — Serviceable). Only 11 files score below
  70; the weakest are `conditions.py` and `variables.py` (56 each), both low
  for stylistic reasons (hardcoded values, deliberate defects) rather than
  functional ones. See `FILE_SCORES.md` for the full breakdown.
- Postgres is planned (`psycopg2` installed, `postgresql/sandbox/aim.sql`
  reserved) but not started.

## References

`PROGRESSION.md` is the narrative review of the 16-week run from 4 June 2026:
the stages of learning and what evidences each, the corrections and mistakes
made by both A.I.M and the assistants, and how the AI collaboration was
arranged - including the point where Claude and Gemini were replaced by
OpenCode for terminal work, and the seven-model free rotation. Its numeric
claims are test-guarded by `tests/test_scripts/test_repo_doc_numbers.py`, so a
stale figure there fails the suite like any other.

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

