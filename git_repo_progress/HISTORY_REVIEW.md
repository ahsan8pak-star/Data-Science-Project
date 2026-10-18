# HISTORY_REVIEW.md — 22 weeks, five identities, one developer

**Span:** 4 June 2026 → 17 October 2026 · **836 commits** · **565 tracked files** ·
**22 weeks** · 8 merge commits · 43 MB `.git`

**Purpose.** A retrospective on how this repository actually grew: what went
well, what went wrong, and which improvement each one was earned by. Every
figure below is derived from the git record and can be re-derived with the
command shown, so a claim here is checkable rather than remembered.

**Method.** `git shortlog`, `git log --format`, `--name-only` and `--numstat`
aggregations, plus `--diff-filter` walks for additions, deletions and renames.
No claim in this document rests on recollection alone; where memory and the
record disagree, the record wins and the discrepancy is itself reported.

**Names.** `A.I.M` is the placeholder for the developer's initials, used
consistently across the repository's own files. The other handles — `om001219`
and `ThenameisAiman` — are real and are named here as they appear in the history,
because the point of §2 is that they were *used* and a review that hid them
would misrepresent the record.

> [AI-authored fix] This document was assembled by an assistant at the owner's
> request from the git record, and every figure in it was produced by a command
> rather than estimated. The judgement calls — which lessons matter, how the
> contributors are characterised — are the owner's to accept or reject.

---

## 1. The contributor register

`git log --format='%an <%ae>' | sort | uniq -c | sort -rn` returns **five**
identity strings, which resolve to **one human developer**, one university
account he committed through, one AI tool that committed under his GitHub
identity, and one AI co-author trailer.

| # | Identity | Email | Commits | Window |
| --- | --- | --- | --- | --- |
| 1 | `ahsan8pak-star` | `ahsan8pak@gmail.com` | 774 | 9 Jun → 17 Oct 2026 |
| 2 | `om001219` | `om001219@student.reading.ac.uk` | 32 | 4–5 Jun 2026 |
| 3 | `A.I.M` | `ahsan8pak@gmail.com` | 17 | 4 Jun → 14 Oct 2026 |
| 4 | `om001219` | `ahsan8pak@gmail.com` | 10 | 5–8 Jun 2026 |
| 5 | `ThenameisAiman` | `90571699+ThenameisAiman@users.noreply.github.com` | 3 | 1 Jul 2026 |
| | **Total** | | **836** | |

Plus **7 commits** carrying `Co-Authored-By: Claude Opus 4.8 (1M context)
<noreply@anthropic.com>`, which `shortlog` does not attribute to an author at
all — a good reminder that the tool's view and the record's view are not the
same view.

### 1.1 `ahsan8pak-star` and `A.I.M` — one developer, two names

Both use `ahsan8pak@gmail.com`, so GitHub attributes all 791 commits to a single
profile. The `A.I.M` name is not a phase of the project; it is intermittent:

| Date | `A.I.M` commits | Context |
| --- | --- | --- |
| 4 Jun 2026 | 1 | the initial README timetable |
| 7 Jun 2026 | 2 | early learning commits |
| 27 Jun 2026 | 7 | the `tests/` scaffolding day |
| 1 Jul 2026 | 1 | the day the Copilot commits landed |
| 31 Aug 2026 | 2 | pre-docstring-sweep |
| 29–30 Sep 2026 | 3 | guard and scope-rule landing |
| 14 Oct 2026 | 1 | a `PROGRESSION.md` correction |

**Reading.** Two names for one person is a traceability cost with no offsetting
benefit. Every question about "who did this" has to be answered by email rather
than by name, and a contributor graph built on names alone miscounts the work.
It is also why §6 recommends a `.mailmap`.

### 1.2 `om001219` — the university account, and what it was used for

**42 commits in five consecutive days, 4–8 June 2026** — 11, 22, 3, 5 and 1 per
day. This is the opening week of the repository and it belongs to the CS1IP
coursework period.

