# Progression and AI Collaboration Review

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
| Test suite | 1650 tests, all passing |
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
edits, and runs `.venv/Scripts/python.exe -m pytest` itself. Claude and
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

Within OpenCode, A.I.M rotates across **twelve free models** — Big Pickle Free,
Space Bunny Free, Nemotron 3.5 Lightning Free, Nemotron 3 Ultra Free, Ling 3.0
Flash Fin Free, Ling 3.1 Flash Free, Muse Spark 1.3 Contributor Free,
MiMo-V2.6-Flash Free, MiMo-V2.5 Free, LongCat 2.5 Preview Free, Exo Free and
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

The twelve-model list in `AGENTS.md` answers *which model to pick*, but it
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
<https://opencode.ai/docs/zen/>. Usage figures are OpenCode's published weekly
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
| Exo Free | 1,048,576 | 131,072 | Yes | below the published top-18 | unmeasured |

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

- OpenCode Zen documentation: `https://opencode.ai/docs/zen/` — the model list,
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
  LongCat) sit on the zero-retention default. Seven (Big Pickle, Exo Free,
  Fledge Alpha Free, both MiMos, both Lings) may have free-period data used to
  improve the model. Two (the Nemotrons) are NVIDIA trial endpoints that log
  use and whose terms ask for no personal or confidential data. One (Muse Spark
  1.3 Contributor) is explicitly a training-data trade. Ten of the twelve send
  prompts somewhere that is not covered by a verified zero-retention default,
  which is why rule 6 exists.
- **The free tier is popular, so it is not private by default.** Six of the
  twelve are 1M-class routes — Space Bunny, Muse Spark 1.3, Nemotron 3 Ultra,
  LongCat 2.5, Fledge Alpha Free and Exo Free — and five of those six now chart
  on the published table, Space Bunny and Muse Spark 1.3 alone carrying 36.6%
  and 22.8% of listed traffic between them. Only Exo Free is too new to appear,
  which is the same gap Fledge Alpha Free had a week earlier. Being on a free
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

This is the repo's own rule 2 — treat an assistant's line-level claim as a
candidate, not ground truth — catching an assistant. The failure was not a
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
project has already paid for once. Exo Free was fingerprinted at 99.4% against
Claude Opus 5.5, which is *not* provenance: a closed-set fingerprint of an
uncatalogued model names its nearest neighbour by construction, so the honest
statement is that the model is unidentified. And LongCat 2.5 Preview Free has
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
| Tests | 1650 passing, 0 failing |
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
| --- | --- | --- | --- |
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
| 2 Oct 2026 | Citation dates reconciled between the two model documents | A.I.M asked for the models' uses and the references to be confirmed as equally provided across AGENTS.md and this file. The nine-model list, all nine route-limit pairs, and every weekly traffic figure and share already matched exactly, and all three sources were named in both files. Four citations did not: AGENTS.md dated its registry retrieval 1 October 2026 in the pick-a-model table and 2 October 2026 in the tokens-and-share table, the §4.3 intro still described usage figures as a daily snapshot taken on 1 October although the table beneath it carried weekly figures for the week ending 2 October, the key-sources line claimed all three sources were retrieved on 1 October, and the Zen documentation URL appeared only here. Unified every retrieval citation to 2 October 2026, rewrote the §4.3 intro to name the weekly week-ending snapshot the table actually holds, gave each key source its own date, and added `https://opencode.ai/docs/zen/` to AGENTS.md's privacy paragraph. Suite unchanged at 1547. | A table can be refreshed while the prose introducing it stays behind, and the prose is what a reader checks the table against — the §4.3 intro was describing a resolution the table no longer used. Equally, a guard that reads table bodies by header cannot catch a stale sentence above them, so the evidence a document presents is not the same as the evidence it is tested on. The check that caught these was a read of both files side by side, not a test run. |
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
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m pytest --cov=python --cov-report=term-missing

# Module counts per lane
find python -name "*.py" ! -name "__init__.py" | wc -l
find python/imperative_programming -name "*.py" ! -name "__init__.py" | wc -l

# Quality mean, recomputed from the score sheet
# (see tests/test_scripts/test_ranking_docs.py for the checked calculation)

# Every file run standalone, the way a user meets it
.venv/Scripts/python.exe scripts/execution_time.py --all
```

The numeric claims in this file and in `AGENTS.md` are pinned by
`tests/test_scripts/test_repo_doc_numbers.py`, so a stale figure fails the
suite instead of quietly misleading the next reader.

