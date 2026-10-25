# Progression and AI Collaboration Review

Markdown reference: [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)

---

A review of the Data Science project that began on **Thursday 4 June
2026** and ran to **Tuesday 29 September 2026** — 117 days, and 714 commits
across four months, mirrored to GitHub and GitLab. Those 117 days are the
reviewed run; the session log below continues past them, because this is a
living record rather than a closed report.

Every figure in this document is pinned by a test, so it cannot quietly go
stale: `tests/test_scripts/test_repo_doc_numbers.py` recomputes the counts
from the repository and fails the suite if a stated figure no longer matches.
Figures that are historical rather than live (the commit count at the end of
the run) are marked as such, because a live count would move the moment this
file was committed.

The document has three parts: what A.I.M built and in what order, where the
mistakes were and what they cost, and how AI assistants were used throughout
(including the point where two of them were dropped for terminal work).

Where a number is an estimate rather than a measurement, it says so.

---

## 1. The shape of the project

| | |
| --- | --- |
| Author | A.I.M |
| Started | 4 June 2026 (first commit: `Initial commit`) |
| Reviewed | 29 September 2026 |
| Duration | 117 days (16.7 weeks), against a 16-week Summer 2026 plan |
| Commits | 714 at the end of the run (historical — see the note below) |
| Peak effort | 28–36 h/week recorded across most weeks |
| Source modules | 160 non-`__init__` files under `python/` |
| Test suite | 2042 tests, all passing |
| Coverage | 99% line, 95% branch |
| Quality mean | 84.6/100 across 160 ranked files |
| Mirrors | 4 (GitHub project + backup, GitLab project + backup) |

### The three programming lanes

The project is organised as a deliberate climb, not a flat pile of scripts.
Each lane answers a different question about how code is put together.

The commit count is quoted as at the close of the run and is deliberately not
a live figure: an earlier draft of this document stated the current `HEAD`
count and the guard test failed the moment the document itself was committed,
because committing it added a commit. A historical figure is stable; a live
one is not, and a test that asserts a live count can never be satisfied.

| Lane | Modules | What it teaches |
| --- | --- | --- |
| `imperative_programming/` | 92 | Top-to-bottom execution: state that changes, loops, conditionals, `input()` |
| `functional_programming/` | 21 | Behaviour as values: comprehensions, `map`/`filter`/`reduce`, closures, `functools` |
| `object_oriented_programming/` | 41 | State as encapsulated objects: inheritance, descriptors, magic methods, abstract bases |
| `advanced_projects/` | 6 | Things with real inputs: a music player with two GUIs, an xlsx pipeline, a scikit-learn transformer |

Plus `sandbox/aim.py`, a scratch file that is deliberately **untracked**: it is
practice reference material, not repository content, so experiments in it cannot
affect the suite and cannot be committed by accident.

[AI] `aim.py` is the one file under `python/` that a `git add .` will not pick
up. That is the point: the file exists so practice code can be written and run
without any risk of it being swept into a commit, which is exactly what
happened the first time it held real code. `tests/test_scripts/
test_repo_hygiene.py` guards the rule so it cannot be undone silently.

The 92 → 21 → 41 shape is worth reading correctly. Imperative has the most
files because it is where fundamentals get drilled; functional is smaller
because each script has to *earn* abstraction rather than loop; OOP sits
between because it is a language A.I.M already knew from CS1OP but now has to
use for structure rather than for its own sake.

---

## 2. Progression: beginner to where A.I.M is now

This is a self-assessment calibrated against the repository, not a
self-congratulatory narrative. The evidence for each stage is a commit or a
file that could not have existed before it.

### The shape of the four months, measured

The stages below are argued from individual commits, which is evidence but is
also the easiest thing to cherry-pick. So the same argument is repeated here on
the *whole* history — every commit up to this one, not a selection — using two
measures that cannot be chosen for: how many commits landed, and how long their
subjects are.

| Month | Commits | Mean subject length | Subjects over 120 chars | What the month was |
| --- | --- | --- | --- | --- |
| Jun 2026 | 154 | 98.9 | 42 | Syntax drills; Git and IDE setup |
| Jul 2026 | 227 | 122.3 | 88 | Testing becomes the work |
| Aug 2026 | 108 | 98.8 | 26 | Narrowing, renaming, consolidation |
| Sep 2026 | 225 | 76.7 | 19 | Documentation, rules, review |

The four counts total 714, the same figure Section 1 states for the run, so
the table is internally consistent and is recomputed by the test suite rather
than trusted. The window closes at the end of 29 September, which is what makes
these numbers stable: a commit made today cannot alter them, so the figures
cannot rot the way a live count does.

Subject length is worth defending as a signal before it is trusted. A long
commit message is not inherently good practice — brevity is usually the goal.
Here it is read as *necessity*: a message is long when the reasoning does not
exist anywhere else and has nowhere else to go. A.I.M's messages run to 138
characters a week at their peak and settle at 64 by mid-September, so the
convergence is not stylistic tightening but reasoning migrating out of the
message and into a test or a written rule.

Counting subject keywords gives the same arc from a different direction:

| Month | test | pytest | README | feat | fix | chore | docs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Jun | 8 | 2 | 19 | 0 | 4 | 1 | 2 |
| Jul | 51 | 24 | 33 | 13 | 25 | 74 | 2 |
| Aug | 27 | 16 | 20 | 10 | 9 | 28 | 3 |
| Sep | 50 | 15 | 22 | 25 | 37 | 39 | 86 |

July's `feat` count of 13 and September's of 25 bracket the middle. The sharpest
movement is not in either: it is `docs`, at 2 in July and 86 in September, while
`chore` collapses from 74 to 39. Chores are the work of *maintaining* a thing
that already exists, and they dominate exactly when there is a lot to maintain.

Weekly resolution puts the turn more precisely than the monthly table can.
The narrative peak is **Weeks 28–29** (late July, 138.0 and 135.9 mean
characters), August is a genuine plateau at 92–110, and then **Week 38** drops to
63.7 — the single largest step in the whole run. June's 98.9 and September's 76.7
are similar, which is why the monthly figures understate the dip: the arc is
up, flat, sharply down, and only the weekly view shows it.

### Stage 1 — Beginner (Weeks 1–2, June): the terminal and Git

The first commits are `Created JSON Files to allow the IDE to run programs
locally` and `Imported PostgreSQL Folder to do SQL Command and scripting`.
Read those literally: a person learning to make a program run, and reaching
for configuration before understanding why it needed configuring. Git arrives
in the same fortnight (`git init`, `git status`, staging), and the habit of a
daily push snapshot is established immediately — which is why there are 714
commits rather than a dozen.

Also from this period, and still visible in the code today: the decision to
keep the scratch `.sql` file under `postgresql/sandbox/` reserved but unused,
rather than deleting it. Nothing depends on it, and it has cost nothing.

### Stage 2 — Beginner-plus (Weeks 3–5): syntax as the main event

Weeks 3 and 4 are conditionals and loops, in volume: `Added a NOT logical
operation example`, `updated conditions file to include an extra example on
while loops`, `Made a Prime Number Function to practice with numerical values`.
The commit subjects from this era are the clearest signal of the level: long,
narrative, and frequently explaining the reasoning *in the message*
(`Updated the following: - Included "U" to complete the word "Undefined" on
line 17 - replaced print("") to compress the file memory...`). That is a
beginner documenting decisions for themselves, because nothing else recorded
them.

Week 5 introduces the first data structures (lists, dictionaries, tuples,
sets, with the 85-game catalogue), and the tests start appearing
(`file(test logic): created a test case for its respective file`).

### Stage 3 — Intermediate (Weeks 6–9, July): abstraction and objects

Week 6 refactors loops into a reusable function — the first time the code is
restructured for reuse rather than for the algorithm. By Week 9 the
constructor, class attributes and inheritance are all in use, and the first
`__init__.py` files appear to make folders importable.

Two things distinguish this stage from the last one. First, the commit
subjects shorten: `feat: implement filter.py and map.py in functional_programming`
is terse because the work no longer needs narrating. Second, the code
defends itself — `chore: add OOP syntax fundamentals practice files` is
followed a few weeks later by `test: implement comprehensive automated test
suite for all Python modules`, which is the moment the project stops being a
demonstration and starts having a safety net.

### Stage 4 — Intermediate-plus (Weeks 10–12, August): tidying, renaming, data work

The data work arrives here, but all of it arrives **in one day**. On 2 August a
single burst commits `data_outlier.py`, `OutlierCapper`, ten Pandas notebooks
across the music and video-game folders, the trained `.joblib` and `.dot`
artefacts, and a `snake_case` rename sweep of the whole tree. Nothing about that
reads as a gradual "NumPy, then Pandas, then `groupby()`" curriculum — it is one
afternoon's work landing together, and the honest description is *breadth, not
sequence*.

What genuinely characterises August is not the libraries but the **renaming**,
and it is the month where the project starts paying for its own structure:

- `chore: rename 'Python' to 'python' due to folder rename change from 'Python' to 'python' to prevent pytest crashes`
- `chore(refactor folder): rename folder under snake_case format`
- `file(pytest): create pytest case dedicated for the previous git commit message made`

The `Python/` → `python/` change is the one that matters most, and it is worth
recording as a *measurement trap* rather than a victory. A per-file "first added"
query run today returns September for nearly every script, because the bulk of
the tree was re-added under the new lower-case path. Only querying the old
capitalised path recovers the true dates. **The lane was renamed on 2 August;
every script before that date is older than its own path suggests.**

This is also where the project's most valuable judgement appears, and it is a
judgement about *not* fixing things.

`chore: update VS Code settings to resolve Windows interpreter fallback` is
routine. The significant commits are these:

- `chore: 'rename Python' to 'python' due to folder rename change from 'Python' to 'python' to prevent pytest crashes`
- `fix: resolve pytest collection errors and refactor test suite`
- `chore: removed module.__name__ = "__main__" due to many pytest errors as it was a brute force to read all scripts not just math science project folder files`

Each records a problem found by the tooling rather than by inspection, and
each records the fix being *partial* — `"brute force"` is A.I.M's own word for
a test harness that was doing the wrong thing. Recognising that a failing
test suite can be the suite's fault is an intermediate-level insight, and it
is the direct ancestor of everything in Section 3.

### Stage 5 — Advanced in process, intermediate in code (Weeks 13–16, Sept)

The capstone weeks bring pipeline ingestion, statistical transformation and
the production README. Here the difficulty moves out of the Python and into
the workflow: branch-and-pull-request review, four-way mirroring, and the
rule system in `AGENTS.md` that now governs every change.

**The honest calibration, which `AGENTS.md` itself records: early-intermediate.**
A.I.M is strong at writing standalone coursework-style scripts and at
following process reliably. Still being learned are test-infrastructure
internals (runpy, mocking, coverage measurement) and metaprogramming. That is
a real and specific position, and it is the reason this document separates
*what A.I.M does* from *what the assistants do* — the boundary is drawn there,
not blurred.

The evidence that this is now stable rather than lucky: the project has
accumulated rules that a beginner would not think to write. Rule 11 (documented
defects stay defective), the coverage caps, the four-way mirror discipline, and
the commit-scope requirement are all the work of someone who has been burned by
the corresponding mistake and decided it should not happen again.

### Where the code scores

The file-ranking pass gives an external, if blunt, measure. Across 160 files:

| Band | Range | Files | Reading |
| --- | --- | --- | --- |
| A | 90–100 | 43 | Exemplary — runs clean, well-documented, durable |
| B | 80–89 | 90 | Strong — minor issues, mostly clean |
| C | 70–79 | 25 | Serviceable — documented defects or minor fragility |
| D | 60–69 | 2 | Weak — real bugs, fragile, or hard to read |
| E | 0–59 | 0 | Broken — cannot run, or misleads |

Mean 84.6. The spread is much narrower than the previous pass, and that is the
finding rather than a disappointment: 133 of 160 files sit in A or B because
the repository is in good shape, not because the rubric is generous. **No file
scores in band E**, and the only two below 70 share a single structural cause.

Two things about how the score is built are worth stating here, because both
change the reading of the numbers. The weights are not one set but two: a
**learning** script is judged on readability at 35%, because a reader has to
learn the idea from it, while an **applied** project is judged on fixability
and robustness at 30% each, because a user has to rely on it. Tier is measured
rather than declared — third-party import, hardcoded path, or class interface —
which is 8 files against 152. And thirteen files tie at 91, so "top three" is
not a claim about quality but about alphabetical order among equals; the sheet
breaks the tie on path, and `functools_module.py` leads only because it sorts
first.

They are `strings.py` at 64 and `variables.py` at 69, both flat scripts with no
function boundary: 321 and 175 lines respectively, so a reader has to hold the
whole file in their head and a test can only check the whole thing at once.
That is the one weakness the rescore was built to surface, and it is worth
acting on — splitting those two files would move the mean and would also make
them teach better.

The previous lowest, `main.py`, is no longer there. It was the deliberate
`IndentationError` stub — the one file in the repository that could not run at
all — and A.I.M added `pass` so it does. It now scores in the middle of the
range and appears in coverage like any other file. That single change also moved
the measured denominator from 159 to 161 and the files-at-100%-lines count from
148 to 150, which is the whole cost of a three-line fix written down: it had to
be reflected in six places, and the guards caught every one.

Rule 11's defects score higher than these, and deliberately so. `conditions.py`
carries a hardcoded `temperature = 25` that makes most of its branches
unreachable, yet it scores above both flat scripts because Risk floors a
documented, test-pinned defect at 72: a defect whose docstring names it and
whose test guards it is *visible* risk, which is the only kind worth carrying
on purpose. An invisible defect and an undocumented flat script are worse.

---

## 3. Corrections, mistakes, and what they cost

This section is the point of the review. None of the following is tidied up.

### 3.1 The mistakes A.I.M made

**The folder rename that broke collection.** Renaming `Python` to `python`
(the repo is on a case-insensitive Windows filesystem) silently changed what
`import` resolved. It was caught by pytest rather than by inspection, and the
fix was in the test configuration, not the code. The commit subject records
the lesson: `to prevent pytest crashes`.

**A `decimal` circular import that killed a file ~60 lines in.**
`fundamental_topics/numbers.py` died whenever run directly, because
`decimal` → `_pydecimal` → `import numbers` resolved to the teaching file
itself, which re-entered and asked `decimal` for `Decimal` while `decimal` was
still half-initialised. The test harness hid it completely, because the real
stdlib `numbers` is already cached in `sys.modules` under pytest. Fixed by
dropping the file's own folder from `sys.path`.

This is the most instructive bug in the project, and the reason it is written
up at length in `NOTES.md`: *the test suite was green and the program was
still broken*. The only way to catch it was to run the file the way a user
would — which is why `scripts/execution_time.py` exists.

**A formatting guard that made the program lie.** `arithmetic_expressions.py`
applied a `:.2f` format to an *error string*, which killed the results loop
and reported bad input for numbers that were perfectly valid. Unlike the
defects that were kept, this one was repaired: a program that reports a valid
input as invalid is lying, and rule 11 only protects deliberate teaching
artefacts, not lies.

**An uncaught `IndexError` on an empty answer** in `login_status.py`,
repaired for the same reason.

**Two `./` vs `../` corrections** in `sine_rule.py`'s trigonometry, where
angle ranges were mishandled so that valid inputs such as 100 degrees were
rejected.

### 3.2 The mistakes the assistants made

These are recorded because the assistants are part of the method, and their
errors are part of the record.

**A `git reset --hard` that destroyed unsaved work.** During a routine
cleanup of a test probe, a `git reset --hard` wiped an in-progress fix along
with the probe. The fix had to be re-applied from scratch. The lesson is
recorded in the workflow: prefer a soft reset plus a targeted restore over a
hard one, and always check `git status` before a reset on a branch carrying
uncommitted work.

**Two probe commits left permanently in the history.** To prove the
commit-scope guard actually failed rather than passing vacuously, deliberately
unscoped commits were created. They worked; cleaning them up did not. Because
`main` is never force-pushed (rule 12), those commits are permanent, and the
guard carries an explicit exemption for them with a comment explaining why.