**What it built:** the `.gitignore`, the `data/` folder for CSVs, the PostgreSQL
import, a C++ folder "as a potential backup for Python memory management", the
IDE JSON files, and the README timetable that was the project's only progress
record for its first fortnight.

**How it was used, stated plainly.** The account was taken to be somebody else's
on the GitHub side — the developer committed through it, and because ten of
those commits carried his personal email rather than the student one, they did
not register against the university profile at all. Commit `687fe8a` (6 Jun) is
the discovery, written at the time:

> *"updated further grammatical errors. Majority of the commits were from a
> student account and this led to an unfortunate issue of not seeing the commits
> accordingly in GitHub despite GitLab registering it properly"*

**Streak continuity.** Six of the 42 commits touch `README.md` and nothing else,
and their subjects are explicit about the purpose — *"Updated README.md to track
my personal project progress overall via using timetable"*, *"Updated the
Timetable structure to make it more neat"*, *"Continued the fixing of the
timetable design structure for a more cleaner look"*. The timetable was the
progress mechanism and the README edits kept the contribution record unbroken
across the five days.

**What this is, honestly.** Not a mistake of knowledge — a mistake of identity
hygiene, made at 20 commits an hour in week one, and diagnosed by the developer
himself within 48 hours. Git attributes on **email**, not on username. That is
the whole lesson, and it is worth more than it cost.

### 1.3 `ThenameisAiman` — GitHub Copilot, and the first real tests

**3 commits, all on 1 July 2026, 172 lines added.** These are the first
substantive tests in the repository: `tests/test_algorithms.py` (72 lines),
`tests/test_math_science.py` (66) and `tests/test_syntax.py` (34), against real
scripts under `python/`. The preceding `tests/` commit, `7048e45` on 27 June,
was A.I.M's own 15-line `test_sample.py` to prove the pipeline worked.

**How it was used.** The GitHub account `ThenameisAiman` is the developer's own,
and the commit messages are Copilot's — structured bullet bodies, a `feat:`
subject, and a forward-looking rationale that no hand-written commit in this
history would have produced:

> *"feat: add pytest test cases for math and science projects — testing
> arithmetic calculator / testing converters (celsius, weight, time) / testing
> geometry functions / **Week 6: ready for CS2DA module**"*

The three commits map to three Year 2 modules — CS2PP (weeks 4–5), CS2DA
(week 6) and CS2SE (weeks 10–12) — so the intent was to write the tests for the
concepts *before* the modules arrived. That is a sound instinct and it is the
reason testing appeared at all this early.

**What survived.** None of the three paths exist today. All three were renamed
within 18 days, twice under prefixes the conventions now forbid:
`file(pytest): rename test_algorithms.py -> (to )test_algorithms_data.py` (5 Jul)
and `rename(pytest): replaced "math" to "maths" to make it grammatically
correct under british english` (5 Jul); the syntax content was "transfer[red]"
on 19 Jul during the paradigm restructure. The area is very much alive —
`tests/test_imperative_programming/test_math_and_science_calculators.py` is
2,303 lines today — but it is a rewrite, not a continuation.

**The lesson.** The work was good and left no trace in the shape it arrived in.
Naming churn and a restructure absorbed it without anyone recording that the
first test coverage in the project had come from a tool rather than a person.

### 1.4 The AI co-author, and an escalation worth recording

AI use is not one event; it is a curve with four observable stages:

| Date | Stage | Evidence |
| --- | --- | --- |
| 22 Jun 2026 | incidental, for an assessed task | `940f466` "Made a Haiku poetry through a mad libs format and the poetry has been gotten through Gemini Google AI" |
| 10 Sep 2026 | engineering as default | `5a691a3` "feat(gui): create mp3 and wav GUI players with AI-assisted agentic engineering" |
| 15 Sep 2026 | governance | `bb7edc4` "docs: add AGENTS.md with project conventions and git workflow" |
| 17 Sep → 17 Oct | delegated execution | the ten mass refactors in §4, the guard suites, `agentic_models/` |

The pivot is 15 September: `AGENTS.md` turned assistance from habit into
something with written rules, and the commit volume in the following weeks
(W37: 66 commits, 571 file-touches; W39: 65 commits, 776 file-touches) reflects
an agent executing against a specification rather than a person typing.

