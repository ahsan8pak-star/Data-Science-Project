# Progression and AI Collaboration Review

A review of the 16-week Data Science project that began on **Thursday 4 June
2026** and ran to **Tuesday 29 September 2026** — 117 days, and 714 commits
across four months, mirrored to GitHub and GitLab.

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
| Test suite | 1538 tests, all passing |
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

Within OpenCode, A.I.M rotates across **eight free models** — Big Pickle Free,
Space Bunny Free, Nemotron 3.5 Lightning Free, Nemotron 3 Ultra Free, Ling 3.0
Flash Fin Free, Muse Spark 1.3 Contributor Free, MiMo-V2.6-Flash Free and
LongCat 2.5 Preview Free. The rotation is selected in the console, not from
inside a conversation: an agent cannot switch its own model mid-session.

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

The eight-model list in `AGENTS.md` answers *which model to pick*, but it
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
substance of the rule. A list of all seven remaining models transfers the whole
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

#### What the research shows about each model

The route limits below are OpenCode's own, not the model's full capability, and
they are what this project actually gets. Both columns come from the
`models.dev` registry entries for the `opencode` provider
(`https://models.dev/api.json`, retrieved 1 October 2026) — exact token
counts, because the rounded versions are ambiguous: 262,144 is 256K, not
262K. The free-pricing and privacy columns come from
<https://opencode.ai/docs/zen/>. Usage figures are OpenCode's observed daily
token volume on 1 October 2026 (<https://opencode.ai/data/>) and are a
snapshot, not a ranking to plan around.

| Model | Route context | Route output | Free-period data used to improve the model? | Daily volume on 1 Oct |
| --- | --- | --- | --- | --- |
| Space Bunny Free | 1,048,576 | 524,288 | No — zero-retention | 57T (most-used model) |
| Muse Spark 1.3 Contributor Free | 1,048,576 | 131,072 | Yes — trains future Meta models | 32T |
| MiMo-V2.6-Flash Free | 200,000 | 32,000 | Yes | 8.7T |
| Nemotron 3 Ultra Free | 1,000,000 | 128,000 | NVIDIA trial terms; use is logged | 3.8T |
| LongCat 2.5 Preview Free | 1,000,000 | 131,072 | No — zero-retention | 2.3T |
| Ling 3.0 Flash Fin Free | 262,144 | 32,768 | Yes | 355B |
| Nemotron 3.5 Lightning Free | 262,144 | 262,144 | NVIDIA trial terms; use is logged | 260B |
| Big Pickle Free | 200,000 | 32,000 | Yes | below the published top-18 |

The table is sorted by observed volume rather than by role, because the
ordering is the finding: the two models A.I.M reached for by default are the
two the whole platform also reaches for, which is not the same as being the
right tool for this repo. The `models.dev` registry also has to be read per
provider, not per model — the same MiMo release is 200,000 on the OpenCode
free route and 1,048,576 everywhere else, so a single "MiMo has a 1M window"
line is true and useless.

**Key sources, all retrieved 1 October 2026:**

- OpenCode Zen documentation: `https://opencode.ai/docs/zen/` — the model list,
  the free-on-input/output/cached-read pricing table, and the privacy section
  that names each exception.
- OpenCode model data: `https://opencode.ai/data/` — observed token volumes,
  unique users and weekly retention per model.
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
  LongCat) sit on the zero-retention default. Four (Big Pickle,
  MiMo-V2.6-Flash, MiMo-V2.5, Ling 3.0 Flash Fin) may use free-period data to
  improve the model. Two (the Nemotrons) are NVIDIA trial endpoints that log
  use and whose terms ask for no personal or confidential data. One (Muse Spark
  1.3 Contributor) is explicitly a training-data trade. Four of the eight
  therefore send prompts somewhere that is not covered by the zero-retention
  default, on a public repository, which is why rule 6 exists.
- **The free tier is popular, so it is not private by default.** The four
  large-window models in the rotation — Space Bunny, Muse Spark 1.3, Nemotron 3
  Ultra, LongCat 2.5 — are also four of the seven most-used models on OpenCode.
  Being on a free tier says nothing about who else can read the prompt.
- **Two models are named for what they are not.** Big Pickle and Space Bunny
  are both described by OpenCode as "stealth models" with no published vendor,
  so any claim about which lab built either one is speculation. The earlier
  draft of this section asserted a DeepSeek origin for Big Pickle from leaked
  provider errors; that was removed, because a provider's error strings are not
  a provenance record.

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
| Tests | 1538 passing, 0 failing |
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
| 1 Oct 2026 | Pros, cons and the hand-off rule | Added a pros/cons and main-purpose table for all eight free models beside the pick-a-model table, plus a hand-off protocol: a model that judges the task wrong for it must decline and name three alternatives ranked best-first, with a stated reason. Two constraints keep it honest — a hand-off is a *request* rather than a switch, because model selection happens in the OpenCode console and an agent cannot move itself; and retention overrides fit, so a credential-bearing prompt narrows the field to the two zero-retention models whatever the ranking says. Added `tests/test_scripts/test_model_rotation_docs.py` (11 tests) and bite-tested four mutations of it. | Writing the ceilings down is what makes declining possible. Before this, "I am not the right model for this" had no stated basis, and a model under pressure to produce something would produce something. The ceilings are measured numbers rather than opinions, so a decline cites evidence. Two of the four mutations did not bite at first, and both were bugs in the test rather than the document: matching single lines flagged correct prose, because the section is hard-wrapped at 80 columns and a sentence's evidence often sits two lines below it; and an assertion demanding that each hand-off mention all seven other models contradicted the rule's own ranked-three. Only two mutations were needed to prove the guard, and one of those had to be re-run because the first version edited a string that did not exist in the file - a false pass that a green run alone would not have revealed. |
| 1 Oct 2026 | Free-model rotation verified against source | Researched all eight free OpenCode models and checked every claim against the `models.dev` registry and OpenCode's own Zen and data pages. Five of the drafted claims did not survive: a "50.8% SWE Atlas resolve rate" attributed to a URL that resolves to a technology news aggregator mentioning neither the model nor the benchmark; a model-catalogue URL returning 404; a DeepSeek origin for Big Pickle inferred from provider error strings; a claim that LongCat was the only zero-retention free model (Space Bunny is too); and seven per-model performance figures with no traceable source. Corrected the context and output columns against the registry's per-provider entries, which showed the free routes are narrower than the models behind them, and rewrote the contributor table to `main` only after finding it had counted a bot whose 7 commits sit on unmerged branches. | A link that resolves is not evidence; it has to resolve to the claim. The whole draft read as research because it had citations in it, and four of the six citations did not support the sentence they were attached to. The second lesson is that the repo's own rule 2 exists precisely to catch an assistant doing this, and it caught one - so the rule is load-bearing, not decorative. |
| 30 Sep 2026 | Progression review & code review | Reconciled the ranking sheet: deduped a 167-entry document down to the 161 real files, aligned all 161 headings to their own tables, normalised 9 entries that rounded an exact `.5` downward against 50 that rounded up, and corrected the guide's pre-verified table and worked example. Corrected four stale figures in the docs (98%→95% branch, 171/182→148/159, "29 lines in 8 caps"→38 in 11, 1350→1538 tests). Fixed a silent failure in `execution_time.py` where a mistyped folder re-prompted with no output. Added 94 guard tests across three files. Wrote this review. | A fact written in prose and never recomputed is a fact that will be wrong. The ranking sheet had 112 of 161 headings disagreeing with their own tables and nobody noticed, because nothing compared them. The fix was not to re-read the prose more carefully — it was to make the stale number fail the suite. |
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