**A merge commit that broke the guard it had just passed.** The first
correction to `main` arrived as `44eb1c1 Merge pull request #11 from ...` —
a subject generated by the forge, carrying no scope. The commit-scope guard
immediately failed on `main` itself. This was the most instructive failure of
the workflow: a rule strict enough to punish correct behaviour gets ignored,
and then protects nothing. The fix was to exempt merge commits by parent count
rather than to loosen the rule, and to record the exemption in rule 12 so it
stays a stated rule rather than a hidden carve-out.

**A test that asserted the wrong denominator.** An early version of the
coverage guard computed 160 measured files where coverage measures 159,
because it counted 22 empty `__init__.py` files and `sandbox/aim.py` but
forgot that `main.py` — the deliberate `IndentationError` stub — is excluded
from the report entirely for being unparseable. The number was wrong by one
and the test caught it.

### 3.3 The mistakes the documentation made

Worth its own subsection, because documentation drift is the most common
failure mode in a self-directed project and the hardest to notice.

The feature summary claimed **98% branch coverage** when the real figure was
95%, and **171 of 182 files at 100% lines** when it was 148 of 159. The
`182` was the number of rows the coverage table prints, which includes 23
files containing no statements at all; the honest denominator is the 159 files
that actually carry at least one.

A checklist said **29 dead-by-design lines in exactly 8 caps** when coverage
reported 38 lines across 11. The ranking sheet itself had **112 of 161
headings** that had drifted away from their own tables, a duplicated section
that made 167 entries out of 161 files, and **9 entries** that rounded an exact
`.5` weighted sum downward while 50 rounded it upward — including
`rock_paper_scissors.py` at 74.5 → 75 next to `qrcode_generator.py` at
74.5 → 74, the same sum with two answers.

**Every one of these is now pinned by a test** in
`tests/test_scripts/test_repo_doc_numbers.py` and
`tests/test_scripts/test_ranking_docs.py`. The generalisation: a fact written
in prose and never recomputed is a fact that will be wrong, and the only
durable answer is to make the stale number fail the build.

---

## 4. AI collaboration: what was used, and how

### 4.0 Who actually wrote the code

`git shortlog -sne main` lists five author identities across the branch. All
five are the same person, writing under three different names and two email
addresses:

| Author identity | Commits on `main` | What it is |
| --- | --- | --- |
| Personal account | 668 | The owner's own GitHub identity |
| University handle | 32 | The owner's university account, used early in the run |
| `A.I.M` | 16 | The pseudonym hardcoded as `name` in several scripts |
| Personal account, university email | 10 | The same account re-authoring after the email changed |
| `ThenameisAiman` | 3 | A second account used for a handful of commits |

Those five rows sum to the branch's current total, which is a live figure and
deliberately not written here; the review's fixed commit count appears in
section 5 and is the one the guards hold.

There is no bot on `main`. `dependabot[bot]` has opened 7 pull requests and
those sit on `origin/dependabot/*` branches that were never merged, so
`git shortlog --all` counts it while `git shortlog -sne main` does not. That
difference is why the table is scoped to `main`: the branch is the portfolio,
and the branch is what the numbers should describe. It is also why an earlier
draft of this section, which used `--all`, reported seven commits by a bot
that has never touched `main`.

This is a one-person project with an AI-assisted workflow layered on top. The
"contributors" are the owner's own identities; every line of code was written
by A.I.M, with AI assistants acting as tools rather than co-authors. That
distinction is why `AGENTS.md` separates *what A.I.M does* from *what the
assistants do* — the boundary is drawn at authorship, not at effort.

### 4.1 The three assistants and their division of labour

A.I.M ran three assistants over the project and used them deliberately
differently, as recorded in `AGENTS.md`:

| Assistant | Used for | Why |
| --- | --- | --- |
| **OpenCode** (plan → execute → verify) | Multi-file repo work; reading, editing, running the pinned interpreter in one loop | Best at holding a repo-wide task to completion; the default for anything spanning several files |
| **Claude** | Code queries, small fixes, debugging | Its distinguishing strength is code specifically — ask it to critique or patch, not to redesign |
| **Gemini** | Research sweeps, long-context reading, open-ended ideas | More generative and broad; its line-level claims are candidates to verify, not ground truth |

The shared failure mode, recorded because it applies to all three: each one
pattern-matches an open prompt like "make it better" and over-reaches. The
`Goal / Files / Constraints / Verify` block exists precisely to prevent that.

### 4.2 What replaced what, and why

**Gemini and Claude were replaced by OpenCode for terminal usage.** The
change was not that the others became worse; it was that OpenCode could do the
whole loop in one place. A.I.M's own summary: OpenCode is strongest at
*plan → execute → verify over the repo* — it reads the files, makes the
edits, and runs `.venv-win/Scripts/python.exe -m pytest` itself. Claude and
Gemini remained in use for code-specific critique and research respectively,
but the terminal work — the part where a change is only real once the pinned
interpreter agrees — consolidated onto one assistant that could verify its own
work in the same turn.

The practical benefit is visible in this document's own history: the ranking
reconciliation above was found by writing a test that read the markdown and
compared it to the tree, not by re-reading the prose. An assistant that can
run the check can close the loop; one that can only suggest a check leaves it
open.

### 4.3 Model rotation, and why it matters

Within OpenCode, A.I.M rotates across **eleven free models** — Big Pickle Free,
Space Bunny Free, Nemotron 3.5 Lightning Free, Nemotron 3 Ultra Free, Ling 3.0
Flash Fin Free, Ling 3.1 Flash Free, Muse Spark 1.3 Contributor Free,
MiMo-V2.6-Flash Free, MiMo-V2.5 Free, LongCat 2.5 Preview Free and
Fledge Alpha Free. The rotation is selected in the console, not from inside a
conversation: an agent cannot switch its own model mid-session.

**An agent cannot reliably self-identify which model is processing a
conversation.** This is stated in `AGENTS.md` because the false claim was
actually made and written into the repository — the line
`This conversation runs on space-bunny-free` had to be removed and replaced
with this note. A model's self-report is not evidence.

The rotation is worth the effort for a reason that is easy to miss: **the same
prompt handled by different models surfaces different mistakes.** Asking two
models the same question and comparing where they disagree is a cheap second
opinion that does not depend on either being right. In practice A.I.M treats
every model's line-level claim — including a line-level claim from the model
currently writing the code — as a *candidate* to be verified against the repo,
never as ground truth. The test suite is the arbiter.

#### The rotation needed a rule, not just a list

The eleven-model list in `AGENTS.md` answers *which model to pick*, but it
initially answered nothing about what happens when a model is executing and
realises the task does not fit it. A.I.M's instruction was blunt: make each
model's pros, cons and main purpose clear, and if the task is not applicable to
the model currently running, it must ask for a different one rather than
produce a mediocre answer that looks like an answer.

That produced two rules now written into `AGENTS.md`.

**First, each model carries an explicit ceiling.** The pros/cons table sits
beside the pick-a-model table because knowing a model's *limits* is what lets
it decline honestly. Without it, "I am not the right model for this" has no
stated basis, and a model under pressure to produce something will produce
something. The ceilings are not opinions here — they are the route limits, the
privacy exceptions and the recorded failures already verified on this page. A
model declining a 1M-window refactor because its output ceiling is 128,000 is
citing a measured number, not expressing a preference.

**Second, a decline must name three alternatives, ranked.** The ranking is the
substance of the rule. A list of all eleven remaining models transfers the whole
decision back to A.I.M and saves him nothing; a ranked three is a decision he
can act on without researching. The table in `AGENTS.md` gives every model its
own fallback column for the same reason, because the right alternative for a
1M-window debugging session is not the right alternative for a one-file edit.

Two constraints keep this honest rather than ceremonial:

- **A hand-off is a request, not a switch.** Model selection happens in the
  OpenCode console, so an agent cannot move itself. The correct behaviour is to
  stop and name the model that should take over, not to continue in the same
  turn hoping the switch lands. Continuing would produce exactly the mediocre
  answer the rule exists to prevent.
- **Privacy outranks fit.** If a prompt carries anything personal,
  confidential or credential-bearing, the ranked column is overridden rather
  than consulted: only Space Bunny and LongCat are zero-retention, so the other
  five are ineligible regardless of how well they fit. This is the one place
  where the "best model for the task" question has the wrong answer.

The rule is also the one piece of this documentation that the models will
actually read, because it is addressed to them rather than to a future
reader. Which is the point: a convention that only appears in a document
nobody re-reads has not been enforced, it has been filed.

#### The pre-flight, and why the choice is not about speed

The rotation grew a selection rule after the tables above were written, because
a list of models is a menu and not a decision. A.I.M's instruction was blunt:
before a model executes, confirm its token usage, confirm how much of the
allowance is left, and confirm that the model is the applicable one for the
task at hand — on efficiency, correctness and speed, with speed the *least*
weight.

That last clause is the whole rule, and it reverses the obvious reading. Speed
is usually the first question asked of a free model, because a free tier is
also a slow one and the temptation is to pick whatever answers fastest. But a
fast answer from a 200,000-token window on a task that needs a 1M window is not
a cheaper answer, it is a wrong answer that has to be redone — and the redo
costs more time than the saving. So the order is fixed: tokens first (does the
task fit the limits), allowance second (how much is unspent, which only
A.I.M can read from the console), applicability third (is this the model's
job), with speed only ever breaking a tie between models that already fit.

The correction this produced is visible in the model tables themselves. Each
row now ends with what the model is actually used for *after* correction, and
several of those corrections moved a model away from the role its own limits
argue against: Big Pickle from "default builder" to review only, MiMo from
"code generation" to boilerplate and docs only, because a 32,000 output
ceiling cannot finish a patch it has begun. That is the pre-flight question
three asked once per model and answered from a number rather than a
preference.

#### What the research shows about each model