---

## 2. WWW — What Went Well

### 2.1 The guard-before-drift habit

The repository's defining strength. `tests/test_scripts/` holds **290 tests**,
**14.7%** of the 1,970-test suite, and they assert things about the repository
rather than about any script:

| Guard | What it prevents |
| --- | --- |
| `test_repo_doc_numbers.py` | a stale figure in `AGENTS.md`, `PROGRESSION.md`, `NOTES.md` or the ranking guide |
| `test_data_files.py` | CRLF endings and a wrong trailing-newline count, repo-wide |
| `test_progression_chronology.py` | the session log going out of order |
| `test_repo_hygiene.py` | a CWD-relative artefact landing in the repo root |
| `test_model_rotation_docs.py` | the rotation docs disagreeing with each other |
| `test_ranking_docs.py` | the scoring sheet drifting from its guide |

The doc-number guards are the clearest case: a count stated in four documents is
four chances to go stale, and the guard catches every copy at once because each
is compared against the same live session.

### 2.2 Writing tests that prove a guard fails

Two `revert` commits exist, and **neither is a failure**:

- `eac4d50` — *"revert(AGENTS.md): remove probe line used to test the
  commit-scope guard"*
- `de0e45f` — *"revert(NOTES.md): remove the bite-check line"*

The branches make it plainer: `reproduce-commit-bug`,
`fix/commit-scope-probe-workaround`, `fix/allow-merge-commits-in-scope-guard`,
`fix/guards-should-read-git-not-disk`. A guard was written, deliberately
violated to watch it fail, and the violation was then reverted. That is the
correct way to validate a guard, and it is rare to find it done deliberately.

### 2.3 Documenting defects instead of quietly fixing them

Project rule 11 keeps coursework scripts broken *on purpose* where the breakage
is the point of the exercise, with a test pinning the defect and the docstring
naming it. Four defects have since been repaired — the `arithmetic_expressions.py`
`:.2f` on an error string that killed the results loop, the `login_status.py`
`IndexError` on empty input, `numbers.py`'s circular import, and
`fundamental_topins/main.py`'s bare `IndentationError` — each with the reasoning
recorded in `AGENTS.md` and `NOTES.md`.

The record is honest in both directions, including against the developer: the
`main.py` entry names it as **the first repair on that list made by the owner**
rather than by an assistant, and notes the cost — one line moved a measured
denominator, a coverage count, a benchmark FAIL count, a ranking score and three
documented figures.

### 2.4 Automated dependency maintenance

Ten Dependabot branches per remote (`numpy`, `matplotlib`, `coverage`, `pytest`,
`psycopg2`, `scikit-learn`, `ipykernel`) — none of which have ever been merged,
so they are proposals rather than churn. `requirements_sync.py` regenerates the
frozen manifests offline from the live .venv-wsl, and a guard keeps
`DEPENDENCIES.md` pinned to the compiled files.

### 2.5 Commit hygiene in the second half

Non-standard commit types stopped dead once the rule existed:

| Month | Non-standard types | Scope-less commits |
| --- | --- | --- |
| Jun 2026 | 6 | **123** |
| Jul 2026 | 2 | 7 |
| Aug 2026 | 5 | 6 |
| Sep 2026 | 1 | 4 |
| Oct 2026 | **0** | **2** |

Rule 12 landed on 29 September. The four months before it hold 140 scope-less
commits; the six weeks after hold two.

### 2.6 British English enforced in the record

Not a stylistic preference but a commit subject: `rename(pytest): replaced
"math" to "maths" to make it grammatically correct under british english` (5 Jul),
and the house style in `AGENTS.md` that mandates SPaG-clean British spelling for
every agent-written word.

---

## 3. What Went Wrong

### 3.1 Four months of convention drift before any rule existed

The 123 scope-less commits in June are not carelessness in the usual sense —
they are what happens when a repository has conventions but no enforcement. The
first 44 commits in a single week used subjects like `updated functions and moved
Tuples into the python folder`. The `file:` prefix appears **98 times** across
the history, and `AGENTS.md` now names it explicitly as the example of a prefix
that must not be used. There is also one `chrore:`, a typo of `chore:`.