The route limits below are OpenCode's own, not the model's full capability, and
they are what this project actually gets. Both columns come from the
`models.dev` registry entries for the `opencode` provider
(`https://models.dev/api.json`, retrieved 7 October 2026) — exact token
counts, because the rounded versions are ambiguous: 262,144 is 256K, not
262K. The free-pricing and privacy columns come from
<https://opencode.ai/v2/docs/zen/>. Usage figures are OpenCode's published weekly
token volume for the week ending 7 October 2026
(<https://opencode.ai/data/>) and are a snapshot, not a ranking to plan around.

| Model | Route context | Route output | Free-period data used to improve the model? | Weekly tokens | Share of listed traffic |
| --- | --- | --- | --- | --- | --- |
| Space Bunny Free | 1,048,576 | 524,288 | No — zero-retention | 53T | 36.6% |
| Muse Spark 1.3 Contributor Free | 1,048,576 | 131,072 | Yes — trains future Meta models | 33T | 22.8% |
| MiMo-V2.6-Flash Free | 200,000 | 32,000 | Yes | 10T | 6.9% |
| Nemotron 3 Ultra Free | 1,000,000 | 128,000 | NVIDIA trial terms; use is logged | 3.6T | 2.5% |
| LongCat 2.5 Preview Free | 1,000,000 | 131,072 | No — zero-retention | 2.1T | 1.4% |
| Fledge Alpha Free | 1,048,576 | 131,072 | Yes — free-period data exception | 1.8T | 1.2% |
| MiMo-V2.5 Free | 200,000 | 32,000 | Yes | 656B | 0.45% |
| Nemotron 3.5 Lightning Free | 262,144 | 262,144 | NVIDIA trial terms; use is logged | 412B | 0.28% |
| Ling 3.0 Flash Fin Free | 262,144 | 32,768 | Yes | below the published top-18 | unmeasured |
| Ling 3.1 Flash Free | 262,144 | 32,768 | Yes | below the published top-18 | unmeasured |
| Big Pickle Free | 200,000 | 32,000 | Yes | below the published top-18 | unmeasured |

The traffic columns are OpenCode's published weekly figures for the week
ending 7 October 2026, expressed as a share of the 144.879T tokens across the
eighteen models that page lists — a share of the listed models, not of all
OpenCode traffic. They replace an earlier daily snapshot taken on 1 October
and a weekly one for the week ending 2 October, which is the same shape of
number at a different resolution.

The table is sorted by observed volume rather than by role, because the
ordering is the finding: the two models A.I.M reached for by default are the
two the whole platform also reaches for, which is not the same as being the
right tool for this repo. The `models.dev` registry also has to be read per
provider, not per model — the same MiMo release is 200,000 on the OpenCode
free route and 1,048,576 everywhere else, so a single "MiMo has a 1M window"
line is true and useless.

**Key sources, each retrieved 7 October 2026:**

- OpenCode Zen documentation: `https://opencode.ai/v2/docs/zen/` — the model list,
  the free-on-input/output/cached-read pricing table, and the privacy section
  that names each exception.
- OpenCode model data: `https://opencode.ai/data/` — weekly token volumes,
  unique users and weekly retention per model, for the week ending 7 October
  2026.
- Models.dev registry: `https://models.dev/api.json` — context window, output
  limit, reasoning and tool-calling support, and release date per model, keyed
  by provider. This is the source for the two limit columns.

**What the research actually established:**

- **The free route is a narrower window than the model.** MiMo-V2.6-Flash is a
  1M-context model at every paid provider, but the OpenCode free route serves
  it at 200K. Nemotron 3 Ultra is 1M. Reading a context number as a capability
  claim would therefore have been wrong in both directions, which is why the
  limits above are labelled "route" rather than "model".
- **Privacy does not split the rotation cleanly.** Two models (Space Bunny,
  LongCat) sit on the zero-retention default. Seven (Big Pickle, Fledge Alpha
  Free, both MiMos, both Lings) may have free-period data used to
  improve the model. Two (the Nemotrons) are NVIDIA trial endpoints that log
  use and whose terms ask for no personal or confidential data. One (Muse Spark
  1.3 Contributor) is explicitly a training-data trade. Nine of the eleven send
  prompts somewhere that is not covered by a verified zero-retention default,
  which is why rule 6 exists.
- **The free tier is popular, so it is not private by default.** Five of the
  eleven are 1M-class routes — Space Bunny, Muse Spark 1.3, Nemotron 3 Ultra,
  LongCat 2.5 and Fledge Alpha Free — and four of those five now chart
  on the published table, Space Bunny and Muse Spark 1.3 alone carrying 36.6%
  and 22.8% of listed traffic between them. Being on a free
  tier says nothing about who else can read the prompt.
- **Two models are named for what they are not.** Big Pickle and Space Bunny
  are both described by OpenCode as "stealth models" with no published vendor,
  so any claim about which lab built either one is speculation. The earlier
  draft of this section asserted a DeepSeek origin for Big Pickle from leaked
  provider errors; that was removed, because a provider's error strings are not
  a provenance record.

- **The newest model is also the least proven, and it failed in the first
  session.** Fledge Alpha Free released on 1 October 2026, and on 2 October it
  returned `Upstream request failed: Endpoint is unavailable.` That is now
  recorded in `AGENTS.md` as a stability fact alongside `nemotron-3-ultra-free`
  and `big-pickle`, both of which had already thrown upstream errors. Three of
  twelve free routes are now known to be unstable, which is a stronger argument
  for the hand-off rule than any of the three had been on its own.

**What was claimed earlier and did not survive checking.** An earlier draft of
this section cited a benchmark page for a "50.8% resolve rate on Scale AI's SWE
Atlas Codebase QnA" for Big Pickle, and a model-catalogue page for
compatibility flags. Both URLs were checked on 1 October 2026: the first
resolves to a technology news aggregator whose front page mentions neither
Big Pickle nor SWE Atlas, and the second returns HTTP 404. The benchmark
figure could not be traced to a source that exists, so it is gone rather than
hedged. Several per-model performance claims (tool-call efficiency, tokens-per-
turn, parameter counts) went with it, for the same reason.

#### The pre-flight's second question, given a file to read

The pre-flight above asks three questions before a model runs, and question two

- how much allowance is left - was the one an agent could not answer at all. It
was answered honestly at the time by refusing to guess, but a rule that is
always unanswerable is not a rule: it is a question that trains everyone to skip
it. A.I.M's later instruction was to name the file an agent reads first.

`agentic_models/MODEL_ALLOWANCE.md` is that file, and splitting the question in two is what
made it answerable. **Token usage is locally measurable** - `opencode stats
--models`, `opencode db`, and the session database at
`~/.local/share/opencode/opencode.db` all carry per-model input, output and
cache-read totals, and the file records them. **The remaining percentage is
not**, because it lives in the OpenCode console, so the only honest local
evidence of exhaustion is the failure itself: `Rate limit exceeded. Please try
again later.` in `~/.local/share/opencode/log/`, timestamped and naming the
model that hit it. Eleven such failures are on record across `big-pickle` (six times, 26 Sep), `muse-spark-1.3-contributor-free` (three times, 26 Sep), `mimo-v2.6-flash-free` (26 Sep) and `longcat-2.5-preview-free` (1 Oct) — and none since.

That asymmetry is the design, and it produced the file's most important line: an
empty or stale row **fails** question two rather than passing it. A blank table
has to read as "ask A.I.M", because a guard that silently passes is worse than
no guard - it reads as coverage. The cost is stated rather than hidden: on any
long run with the table empty, the correct behaviour is to stop and ask, which is
a question A.I.M had not been asked before.

Two things the file deliberately refuses to do. It does not estimate a
percentage, because a guess in a table is exactly the failure mode
`test_model_rotation_docs.py` forbids for the traffic shares - `unmeasured` is
the honest cell and the same discipline applies here. And it names the
credential tables it will never read (`account`, `control_account`,
`credential` all hold live tokens in `opencode.db`), because rule 6 protects the
local store as much as it protects a prompt.

The guard was bite-tested before being believed, and the bite-testing found a
weakness in the guard rather than in the document. Deleting the file fails the
suite, as it should. But the first version also passed against a mutation that
dropped the folder from one of the two references to it, because it checked
that the file's *name* appeared somewhere in the pre-flight rather than that
  every reference was the correct path - and after the file moved into
  `agentic_models/`, a name present somewhere and a path that opens are two
different things. The check now enumerates every backticked mention and
requires each to be the real relative path, which is what catches the realistic
failure: an agent following a stale `MODEL_ALLOWANCE.md` from the repository
root and finding nothing there.

That move is the other half of this session's work, and it is worth recording
for what it says about the repo's own layout rule. Rule 7 says keep the README
tree and `TREE_SKIP` in sync when folders move, and the tree guard enforces it
from both directions - but it also carried an explicit allow-list of root
documents, so `MODEL_ALLOWANCE.md` had been added to that list one commit
earlier and was now being *removed* from it. A guard that pins an explicit list
is a list that has to be maintained, and the cheaper shape turned out to be
`allowed_parents`: naming the folder once admits any document inside it, so the
next file to move there needs no edit to the test at all. That prediction was
tested the next day: on 9 October `AGENTS.md` itself moved in beside the
allowance file and the folder was renamed `agentic_models/`, and the only edit
the tree guard needed was the folder name in `allowed_parents` plus dropping
`AGENTS.md` from the root-document allow-list — no new exception, no new test.

This is the repo's own rule 2 - treat an assistant's line-level claim as a
candidate, not ground truth - catching an assistant. The failure was not a
hallucinated statistic appearing from nowhere; it was a real-looking URL
attached to a figure nobody had published. **A link that resolves is not
evidence; the link has to resolve to the claim.**

#### Independent capability evidence, retrieved 8 October 2026

A.I.M asked for the rotation to be ranked from outside evidence — articles,
reports and genuine reviews — rather than from his own usage, explicitly
excluding the traffic table above, which measures popularity and not
suitability. Three findings came out of it, and one of them corrects a
judgement this file had already recorded.

**The free route's own limits understate two models.** Nemotron 3 Ultra Free is
capped at 128,000 output against a 1,000,000-token window on the OpenCode free
route, which reads like a weak model and was corrected down to "complex
debugging" for exactly that reason. Measured capability says otherwise: 47.7 on
the Artificial Analysis Intelligence Index at release (48.2 in BF16), the
strongest US open-weights release, with RULER 94.7 at 1M context, SWE-Bench
Verified 71.9, PinchBench 90 and over 400 tokens per second. The 128,000 ceiling
is real and still governs planning a single response; what it does not govern is
whether the model is any good. Fledge Alpha Free is the mirror image: its 131,072
output against a 1,048,576 window is generous, and its measured coding is the
best of the three stealth routes (Terminal-Bench 79, SciCode 52, SWE-Mini 75, and
15 of 15 on an independent bug-fix battery), while its factual knowledge is the
worst figure in the whole rotation — an Omniscience index of −5, 37 right against
42 wrong, 67% hallucination. Big Pickle Free's corrected use of "review only"
was recorded on 29 September as a consequence of its 200,000 window; the
external evidence agrees with the conclusion and supplies the missing reason,
which is that it is the best *knowledge* model available — Omniscience +43, 38%
on Humanity's Last Exam, and the only model in the battery that answered all 100
questions rather than leaving some blank.

**The measurement itself has to be policed harder than the models.** Three
rules were applied to the incoming figures and each one changed what could be
claimed. A benchmark is not a verdict: NVIDIA, Meta, Xiaomi and Meituan all
publish vendor-run rows, a vendor harness and a vendor grader are not a neutral
comparison, and Meta's own scorecard is the sharpest case — its Muse Spark 1.3
column is the gated `max` tier while its 1.2 column is `xhigh`, so part of the
headline jump is a reasoning-tier change rather than a generation change. Index
versions do not travel: Artificial Analysis rescores its composite when it
revises it, and the same model reads 47.7 at release and 38 on a later build of
the same v4.1.1 index, which is why every figure above names its snapshot. And a
stealth model has no index at all, so the only like-for-like evidence for Big
Pickle, Space Bunny and Fledge Alpha is one reviewer's own five-benchmark
battery — labelled as a single source rather than presented as a leaderboard.

**The counterweight is the finding that matters most.** That same independent
reviewer put the three stealth models against two *paid* references on the same
gateway, and none of the three free models beat the cheapest paid reference on
agent work: DeepSeek V4.1 Flash solved 14 of 14 on Terminal-Bench and 17 of 20
on SWE-Mini, more than any free route, at a lower cost than two of the three.
Big Pickle beat both paid references on knowledge. So the free tier is good
value and specifically useful — it is not competitive with a paid route on
agentic work, and the rotation's value is that it gives A.I.M a cheap second
opinion and a free first pass, not that it replaces a frontier model.

Two provenance notes are recorded because they are the failure mode this
project has already paid for once. LongCat 2.5 Preview Free has
published no benchmark of any kind; its family's last published figure is
LongCat-2.0's 59.5 on SWE-bench Pro, which does not transfer to a new release,
and Meituan's own "two weeks" framing for the free window puts its end around
10 October 2026 — two days after this was written.

**Sources, all retrieved 8 October 2026:** Artificial Analysis model pages and
index articles (`artificialanalysis.ai`); Fellipe Soares' independent
stealth-model battery of 2 and 4 October 2026 (`fellipesoares.com.br`), which is
the only like-for-like comparison of the three stealth routes; NVIDIA's release
material and open-weights model card (`research.nvidia.com`,
`huggingface.co/nvidia`); Meta's Muse Spark 1.3 announcement with its own
four-model scorecard plus the independent rescore two days later; Meituan's
LongCat platform changelog and model documentation; and OpenRouter's model pages
for provider-side route behaviour, context limits and throughput.

### 4.4 The rules that keep the collaboration honest

Three conventions, all added because the failure they prevent actually
happened:

1. **Verification culture.** Every change is accompanied by the exact command
   and its output, so A.I.M can re-run it himself. A claim without a command
   is an opinion.
2. **Fact vs heuristic vs opinion.** Claims are labelled, and the repo is the
   final authority — this file, the tests, and the results of the commands
   shown.
3. **AI-authored comments are marked.** Anything an assistant writes to explain
   its own fix starts with an `[AI-authored fix]` marker inside a `"""` block,
   so it is instantly distinguishable from A.I.M's own notes. Comments explain
   *why*, not *what*; short notes use `#` (max two lines), longer ones use
   `"""` blocks.

### 4.5 What the git history can and cannot show about model use

This section exists because an earlier draft of this review implied the commit
history could identify which model wrote what. It cannot, and the honest
version is worth more than the impressive one.

**What is measurable.** The tooling timeline is recoverable from the tree:

| Evidence | First appears | What it shows |
| --- | --- | --- |
| `AGENTS.md` created | 15 Sep 2026 | The owner started writing down conventions for assistants |
| Model rotation documented | 26 Sep 2026 | The free-tier rotation became a deliberate practice |
| Scoped commit messages enforced | 29 Sep 2026 | Rule 12 promoted from rule of thumb after five violations |
| This review's own corrections | 29–30 Sep 2026 | The guards were written as part of reviewing the review |

Commit volume rose through the run — 154 in June, 227 in July, 108 in August,
240 in September — which shows sustained work, not which tool did it.

**What is not measurable.** Nothing in the repository records a model ID per
commit. A conventional-commit subject, a comment marker and a docstring tell
you *that* an assistant was involved, never *which* one. So the per-model
usage ratings in `AGENTS.md` are **A.I.M's own assessment of his habits**, not
a measurement, and the only part that is measured is the imbalance: two models
logged most of the sessions and the four with genuinely large context windows
logged the fewest.

**Why this distinction matters for the career plan.** The post-university ladder
is Data Analyst → Data Science → ML/AI. In that field, the ability to say "I
used model X" is worth very little and "here is how I verified it" is worth a
great deal. This section is deliberately the weakest claim in the document for
that reason. The research correction above is the same lesson applied to a
harder case: a plausible URL with an unverifiable figure behind it is worse
than no claim, because it invites someone to rely on it.

### 4.6 How useful each markdown file actually is

A.I.M asked for an honest ranking of the repo's own documents, scored by how
much they help a reader (or a future contributor) rather than by how much
effort went into them.

| File | Usefulness | Verdict |
| --- | --- | --- |
| `PROGRESSION.md` | 9/10 | The only document that explains *why* the project is shaped this way. Highest value per line, and the only one carrying the correction record |
| `AGENTS.md` | 8/10 | Operational rules an assistant or contributor needs on the first day. Long, but almost every section is load-bearing |
| `NOTES.md` | 7/10 | The engineering diary. Valuable as history, hard to navigate — superseded figures are still marked rather than removed, which costs a reader time |
| `README.md` | 6/10 | Does its job as an entrance, but the tree and install instructions have outgrown the project and need pruning |
| `FILE_RANKING_GUIDE.md` | 5/10 | Explains the scoring method well. Once the scores exist, the method is interesting rather than necessary |
| `FILE_SCORES.md` | 4/10 | 160 entries of generated output. One command regenerates it, so almost none of it needs to be read by hand — and a reader who opens it by hand is reading the least interesting file in the repo |

The honest summary is that this repository's documentation effort is
front-loaded: two files carry most of the value, and the remaining four are
either regenerable (`FILE_SCORES.md`) or better served by deletion than by
maintenance. The meta-work around this project has been proportionally larger
than its code work at times, which is worth noticing precisely because the
career plan says the next gap is *applied* experience, not more process.

### 4.7 Chronology of the usage of AI tooling as the git log records it

| Date | Milestone | Evidence |
| --- | --- | --- |
| 15 Sep 2026 | `AGENTS.md` created with project conventions and git workflow – no AI tool named yet | `bb7edc4` |
| 17 Sep 2026 | OpenCode first named in AGENTS.md, alongside Claude and Gemini, for cross-auditing | `938689c` |
| 20 Sep 2026 | Tool-choice guide records OpenCode as the default plan → execute → verify tool for terminal work, Claude for code critique, Gemini for research | `2ebe8da` |
| 26 Sep 2026 | Free-tier OpenCode model rotation recorded in AGENTS.md – seven models | `024cc12` |
| 29 Sep 2026 | PROGRESSION.md created; the review summary states Claude and Gemini were replaced by OpenCode for terminal usage | `4fad60b` |
| 1 Oct 2026 | Free-model rotation verified against `models.dev` and OpenCode's published pages; LongCat 2.5 Preview Free added, making it eight models | `8b9e4fe` |
| 1 Oct 2026 | Model ceiling table and the three-ranked hand-off rule added; `test_model_rotation_docs.py` guard created | `45ca43f` |
| 2 Oct 2026 | Fledge Alpha Free added; rotation now nine models | `c420e33`, `80f4b47`, `0c3a55f` |
| 2 Oct 2026 | `requirements/` and `file_scores_ranking/` reorganisation; Dependabot and pyproject paths updated | `a4e468f`, `bced1be` |
| 7 Oct 2026 | Model tables refreshed to twelve free routes: Exo Free, MiMo-V2.5 Free and Ling 3.1 Flash Free added; Fledge Alpha Free confirmed documented rather than undocumented | `a1a13f0` |
| 9 Oct 2026 | `MODEL_ALLOWANCE.md` added as the pre-flight read before every model switch; `AGENTS.md` and the allowance file moved together under `agentic_models/` | `d508dda`, `ef87752`, `56cbd47` |
| 11 Oct 2026 | Exo Free removed from the rotation (deprecated upstream); count twelve -> eleven | `6792d94`, `e492549` |

---

## 5. The corrections loop, as practised

The project's correction workflow is recorded in `AGENTS.md` and was used
twice during this review:

> A mistake on `main` is corrected on a branch, never on `main` directly. Open
> a branch, commit the fix with a subject stating both the change and the issue
> behind it, verify it properly, then force-push the branch and open a pull
> request. `main` is never force-pushed, so a bad commit is not erased — it is
> superseded.

Verification before force-push means more than "the tests pass":

- the full suite green, run **more than once**;
- for a change to a script, the script **executed for real** with
  representative user input — `scripts/execution_time.py --all` is the only
  harness that runs every file standalone;
- the wrong behaviour **reproduced before the fix** and shown absent after;
- any test added to prove a fix confirmed to **fail against the old code**,
  otherwise it may be passing for an unrelated reason.

Branch and PR work is force-pushed with `--force-with-lease` so a stale local
ref cannot clobber someone else's work, and the same shape is applied to all
four mirrors — a correction applied on the GitHub Project and not on the
GitLab backup is a half-applied correction. That discipline caught a real
drift during this review: after two merges reached only the GitHub Project, two
mirrors were found lagging at an older commit.

---

## 6. Where the project stands

| | |
| --- | --- |
| Tests | 2042 passing, 0 failing |
| Coverage | 99% line, 95% branch |
| Quality mean | 84.6/100 over 160 files |
| Document drift | 0 known — all numeric claims test-guarded |
| Mirrors | 4, synchronised |
| Frozen lane | `object_oriented_programming/` — `decorator.py`, `generator.py`, `multitasking.py`, `dice.py` |

Next, per the roadmap in `README.md`: Year 2 (CS2DA Data Analytics, CS2PP
Python Programming, CS2SE Software Engineering, then CS2AI, CS2ON, CS2SD),
followed by Summer 2027 Block II and the Year 3 project work.

---

## 7. Session log

This review is not a finished document. It is appended to whenever the project
moves, per project rule 13: a session that changes the project but leaves this
log unchanged has left the record behind. Newest first.

| Date | Session | What changed | What it taught |
| 25 Oct 2026 | Pytest coverage added for the twelve translated coursework modules | Added `tests/test_university_courseworks/test_cs1ip_translations.py` (32 tests) and `tests/test_university_courseworks/test_cs2da_translations.py` (20 tests) covering the eight CS1IP translations (print loop, fall/bounce ball, snakes and ladders, doodle, doodle house, door animation, falling snow) and the four CS2DA translations (convex hull, AVL symbol table, AVL set, sort benchmark). Each module is exercised with the known Java-derived fixtures (exact print output, five door frames, the `S E A R C H E X A M P L E` sample, all four sorts against `sorted()`) plus fresh inputs and outputs (edge heights, overshooting dice rolls, zero-ray suns, removal of off-screen flakes, AVL corruption). Exception messages are asserted verbatim (`argument to get() is null`, `called min() with empty symbol table`, `k is not in range 0-{size-1}`, `timer already started`, `timer was not started`). GUI tests use recording canvas/root doubles instead of a real Tk window, and the sort benchmark wiring is tested without running the ten-second loop. The test-equity ratchets were raised to 130 unattributed cases and 400 unattributed guards to absorb the new functions, and the density min/max ratio ratchet to 450. Full suite 2042 passed, 0 failed, 0 skipped, 0 warnings with `-W error` on Windows. | A test that only re-runs the known fixture cannot catch a regression that changes the fixture too, so each module is given both the Java-derived case and a fresh one. The GUI doubles are the part that keeps the suite headless: real Tk windows cannot open on WSL, so the recording canvas is the only way to assert drawing order without a display. The equity instrument counts test functions, not parametrised cases, so adding many methods moves the ratchet even when the code under test is unchanged; raising the ratchet with a comment is the honest response, not silently loosening it. |
| 23 Oct 2026 | WSL suite re-run after the skip removal, and the live counts corrected | The WSL/Linux run that had been outstanding since the three `skipif` markers were removed was executed on `ffbeeb5`: `.venv-wsl/bin/python -m pytest -W error -q` reports 2042 passed, 0 failed, 0 skipped and 0 warnings in 10:35, level with the Windows run. The two live documents that still quoted the old figure were corrected: root `AGENTS.md` and the environment table in `agentic_models/AGENTS.md` now say 2042 passed instead of 1800 passed with 12 skipped. The historical rows in this file keep the old figure, because the append-only rule protects the record rather than the current state. | A count measured on one platform is a claim about that platform, not about the suite. The twelve skips were removed at the root cause (portable paths and a tkinter stub), so the WSL run reaching the same 2042 is the evidence that the fix was cross-platform rather than a Windows-only workaround. It also shows the limit of the Windows guards: they cannot see the WSL tally, which is why the stale 1800 survived a green suite - a number no test asserts is a number that drifts silently. |
| 23 Oct 2026 | Remaining Java coursework translated to Python, line by line | Twelve Java files that had no Python twin were translated: eight in year 1 semester 1 CS1IP (`week3` console loops and games, the two `week8` lecture drawings, the `week8` practical door animation, and the `week12` falling-snow window) and four in year 2 semester 1 CS2DA (`DCConvexHull`, `AVLTreeST`, `BasicAvlTreeSet`, `SortBenchmark`). Each translation keeps the Java method boundaries and explains the non-obvious mappings in place: `LinkedList.removeFirst` becomes `pop(0)` with its cost stated, Swing `drawOval` and `fillOval` become tkinter `create_oval` with the width-and-height-to-corner conversion, `ThreadMXBean.getCurrentThreadCpuTime` becomes `time.thread_time_ns`, Java text-block leading-newline semantics become an explicit `lstrip("\n")`, and `EMPTY_LEAF`'s static-initialisation order is reproduced so the sentinel's children are `None` while every later node points at it. GUI and benchmark entry points sit behind `if __name__ == "__main__":`, so an import never opens a window or starts a ten-second benchmark. The Windows suite is 2042 passed, 0 failed, 0 skipped and 0 warnings with `-W error`; the file-shape and structure guards pass after staging, and the pure-logic translations were checked against known console output, the sample `S E A R C H E X A M P L E` symbol table, 200-element AVL set operations, and `sorted()` for all four sorts at sizes 0 to 1000. | The verification gap was in the guard, not the code: `test_no_governed_file_has_a_hash_run_longer_than_two_lines` reads `git ls-files`, so twelve finished files sat invisible to it until `git add` ran. Staging belongs to verification, not only to commit preparation. The translation also showed where "line by line" needs a judgement call: Java text blocks do not include the newline after the opening delimiter while Python triple-quoted strings do, so a literal transcription would have added one blank line per frame; and Java's `Point == Point` is identity, so `is` is the faithful test rather than a value comparison. Both are differences that compile, run and are still wrong, which is why the checks compared output rather than trusting the shape. |
| 20 Oct 2026 | Repository retained as the single Data Science project; OpenCode free-tier investigation logged | A.I.M confirmed the repository stays the main Data Science project rather than splitting into a separate directory or branch: university coursework, personal public learning and applied projects share one governed record (AGENTS.md rules, PROGRESSION/NOTES logs, pytest guards) instead of a second repo. The OpenCode free-tier error raised in the VS Code WSL terminal was investigated end to end: WSL runs a current official release (v2.0.32), the service restarts cleanly and its API responds, and the WSL server log contains no FreeTierError at all - the chronic failures are capacity and upstream ones (rate limits, 300 s header timeouts, dead vendor endpoints, one WSL network day). The bare "free tier can only be used from within OpenCode" message is the gateway's server-side gate for free models and historically appeared in two waves that hit official clients on every platform (17-18 Sep, 3 Oct 2026); a hygiene trip in `python/sandbox/aim.py` (two trailing-whitespace lines) was cleared, restoring the suite to 2042 passed on Windows. | Keeping one repository is a governance choice, not just a convenience: the guards (doc numbers, coverage, tree, progression chronology, hygiene) only stay coherent when there is one tree to measure, and a second repo would duplicate the venvs, the CI and the session log for no gain. The investigation's real lesson is that a message on the screen is not the same as a line in the log - the WSL install was innocent and the genuine recurring cost is free-route capacity, so the right response is rotation (per the model discipline in `agentic_models/AGENTS.md`) rather than reinstalling. The aim.py trip is the same pattern as the rest of the repo: a guard that scans the disk catches an untracked file the suite never imports, which is exactly the point of keeping it outside version control. |
| 17 Oct 2026 | Folder renames followed through: README tree repointed, eleven test paths, and the generator the suite never checked | A.I.M renamed two folders to lead with action words - `progress/` to `git_repo_progress/` (`3bc5bc2`) and `file_scores_ranking/` to `rank_file_scores/` (`22492c0`) - both as clean R100 renames, then asked for the README architecture tree to follow and for the resulting failures to be fixed. The tree now carries `git_repo_progress/` between `data/` and `htmlcov/` and `rank_file_scores/` between `python/` and `requirements/`, each with its two documents listed, and `NOTES.md` closed the root as the final entry. Eleven path literals across five guard files were repointed, and the README tree guard's registry moved with them: both filenames left `allowed_files` and the two new folder names joined `allowed_parents`, so a further document in either needs no guard edit. Live prose in `AGENTS.md` rule 13 and its References section and in `MODEL_ALLOWANCE.md`'s long-document table was repointed; the dated historical log rows in `NOTES.md` and `PROGRESSION.md` still name the old folders, because rule 13's append-only half is about the record, not about tidiness. The find worth recording is the one the suite could not see. `scripts/score_ranking.py` writes `FILE_SCORES.md`, and its `OUT` constant still named `file_scores_ranking/` - so every ranking guard passed, because the sheet itself had already moved, while running the generator would have created a fresh `file_scores_ranking/` beside it and left the tracked sheet stale. Nothing tested it: `test_ranking_docs.py` reads the artefact and never the tool that produces it. The path is fixed and two cases now pin it, parsing `OUT` with `ast` rather than importing the module, so the check has no side effects and does not need the signals JSON to exist. Both were mutation-tested: pointing `OUT` back at the old folder name fails two, and pointing it at the right folder with the wrong filename fails one. Suite 1980 to 1982. | A guard that only reads an artefact cannot see the tool that writes it, and that gap survived a rename that every other check absorbed cleanly - 70 of the failures were path literals in tests, which fail loudly, and the one that mattered was silent. The general lesson is about which failures are cheap: a `FileNotFoundError` in a test is the cheapest possible report of a mistake, so it is easy to assume the suite is covering the change because it went red. The generator's broken path produced no red at all, and the fix that mattered came from asking what else names the old folder rather than from reading the failures. The second lesson is that `ast` beats a regex for this, and only after the first attempt was wrong: the chain `REPO_ROOT / "a" / "b"` parses as `(REPO_ROOT / "a") / "b`, so a one-level loop stops at the inner `BinOp` and quietly returns `REPO_ROOT` itself - a resolver that appears to work and silently returns the wrong path. Recursing over the tree fixed it, and the mutation test is what proved the fix rather than the green run, since the first version also went green on the correct input and would have caught nothing. The third is that the append-only rule has a real cost the log rows now show: three dated entries name folders that no longer exist, which is correct as history and will read as an error to anyone who greps for a path without reading the date first. |
| 17 Oct 2026 | Beam Free added to the rotation, and the catalog checked against the registry rather than remembered | A.I.M asked for Beam Free to be added and for the rotation to be kept current as models appear and disappear, citing Exo Free as the lesson. Beam Free was read from the models.dev registry entry (`beam-free`, 1,048,576 context, 131,072 output, zero cost) and added as the twelfth rotated model across the pick-a-model table, the assets/weaknesses table, the hand-off table, the usage share table and `MODEL_ALLOWANCE.md`. Its usage row reads `not yet used` rather than a fabricated share, and its weaknesses are stated as unknowns, because nothing about it has been observed. Two registry findings went in alongside it. **Exo Free is still live** - `exo-free` is present with the same 1,048,576 / 131,072 limits - so the 11 October removal was a decision about this project's rotation, not a discontinuation upstream, and the two should not be conflated. And the registry now lists **44 zero-cost models** against the twelve rotated here, so "the free models" was never a closed set: the rotation is a deliberately short shortlist, and the discipline that keeps it honest is a recorded retrieval date rather than an assumption that memory still holds. | The useful discipline is the difference between a list and a habit. Exo Free was dropped when it stopped being useful here, which was correct, but nothing recorded *why* - discontinued or just unwanted - so the next reader has to rediscover it, and `HISTORY_REVIEW.md` had to be the place that recovered it. Recording the registry URL, the retrieval date and the catalogue size next to the table turns a memory into a claim that can be checked, and the same treatment is now applied to the five models `TASK_MODEL_GUIDE.md` §6 already flagged as missing from the Zen list. What is deliberately not done is a test that fetches the registry: a suite that reaches the network becomes a suite that fails for reasons unrelated to the repository, and the guard that this repository already learned to prefer - pin the stated figure to the recorded one, and refresh both together - gives the same protection offline. |
| 17 Oct 2026 | Two virtual environments named per platform, and the suite made genuinely cross-platform | A.I.M observed that the WSL environment had been overlooked and asked for the Windows one to be renamed `.venv-win` for consistency. Both turned out to exist: `.venv` was Windows (3.14.5) and `..venv-wsl` was already WSL (3.12.3), fully installed and able to run pytest, coverage and pygame. They were renamed to `.venv-win/` and `.venv-wsl/`, and all 81 tracked references across 31 files were repointed, including twelve notebooks and the VS Code interpreter setting. The move alone was not enough: the Linux console scripts carry absolute shebangs (`#!/…/..venv-wsl/bin/python`), so 53 of them and the four activate scripts plus both `pyvenv.cfg` files were rewritten; both interpreters were then verified to still resolve, which is the check that says a .venv-wsl move succeeded rather than the one that says it did not. Making the Linux run real exposed four defects that Windows had been hiding: `test_tui_players.py` asserted list order from `os.listdir`, which NTFS returns alphabetically and ext4 does not; `test_data_files.py` and `test_repo_doc_numbers.py` filtered `rglob` results after walking, so they crawled both environments and the full suite stopped completing on the /mnt/c mount at all; `_is_full_run` only looked under `tests/` and so failed both suite-count guards on any platform that skipped the coursework package; and the coursework conftest needed `collect_ignore_glob` rather than `importorskip`, which pytest 9 treats as a collection error. Windows is 2042 passed; Linux is 2042 passed with 0 skipped, and the skips are named rather than hidden. Suite unchanged at 2042 on Windows. | The honest headline is that a suite which had only ever run on one operating system was not cross-platform, it was Windows-only with extra steps. Three of the four defects were in the tests rather than the code, and all three were the same mistake: asserting something the underlying system never promised - a directory listing's order, a walk that had already happened, a collection total that assumed nothing was skipped. The fourth was environmental and is now recorded instead of patched, because `file_reader.py` and `generator.py` both hardcode `C:\Users\A.I.M\...` and `FILE_SCORES.md` already scores that as a real Durability weakness, so rewriting the scripts would quietly change a lesson the owner still owns. The lesson worth keeping is the performance one: a post-filter is not a prune. The hygiene guards were correct in what they kept and still crawled tens of thousands of site-packages modules, and moving that filter from after the walk to during it cut the Windows suite from 150 seconds to 47. |
| 17 Oct 2026 | Test-equity instrument added: live proportional coverage of cases and guards | A.I.M asked for the pytest cases and guards themselves to be distributed proportionally across the portfolio rather than pinned in one file: each module's test density should be ratio-equivalent to a composite of its methods, attributes, command types and input/output points, with the full input/output range exercised. `scripts/test_equity.py` measures that live from the AST and the test files (attributing cases by resolved FILE/FOLDER constants and path literals, with conftest constants loaded up the tree), and `tests/test_scripts/test_test_equity.py` guards it: 160 modules measured, 159 with tests, only the deliberate `main.py` stub left untested, full-range failures 1, density CV 2.69 ratcheted at 2.7, min/max ratio 447.99 ratcheted at 450, 79 unattributed cases ratcheted at 130. Suite 1982 to 2042. | The attribution problem turned out to be the real work. A first pass counted 99 unattributed cases because it scanned each test function's own text for path literals, but the portfolio's tests name their source through class-level `FILE = f"{FOLDER}/x.py"` constants and through imported conftest constants such as `MP3_TUI`, so a function body contains neither a path nor a stem. Resolving those constants up the directory tree and attributing by them fixed most of it; the remainder are meta-tests that genuinely do not belong to one module. The second lesson is about false positives: once attribution worked, stem-token scanning in a method body still hijacked classes whose `FILE` was known, because words like `divide` and `square` are also module names. The fix was to prefer a resolved `FILE` over any stem match, never the reverse. The third is that `full_range_ok` had to stop comparing category names as substrings, since no test contains the literal string `io_in`; it now checks that inputs are exercised and at least one guard exists. |
| 17 Oct 2026 | Contributor retrospective written; `HISTORY_REVIEW.md` added and guarded | A.I.M asked for a review of the whole directory's progress and the mistakes made by each contributor across his three profiles — his own A.I.M account on GitHub and GitLab, `ThenameisAiman`, and the university account `om001219` used in the first weeks — structured on a What Went Well / What Went Wrong plus Evidence-Based Improvements framework, with lessons pitched at the kind of programmer he is and the gaps named. `HISTORY_REVIEW.md` was added at the root beside `NOTES.md` and `PROGRESSION.md`, and `tests/test_scripts/test_history_review.py` guards it. The whole 836-commit record was read: five git identities resolving to one developer, one university account he committed through, one tool that committed under his GitHub identity, and one co-author trailer shortlog does not attribute at all. The university account's use is the most useful finding, because the developer diagnosed it himself at the time in commit `687fe8a` — commits made through the student account were invisible on GitHub because they carried his personal email rather than the student one, and six README-only commits kept the contribution record unbroken across the five-day streak. `ThenameisAiman` turned out to be GitHub Copilot: three commits on 1 July whose messages carry bullet bodies and a forward rationale naming the module each block prepares for (CS2PP weeks 4-5, CS2DA week 6, CS2SE weeks 10-12). Those 172 lines were the repository's first substantive test coverage, and none of the three files survives under its original name — all were renamed inside a fortnight and superseded by the July restructure, so the project's first testing work left no trace in the shape it arrived in. What Went Wrong is anchored on the record rather than on impression: 123 scope-less commits in June against 2 in October, with rule 12 landing on 29 September; 98 forbidden `file:` prefixes; the `Python/` to `python/` case rename done as a two-hop through `python_tmp` to defeat `core.ignorecase`, which was correct and produced an 886-line README diff inside a path commit; and ten mass mechanical commits touching 82 to 261 files each, of which three landed within twelve days of each other. The `university_courseworks/` question is answered by analysis rather than action, as A.I.M chose: 285 of 565 tracked files is 50.4% of the repository, it is assessed submitted work that `AGENTS.md` itself flags as a different risk profile, and its provenance is recorded in the history — downloaded from the module site in `0bd93ca` and placed from another repository in `c99610b` — with no recorded decision to publish it. The recommendation is to leave it for the rest of Semester 2, redact the four tracked files carrying the university identifier, and move it to its own repository when CS1OP finishes, because the thing being protected expires in May while the cost of the split does not. Suite 1970 to 1980. | A retrospective is the easiest document in a repository to let rot, because nothing reads it and it still looks finished, so it needed a guard — and writing that guard produced the sharpest lesson of the session. The first version asserted the figure the document stated against `git rev-list --count HEAD`, which failed on the very next commit: the one that added the document. A guard that fails on being correct is a guard that gets deleted, so the total is now checked for internal consistency instead — the five per-identity figures must sum to the stated figure. That catches the mistake actually worth catching, a mistyped number in a table, and it survives every commit after this one. The second lesson is about attribution, and it is the reason the review names the handles instead of anonymising them: a repository that appears to have three contributors and has one has a measurement problem, not just a tidiness problem. Five identities is what `shortlog` reports; one person is what happened. Two names on one email and one name on two emails means every question of who wrote what has to be answered from the email column, which is why §6 of the review puts a `.mailmap` first in the remediation order — it fixes the history, and a branch or a repository split does not. The third is that an escalation curve is worth more than any single tool choice: incidental use for an assessed haiku on 22 June, AI-assisted engineering by 10 September, written governance in `AGENTS.md` on 15 September, and delegated execution from 17 September, with the commit volume afterwards showing the difference between a person typing and an agent executing against a specification. The last is the one the review is honest about rather than congratulatory: the repository has become partly self-referential, with 290 of its tests now asserting things about the repository rather than about any script, and the tripwire for that is written down at 14.7%. |
| 17 Oct 2026 | CS1OP sound levels equalised and cross-language parity cases added | A.I.M asked for two things, and was explicit that the second outranks the first: the CS1OP sound effects were to be brought up to a level the user can hear, and, only if everything else succeeded, the coursework was to carry test cases showing how a free agentic AI service was used - Python as the emphasis, with JSON available for the Java side to be compared. The optional item was done second, as asked, and it is where the session's real lesson sits. The sound folder holds 34 clips and they are not the same format: 8-bit, 16-bit and 24-bit PCM, mono and stereo, at 11025, 44100 and 48000 Hz. The first attempt unpacked every clip as 16-bit shorts, which shifts every sample after the first in an 8- or 24-bit frame, so the clips were silently turned into noise and every RMS figure was meaningless; the files were restored from git and the work redone with a decode and encode per width, in `scripts/normalize_sound_volumes.py` rather than the inline command it replaced. The second attempt then picked the wrong ruler: plain RMS ranks `Main Menu GUI.wav` last at -33.50 dBFS, but that clip is 88% silence around a short burst and peaks at -3.50 dBFS, so it was never quiet, and ranking it so demanded +25.8 dB that only a hard limiter could deliver. Measured on RMS gated to 50 dB below each clip's own peak, it sits at -24.88 dBFS and needs +14.04 dB. Levels are now mapped by range compression onto a floor of 20% of the loudest, the floor A.I.M asked for with 15% named as too quiet: the spread went from 6.0% to 20.0%, nothing landed below target, and peaks rest at the -1 dBFS ceiling without reaching full scale. `python/` and `java/` hold byte-identical copies of all 34 clips and are rewritten together, so a fork cannot appear on the platform nobody tests. `sound_volumes.json` records every clip's format, level and gain before and after, and 17 new tests re-measure the clips from disk rather than trusting it. The parity work put thirteen cases in `ai_parity_cases.json` beside the coursework rather than inside the Python test file, so a Java suite can read the same list: each case names one behaviour, one shared expectation, the Java class and method that produce it, and the steps in plain language so neither side gets a case phrased in the other's terms. `test_ai_parity.py` runs all thirteen against the Python modules - that is the emphasis - and checks the Java half statically, that the named class exists and the method is public in it. A.I.M's instruction that the Java work was not needed was honoured: three JUnit files and a `GameTest` edit written earlier in the session were removed, and the Java suite runs at its committed 26 tests, which pass against the re-levelled audio. Full suite 1887 to 1970. The workflow is recorded as a worked example in `TASK_MODEL_GUIDE.md`. | Reading a folder's actual formats before writing the tool that rewrites it is not a formality: nothing in the Java or Python source would ever have reported that the clips were mixed-depth, and the failure mode was silent - the files still parsed as valid WAV, so only a byte comparison against git showed the damage. The metric mattered more than the algorithm. Two range-compression implementations agreed on the maths and disagreed completely on the answer, because plain RMS spends its votes on silence; a thirty-second inspection of one clip's waveform - how much of it was above -50 dBFS - is what showed the ranking was ranking silence rather than loudness. And a limiter absorbs the boost you ask for, so a gain computed up front lands short: the first pass aimed at a 20% floor and delivered 13.7%, and the gain now has to be bisected until the measured level reaches the target, re-limiting the original samples each time so nothing compounds. On the parity side, the useful move was refusing to keep the expectations inside the Python test file. Written there they would have been Python's opinion of the Java original, checked by Python, and true by construction; in a JSON file both languages read, the expectation is a claim about the Java that Python is obliged to match, and the Java side can be checked for truth even though no Java was written - the named class exists, the named method is public, and the doors case is driven by a pinned generator so "the factory can make four kinds of door" is a certainty rather than a seed. The `text_ui` case is the one that earned its keep by being wrong first: it was drafted as "the box has a fixed width", and reading `TextUI.box` showed both languages use `max + 4`, so the parity claim was fixed to the formula that is actually shared. And the doors case started life drawing fifty random doors, which is a test that passes or fails on the seed - pinning the generator is what made it deterministic. |
| 14 Oct 2026 | Java coursework updated to match the translation: CRT reachable, dead rows removed, overlay applied | A.I.M moved the CRT work onto the Java side of the coursework, in `university_courseworks/year1/semester2/cs1op/coursework/java/`, having first clarified that the target was the folder inside Data-Science-Project rather than the public `om001219/cs1op-textgame` repository. The Java original carried the same three defects the Python translation had: `GameController.showCRTScreen()` built a `CRTScreen` that does not exist in the Java sources, so the tree did not compile as committed; `OptionsScreen` held `soundEnabled` and `volume` fields that were written by the UI and read by nothing, because the real sound state lives in `SoundSettings`; and `CRTSettings.drawCRT()` was called by neither `GamePlayScreen`, `DoorSelectionScreen` nor `DialogueScreen`, so the overlay appeared in the minigames and nowhere else. All three were repaired: a new `src/CRTScreen.java` provides the missing screen (on/off toggle, 0-100 intensity slider and the band legend), `OptionsScreen` now carries DIFFICULTY / DISPLAY / SOUND / BACK with DISPLAY navigating to the CRT page and echoing the live state, and the three screens each call `CRTSettings.drawCRT()` as their last draw call, matching the Python translation. | The Java original was not merely a behind-the-times copy of the translation - it held the same bugs, which is a useful check on the whole exercise: the defects were in the coursework as first written, not introduced by the translation, so fixing both trees was the correct target rather than reconciling the Python back to a broken Java. The second point is that the divergence is now symmetric. The Python `draw_crt_overlay` draws scanlines only, because the tkinter canvas has no per-pixel alpha, while the Java `drawCRT` draws scanlines, vignette, flicker and a phosphor tint; the translation keeps the same thresholds and the same 0-100 intensity, and documents the difference rather than pretending the two renders are identical. Running the Java suite was the real confirmation: 26 JUnit tests pass against the same file set, and the Python CRT guard tests pass alongside them, so the behaviour is verified in both languages rather than assumed from reading. |
| 14 Oct 2026 | CRT settings made reachable before the game and applied across the game loop | A.I.M moved onto the CS1OP coursework and asked for the CRT settings to be editable before starting a game, applied across the minigames and the door selections, with any collisions, misuses and confusion cleaned up. Three defects were found and repaired. First, the CRT settings were not reachable at all before a game: `GameController.show_crt_screen()` builds a `CrtScreen` that nothing called, so the translation's own full-screen CRT page - the one added because the Java builds a `CRTScreen` that does not exist - was unreachable dead code. The OPTIONS screen now carries a DISPLAY row that navigates to it, and the row text echoes the live overlay state so the setting can be checked without opening it. Second, the OPTIONS screen carried two rows that lied: SOUND toggled `OptionsState.sound_enabled` and VOLUME adjusted `OptionsState.volume`, and neither attribute was read by anything - the real sound state lives in `sound_settings` - so the screen reported settings the game never consulted. Both rows are gone, replaced by DISPLAY and a SOUND row that navigates to the same per-sound page the main menu opens, so one name now means one destination instead of two. Third, the CRT overlay was drawn only by the two minigame views; the door selection screen played between every minigame ignored it entirely, and the dialogue and gameplay panels did too. All three now draw it, and the pre-game menus deliberately do not, so the setting is legible while it is being edited. The coursework suite now collects 178 cases and the repo suite 1887. | The most useful lesson is that the dead code was not dead weight but an unfinished feature: the translation had already written the screen the Java intended, and the only thing missing was the one call that reached it, so the repair was wiring rather than building. The second is that a settings row that reports a value nothing reads is worse than a missing row - it looks like coverage. A guard now asserts the options state carries no private sound or volume attribute, and another asserts every screen in the game loop draws the overlay, so both defects fail rather than drift. Both were mutation-tested by reinstating the old row and by deleting the door overlay. A mechanical error worth recording: an edit intended for one spot in `door_selection_screen.py` swallowed a newline and joined the closing docstring quotes to the `return`, which no test would have caught until import. Parse-checking the four edited files before running the suite caught it in the same step. |
| 14 Oct 2026 | Coursework suites wired into the main suite; GUI:TUI case ratio pinned at 1.25 | A.I.M asked for the coursework pytest cases to be consistent with the advanced projects, for the GUI suite to carry about a quarter more cases than the terminal suite, and for the Java-to-Python translations to be tested across every module regardless of year. The first finding was that the CS1OP translation's own suite of 174 cases had never been in the main suite at all: `testpaths` named `tests` alone, so the coursework suite only ran from inside its own folder and a bare `pytest` reported 1691 green tests while an entire assessed module went unseen. That path is now declared in `pyproject.toml`, taking the suite to 1865. A new `TestCourseworkSuitesAreCollected` guard asserts every `university_courseworks/**/python/tests` directory is declared, and that no weekly lecture or practical folder is - the two halves of the contract, since the weeks are practice material rather than assessed code. The GUI suite sat at 31 cases against the terminal suite's 34, the thinner suite owning the larger surface; twelve cases were added (six per player) pinning exact delegation arguments, the listbox-driven track choice and the status-label refreshes, bringing it to 43 against 34, and `test_suite_shape.py` now guards the ratio with a floor of 1.15 and a target of 1.25 so the drift is caught rather than noticed. The suite is 1883. | A suite that only runs from its own directory is invisible to every other guard: coverage, the doc-number guards and the reviewer all read the same `pytest` invocation, so a module outside `testpaths` is a module nothing checks. That is the same failure the doc-number guards exist for, one level down, and it is worth naming that the numbers looked healthy throughout - the figure of 1691 was true, and also wrong. The second lesson is that a test-count ratio is a real contract, not vanity: the GUI wrapper had become the thinner suite while owning more surface, which is exactly the direction it drifts because adding a GUI case costs more thought than adding a terminal one. The guard was mutation-tested by deleting six GUI cases, and it failed as intended. Both guards also caught two violations of the house file convention in the files written to hold them - a missing trailing newline and a stray CRLF - which is a reminder that the byte invariants bite the agent's own output first. |
| 14 Oct 2026 | Task-to-model guide added; rule 14 makes the context-first check binding | A.I.M asked which model suits each task, confirmed against third-party and in-party sources, and asked that the fit be checked before every task rather than assumed. `agentic_models/TASK_MODEL_GUIDE.md` was added with an eleven-row task-to-model matrix (factual Q&A, code review, long-document reading, test writing, root-cause debugging, multi-file refactors, single-file edits, boilerplate, agentic tool use, long-context retrieval and private work), each row carrying a primary model, a fallback, an effort level, an in-party citation, a third-party citation, pros, cons and an authentic user note. Effort levels were read from the live catalog rather than the model card: `opencode models opencode --verbose` declares Space Bunny `low, medium, high, xhigh, max`; Muse Spark 1.3 `minimal, low, medium, high, xhigh`; LongCat 2.5 Preview `low, medium, high`; and Big Pickle, both Nemotrons and MiMo-V2.6 expose no selectable variant at all. Rule 14 was added to `AGENTS.md`, and the rule, the pre-flight section and `MODEL_ALLOWANCE.md` were all updated to state that the check holds in both Plan and Build mode. | Three findings moved the guide beyond the tables it was built from. First, "levels" means the model's own `/variants` effort list, and it is not uniform: only four of the eleven free models expose one, so "pick a level" is advice that applies to a subset. Second, the live Zen catalog no longer lists five of the eleven rotated models - `nemotron-3-ultra-free`, `fledge-alpha-free`, `ling-3.0-flash-fin-free`, `ling-3.1-flash-free` and `mimo-v2.5-free` - so the rotation docs have drifted from what the console serves, which is the same failure mode the doc-number guards exist to catch. Third, the external evidence reorders the internal tables: Big Pickle is the rotation's *knowledge* model despite the smallest window, and Nemotron 3 Ultra's 128K output ceiling disqualifies it for long patch-writing even on a 1M window. A rule that binds only the agent that writes it is a preference; the rule had to be restated in all four places before it was binding. |
| 14 Oct 2026 | CS1IP weeks suite corrected; count repaired to 1691 | The suite added on 13 Oct was reworked. Its `KNOWN_EXECUTION_FAILURES` now asserts the two genuine material defects - `task10.py`'s `%d` format given a string, and `week2/lecture/python/input.py`'s module-level `input()` (run with an empty stdin so the failure is `EOFError` rather than capture-mode `OSError`) - instead of catching every exception as an xfail. Six phantom `week1/lecture/python/*` entries and a duplicate week8 `map_generator` were removed, leaving exactly the 34 files on disk (18 lecture + 16 practical); the docstring structure and trailing newlines were brought to the house rules. The README architecture tree was reordered so folders stay alphabetical first and `NOTES.md`/`PROGRESSION.md` sit at the end, and the suite figure was corrected to 1691 in `AGENTS.md`, this document and `FILE_RANKING_GUIDE.md`. | A catch-all `except: xfail` is a guard that cannot fail, and it hid six paths that did not exist: the parametrise list looked like 41 tests while the tree held 34 files. Asserting a known failure, and failing when it stops failing, is what keeps the exception list honest. And a count stated in three documents is three chances to go stale - the guard catches every copy only because each is checked against the same live session. Landed as PR #22 on branch `fix/readme-tree-cs1ip-suite`, pushed to all four mirrors; clean fast-forward, no conflicts. |
| 13 Oct 2026 | README cs1op tree expanded to match disk | The `cs1op/` entry in the README architecture tree was expanded from a one-line stub to the full structure: `coursework/` (java/ 30 classes + gradle + JUnit, python/ 31 files + pytest, pdf/) and `week1/ ... week11/` with lecture/ and practical/ splits. The convention note now groups cs1op with cs1ip and cs2da as java-primary modules. | A stub entry in an architecture tree is a promise the tree does not keep - a reader who navigates to cs1op/ finds eleven week folders and a coursework/ the README never mentioned. The fix is the same as the requirements collapse: the tree must either show the structure or say it is omitted, not imply simplicity that is not there. |
| 13 Oct 2026 | README requirements tree collapsed to folder-level | The `requirements/` entry in the README architecture tree listed all five files individually; collapsed to a single folder-level comment matching `roadmap/` and `scripts/`. The `allowed_parents` exception for `requirements/` was removed from the README architecture guard and its docstring updated. File-level detail preserved in `DEPENDENCIES.md`. | A tree that lists some folders' files and not others needs a reason for each exception. The requirements file-level listing was that reason — once it was gone, the exception became dead weight in the guard. |
| 13 Oct 2026 | Music player tests restructured; CS1OP translation verified | The monolithic `tests/test_advanced_projects/test_music_player.py` (852 lines, 68 tests) was split into `tests/test_advanced_projects/music_player/` with its own `conftest.py`, `test_tui_players.py` and `test_gui_players.py`, matching the CS1OP coursework's self-contained package pattern. Net test count unchanged (68 to 68). CS1OP coursework verified: 174 pytest tests pass, 30 Java source files map to 31 Python files. | The cs1op pattern - own conftest, per-module test files, isolated fixtures - is portable to any project in the repo, not just coursework. A net-zero test count change keeps every count guard quiet: the suite total, the paradigm counts and the coverage denominators all stay valid without touching a single claim.
| 13 Oct 2026 | CS1IP weeks test suite added; test count 1657 → 1686 | New `tests/test_university_courseworks/test_cs1ip_weeks.py` covering 34 week Python files (24 lecture + 16 practical) via `load_module` import pattern. 33 passed, 8 xfailed (import bugs in educational material). Suite total 1657 to 1686. | The week-folder suite finally exercises the 34 previously-untested cs1ip Python files (week1–12 lecture + practical tasks). Xfail modules have runtime bugs (% formatting) being fixed in the course material. The import-check guard is lightweight and keeps the suite green while material stabilises. |
| 12 Oct 2026 | Dependencies brought current, two stale documents repaired, the logs backfilled | `pip list --outdated` showed fourteen packages; all upgraded to latest with `pip check` clean (executing 2.3.0, iniconfig 2.3.1, json5 0.17.3, jsonpointer 3.2.1, narwhals 2.27.1, nest-asyncio2 1.7.4, notebook 7.6.3, numpy 2.5.4, pip-tools 7.6.2, platformdirs 4.13.0, pycparser 3.11, rpds-py 2026.9.1, soupsieve 3.0.1, wcwidth 0.9.2). Four stale `~`-prefixed site-packages directories left by interrupted uninstalls were deleted after verifying the real packages were present - pip's invalid-distribution warning named only one of the four. `requirements_sync.py` fixed to write LF on every platform (`newline=""`), after it had emitted CRLF into both compiled files on Windows; re-synced, audit CLEAN. The `aim.py` sandbox guard repaired: the owner's new interactive prompts made the first `input()` die on mocked stdin, so the test now feeds answers and treats exhaustion as end-of-run. CS2PP week 3 lecture notebook committed (`ae38c48`, `610f138`, `e386de6`, `d79082e`). `DEPENDENCIES.md` had drifted in eleven catalogue cells and three command paths - the sync and install invocations still pointed at the repo root from before the folder move, and the VS Code task carried the same broken command - so the catalogue was corrected and a six-case guard now pins its tables to the compiled requirements files. Finally, a git-history sweep found the maintenance log and this session log had never recorded a string of pass-through days: rows for 21, 22, 27, 28, 29 Sep and 1-6 Oct went into NOTES.md's log, and rows for 3, 5, 9, 11 Oct plus this one went in here. | A warning names the symptom, not the set: pip reported one invalid distribution while four stale directories sat on disk, so the fix had to start from the filesystem rather than from the message. The CRLF and the catalogue drift were the same defect in two documents - a fact maintained by hand beside a machine-readable source, with nothing comparing them - which is why the repair here is the guard, not just the cells. The sandbox guard failed exactly as its own docstring had predicted: a scratch file is supposed to grow, so running out of mocked answers has to be the end of the run rather than a failure of the file. And the backfill is the quiet lesson - the days a log misses are the ones where nothing broke, so only a deliberate sweep of the git dates finds them. |
| 11 Oct 2026 | Exo Free removed; the two evaluations recorded | OpenCode deprecated Exo Free, so it was removed from every live document: the model list, route ceilings, tokens-and-share, pros/cons, hand-off, privacy and stability tables in `agentic_models/AGENTS.md`; the route ceilings, usage and largest-context tables in `agentic_models/MODEL_ALLOWANCE.md`; the roster, research table and privacy paragraph in `PROGRESSION.md`; and the `MODELS` list plus count assertions in `test_model_rotation_docs.py`. Twelve to eleven everywhere written, historical session rows untouched per rule 13. The pytest-access evaluation was placed in `NOTES.md` and the agentic-usage evaluation in `MODEL_ALLOWANCE.md` - Big Pickle served 403.6K tokens against a 200K published window (202% of its ceiling, 4,100 messages), Space Bunny is the other default-trap, Ling drew 83 messages in the same period; the `[AI-authored fix]` inventory counts 46 markers across 17 files, led by 12 in the doc-numbers guard itself. The CS1OP loose ends closed: the owner had already committed the resources (`627663a`, 34 WAVs byte-verified), and `.gitattributes` now names `*.wav binary` in place of the `text=auto` NUL-sniffing heuristic (`6792d94`, `e492549`, `fa87377`). | Deprecation is a counting problem before it is an editing problem: "twelve" lived in prose, tables and guard assertions at once, and only the guard could prove eleven had replaced it everywhere - the historical rows staying at twelve is the append-only rule doing its job, not drift. The marker inventory answers a question the suite cannot ask - how much of the AI-authored history is repair versus bookkeeping - and the honest answer is that the largest single cluster is mechanical doc reconciliation, which is neither repair nor decoration but maintenance. And `*.wav binary` is the same move as pinning a version instead of trusting a resolver: a heuristic that happens to work, replaced by a stated fact. |
| 9 Oct 2026 | `agentic_models/` formed around the allowance file | `MODEL_ALLOWANCE.md` created as the file the pre-flight reads before any model switch - applicability, token fit and remaining allowance, the first two answerable locally and the third only from A.I.M's console, so an empty cell is a failed check rather than a silent pass. It moved to `model_rotation/` the same day, and on 10 October A.I.M directed `AGENTS.md` in beside it, the folder renamed `agentic_models/`, with the README tree, the tree guard's `allowed_parents` and the pytest paths repointed; the pre-flight guard caught its own stale path inside the moved `AGENTS.md` before any human did. The all-model observed-context snapshot came from a read-only pass over the session database (31 project sessions): Big Pickle 4,100 messages and Space Bunny `max` 2,499 lead the traffic; the largest-context table shows LongCat 546.5K, Fledge 520.0K and Space Bunny 504.3K all comfortable, but Big Pickle served 403.6K against a 200,000 published ceiling and Nemotron 3.5 Lightning 357.2K against 262,144, so the ceilings table is now labelled the documented limit and the pre-flight answers against it conservatively. The rate-limit history was corrected from six to eleven entries across the logs - five 26 Sep lines had been missed (`d508dda`, `ef87752`, `910d7bc`, `d0f3720`, `56cbd47`, `0707a59`, `8b874f4`). | The measured-versus-published gap is the finding that matters: three routes serve beyond their documented windows, so a ceiling table is a claim about the provider, not a fact about the session, and the honest label is "documented limit". A folder move is an API change for everything that resolves a path by name, and this one was repointed while the guard for it still read the old address - a guard failing on its own document in the same session it moved is the move working as designed. And the allowance split is what keeps the pre-flight honest: the two questions this machine can answer are separated from the one only the console can, so silence on the third is recorded as absence rather than assumed as fine. |
| 5 Oct 2026 | CS2DA mergesort committed; the 4 Oct session's guard work landed | CS2DA week 2 committed: mergesort plus the selection-sort comparison, with only task 1 of the Complex Hall divide-and-conquer briefing complete because the remaining methods resisted the pseudocode and the incomplete state is recorded rather than padded. CS2PP week 2 lecture notebook added with the Python fundamentals. The coursework-tree reorganisation's layout contract was realigned for the notebook split (`826f5ae`, `3372993`, `d071c5b`, `c55fb47`). The guard work narrated in the 4 Oct rows - the maintenance-log reorder and its new `TestNotesMaintenanceLogOrder`, the skip registry, the pinned coverage figures, the retired "16-week" label - carries these dates because the session ran past midnight (`3dbc52e`, `7e08ea5`, `778553e`, `6e0f6b2`, `e01e9f4`, `2f3639e`). | The maintenance log had drifted in exactly the ways its new guard now prevents - out of order, and with a row stranded below a blank line reading as a footnote - and it was the only dated log in the repo with nothing checking it, which is the pattern this repo has now seen twice: the unguarded copy is the one that goes stale. A floor rather than an exact row count is what lets an append-only log stay append-only. And the mergesort task is the honest kind of incomplete - committed as far as it actually worked, with the reason on the record - which is worth more in a learning portfolio than a finished-looking file nobody can defend. |
| 3 Oct 2026 | CS1IP semester 1 content placed and translated | CS1IP's semester 1 material was placed into the reorganised tree: weeks 1 to 5 of Java lecture and practical content, week 1's practical solutions and tasks in their expected languages, and tasks 1-14 translated from Java to Python; `task3.java` given a one-space string correction. None of this had a session-log row until the 12 October git-history sweep found it missing (`f00bb21`, `19fe49f`, `3046928`, `dcb26fc`). | The translation habit predates CS1OP by a week and looks the same from here: the marked Java stays byte-frozen and the Python stands beside it rather than replacing it, which is the rule CS1OP would later have to write down. And the quieter lesson is about the log itself - content-only sessions are the ones a memory-kept record misses, because nothing breaks and no guard fires; a sweep of the git dates is what surfaced this one, not a test failure. |
| 10 Oct 2026 | CS1OP coursework translated Java to Python, playable | Translated all 30 Java sources (5,359 lines) into `coursework/python/src/` (26 modules): domain, TextUI, tkinter screens, both minigames with headless logic cores, and a pluggable sound backend (silent default, pygame optional). `Sound Effects` renamed `sound_effects` on both trees with every reference repointed; resolution is case-exact even on Windows. 174 pytest cases green, all headless; the new files pass the repo's own file guards. Three Java divergences, all documented in `coursework/python/README.md`: the missing `CRTScreen` class the Java references (implemented, not reproduced), the `lifes` typo, and the folder rename. | A translation that cannot be tested headlessly is a second codebase to maintain by hand: separating state from canvas made 174 pins possible with no display and no audio device. The Java tree as committed does not compile (`CRTScreen` has no class); the Python fixes the wiring and says so, leaving the marked Java untouched. |
| 8 Oct 2026 | CS2PP Week 2 practical completed in the notebook | Completed the CS2PP Week 2 practical (Basic Python Constructs) in `university_courseworks/year2/semester1/cs2pp/week2/practical/jupyter/week2.ipynb`, which began as A.I.M's ten hand-written cells and was extended with the briefing's tasks from page 3 onwards, mirroring the shapes the lecture notebook teaches - match/case dictionary patterns, the walrus operator, sets, string methods, a daffodil-number conditional, the collatz sequence and an Excuse Quality Control loop that reads exactly three responses. The continuation's `##` / `###` headings were also given to the original cells, so every task is illustrated from its header. All 73 cells verified by executing each one's exact source under the pinned interpreter with mocked `input()`: 0 failures, including the case-insensitive Cat Game count (Foster works in 10 of the 12 `meow` mentions once the cursor is lowercased). Committed in three stages - two pure renames (`test.ipynb` to `week1.ipynb`, `basic.ipynb` to `basics.ipynb`) and the notebook as `feat(cs2pp/week2/practical)`. The briefing PDFs stayed untracked because `*.pdf` is gitignored by design; a `html/` export made locally as a reading workaround was deleted after it broke the lecture/practical layout contract, which admits only `jupyter` and `pdf` in a cs2pp practical half. | The notebook-as-deliverable needed a verification harness the rest of the repo never required: each cell had to run by exact source with mocked `input()` under `.venv/Scripts/python.exe`, which is the Windows interpreter and cannot open `/tmp` or `/mnt` paths, so the helper scripts had to be copied into the repo root as `zz_*.py`, run and deleted. And the proposed commit of the briefing PDF was wrong for a reason only ground truth shows: `*.pdf` and `*.html` are ignored on purpose so course material stays local-only, and the layout guard then caught the `html/` folder as collateral - a contract walks the filesystem, so a gitignored folder still violates it. |
| 7 Oct 2026 | Model tables refreshed to twelve free routes | Checked OpenCode's Zen page, its published data page and the `models.dev` registry on 7 October 2026 and found three free models the rotation had not recorded: Exo Free (1,048,576 / 131,072), MiMo-V2.5 Free (200,000 / 32,000) and Ling 3.1 Flash Free (262,144 / 32,768). Added all three to AGENTS.md's pick-a-model, tokens-and-share, pros/cons and hand-off tables, to PROGRESSION's section 4.3 roster and research table, and to the `MODELS` list in `test_model_rotation_docs.py`, taking the stated count from nine to twelve everywhere it is written. Two fact changes came out of the same check: Fledge Alpha Free is now listed in OpenCode's published privacy and pricing tables as a free-period data exception rather than being undocumented, so the "treat as undocumented" caveat is gone; and the weekly traffic figures moved to the 144.879T total for the week ending 7 October 2026, with Fledge charting at 1.8T / 1.2% and Ling 3.0 Flash Fin dropping out of the top-18 alongside the two new arrivals, leaving four honest "unmeasured" cells instead of two. | The privacy paragraph and the stability note were the two places a new model actually had to be reasoned about rather than just appended: three of the twelve now share a hand-off row shape with an identical ranked three, and the zero-retention set is still only Space Bunny and LongCat, so "ten of the twelve" send a prompt somewhere not covered by a verified default. The guards are what made this cheap - `test_model_rotation_docs.py` failed the moment the roster and the prose disagreed, and it is the only reason nine and twelve could not quietly coexist. Refreshing a dated table also forced a decision the prose alone would have hidden: section 4.3's research snapshot said 2 October in four places, and leaving it would have put two different answers to "when were these figures taken" in one document. |
| 7 Oct 2026 | Method-first test audit: 13 cases added by input surface, not by line count | Ranking source files by lines of code suggested a large, under-tested set - `conditions.py` at 648 lines with 9 cases against `arithmetic_calculator.py` at 132 lines with 40. Mapping pytest cases to source files by coverage context (`COVERAGE_CORE=pytrace --cov-context=test`, then `contexts_by_lineno` from `.coverage`, because the default sysmon core silently drops dynamic contexts) showed the ranking was mostly noise: statement coverage was already complete on almost every file, and the apparent outliers were print-heavy or dead-by-design teaching sections. Re-derived the map from method signatures instead, and only methods with a real input surface could carry an untested behaviour. Added 13 cases across three areas: `rock_paper_scissors.py` (+3, closing its only uncovered statement at the `get_player_choice` retry branch and the two untied pairs of `determine_outcome`'s nine inputs), `transactions.py` (+5, driving the `file_path` parameter with synthetic workbooks - numeric cells, sub-penny prices, a single-row sheet, a wrong sheet name - where every pre-existing case fed the same committed workbook and so a hardcoded 90% would have passed all of them), and the functional receipt/grade methods (+5 for the empty basket, zero-quantity line, fractional threshold, and odd-length mean). Suite 1637 to 1650. | Method-first beat LOC-first because LOC cannot distinguish a function with four behaviours from a page of `print` calls, and two of the five priority targets turned out to need nothing. `number_pipeline.py` and `word_frequency.py` each carry a single no-argument entry point, so their one case is complete rather than thin - a conclusion only the signature gives you, and adding tests there would have been volume for its own sake. `multitasking.py` reported fifteen missing statements in a full-suite run and none when run alone; its two tests already assert all three chore messages and the closing line, so that is a coverage-attribution artefact in the frozen OOP lane, not a gap, and it was left alone rather than papered over. Two of my own cases were also wrong on first write and the mutants caught them: an uppercase `"R"` is a loss against paper, not a win, and a retry-loop assertion passed even with the loop deleted because `play_round`'s always-truthy bug prints the identical message - the fix was to call the method directly and assert both the return value and a message count. Five mutation checks confirm the new cases bite: `>= 40` to `> 40`, an `average()` divisor off by one, a `reduce()` seed removed, quantity dropped from the total, and a dropped `.2f` spec each fail at least one new case, and no source file was modified. |
| 6 Oct 2026 | README architecture folder themes corrected, and context heading retired | Applied the approved, purpose-first folder themes to `README.md`'s Project Architecture tree: functional fundamentals are described as a full toolkit rather than four example names, `sandbox/` is deliberately untested, converters no longer invents a rate bridge, and the object-oriented lanes no longer overstate TUI graphics. The separate `### Context` heading is folded into the paragraph under the architecture tree. | A comment should state what a folder does, not merely list its files or repeat its name. Naming four examples can overfit to today's contents and go stale; these rewrites describe the durable role of each folder. |
| 6 Oct 2026 | README architecture comments made purpose-first | The architecture tree's folder labels now explain what each part of the repository is for: learning portfolio, applied builds, dependency manifests, benchmark utilities, checks, and coursework. Frameworks remain only where they justify the folder's role. ``roadmap/`` casing in the references is corrected. | Architecture comments are easier to maintain when their theme is meaning rather than technology; technology changes, but the reason a folder exists usually does not. The README now says that rule explicitly, so later edits have a stated consistency target. |
| 6 Oct 2026 | README Friday resource status corrected, and pytest concentration evaluated | Counted collected pytest cases by test file and top-level folder, mapped them back to source areas, and placed the concentration tables in `NOTES.md`. `README.md` now states that TargetConnect, FutureLearn and The Forage have login credentials only and no courses/modules/certificates completed, while Bright Network, Gradcracker and the other listed resources, apart from CodeCracker, are completed and feed constant internship searches/applications. | The status correction matters because an unverified checkbox can easily be read as coursework completed; writing the credential-only scope explicitly stops that. Concentration is dominated by imperative programming and repo guards, which is useful evidence of coursework coverage but also a risk that functional and advanced work are under-exercised. Bright Network/Gradcracker being the actual recurring career channel should drive an application ledger rather than more profile polish. |
| 4 Oct 2026 | GitLab push access documented as Maintainers-only, and guarded | A.I.M moved the GitLab Project's *Allowed to push* from Developers + Maintainers (30) to Maintainers (40), and asked why Developers were not considered. `AGENTS.md` now records the level in the protection table and adds a *Why the Projects are Maintainers-only on GitLab* subsection covering the Guest/Reporter/Developer/Maintainer/Owner ladder, why Developer exists (the lowest role that can write code), and why granting it push access on `main` would let any Developer bypass the review step, protecting `main` from Guests and Reporters and from nobody who actually works on the repository. Added a fifth check to `TestMainBranchProtectionIsEnforced` asserting the live `push_access_levels` never fall below 40, and that the doc still records the choice. Suite 1636 to 1637. | The two settings are behaviourally identical while A.I.M is the sole owner, so this change fixes nothing today - which is exactly why it is worth making deliberately. It moves the intent out of A.I.M's vigilance and into the permission system: the moment a collaborator is added as a Developer, the ladder already stops them reaching `main` without anyone having to remember. The honest admission in the docs is that the old level 30 was not wrong so much as invisible - it only becomes a hole at the moment a second person arrives, which is precisely the moment nobody is re-reading the settings. The guard is the same lesson as the mirror check: a security setting that is not read is a security setting nobody has, and a comment saying why the value is 40 is what stops a future editor 'simplifying' it back to 30. |
| 4 Oct 2026 | Backups deliberately left unprotected, and mirror consistency guarded instead | A.I.M's correction: the two Backup repositories carry no protection **on purpose**, because a backup exists to be restorable and locking it means the one moment it is needed is the moment every repository refuses the write. My earlier recommendation to protect all four was wrong - I had read AGENTS.md's "this holds on all four mirrors" as a reason to lock them, when that rule is about *content* consistency, not protection. `AGENTS.md` now records the asymmetry as the design, with the public face locked and the recovery target open. Added `TestMirrorsAreLevel` (2 checks) comparing all four remotes over SSH and asserting they resolve `main` to the same commit, which is what actually keeps them consistent now that the backups accept writes. `TestMainBranchProtectionIsEnforced` was changed from requiring the backups to be recorded as "Unverified" to requiring them recorded as deliberately unprotected. Suite 1634 to 1636. | Writing the new guard surfaced two of my own recurring mistakes in miniature. It skipped the whole comparison when any one mirror was unreadable - so a single dead repository would have silenced drift detection for the other three, which is the exact failure it exists to catch; it now compares whatever it can read and skips only when nothing was readable. And I twice wrote assertions ending in `or True`, which always pass, then had to remove them. The third repeat was writing the test count as 1639 from memory when the collection said 1636 - the same class of error as reading a dry-run as proof, or a 404 as "private": treating an unexamined value as a finding. The skip registry then did its job for the first time in anger, catching the three new `pytest.skip` calls I had just introduced, and the registry was updated with reasons - which is exactly the reviewable path it was built for. |
| 4 Oct 2026 | Server-side branch protection on `main`, verified and guarded | `main` had been protected by discipline only. A.I.M configured rulesets on the two GitHub repositories and protected branches on the two GitLab projects; what is now enforced is **Restrict deletions** and **Restrict force pushes** on GitHub (active, bypass list empty, targeting the default branch) and `allow_force_push: false` on GitLab. Feature branches are deliberately untouched, so the `--force-with-lease` correction path is unaffected. `AGENTS.md` gained a *Server-side protection on `main`* subsection recording the verified state per repository, naming the four repositories, and documenting the escape hatch (toggle enforcement, rewrite all four mirrors, restore). Added `TestMainBranchProtectionIsEnforced` (4 checks) reading the two public mirrors over the unauthenticated API, and recording the two private backups as unverified rather than assuming them. Suite 1630 to 1634. | Two of my own claims this session were wrong in the same direction, and both were caught by checking rather than reasoning. I told the user verification was impossible because an early probe returned 404 and I read that as 'private' - the repositories are public and the API answered unauthenticated throughout; I repeated the claim twice before re-testing. And I had handed them a `git push --dry-run` 'verification' that cannot verify anything, because protection is enforced in the server's receive-pack hook while `--dry-run` is documented as not sending the updates at all, so it reports success on a protected and an unprotected branch alike. The common error was treating an unexamined result as a finding. The guard is deliberately asymmetric about the two states it can see: it **fails** rather than skips when the API is unreadable, because a protection check that silently vanishes offline is worse than one that is honestly absent - and it records the private backups as a documented gap instead of quietly passing them. That gap is the live risk now: an unconfigured backup accepts a force-push today. |
| 4 Oct 2026 | CS2PP weeks restructured to notebooks in both halves, contract realigned | A.I.M moved CS2PP's Python material into `jupyter/` folders, so all eleven weeks now carry `jupyter/` and `pdf/` in **both** the lecture and the practical half rather than `python/` and `pdf/`. The layout guards caught it at once: four failures, three of them the `SPLIT_MODULES` contract asserting the shape CS2PP no longer had. The contract now reads `{lecture: jupyter+pdf, practical: jupyter+pdf}`, and a new `STALE_TYPE_FOLDERS` set with a matching check records that the twenty empty `python/` folders CS2PP carried are leftovers rather than design - so they are now a test failure instead of twenty empty directories nobody re-examines. The lecture half's notebook presence, previously asserted *absent*, now asserts *present*. Suite 1628 to 1630. | The fourth failure was the only one that was not mine, and it is worth separating from the other three. The contract had been written hours earlier from a tree in which CS2PP's lectures held `python/`; the tree then changed under it. That is the guard working rather than failing - but it is the cost of pinning a contract, and the honest form of the lesson is that a layout guard is a photograph of a decision somebody made, so it is only as current as the last time that decision was confirmed. Writing the contract loosely enough that any shape passes is the opposite mistake, and was rejected earlier the same day for good reasons, so the answer is that the contract has to be *maintained*. The second point is quieter: git does not track empty directories, so deleting twenty of them left no trace in the history at all. The only record that CS2PP ever carried `python/` folders is the guard that now forbids them. |
| 4 Oct 2026 | Coverage-run audit, and the guards that were weaker than they looked | A.I.M pasted a `pytest --cov` run and asked for the results investigated with an eye to what the test suite does and does not protect against LLM-written code, plus a check of the timelines across the markdown files. The run itself was sound: the coverage database holds 182 files, every path exists on disk, and 5991 statements / 38 missed / 1318 branch / 54 partial / 149 of 160 files at 100% reconcile exactly with what the docs claim. The pasted output carried one corrupted row - a `fundamentalve_programming` path that does not exist, which had swallowed the `main.py`, `modules.py` and `numbers.py` rows beside it. Timeline audit found all nine chronology hashes matching their claimed commit dates and every weekday claim correct, but three real defects, all fixed: the "16-week" label outlived the 117-day window it described; NOTES.md's maintenance log ran out of order and left Wed 23 Sep stranded below a blank line; and a test docstring still described `main.py` as an unparseable stub five days after it was repaired, deriving 159 where 160 is correct. Four guards were strengthened, two of them from findings that only a mutation exposed. | The most useful finding was that a guard's strength is not its passing, it is what it refuses to accept - and that the two ways to write a guard wrong are both invisible in a green run. The branch-coverage check asserted only "not 98", so a figure drifting to 94% was fine; the skip-registry first counted with a regex and audited its own docstring; its tracked-file check inferred a path from a message string and looked in the wrong directory, so it passed against a mutation naming a tracked file. Four of the six guards I wrote across the last two sessions were caught by something other than review, and every one of them was caught by making it fail on purpose. The second lesson is about direction of comparison: a tree check failed to notice a deleted folder because I ran the assertion that measures the other direction, and a fix that makes an assertion stricter can still be measuring the wrong thing. Stale prose survived five days beside an assertion that passed throughout, because it recomputed live rather than trusting the note next to it - which is the right way to write the assertion and the wrong way to leave the explanation. |
| 4 Oct 2026 | README architecture tree rewritten to folders-only and guarded | A.I.M asked for the README tree to list folders only, with filenames kept inside `file_scores_ranking/` for context. The tree had drifted badly: it still showed `Data/`, `Python/`, `FILE SCORES RANKING/` and a flat `coursework1/`, none of which existed, and it listed eighteen root files as if the tree enumerated the repository. Rewritten at the real lowercase paths, folders only, with the three root documents and the two ranking documents named deliberately. The eleven CS1IP weeks are collapsed into one `week1/ ... week12/` line with the convention stated once in prose, because repeating it eleven times is how a tree goes stale. Added `TestReadmeArchitectureTree` (5 checks) comparing the tree against the filesystem in both directions, and asserting the folder-only convention. Suite 1613 to 1618. | The first draft of the guard passed a mutation that removed a folder from disk, which is the most basic failure a filesystem comparison can have. The reason was not the comparison but the fixture: `roadmap/` was still named in the README, so nothing detected its absence — the test that should have caught it was the claims guard, and the one I had chosen to run was checking the other direction. A guard is only as good as the mutation you try against it, and "did I test the right assertion" is a distinct question from "did the test pass". The same pass also caught the README silently dropping its only `PROGRESSION.md` reference, which a folder-only tree had made invisible: a file that names no folder is the easiest line in a document to delete without noticing it mattered. |
| 4 Oct 2026 | CS2PP joined the lecture/practical convention, guards generalised and two false passes found | A.I.M gave CS2PP the same treatment as the year1 modules: all eleven weeks now split into `lecture/{pdf,python}` and `practical/{python,jupyter}`, plus `coursework1/` and `coursework2/`. `test_structure.py` was generalised from a CS1IP-only class into a module-driven one, so CS2PP is checked by the same rules as CS1IP, CS1DB and CS1OP, and a notebook check was added for CS2PP's only tracked file. Guard count 40 to 53, suite 1587 to 1613. | Two of the new guards passed when they should have failed, and both were found by mutating the tree rather than by reading the code. `test_no_unexpected_type_folders` only inspected folders *inside* `lecture/` and `practical/`, so a stray directory dropped beside them passed unnoticed; the fix added a week-level check, since a guard scoped to a subtree cannot see its own parent. Worse, `test_cs2da_is_the_only_module_without_the_split` iterated `SPLIT_MODULES`, which excludes CS2DA by design, so it asserted over an empty set and passed no matter what the tree contained — a guard that cannot fail is worse than no guard, because it reads as coverage. The lesson is the same one the CS1IP guards already taught, now at a second remove: a green guard is a claim about the world, and only a deliberate violation tells you whether the claim has any content. Two smaller corrections came out of the same pass: the notebook check had to skip `.ipynb_checkpoints/`, whose autosaved copies carry no kernel metadata and are gitignored, and `week7/lecture/txt` had to be named as an exception rather than added to every week's expectation, since one week reading text files is not a convention for all eleven. |
| 4 Oct 2026 | Coursework tree reorganised into lecture/practical sub-folders, tests extended and repointed | A.I.M split every CS1IP week folder into `lecture/` and `practical/`, each with `java/`, `python/` and `pdf/` beneath it, and gave `coursework1/` and `coursework2/` a `java/`, `python/` and `data/` split; CS2DA's weeks split by language and CS1DB's by `sql/` and `data/`. The reorganisation broke 59 tests before a line was written: `conftest.py` resolved coursework modules at the folder root, and three of the four `sort_comparison` tests failed for a second reason. Repointed `conftest.py` at named constants (`COURSEWORK1_PYTHON`, `COURSEWORK2_DATA`, ...) rather than joining paths per assertion, and added `tests/test_university_courseworks/test_structure.py` (40 checks) covering the top-level layout, the coursework splits, every week folder, type-folder extension purity, and the three deliberately non-uniform modules. Suite 1547 to 1587. | The second failure was the interesting one. `sort_comparison.py` resolves its deck fixtures against `dirname(__file__)`, so moving the fixtures into `data/` left the marked script unable to find its own inputs — and one test still passed, for the wrong reason: `os.path.exists` failed before its `fake_open` patch ever fired, so a test named for the missing-file branch was really asserting the file-missing branch by accident. Three ways to read that: the marked script is submitted work and must not be edited to suit a folder move, so the fix belonged in the tests; a passing test proves nothing unless you have watched it fail against the old code, which is why the patch was neutralised to confirm it bites; and a folder move is an API change even when nothing imports the moved code. The new guards were bite-tested six ways before being believed. |
| 2 Oct 2026 | Citation dates reconciled between the two model documents | A.I.M asked for the models' uses and the references to be confirmed as equally provided across AGENTS.md and this file. The nine-model list, all nine route-limit pairs, and every weekly traffic figure and share already matched exactly, and all three sources were named in both files. Four citations did not: AGENTS.md dated its registry retrieval 1 October 2026 in the pick-a-model table and 2 October 2026 in the tokens-and-share table, the §4.3 intro still described usage figures as a daily snapshot taken on 1 October although the table beneath it carried weekly figures for the week ending 2 October, the key-sources line claimed all three sources were retrieved on 1 October, and the Zen documentation URL appeared only here. Unified every retrieval citation to 2 October 2026, rewrote the §4.3 intro to name the weekly week-ending snapshot the table actually holds, gave each key source its own date, and added `https://opencode.ai/v2/docs/zen/` to AGENTS.md's privacy paragraph. Suite unchanged at 1547. | A table can be refreshed while the prose introducing it stays behind, and the prose is what a reader checks the table against — the §4.3 intro was describing a resolution the table no longer used. Equally, a guard that reads table bodies by header cannot catch a stale sentence above them, so the evidence a document presents is not the same as the evidence it is tested on. The check that caught these was a read of both files side by side, not a test run. |
| 2 Oct 2026 | Pre-flight added, model categories corrected, folder move followed through | A.I.M asked for a selection rule before every model runs: confirm token usage, confirm percentage left, confirm which model is applicable, with speed the least weight. Added as a three-question pre-flight to AGENTS.md, noting that only A.I.M can read the remaining allowance from the console — an agent that cannot see it cannot claim it passed. Extended the pros/cons table to name each model's main purpose, main assets, weaknesses and the applied use that survived correction, and added a tokens-and-share table from OpenCode's published weekly figures (160.524T tokens across eighteen listed models; the rotation's own models are 69.6% of that, Space Bunny alone 38%, Big Pickle and Fledge Alpha Free unmeasured). Recorded Fledge Alpha Free's `Upstream request failed: Endpoint is unavailable.` as a stability fact, making three of nine free routes known-unstable. Also followed through the last commit's folder reorganisation: `university_courseworks/` moved to `year1/semester1/cs1ip/`, `year2/modules/` and `university_modules/`, and the pytest paths, `test_courseworks.py`, `convert_hash_comment_runs.py` and the AGENTS/NOTES/UNIVERSITY_MODULES references were all repointed. Suite 1543 to 1547. | Popularity is not suitability, and the two claims that looked like evidence for it are not: Big Pickle is the rotation's most-used model yet is unmeasured on the platform's own traffic table, and Fledge Alpha Free was released the day before the snapshot, so it has no measured share at all. The honest cell is `unmeasured`, and a guard now fails if anyone fills it with a number. The second lesson is that a folder move is an API change: three of the nine models in the rotation table are referenced by pytest path, and every one of them was silently skipping rather than failing. |
| 2 Oct 2026 | Fledge Alpha Free added to the rotation | Added Fledge Alpha Free to the rotation tables and hand-off columns in AGENTS.md and PROGRESSION.md, and to the MODELS list in the rotation-docs guard, after verifying it against models.dev (free, 1,048,576 context, 131,072 output, multimodal input, released 1 October 2026; not yet in OpenCode's published privacy or pricing table). Bumped every stated model count from eight to nine. | A newly released model arrives with a route limit but no track record, so it gets a conservative handling: its row exists, it carries a reason to pick it, and it is excluded from the zero-retention claims until OpenCode documents it. |
| 2 Oct 2026 | AI-tooling chronology logged and guarded | Reconstructed the usage chronology of the AI tooling from the git log and added it as a dated table in section 4.7. Added `tests/test_scripts/test_progression_chronology.py` (five checks: table exists with the expected row shape, each date parseable, the dates in chronological order, the model names present in the table all members of `MODELS`, and each row carrying commit-evidence). Added two AGENTS.md house-style bullets: multi-intent prompts are split before acting, and a model-scoped review fallback for bundled asks. Refreshed the stated suite count from 1538 to 1547 in AGENTS.md, PROGRESSION.md and FILE_RANKING_GUIDE.md. | A chronology that is not guarded is just prose twice removed from the tree. The rules applied here were the same three that govern the rotation guard: dates must parse, order must be chronological, and any model name that appears must exist in the same list the rotation table uses — here `MODELS` in `test_model_rotation_docs.py`. |
| 2 Oct 2026 | Folder moves, docs aligned | Moved `FILE_SCORES.md` and `FILE_RANKING_GUIDE.md` under `file_scores_ranking/` and the four `requirements*` files plus `requirements_sync.py` under `requirements/`; updated the path constants in the two test files and `score_ranking.py`, the Dependabot `directory`, `pyproject.toml`'s `pythonpath`, and the README tree. | A folder move is an API change for everything that resolves a path by name. The four places a move breaks were found by name-references, not by globbing: a script that writes to a moved path (`scripts/score_ranking.py`'s output), an import (`import requirements_sync`, fixed via `pythonpath`), a test file that builds `REPO_ROOT / "<filename>"` from the file's name, and the Dependabot directory setting. |
| 1 Oct 2026 | Pros, cons and the hand-off rule | Added a pros/cons and main-purpose table for all eight free models beside the pick-a-model table, plus a hand-off protocol: a model that judges the task wrong for it must decline and name three alternatives ranked best-first, with a stated reason. Two constraints keep it honest — a hand-off is a *request* rather than a switch, because model selection happens in the OpenCode console and an agent cannot move itself; and retention overrides fit, so a credential-bearing prompt narrows the field to the two zero-retention models whatever the ranking says. Added `tests/test_scripts/test_model_rotation_docs.py` (11 tests) and bite-tested four mutations of it. | Writing the ceilings down is what makes declining possible. Before this, "I am not the right model for this" had no stated basis, and a model under pressure to produce something would produce something. The ceilings are measured numbers rather than opinions, so a decline cites evidence. Two of the four mutations did not bite at first, and both were bugs in the test rather than the document: matching single lines flagged correct prose, because the section is hard-wrapped at 80 columns and a sentence's evidence often sits two lines below it; and an assertion demanding that each hand-off mention all seven other models contradicted the rule's own ranked-three. Only two mutations were needed to prove the guard, and one of those had to be re-run because the first version edited a string that did not exist in the file - a false pass that a green run alone would not have revealed. |
| 1 Oct 2026 | Free-model rotation verified against source | Researched all eight free OpenCode models and checked every claim against the `models.dev` registry and OpenCode's own Zen and data pages. Five of the drafted claims did not survive: a "50.8% SWE Atlas resolve rate" attributed to a URL that resolves to a technology news aggregator mentioning neither the model nor the benchmark; a model-catalogue URL returning 404; a DeepSeek origin for Big Pickle inferred from provider error strings; a claim that LongCat was the only zero-retention free model (Space Bunny is too); and seven per-model performance figures with no traceable source. Corrected the context and output columns against the registry's per-provider entries, which showed the free routes are narrower than the models behind them, and rewrote the contributor table to `main` only after finding it had counted a bot whose 7 commits sit on unmerged branches. | A link that resolves is not evidence; it has to resolve to the claim. The whole draft read as research because it had citations in it, and four of the six citations did not support the sentence they were attached to. The second lesson is that the repo's own rule 2 exists precisely to catch an assistant doing this, and it caught one - so the rule is load-bearing, not decorative. |
| 30 Sep 2026 | Progression review & code review | Reconciled the ranking sheet: deduped a 167-entry document down to the 161 real files, aligned all 161 headings to their own tables, normalised 9 entries that rounded an exact `.5` downward against 50 that rounded up, and corrected the guide's pre-verified table and worked example. Corrected four stale figures in the docs (98%→95% branch, 171/182→148/159, "29 lines in 8 caps"→38 in 11, 1350→1547). Fixed a silent failure in `execution_time.py` where a mistyped folder re-prompted with no output. Added 94 guard tests across three files. Wrote this review. | A fact written in prose and never recomputed is a fact that will be wrong. The ranking sheet had 112 of 161 headings disagreeing with their own tables and nobody noticed, because nothing compared them. The fix was not to re-read the prose more carefully — it was to make the stale number fail the suite. |
| 30 Sep 2026 | Documentation brought into line with the rescore and the repair | Swept every markdown file for figures the guards do not cover, and found four that had gone stale: the benchmark's file count, the maintenance log's test count, the README's ranking description, and the two-tier weighting and tie-break, which were in the generated sheet but not explained in prose. Also fixed a defect in the scorer itself, where a note written as two adjacent strings rather than a `(sign, text)` tuple rendered a strength under **Weaknesses** with a stray `+`. | The guards check arithmetic - weighted cells against criteria, totals against the tree - and none of them reads a sentence. A ranking scheme documented only inside a generated table is invisible to anyone who has not regenerated it, which is how 'four criteria' and '161 files' survived a rescore to five and 160. The sign leak is the more interesting one: implicit string concatenation looks exactly like a tuple in source, so it passed the overlap assertion and shipped in main.py's entry until it was read by eye. Verified it bites by injecting the fault before trusting it. |
| 30 Sep 2026 | main.py repaired; the IndentationError stub now runs | A.I.M added `pass` to `fundamental_topics/main.py`, which had carried a deliberate `IndentationError` since June. The file now parses, runs, and appears in coverage; two tests that asserted it raises `SyntaxError` were rewritten to assert the opposite, and its `pyproject.toml` coverage omit was removed. | A three-line fix that only *looks* small. It moved the measured denominator, the files-at-100% count, the benchmark FAIL count, the lowest-scored file, the mean from 84.4 to 84.6, and two documented figures in three files - and the guards caught every one, which is the first time they have all fired on the same change. The tests were the real cost: they pinned a defect that had been legitimately repaired, so correct code failed the suite. That is exactly what rule 11 warns about, and the fix is to move the test forward rather than break the code back. |
| 30 Sep 2026 | File ranking rescored on two tiers, Risk added | Rescored all 160 files on five criteria with per-tier weighting — learning material judged on readability (35%), applied projects on fixability and robustness (30% each) — and made every score generated from measured signals by `scripts/measure_ranking_signals.py` and `scripts/score_ranking.py`. Mean 84.4, spread 50-92, with 43 A / 89 B / 25 C / 2 D / 1 E. | The first pass scored four criteria with one flat weighting and was written by eye, so a disputed mark could not be traced to anything. Three findings changed the shape of the work: 81 of 160 files have no functions at all, and a rubric that awarded near-full marks for 'nothing undocumented' rewarded exactly the flat scripts a reader struggles with; starting every criterion from 100 and deducting produced a 98.4 mean that could not tell a perfect file from a broken one; and float arithmetic made the sheet disagree with its own guard by a tenth, because 96 * 0.15 is 14.399999999999999 in binary. |
| 30 Sep 2026 | Post-merge fix: four counting paths still read the disk | After PR #13 merged, four guards still counted modules with `rglob`, so they counted the newly untracked practice file and then broke when it went missing. Re-pointed all four at git and removed a hardcoded 161 that would have invited bumping itself. Added a skip so a fresh clone without the sandbox passes. | The failure surfaced the moment `git checkout` deleted the untracked file, which is a sharper test than any I could have written: a guard that reads the filesystem cannot tell an intentional untracking from an accident. A literal like 161 inside an assertion is worse still - it fails for a real reason and invites a maintainer to change the number rather than the cause. The suite now passes with the practice file present and absent, which is the condition that actually matters. |
| 30 Sep 2026 | Sandbox untracked, comment rule widened repo-wide | Restored `sandbox/aim.py`'s practice code after it was lost, then made the file untracked and gitignored so practice work can never be committed again, with three guards asserting it stays that way. Widened the two-line-hash-comment rule from three files to every tracked file: 328 runs became triple-quoted blocks across 52 files, with the frozen OOP lane and the marked coursework exempt by name. | aim.py is practice reference material, not repository content, and the guard that counted the remaining overlong runs was a debt register rather than a rule - it recorded a number without constraining anything, so roughly 1100 non-compliant lines sat there for weeks with nothing failing. Two tests broke in the conversion and both were tests asserting a spelling rather than a behaviour: one looked for a leading `#` on code that had become inert as a string literal, which is a stronger guarantee, not a weaker one. |
| 30 Sep 2026 | Month-by-month progression, measured | Replaced the impressionistic monthly narrative with two recomputed tables - commits and mean subject length per month, plus a keyword mix - and corrected Stage 4. Weekly data shows the real arc: a narrative peak at 138.0 chars in Week 28, an August plateau, then the single largest step of the run at Week 38 (63.7). | Writing the progression from a handful of sampled commit subjects produced a claim that was wrong in a way sampling invited: 'NumPy, then Pandas, then groupby()' implied a curriculum, when pandas, ten notebooks and the OutlierCapper all landed in a single burst on 2 Aug. Measuring every commit rather than selecting some also exposed that the subject-length peak is in July, not June. |
| 30 Sep 2026 | Docstring structure & end-of-file bytes | Normalised every `.py` and `.md` file in the tree to exactly two trailing newlines (224 were at three, 6 markdown files at one, so all 232 are now uniform), converted 14 over-long hash-comment runs to """ blocks, and added guards for both. Separately corrected 3 docstrings whose opening quotes shared a line with their summary. | The convention had been written down but enforced nowhere, so it drifted twice - once to three newlines, once to quote-on-the-same-line - and both were invisible in review. A rule that exists only in prose is a preference; the guards are what make it a constraint. |
| 30 Sep 2026 | Trailing-whitespace sweep | Stripped 853 trailing-whitespace lines from 103 Python files and added a guard. Fifteen lines were left alone because they sit inside multi-line string literals, two of them expected-output strings in `test_math_and_science_calculators.py` where a stripped space would change what the test asserts; the exemption is computed with `tokenize`, so it follows a line as it moves in or out of a string. | Trailing whitespace is invisible in review and in most editors, so 853 lines accumulated unnoticed. Only whitespace at the end of a line was removed - never leading indentation - so no code changed shape, and the full suite confirmed it. A cleanup that touches a third of the tree has to be provably behaviour-free, which is why the string-literal exemption is derived rather than hardcoded. |
| 30 Sep 2026 | Data-file validation & byte invariants | Fixed `input.csv`, whose header (`gamertag, gamerscore, is_online, account_made`) carried a leading space in every cell after the first - invisible in output because `file_reader.py` strips its data rows but not the header. Added `tests/test_scripts/test_data_files.py` (65 tests, kept out of the main suite because these files have no module to import) covering JSON parsing, CSV rectangularity, header whitespace, LF endings, and that each fixture is still named by the script that uses it. Normalised 9 Python files to exactly 3 trailing newlines and guarded the invariant. | The same class of defect as the 112 stale ranking headings: something wrong that reads perfectly well on screen. A leading space in a CSV header and a missing trailing newline are both invisible in review and both caught by the first test written to look. |
| 30 Sep 2026 | Guard hardening (same day, follow-up) | `test_total_commit_count` asserted the document states the *live* `HEAD` commit count, so it failed the instant this file was committed — committing a document that states the commit count adds a commit. Rewrote it to count commits before a fixed date cutoff. Corrected the duration from "17 weeks" to 117 days (16.7 weeks). | A guard that cannot pass is worse than no guard, because it teaches you to ignore failures. Two figures in this file have now broken on the same root cause: any number that changes *because of the act of writing it down* cannot be asserted against a live source. |
| 29 Sep 2026 | Ranking drift & merge-commit fix | Landed the commit-scope guard (rule 12) and the branch-and-PR correction workflow, then found that the first merge commit broke the guard it had just passed. Exempted merge commits by parent count. | A rule strict enough to punish correct behaviour gets ignored, and then protects nothing. The fix was to make the rule right, not to weaken it — and to record the exemption in the rule itself so it stays stated rather than hidden. |
| 29 Sep 2026 | Doc-drift audit | Found and fixed stale figures across `AGENTS.md` and `NOTES.md`; added `test_repo_doc_numbers.py` to pin them. Verified 10 consecutive clean suite runs and 17 test files in isolation. | Documentation drift is the most common failure in a self-directed project and the hardest to see, because the stale sentence still reads perfectly well. It was only visible by recomputing the numbers. |

Two patterns recur across these sessions, and are the real content of this log:

1. **The bugs worth fixing are the ones the tooling finds, not the ones you
   spot.** The `decimal` circular import survived because the test suite was
   green; it died only when the file was run the way a user runs it. Every
   genuine defect found in this period came from running or re-measuring
   something, never from reading the code more carefully.
2. **Every correction produced a second-order problem.** Fixing the ranking
   drift required a guard, which was then satisfied by a substring check that
   let a partial edit through. Fixing that required a stricter check, which
   then failed on a self-referential count. The pattern is worth expecting:
   each fix lands correctly and immediately creates the conditions for the
   next one.

---

## Verifying this document

Every claim above is checkable. The commands that regenerate the figures:

```bash
# Project span and commit counts
git log --reverse --format="%ad" --date=short | head -1
git log -1 --format="%ad" --date=short
git rev-list --count HEAD
git log --format="%ad" --date=format:%Y-%m | sort | uniq -c

# Suite and coverage
.venv-win/Scripts/python.exe -m pytest -q
.venv-win/Scripts/python.exe -m pytest --cov=python --cov-report=term-missing

# Module counts per lane
find python -name "*.py" ! -name "__init__.py" | wc -l
find python/imperative_programming -name "*.py" ! -name "__init__.py" | wc -l

# Quality mean, recomputed from the score sheet
# (see tests/test_scripts/test_ranking_docs.py for the checked calculation)

# Every file run standalone, the way a user meets it
.venv-win/Scripts/python.exe scripts/execution_time.py --all
```

The numeric claims in this file and in `AGENTS.md` are pinned by
`tests/test_scripts/test_repo_doc_numbers.py`, so a stale figure fails the
suite instead of quietly misleading the next reader.