**Cost:** roughly four months of history that a conventional-commit linter would
have rejected, and a rule that had to be written from a body of evidence rather
than followed from the start.

### 3.2 `Python/` → `python/`, and the 886-line README diff

Commit `4abe362` (11 Sep) is a case-only rename done as a deliberate two-hop
through `python_tmp` to defeat `core.ignorecase=true` — correct, and clever, and
necessary. It touched **193 files** and produced an **886-line diff in
`README.md`**, a documentation file the commit was not about.

The lesson is the one every case-insensitive filesystem eventually teaches: on
Windows, changing the *case* of a tracked path is not a rename git can see, so
it has to be engineered, and the collateral lands wherever the old spelling was
written down.

### 3.3 Ten mass mechanical commits, 82–261 files each

| Date | Commit | Files |
| --- | --- | --- |
| 17 Jul | `a4320f3` restructure python codebase into paradigm-based directories | 84 |
| 29 Jul | `cb6eafa` rename imperitive to imperative for spelling correction | 104 |
| 11 Sep | `4abe362` normalise `Python/` to `python/` | 193 |
| 14 Sep | `c55a1fe` rename lane folders and relocate misfit scripts | 95 |
| 18 Sep | `34c2b78` add exactly two trailing blank lines to remaining tracked files | 261 |
| 26 Sep | `91743f4` give all 161 modules a docstring | 147 |
| 30 Sep | `8e978d9` normalise every file to two trailing newlines and guard the doc | 230 |
| 30 Sep | `d36fd35` strip trailing whitespace repo-wide | 107 |
| 4 Oct | `988b9e1` split weeks into lecture/ and practical | 86 |
| 9 Oct | `c99610b` place the coursework from its respective git repo | 82 |

Every one was the right call. Every one was also unreviewable as a diff, and
each needed a full-suite run to be trustworthy. Three of the five largest landed
within twelve days of each other in late September — the docstring sweep, the
newline normalisation and the whitespace strip are one campaign wearing three
commits.

**The cost is not correctness, it is reviewability.** A 261-file whitespace
commit cannot be reviewed by reading it; it can only be verified by a guard.
That is why the byte-invariant guards in `test_data_files.py` matter more than
their line count suggests.

### 3.4 Identity fragmentation

Two names on one email, one name on two emails, and a GitHub identity used by a
tool. There is no `.mailmap`, no `CONTRIBUTORS`, no `AUTHORS`. Every question of
"who wrote this" currently requires the email column, and `git shortlog` reports
five identities where the truth is one person.

### 3.5 Assessed coursework is public by default, not by decision

`university_courseworks/` is **285 of 565 tracked files — 50.4%** of the
repository, the single largest area. `AGENTS.md` flags the risk itself:

> *"These are the submitted, marked artefacts, so they carry a different risk
> profile from the rest of the repo… behaviour that was correct on submission day
> should not be changed casually"*

The provenance is in the history: `0bd93ca` (24 Jul) — *"chore: download volume
java folder from university's own coursework website and placed it under
C:\Users\A.I.M\C.S\Data-Science-Project\Java-To-Python-Conversion\cs1ip\coursework1"*
— and `c99610b` (9 Oct) places coursework "from its respective git repo". So
material obtained from the module site and from another repository was committed
into a public portfolio without a recorded decision to make it public.

To be fair to the record: it contains no credentials and no personal data beyond
the identifiers below, and the PDFs are already gitignored. The criticism is
procedural — the decision was never *made*, it was inherited from the default.

### 3.6 Personal identifiers in a public repository

| Where | What |
| --- | --- |
| Git history, permanent | `om001219@student.reading.ac.uk` in 32 commits; `ahsan8pak@gmail.com` in 801 |
| `NOTES.md` | `om001219` / `student.reading.ac.uk` |
| `PROGRESSION.md` | same |
| `cs1op/coursework/README.md` | same |
| `cs1op/coursework/REPORT.md` | same |

A university identifier is named in `AGENTS.md`'s own privacy override as a
trigger that restricts model eligibility to the two zero-retention routes. It is
in the repository. Six Year 2 briefing files are also tracked, their filenames
carrying a cohort token (`~0022~20267`) — a cohort rather than a personal
number, so materially lower risk, and the Year 1 briefings are correctly
untracked.

### 3.7 The first tests left no trace

Covered in §1.3: 172 lines of good coverage from the project's first testing
tool, renamed twice inside a fortnight and superseded by a restructure, with
nothing in the documentation recording where the project's first test coverage
came from.

---

## 4. EBI — Evidence-Based Improvements

Each improvement below is paired with the evidence that demanded it. An
improvement without a recorded cause is a preference; this table is the audit.

| # | Improvement | Evidence that earned it | Landed |
| --- | --- | --- | --- |
| 1 | Commit scope is mandatory (rule 12) | 123 scope-less commits in June alone | 29 Sep 2026 |
| 2 | Conventional types only | 98 `file:` subjects, plus `doc:`, `pytest:`, `chrore:` | 29 Sep 2026 |
| 3 | Merge commits exempt from the scope rule, by parent count | the rule punished a correct merge and was ignored within the session | 29 Sep 2026 |
| 4 | Context-first reading (rule 14) | the tree guard read a stale path inside the folder it had just moved | 15 Sep 2026 |
| 5 | LF enforced by `.gitattributes` | persistent CRLF noise; `requirements_sync.py` re-emitted CRLF on Windows after being fixed once | 11 Sep 2026 |
| 6 | `*.wav binary` stated explicitly | the `text=auto` heuristic only worked by accident | 11 Oct 2026 |
| 7 | Doc-number guards | a figure lives in four documents at once | 13 Oct 2026 |
| 8 | Log chronology guard | the maintenance log drifted out of order with a row stranded below a blank line | Oct 2026 |
| 9 | Two trailing newlines, every tracked `.py` | two of the repo's own new files violated it in one session | 18–30 Sep 2026 |
| 10 | Coursework suites added to `testpaths` | an assessed module's 174 tests ran in no other suite; the reported total was true and also wrong | 14 Oct 2026 |
| 11 | GUI:TUI ratio guard | the thinner suite had come to own the larger surface | 14 Oct 2026 |
| 12 | Dead settings rows removed | a row that reports a value nothing reads looks like coverage | 14 Oct 2026 |
| 13 | Byte-width-aware audio handling | the clips are 8/16/24-bit; reading them as 16-bit turned them to noise | 17 Oct 2026 |
| 14 | Gated RMS instead of plain RMS | the quietest clip by plain RMS is 88% silence and peaks at −3.50 dBFS | 17 Oct 2026 |
| 15 | Model fit checked before acting (rule 14, `TASK_MODEL_GUIDE.md`) | five of eleven rotated models had left the live catalog | 14 Oct 2026 |

**The pattern worth naming.** Thirteen of the fifteen came from a guard failing,
a drift being observed, or a defect being found by running something — not from
a decision to improve. That is what a verification culture looks like from the
outside: the improvements are downstream of evidence because the evidence is
what arrives first.

**The counter-pattern.** Every one landed in the last eight weeks. The first four
months had no rules and therefore no improvements; the rules arrived once there
was enough history to generalise from. That is a defensible order, but it means
the first 123 commits are permanently unrecoverable and the lesson was paid for
in history rather than avoided.

---

## 5. A.I.M as a programmer: strengths and gaps

### 5.1 What the record shows is genuinely strong

1. **Verification before assertion.** 1,970 tests, 14.7% of them about the
   repository's own integrity. Commands are quoted so they can be re-run. This
   is the habit that separates the project from a portfolio of scripts.
2. **Defects as documentation.** Choosing to keep a broken script broken, with
   a test pinning it, is a more mature position than tidying it away — and it
   is enforced as a numbered rule rather than left to judgement.
3. **Naming things precisely.** `scripts/measure_ranking_signals.py` turns a
   disputed score into a disputed *formula*; `TASK_MODEL_GUIDE.md` records five
   models that have left the live catalog rather than quietly dropping them.
4. **Honest self-assessment.** The `main.py` entry records the owner's own
   repair and the cost it caused. The 11 Oct row records that the rotation was
   over-used on two models and says which.
5. **Learning in the open.** The commit log from week one — `Understood
   variables as a whole`, `Started Python from the beginning` — is a readable
   record of a syllabus being worked through, which is exactly what a learning
   portfolio should contain.

### 5.2 The gaps, each with the evidence

| Gap | Evidence | Cost |
| --- | --- | --- |
| **Identity hygiene** | 5 identities, 1 person, no `.mailmap` | §3.4 |
| **Convention adoption lag** | 140 violations before the rule, 2 after | 4 months of history |
| **Unreviewable commits** | 10 commits touching 82–261 files | review by verification only |
| **Single-maintainer bus factor** | 774 of 836 commits, one email, one person | the project cannot be handed over |
| **Decisions inherited, not made** | coursework public by default | §3.5 |
| **Guards growing faster than product** | 14.7% of the suite is meta | maintenance of the meta-layer is now the work |
| **Discovery not recorded** | Copilot's first tests vanish silently | §3.7 |
| **Provenance of external material unrecorded** | coursework downloaded from the module site, no note saying so | a reader cannot tell what is original work |

### 5.3 The gap that matters most

The project has become **self-referential**: 290 tests about the repository, a
file-scoring system scoring the developer's own scripts, a ranking guide, a
progression review, a notes file. That is a genuine and unusual strength, and it
is also the point at which the meta-work starts competing with the coursework
the portfolio exists to evidence.

The honest measure is in the weekly record. `python/` was the dominant area
through W38; `university_courseworks/` took over in W39 and has held the largest
share since. The project corrected itself. The remaining question — §6 — is
whether that coursework belongs in this repository at all.

---

## 6. The `university_courseworks/` question

**Recommendation: leave it in place for the rest of Semester 2, redact the four
tracked files, and move it to its own repository when CS1OP is finished
(~May 2027). Do not use a private branch.**

### 6.1 The evidence

- **285 of 565 tracked files — 50.4%** of the repository; the largest single area.
- It is **assessed, submitted work**, and `AGENTS.md` says so explicitly.
- Provenance: downloaded from the module site (`0bd93ca`) and from another
  repository (`c99610b`), with no recorded decision to publish it.
- Four tracked files carry the university identifier; history carries both email
  addresses permanently.
- PDFs are already gitignored, so a boundary already partly exists.

### 6.2 The three options

| Option | Fixes | Costs |
| --- | --- | --- |
| **A · Own repository** | Clean boundary; assessed work gets its own protection, its own README and its own history | Breaks the single-README story; extraction is a `git filter-repo` history rewrite, which under the repo's own rule 12 correction workflow means a branch and a pull request |
| **B · Private branch** | Fast; one clone, one history | **Achieves nothing on a public remote.** A branch on a public mirror is public. It would need a private remote too, which the four-mirror design complicates for no offsetting gain |
| **C · Status quo + redaction** ✅ | Removes the identifiers from tracked files at near-zero cost and risk | Assessed code stays public; 50.4% of the repo remains assessed material |

### 6.3 Why C now and A later

The coursework's value to the portfolio is the **translation discipline**, and
that is already demonstrated somewhere else: `agentic_models/TASK_MODEL_GUIDE.md`,
`ai_parity_cases.json` and the cross-language guards are all about *how the work
was done* rather than the work itself. Meanwhile the thing being protected —
assessed status — **expires**. In May 2027 the coursework is no longer
submitted work; it is a portfolio artefact, exactly like everything else here.

Splitting it now pays a permanent cost (a rewritten history, four mirrors to keep
level, a broken narrative) for a benefit that lasts eight more months. Redacting
the four files costs minutes. The `.mailmap` in §6.4 addresses the history
problem that neither option fixes.

### 6.4 If you do it later, do it this way

- [ ] `git filter-repo --path university_courseworks --invert-paths` on a **branch**, never on `main`.
- [ ] Force-push the branch with `--force-with-lease`, open a pull request, merge — the workflow in `AGENTS.md`.
- [ ] Land the same change on **all four mirrors** and confirm with `TestMirrorsAreLevel`, or it is a half-applied correction.
- [ ] Add a `.mailmap` **first**, in a separate ordinary commit, so the two histories keep their attribution.
- [ ] Keep a one-paragraph pointer in this repository to where the coursework now lives, so the README does not lie about the tree.

### 6.5 Immediate, cheap, and worth doing regardless

- [ ] Add `.mailmap` collapsing `A.I.M` and `ahsan8pak-star` to one identity, with `om001219` mapped as the university account it is.
- [ ] Decide, per file, whether the university identifier should stay in the four tracked documents. It is in `PROGRESSION.md` as history and in the coursework README as provenance — both defensible, but they should be *kept* deliberately rather than by omission.
- [ ] Add one sentence to `HISTORY_REVIEW.md` §3.5 recording the decision, so the next reader knows it was made.

---

## 7. Standing checklist for the next 22 weeks

**Identity**
- [ ] One git identity, one email, one GitHub handle. `.mailmap` present.
- [ ] Every commit carries `type(scope):` — the guard exists; use it.
- [ ] A tool that commits under your account (Copilot, an agent) is named in `PROGRESSION.md` when it first lands, so its contribution is attributable.

**Commits**
- [ ] No commit over ~40 files unless it is mechanical *and* a guard verifies it.
- [ ] Mass mechanical work is split so each commit is verifiable in one sitting.
- [ ] A `type(scope):` subject that says what changed, not what was done.

**Decisions**
- [ ] Anything entering the repository from outside it — module sites, other repositories, licensed material — gets one recorded line saying where it came from and why it may be published.
- [ ] Anything leaving the repository that is assessed, personal or licensed is a decision, not a default.

**Evidence**
- [ ] A new improvement is recorded against the evidence that produced it, as in §4.
- [ ] `PROGRESSION.md` gains a session row whenever the project moves (rule 13).
- [ ] A guard is validated by making it fail once before trusting it.

**Direction**
- [ ] The meta-layer (guards, rankings, notes) must not outgrow the coursework it documents. The 14.7% figure in §5.3 is the tripwire.

---

## 8. Reproducing every figure in this document

```sh
# the five identities and their commit counts
git log --format='%an <%ae>' | sort | uniq -c | sort -rn

# the co-author trailer shortlog does not attribute
git log --format='%B' | grep -i 'co-authored-by' | sort | uniq -c

# scope-less commits by month
git log --format='%ad|%s' --date=format:'%Y-%m' \
  | grep -vE '\|[a-z]+(\([^)]+\))?:' | cut -d'|' -f1 | sort | uniq -c

# commits by week
git log --format='%ad' --date=format:'%Y-W%W' | sort | uniq -c

# the ten mass commits, largest first
git log --format='@@%h|%ad|%s' --date=short --name-only   # then count files per commit

# the university account's five-day streak
git log --format='%ad|%an' --date=short --author=om001219 | cut -d'|' -f1 | sort | uniq -c

# the coursework README-only commits
git log --format='%h' --author=om001219   # then git show --name-only on each

# Copilot's three commits and whether the files survived
git log --author=ThenameisAiman --numstat --format='' | awk '{a+=$1} END{print a}'
git log --diff-filter=D --format='%ad %s' --date=short -- tests/test_algorithms.py

# area composition
git ls-files | awk -F/ '{print $1}' | sort | uniq -c | sort -rn

# the guard share of the suite
.venv-win/Scripts/python.exe -m pytest tests/test_scripts/ -q --collect-only | tail -2

# the courseware provenance
git log --diff-filter=A --format='%ad %s' --date=short -- 'Java-To-Python-Conversion/*'
```

`tests/test_scripts/test_history_review.py` guards this document: it fails if a
git identity appears that §1 does not name, if the five commit counts stop
summing to the stated total, or if the WWW and EBI sections go missing.

