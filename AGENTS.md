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
  `university_courseworks/year2/modules/YEAR2_SEMESTER1.md` and
  `university_courseworks/year2/modules/YEAR2_SEMESTER2.md`; keep them in sync when the
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
- **Multi-intent prompts are split before acting.** When one message bundles
  several different asks, name them explicitly and confirm the intended
  split before doing the work. If an intent is out of scope for OpenCode's
  role (for example, experimental Postgres work belongs to `postgresql/`),
  say so and defer rather than silently ignoring it.
- **Model-scoped review on multi-intent prompts:** when one of A.I.M's
  instructions bundles several intents, the model names each intent it has
  heard, picks the one it is scoped correctly for, and hands the remainder
  off using the model-scoped ranked fallback in §Free-tier model rotation,
  rather than blending them into one answer. If the split is genuinely
  unclear, the model asks one clarifying question before acting.
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

The rotation's own documents live in **`model_rotation/`** —
`MODEL_ALLOWANCE.md` is the file an agent reads *before* a switch, holding the
route ceilings, the locally measured token usage and the allowance A.I.M states
from the console. The tables below stay here, beside the rules that use them.

The twelve free OpenCode models rotated are: Big Pickle Free,
Space Bunny Free, Nemotron 3.5 Lightning Free, Nemotron 3 Ultra
Free, Ling 3.0 Flash Fin Free, Ling 3.1 Flash Free, Muse Spark 1.3
Contributor Free, MiMo-V2.6-Flash Free, MiMo-V2.5 Free, LongCat
2.5 Preview Free, Exo Free and Fledge Alpha Free. Rotation is
selected in the OpenCode console, not from inside a conversation — an
agent cannot switch its own model mid-session.

An agent cannot reliably self-identify which model is processing a
conversation — do not trust a claim of the form "I am model X" made by
the agent itself. The same discipline applies regardless of model: give a
Goal/Files/Constraints block, and treat any model's line-level claims as
candidates to verify against the repo rather than ground truth.

#### What each model is for

The rotation is a habit, not a strategy, unless each model has a job. All
twelve free models share one endpoint
(`https://opencode.ai/zen/v1/chat/completions`, provider
`@ai-sdk/openai-compatible`), so the choice is about context and strength,
not access. The limits below are OpenCode's own *route* limits, read from the
`opencode` provider entries in the `models.dev` registry
(`https://models.dev/api.json`, retrieved 7 October 2026). They are given as
exact token counts because the rounded versions are ambiguous — 262,144 is
256K, not 262K. The underlying model's full window is often larger, but the
free route is what this project actually gets.

| Model | Route context | Route output | Plan mode — use for | Build mode — use for |
| --- | --- | --- | --- | --- |
| Big Pickle Free | 200,000 | 32,000 | Quick code review, pattern matching | Focused code review, spot checks |
| Space Bunny Free | 1,048,576 | 524,288 | Long-document reading, research synthesis | Large refactors spanning many files |
| Nemotron 3.5 Lightning Free | 262,144 | 262,144 | Medium-complexity analysis | Test writing, verification |
| Nemotron 3 Ultra Free | 1,000,000 | 128,000 | Complex multi-file analysis, architecture | Complex debugging, multi-step reasoning |
| Ling 3.0 Flash Fin Free | 262,144 | 32,768 | Quick answers, simple lookups | Quick fixes, single-file edits |
| Ling 3.1 Flash Free | 262,144 | 32,768 | Quick answers, simple lookups | Quick fixes, single-file edits |
| Muse Spark 1.3 Contributor Free | 1,048,576 | 131,072 | Debugging, root-cause analysis | Architecture design, trade-off analysis |
| MiMo-V2.6-Flash Free | 200,000 | 32,000 | Code generation, boilerplate | Commit messages, documentation |
| MiMo-V2.5 Free | 200,000 | 32,000 | Code generation, boilerplate | Commit messages, documentation |
| LongCat 2.5 Preview Free | 1,000,000 | 131,072 | Long-context refactors, image-heavy review | Complex debugging, multi-step reasoning |
| Fledge Alpha Free | 1,048,576 | 131,072 | Long-context refactors, code generation, multi-file agents | Complex debugging, multi-step reasoning |
| Exo Free | 1,048,576 | 131,072 | Long-context refactors, code generation, multi-file agents | Complex debugging, multi-step reasoning |

Three rules of thumb follow from the table. A 256K model is the right tool for
a single-file edit — a 1M model costs more in tokens and latency for context
that is never used. A task should stay on one model across Plan and Build:
switching mid-task discards the analysis and pays for it twice. And the free
routes are not the models: MiMo-V2.6-Flash is served at 200,000 here and at
1,048,576 by every paid provider, so a context figure read off a model card
will not match what this project can actually use.

**The rotation has been over-used on two models.** A.I.M reached for Big
Pickle and Space Bunny by default, so both logged the most sessions without
earning the widest role. The correct reading of the table is that Big Pickle
is a *review* model, not a default builder: it is a 200K context model with
no independent identity, and the six models with genuinely large windows
(Nemotron 3 Ultra, Space Bunny, Muse Spark 1.3, LongCat 2.5, Fledge Alpha
and Exo Free) are the ones suited to the repo's long files. Ling and
Nemotron 3.5 Lightning are the right answer for the small, mechanical work
that filled Big Pickle's column.

**Privacy is not uniform, and this is a public repository.** OpenCode's
privacy section (<https://opencode.ai/docs/zen/>, checked 7 October 2026)
states a zero-retention default with named exceptions, so
which model is selected decides what leaves the machine. Space Bunny and
LongCat follow the zero-retention default. Big Pickle, Exo Free, Fledge
Alpha Free, MiMo-V2.6-Flash, MiMo-V2.5 Free and Ling 3.0 Flash Fin / Ling
3.1 Flash Free may use free-period data to improve the
model. The two Nemotron free routes are NVIDIA *trial* endpoints: use is
logged and NVIDIA's terms say not to submit personal or confidential data.
Muse Spark 1.3 Contributor Free trades heavily discounted pricing for
permission to use prompts and completions to train future Meta models. Fledge
Alpha Free is now listed in that table — checked 7 October 2026 — as a
free-period data exception, so it is documented but not zero-retention. No
credentials or `.env` values belong in a prompt on any of them (rule 6).

**LongCat 2.5 Preview Free** is one of two free models confirmed on the
zero-retention default rather than an exception, alongside Space Bunny, and it
is free "for a limited time" with no published end date, so budget for the
window closing without warning. **Fledge Alpha Free** (released 1 October
2026) now appears in OpenCode's published pricing and privacy tables — checked
7 October 2026 — as a free-period data exception with a 1,048,576 context and
131,072 output on the free route; that it is *documented* removes the
earlier "treat as undocumented" caveat, but it is still not zero-retention.
**Exo Free** and **Ling 3.1 Flash Free** joined the same route over the same
week, both free-period data exceptions, and **MiMo-V2.5 Free** is the
second-generation free MiMo route (200,000 / 32,000) alongside MiMo-V2.6;
none of the four carry a zero-retention claim, so the two-model privacy list
is unchanged.

Free-tier stability is uneven. `nemotron-3-ultra-free`, `big-pickle` and
`fledge-alpha-free` have all thrown upstream errors — the last of those
surfaced as `Upstream request failed: Endpoint is unavailable.` on 2 October
2026 — and the tier as a whole is prone to timeouts, so a failing model is a
reason to switch, not a reason to retry.

#### Tokens and usage share, as published

The pre-flight needs two numbers per model that are not the same thing: what
the route will accept, and how much of the platform's traffic the model
actually carries. Both are snapshots, dated, and both move. Route limits come
from the `models.dev` registry (`https://models.dev/api.json`, retrieved
7 October 2026); traffic is OpenCode's own published weekly figure
(<https://opencode.ai/data/>, week ending 7 October 2026), expressed as a
share of the 144.879T tokens across the eighteen models that page lists.

| Model | Route context | Route output | Weekly tokens | Share of listed traffic |
| --- | --- | --- | --- | --- |
| Space Bunny Free | 1,048,576 | 524,288 | 53T | 36.6% |
| Muse Spark 1.3 Contributor Free | 1,048,576 | 131,072 | 33T | 22.8% |
| MiMo-V2.6-Flash Free | 200,000 | 32,000 | 10T | 6.9% |
| Nemotron 3 Ultra Free | 1,000,000 | 128,000 | 3.6T | 2.5% |
| LongCat 2.5 Preview Free | 1,000,000 | 131,072 | 2.1T | 1.4% |
| Fledge Alpha Free | 1,048,576 | 131,072 | 1.8T | 1.2% |
| MiMo-V2.5 Free | 200,000 | 32,000 | 656B | 0.45% |
| Nemotron 3.5 Lightning Free | 262,144 | 262,144 | 412B | 0.28% |
| Ling 3.0 Flash Fin Free | 262,144 | 32,768 | below the published top-18 | unmeasured |
| Ling 3.1 Flash Free | 262,144 | 32,768 | below the published top-18 | unmeasured |
| Big Pickle Free | 200,000 | 32,000 | below the published top-18 | unmeasured |
| Exo Free | 1,048,576 | 131,072 | below the published top-18 | unmeasured |

Three readings of that table matter more than the numbers themselves:

- **The rotation's own models are 72.2% of listed traffic**, so the rotation is
  not a fringe habit — but that figure is dominated by one model. Space Bunny
  alone is 36.6%, and DeepSeek models that are *not* rotated account for a
  further 25.4%, which says the free tier's popular choices are wider than
  the twelve the rotation uses.
- **Popularity is not suitability.** Big Pickle is unmeasured on the same table
  where it has been the rotation's most-used model, because platform-wide
  traffic and this repo's needs are different questions.
- **Four entries have no measured share.** Ling 3.0 Flash Fin dropped out of
  the top-18 in the week just ended, Ling 3.1 Flash and Exo arrived after the
  cut, and Big Pickle never charted. "Unmeasured" is the honest cell; a
  percentage would be a guess.

#### Before each run: the pre-flight check

A model is selected before it starts, not after it fails. Three questions, in
order, and the third is the one that matters:

1. **Tokens.** Does the task fit the model's route limits — the context it can
   read and the output it can emit? A patch larger than the output ceiling is
   a truncated patch, so the ceiling decides before the task does. The ceilings
   for all twelve models are tabulated in
   `model_rotation/MODEL_ALLOWANCE.md`.
2. **Percentage left.** How much of the day's or month's allowance is
   unspent? **Read `model_rotation/MODEL_ALLOWANCE.md` first.** Token usage is
   measurable locally via `opencode stats --models` and `opencode db`, but the
   remaining *percentage* is not: it lives in the OpenCode console, which no
   agent can read, so A.I.M states it and the agent records it in that file's
   "Allowance remaining" table. **An empty or stale row means this question has
   not been answered** — ask rather than assume, and treat an agent that claims
   it passed without a recorded number as having failed it.
3. **Applicability.** Is this the model's job at all — purpose and context
   budget both? **Correctness and context drive the choice; speed is the last
   consideration.** A faster model that answers from a narrower window is the
   wrong model for a long refactor, however quick it returns a first draft.

If the answer to (3) is no, hand off rather than continue — the ranked table
below is the mechanism, and the privacy override below it outranks it.

#### Pros, cons, and main purpose of each model

The table above says when to *pick* a model. This one says what each model is
*good and bad at*, because knowing a model's ceiling is what lets a model admit
a task is wrong for it. Limits are the route limits above; privacy and
stability notes are the verified facts recorded earlier on this page.

| Model | Main purpose | Main assets | Weaknesses | Corrected applied use |
| --- | --- | --- | --- | --- |
| Big Pickle Free | Focused code review and spot checks | Reliable pattern matching; smallest window in the rotation, so a review pass carries little context | Tied-smallest output ceiling (32,000); no published vendor, so no provenance; free-period data may train the model; has thrown upstream errors | Review only. Corrected from "default builder", which was the over-use the rotation records |
| Space Bunny Free | Long-document reading and large multi-file refactors | Largest window (1,048,576) and by far the largest output budget (524,288) in the rotation, so a long patch cannot be truncated; zero-retention | 38% of all published OpenCode traffic, so it is the default trap — heavy use is not the same as suitability; zero-retention does not make a prompt private when everyone else is on the same route | Large multi-file refactors and long-document reading. Corrected from "default for most build tasks", which is what made it the second over-used model |
| Nemotron 3.5 Lightning Free | Test writing, verification, medium-complexity analysis | Its output ceiling equals its window (262,144), so it can emit a long test file or a long report in one turn without truncating | Mid-sized window, so a whole-repo read is out of reach; NVIDIA *trial* endpoint that logs use, so nothing personal or confidential; a logged endpoint is the wrong choice for a private prompt | Test writing and verification, and the mechanical work that filled Big Pickle's column. Corrected from "medium-complexity analysis", which understated its output ceiling |
| Nemotron 3 Ultra Free | Complex debugging, root-cause analysis, multi-step reasoning | 1,000,000 window for whole-repo reasoning, and built for hard multi-step problems | Smallest output ceiling of the large-window models (128,000, well below its own window), so a huge single response will not fit; NVIDIA *trial* endpoint that logs use; already known to throw upstream errors and time out | Whole-repo debugging and architecture. Corrected from "complex debugging", which did not name the output ceiling that disqualifies it for patch-writing |
| Ling 3.0 Flash Fin Free | Quick fixes, single-file edits, small lookups | Fast and cheap for small, well-specified edits; adequate reasoning support | One of the smallest output ceilings (32,768), and the smallest of the 256K models; named for a finance specialisation, so it is not the obvious first choice for general code reasoning; free-period data may train the model; dropped out of the published traffic ranking in the week ending 7 Oct 2026 | Single-file edits and small lookups. Corrected from a general "quick answers" default, which was never earned |
| Ling 3.1 Flash Free | Quick fixes, single-file edits, small lookups | Same 256K shape as Ling 3.0 Flash Fin, so the same cheap-fit profile for small well-specified edits | One of the smallest output ceilings (32,768); free-period data may train the model; no published traffic yet, so no evidence of scale | Single-file edits and small lookups. Corrected from the general "quick answers" default that was never earned |
| Muse Spark 1.3 Contributor Free | Root-cause debugging, architecture and trade-off analysis | Largest window in the rotation (1,048,576) alongside Space Bunny, and the model to reach for when the answer is "why does this break"; 21% of published traffic, so it is proven at scale | Explicitly trades prompts and completions for training future Meta models, which is the wrong trade on a public repo; 131,072 output ceiling, under a fifth of Space Bunny's; the least private of the twelve | Root-cause analysis and architecture, accepting the training trade. Corrected from "debugging" alone, which ignored what it costs privacy-wise |
| MiMo-V2.6-Flash Free | Boilerplate, documentation, commit messages | A 200,000 window is ample for a docs or commit-message task, and it is one of the cheapest routes to hand repetitive generation to | Tied-smallest window and output (200,000 / 32,000) in the rotation, despite the same release being 1,048,576 on paid routes; free-period data may train the model; weak choice for anything needing careful reasoning | Boilerplate, docs and commit messages only. Corrected from "code generation", which invited it onto work its 32,000 output ceiling cannot finish |
| MiMo-V2.5 Free | Boilerplate, documentation, commit messages | The second-generation MiMo free route, cheaper and older than V2.6; a 200,000 window is still ample for mechanical work | Same tied-smallest window and output (200,000 / 32,000) as V2.6; free-period data may train the model; no distinguishing strength over V2.6 for this repo's needs | Boilerplate, docs and commit messages only. Corrected from a separate niche to "either route does the same jar", so pick on availability, not loyalty |
| LongCat 2.5 Preview Free | Long-context refactors, image-heavy review, complex debugging | 1,000,000 window; zero-retention, so the safer large-window option; released 25 September 2026 | A "Preview" build released 25 September 2026 with no published end date to its free period, so both its behaviour and its availability can change without notice | Long-context work where retention matters. Corrected from "the only zero-retention model", which was wrong — Space Bunny is too |
| Fledge Alpha Free | Long-context refactors, code generation, multi-file agents | Free on the same endpoint; 1,048,576 context and 131,072 output on the free route; multimodal input (text and image); now documented in OpenCode's pricing and privacy tables, checked 7 October 2026 | Released 1 October 2026 and a free-period data exception, so not zero-retention; has already thrown `Endpoint is unavailable` | Long-context and multi-file agent work, provisional. Corrected from "undocumented" to "documented but not zero-retention" on the 7 October check |
| Exo Free | Long-context refactors, code generation, multi-file agents | Same 1,048,576 / 131,072 shape as Fledge on the same endpoint, so the same large refactor headroom | Free-period data may train the model; absent from the published traffic ranking, so no evidence of scale; no provenance published | Long-context and multi-file agent work, provisional. Corrected from "unproven" to "tracked but unmeasured" once it joined the published model list |

#### If the task is wrong for the model you are on: hand off, do not force it

**A model that judges the task to be outside its ability must say so and hand
the task off, rather than producing a mediocre answer that looks like an
answer.** This is the same rule as "treat a claim as a candidate, not ground
truth", applied to the model's own capability. The cost of a wrong-model answer
is a plausible patch that fails a guard three steps later, which is more
expensive here than an honest hand-off.

When declining, name **three other models in ranked order, best first**, and
give the reason in one line each. The ranking is the part that matters: a list
of eight names is noise, a ranked three is a decision A.I.M can act on without
researching.

An agent **cannot switch models mid-session** — selection happens in the
OpenCode console. So a hand-off is a *request*, not a switch, and the correct
form is to stop and say which model should take over next, not to keep working
in the same turn hoping the switch happens.

The hand-off table below is the default. Read it as a ranked fallback for
*fit*, then apply the privacy override that follows it.

| If you are on | Decline and recommend, best first |
| --- | --- |
| **Big Pickle Free** | 1. Ling 3.0 Flash Fin Free — small, fast, for a single-file edit. 2. Nemotron 3.5 Lightning Free — for test writing and verification. 3. Space Bunny Free — when the task genuinely needs a long document or a multi-file refactor |
| **Space Bunny Free** | 1. Ling 3.0 Flash Fin Free — when the task is one small edit and a 1M window is overkill. 2. Big Pickle Free — when all that is needed is a review pass, with no edits. 3. Nemotron 3 Ultra Free — when the problem is hard reasoning rather than volume |
| **Nemotron 3.5 Lightning Free** | 1. Nemotron 3 Ultra Free — for deeper reasoning on a wider window. 2. Space Bunny Free — when the work needs a window above 262,144. 3. Muse Spark 1.3 Contributor Free — for root-cause work that needs a wide window |
| **Nemotron 3 Ultra Free** | 1. Space Bunny Free — same 1M class, larger output ceiling, and zero-retention. 2. LongCat 2.5 Preview Free — the other 1M, zero-retention option. 3. Muse Spark 1.3 Contributor Free — when the tradeoff is reasoning depth and the prompt is not sensitive |
| **Ling 3.0 Flash Fin Free** | 1. Big Pickle Free — for a review pass rather than an edit. 2. Nemotron 3.5 Lightning Free — when the output must be long. 3. Nemotron 3 Ultra Free — when the task is real reasoning rather than a mechanical fix |
| **Ling 3.1 Flash Free** | 1. Big Pickle Free — for a review pass rather than an edit. 2. Nemotron 3.5 Lightning Free — when the output must be long. 3. Nemotron 3 Ultra Free — when the task is real reasoning rather than a mechanical fix |
| **Muse Spark 1.3 Contributor Free** | 1. Space Bunny Free — same 1M window, zero-retention, so the right default on a public repo. 2. LongCat 2.5 Preview Free — the other zero-retention 1M option. 3. Nemotron 3 Ultra Free — for reasoning depth, accepting a logged trial endpoint |
| **MiMo-V2.6-Flash Free** | 1. Ling 3.0 Flash Fin Free — another cheap route for small mechanical work. 2. Big Pickle Free — when a review, not a rewrite, is wanted. 3. Nemotron 3.5 Lightning Free — when the task needs care rather than boilerplate |
| **MiMo-V2.5 Free** | 1. MiMo-V2.6-Flash Free — the identical window with one more generation of polish. 2. Ling 3.0 Flash Fin Free — another cheap route for small mechanical work. 3. Nemotron 3.5 Lightning Free — when the task needs care rather than boilerplate |
| **LongCat 2.5 Preview Free** | 1. Space Bunny Free — the mature alternative in the same 1M, zero-retention class. 2. Nemotron 3 Ultra Free — for reasoning-heavy debugging. 3. Muse Spark 1.3 Contributor Free — for architecture work where the preview build is not trusted |
| **Fledge Alpha Free** | 1. Space Bunny Free — the mature 1M alternative. 2. LongCat 2.5 Preview Free — the zero-retention 1M option. 3. Muse Spark 1.3 Contributor Free — for reasoning depth, accepting the Meta training trade |
| **Exo Free** | 1. Fledge Alpha Free — the same 1,048,576 / 131,072 shape, so the same headroom from a model with a published privacy table. 2. Space Bunny Free — the mature zero-retention alternative. 3. LongCat 2.5 Preview Free — the other zero-retention 1M option |

**Privacy overrides the ranking.** If the prompt contains anything personal,
confidential, or credential-bearing — a `.env` value, an API key, an email
address, a university identifier — then only the two zero-retention models are
eligible, whatever the table above says: **Space Bunny Free** and **LongCat 2.5
Preview Free**. Every other route is out: the two Nemotrons are logged trial
endpoints, Muse Spark trains future Meta models on prompts, and Big Pickle,
Exo Free, Fledge Alpha Free, both MiMos and both Lings may train on
free-period data. In that case recommend Space Bunny first and LongCat
second, and say plainly that the reason is retention, not fit. Rule 6 already
forbids putting `.env` in a prompt on any model; this is the second line of
defence.

**A hand-off needs a reason and a check, not just a name.** The useful form is
one line of decline, the three ranked models, and what has *not* been done yet:

> This is a 1M-window refactor across `tests/` and `python/` and my output
> ceiling is 128,000, so I would truncate the patch. Handing off: 1. Space Bunny
> Free — same 1M, zero-retention, 524,288 output; 2. LongCat 2.5 Preview Free —
> the other 1M option; 3. Muse Spark 1.3 Contributor Free — if the depth matters
> more than retention. Nothing has been edited yet; the full suite is green as
> of the last commit.

Declining is not a reason to stop verifying. If the model hands off mid-task, it
still leaves the tree in a known state and still states which command proves
it — the hand-off is a change of model, not a surrender of the discipline that
makes the answer trustworthy.

#### Independent capability evidence (retrieved 8 October 2026)

The tables above are OpenCode's *route* figures. The figures below are
*capability* figures measured by other people, and they answer pre-flight
question three (applicability) with evidence rather than with a preference.
Three rules govern how they are read here, and they are the same three the
section 4.3 research is held to:

- **A benchmark is a benchmark, not a verdict.** Vendor-run rows (NVIDIA, Meta,
  Xiaomi, Meituan) are labelled as such. A vendor harness, a vendor grader and
  a different reasoning tier are three ways of producing a number that looks
  like a comparison without being one.
- **Index versions are not comparable with each other.** Artificial Analysis
  rescores its index when it revises it, so a figure from v4.1 and a figure
  from v4.2 are different scales. Each figure below names the snapshot it came
  from.
- **A stealth model has no index at all.** Big Pickle Free, Space Bunny Free
  and Fledge Alpha Free are anonymised, so no Artificial Analysis page exists
  for any of them. The only like-for-like comparison of the three is one
  reviewer's own battery, and it is labelled as such.

**Independently measured intelligence** (Artificial Analysis Intelligence Index,
by snapshot):

| Model | Index | Snapshot | Note |
| --- | --- | --- | --- |
| Muse Spark 1.3 Contributor Free | 62 (#6 of 636) | v4.1.1, `max` reasoning | The `max` tier was gated at launch; the shipping tier is `xhigh` |
| Muse Spark 1.3 Contributor Free | 52–53 | v4.2, `xhigh` / `max` | Honest figure for what actually ships; index v4.2 added private held-out weighting |
| Nemotron 3 Ultra Free | 47.7 (NVFP4) / 48.2 (BF16) | release-day, v4.1 | Leading US open-weights model at release |
| Nemotron 3 Ultra Free | 38 | v4.1.1 model page | Same model, later index build — the gap is the index, not the model |
| Ling 3.0 Flash Fin Free | 23 (22.6 on OpenRouter) | v4.3 | Above its own generalist parent (21); finance-specialised, not general-purpose |
| Big Pickle Free, Space Bunny Free, Fledge Alpha Free | none | — | Stealth models; no index exists, so no figure can honestly be given |

**Best measured by use case**, each from the sources named:

| Use case | Order of preference, on external evidence |
| --- | --- |
| Coding / software engineering | Muse Spark 1.3 (DeepSWE 75.4, Terminal-Bench 2.1 88.8, SWE-Atlas 59.4) → Fledge Alpha Free (Terminal-Bench 79, SciCode 52, SWE-Mini 75) → Space Bunny Free (SWE-Mini 75) → Nemotron 3 Ultra Free (SWE-Bench Verified 71.9) |
| Knowledge / factual accuracy | Big Pickle Free (Omniscience +43, HLE 38, 0 unanswered of 100) → Nemotron 3 Ultra Free (strong formal reasoning, 70–79% non-hallucination) → Muse Spark 1.3 |
| Agentic / multi-step tool use | Nemotron 3 Ultra Free (PinchBench 90, TauBench avg 70.9) → Space Bunny Free → Fledge Alpha Free → MiMo-V2.6-Flash Free (strong on routine automation, weak on recovery) |
| Long context (1M) | Muse Spark 1.3 (MRCR 98.5 / 98.1) → Nemotron 3 Ultra Free (RULER at 1M 94.7) → Space Bunny Free → LongCat 2.5 Preview Free (no published benchmarks) |
| Speed | Nemotron 3.5 Lightning Free (~670 tok/s, 3B active) → Nemotron 3 Ultra Free (400+ tok/s) → Space Bunny Free (~90–94 tok/s) → Fledge Alpha Free (~61 tok/s) |
| Finance-specific | Ling 3.0 Flash Fin Free, and it is the only one: Finance & Accounting Index 24, MIT weights, source-grounded retrieval |
| Multimodal input | Space Bunny Free and LongCat 2.5 Preview Free (text, image, video, zero-retention) → Muse Spark 1.3 → MiMo-V2.6-Flash Free (text, image, audio, video) → Exo Free (text, image only) |

**What this changes about the rotation.** Three corrections the tables above did
not carry, because none of them is an OpenCode figure:

- **Nemotron 3 Ultra Free is a stronger model than its route implies.** The
  free route caps it at 128,000 output against a 1,000,000 window, which reads
  as a weak model. On capability it is the second-strongest route here and the
  fastest large-window one, so the ceiling is the limit to plan around, not the
  ceiling to judge it by.
- **Fledge Alpha Free is a coding model, explicitly not a factual one.** Its
  Omniscience index is the only negative one measured (−5: 37 right, 42 wrong,
  67% hallucination). The rule that follows is specific — never let it state a
  fact, a version number, or a file path that has not been read.
- **Big Pickle Free is the knowledge model of the rotation, which the pick-a-model
  table never claimed.** Its corrected use is "review only"; the external
  evidence supports that and adds the reason (it answered every question in the
  battery, so it is the route to use when a question must be answered rather
  than escalated).

**One result worth stating plainly, because it is the counterweight to all of
the above.** A single independent review ran Big Pickle Free, Space Bunny Free
and Fledge Alpha Free through five benchmarks (254 items each) against two
*paid* references on the same gateway: **none of the three free stealth models
beat the cheapest paid reference on agent work.** DeepSeek V4.1 Flash solved
14/14 on Terminal-Bench and 17/20 on SWE-Mini, more than any free route, and
cost less than two of the three. Big Pickle was the only model — free or paid —
to beat both references on knowledge. The correct reading is therefore that the
free tier is good value and specifically useful, not that it is competitive with
a paid route on agentic work.

**Stability and provenance notes, from the same sources:**

- `nemotron-3-ultra-free`, `big-pickle` and `fledge-alpha-free` have all thrown
  upstream errors; a switch is the response, not a retry.
- Exo Free arrived on 6 October 2026 with no published benchmarks, frequent
  `429`s and endpoint dropouts. A fingerprinting tool reported a 99.4% match to
  Claude Opus 5.5, which is **not** provenance — a closed-set fingerprint of an
  uncatalogued model will always name its nearest neighbour.
- LongCat 2.5 Preview Free has **no published benchmark of any kind**. Its
  family's last published figure is LongCat-2.0's 59.5 on SWE-bench Pro, and
  that does not transfer. Meituan described the free window as "two weeks" on
  26 September, which puts its end around 10 October 2026.
- MiMo-V2.6-Flash Free replaced MiMo v2.5 in place on some routes; the old
  identifier is documented as working until 23 October 2026, so a route that
  "silently changed" is the vendor's substitution rather than a fault.
- One community report describes Big Pickle Free as switching behaviour
  mid-task. That is a single unverified report and is recorded as a
  possibility, not a fact.

**Sources, all retrieved 8 October 2026:**

- Artificial Analysis model pages and index articles — `artificialanalysis.ai`
  (Muse Spark 1.3, Nemotron 3 Ultra, Ling-3.0-flash-Fin, MiMo-V2.6).
- Fellipe Soares' independent stealth-model battery, 2 and 4 October 2026 —
  `fellipesoares.com.br` (the five-benchmark comparison and the 15-run
  bug-fix battery; the only like-for-like evidence for the three stealth
  routes).
- NVIDIA's release material and open-weights model card — `research.nvidia.com`
  and `huggingface.co/nvidia` (RULER, SWE-Bench Verified, throughput).
- Meta's Muse Spark 1.3 announcement with its own four-model scorecard, plus the
  independent Artificial Analysis rescore that followed it two days later.
- Meituan's LongCat platform changelog and model documentation.
- OpenRouter model pages for provider-side route behaviour, context limits and
  throughput.

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
   are `university_courseworks/year1/semester1/cs1ip/coursework1/*.py`). Two
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
      A fourth was repaired on 30 Sep 2026, this time by the owner rather
      than an assistant: `fundamental_topics/main.py` had carried a
      deliberate `IndentationError` since June — `def main():` with only a
      comment as its body, which is not a statement — and A.I.M added `pass`.
      It is now a working `__main__` guard example, it is measured by coverage
      like every other file, and the two tests that asserted it raised
      `SyntaxError` were rewritten to assert the opposite. Worth recording
      because it is the first repair on this list made by the owner, and
      because it showed the cost: one line of code moved a measured
      denominator, a coverage count, the benchmark FAIL count, the
      lowest-ranked file, the sheet's mean, and two figures in three documents.
      The guards caught every one, which is the first time they have all fired
      on a single change.
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
    The review is not a one-off write-up of the 117-day run that closed on
    29 September 2026; it is the running
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
  left here. Since 4 October 2026 this is **enforced server-side**, not merely
  stated, on the two public mirrors - see the table below.
- **Force-pushing a branch is allowed**, with `git push --force-with-lease`
  rather than `--force` so a stale local ref cannot clobber someone else's
  work. This is the correction path: when a pushed commit is wrong, branch
  from `main`, amend or re-commit there, force-push the branch, and open a
  pull request rather than editing `main` in place. `--force-with-lease`
  refuses when the remote has moved since the last fetch, which is exactly the
  case a blind `--force` would destroy. Branch protection targets `main` only,
  so this path is unaffected by any of the settings below.
- This holds on **all four mirrors**, backups included. A branch that is
  rewritten on the GitHub Project but not on the GitLab Backup is a half-fixed
  correction, so all four have to end up at the same commit. That is a rule
  about *content*, and it is enforced by verifying all four are level rather
  than by locking them all - see the subsection below, because the backups are
  deliberately left unlocked.

#### Server-side protection on `main` (added 4 October 2026)

The rule above is now backed by repository settings rather than discipline -
but **only on the two Project repositories, and the backups are left open on
purpose**. GitHub expresses this as a **ruleset** and GitLab as a **protected
branch**, so the wording differs; the effect is what matters.

| Repository | Protection | State on 4 Oct 2026 |
| --- | --- | --- |
| GitHub Project | ruleset `main-protection` | Active - bypass list empty, rules `deletion` + `non_fast_forward`, targets the default branch |
| GitLab Project | protected branch `main` | Protected - `allow_force_push: false`, *Allowed to push: Maintainers* |
| GitHub Backup | **none, deliberately** | Unprotected - see below |
| GitLab Backup | **none, deliberately** | Unprotected - see below |

**Why the Projects are Maintainers-only on GitLab.** GitLab's project roles run
Guest (10), Reporter (20), **Developer (30)**, **Maintainer (40)**, Owner (50).
Developer is the lowest role that can write code: it can clone, push to
branches, open merge requests and run CI, but not change settings, manage
members, or merge into a protected branch. The ladder therefore already splits
the work - Developers *produce* a change on a branch, Maintainers decide what
lands in the shared history - and the protection is only worth anything while
that split survives. *Allowed to push: Maintainers* keeps it: a Developer can
open a merge request against `main` but cannot land it, so one reviewed step
stays the only path onto the public face. "*Allowed to push: Developers +
Maintainers*" would let a Developer write straight to `main`, which protects it
from Guests and Reporters and from nobody who actually works on the repository.

Nothing changes for A.I.M today, since he is the sole owner and holds no other
role; the setting is behaviourally identical to its former level-30 value while
he works alone. It is set this way so the *intent* is held by the permission
system rather than by vigilance - adding a collaborator as a Developer later
then cannot silently hand them direct write access to `main`. This mirrors
GitHub, where the empty bypass list denies that route to every role including
the owner, and it matches the rule of thumb this repo already follows: adding a
collaborator needs no permission, but the rules should make an unreviewed push
to `main` impossible rather than merely discouraged.

**Why the asymmetry is the design and not a gap.** A backup exists to be
restorable. If the backups carried the same two rules, then the one moment
they are needed - `main` has been damaged and history has to be restored -
would be the moment both the Project rules and the backup rules refuse the
write. Protecting a backup removes the only property that makes it a backup.
The Projects are the public face, so that is where a random or accidental
force-push does the damage worth preventing; the backups are the recovery
target, so that is where free writing is the feature.

The cost is honest and worth naming: with the backups unlocked, a force-push
reaches them and is refused by the Projects, so the four **can** drift apart.
That is why the invariant is not enforced by locking everything. All four have
to end up at the same commit, and that is verified directly -
`TestMainBranchProtectionIsEnforced` checks the two Projects' settings over the
unauthenticated API and `TestMirrorsAreLevel` checks that all four resolve to
the same commit over SSH. The first says the public face is locked; the second
is what actually keeps the mirrors consistent now that the backups are not.

**Escape hatch.** When a rewrite of `main` is genuinely necessary: set the
GitHub ruleset `main-protection` to `Disabled`, tick "Allowed to force push" on
the GitLab protected branch, perform the rewrite **on all four mirrors**, then
restore both settings. The backups need no unlocking, so this is already a
partial-restoration risk rather than a four-way one. The settings change is
deliberate and leaves an audit-trail entry, which is the point.

One thing that **cannot** verify any of this: `git push --dry-run`. Protection
is enforced in the server's `receive-pack` hook, and `--dry-run` is documented
as "do everything except actually send the updates", so the hook is never
reached and a dry-run reports success on a protected and an unprotected branch
alike. Reading the settings, or making a real push, is the only way to know.
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
- 1651 passing tests, ~99% line coverage and 95% branch coverage (149 of the
  160 measured `python/` files at 100% lines, including both music-player
  GUIs; the 160 non-`__init__.py` files are the number a docstring sweep
  covers). The 160 counts files that carry at least one statement. The
  coverage table prints 182 rows because it also lists 22 files that have no
  statement - the empty `__init__.py` files - which report 100% without
  anything having run. `main.py` was until 30 Sep 2026 a deliberate
  `IndentationError` stub, excluded from the report because it could not be
  parsed; A.I.M added `pass` so it runs, and it is measured like every other
  file now. Branch coverage is
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
    the 183 files the harness walks do), `TIMEOUT` (ran past 2s), `FAIL` (raised
    a real error, currently none — `main.py` was the only one until A.I.M added
    `pass` on 30 Sep 2026, which makes it a `PASS`) and `ERROR` (the harness
    could not launch it, currently none). It benchmarks
  `sys.executable` rather than a bare `python`, so it measures the pinned venv
  interpreter, and derives `PROJECT_ROOT` from `__file__` rather than a baked
  absolute path.
- `FILE_RANKING_GUIDE.md` and `FILE_SCORES.md`: a 0-100 scoring guide and the
  results for all 160 non-`__init__` Python files under `python/`. Five
  criteria — Readability, Fixability, Robustness, Risk and Durability —
  weighted differently per tier: a **learning** script is judged on whether a
  reader can learn from it (Readability 35%), an **applied** project on whether
  a user can rely on it (Fixability and Robustness 30% each). The split is
  measured, not assumed: a file is Applied if it imports a third-party library,
  hardcodes a path, or exposes a class interface, which assigns 8 files to
  Applied and 152 to Learning. **Risk** is a separate criterion because "is it
  broken" and "what happens if it is" are different questions — a script that
  prints a wrong answer is worse than one that crashes. Every score is
  generated from measured signals by `scripts/measure_ranking_signals.py` and
  `scripts/score_ranking.py`, so a disputed score is a disputed formula rather
  than a disputed memory. Each entry carries a criterion-by-criterion
  breakdown and a written reason.
  Overall average: 84.6/100 (band B — Strong). Only 2 files score below
  70; the weakest are `strings.py` (64) and `variables.py` (69), both flat
  scripts with no function boundary — `strings.py` runs 321 lines, so a reader
  must hold the whole file at once and a test can only exercise it end to end.
  See `FILE_SCORES.md` for the full breakdown.
- Postgres is planned (`psycopg2` installed, `postgresql/sandbox/aim.sql`
  reserved) but not started.

## References

`PROGRESSION.md` is the narrative review of the run from 4 June to 29
September 2026, and of every session since:
the stages of learning and what evidences each, the corrections and mistakes
made by both A.I.M and the assistants, and how the AI collaboration was
arranged - including the point where Claude and Gemini were replaced by
OpenCode for terminal work, and the twelve-model free rotation. Its numeric
claims are test-guarded by `tests/test_scripts/test_repo_doc_numbers.py`, so a
stale figure there fails the suite like any other.

External study/project resources tracked in `NOTES.md`, plus the local module
briefing documents under `university_courseworks/` (tracked in git; the
accompanying `.pdf` / `.txt` copies are local-only).
`university_courseworks/university_modules/UNIVERSITY_MODULES.md`
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
| CS1AC | Applications of Computer Science (Year 1) | `university_courseworks/year1/modules/CS1AC~0022~20256.html` |
| CS1CA | Computer Systems Architecture (Year 1) | `university_courseworks/year1/modules/CS1CA~0022~20256.html` |
| CS1DB | Databases - group assessment (Year 1) | `university_courseworks/year1/modules/CS1DB~0022~20256.html` |
| CS1IP | Imperative Programming (Year 1) | `university_courseworks/year1/modules/CS1IP~0022~20256.html` |
| CS1MA | Mathematics and Computation (Year 1) | `university_courseworks/year1/modules/CS1MA~0022~20256.html` |
| CS1OP | Object-Oriented Programming (Year 1) | `university_courseworks/year1/modules/CS1OP~0022~20256.html` |
| CS2DA | Data Analytics (Year 2) | `university_courseworks/year2/modules/CS2DA~0022~20267.htm` |
| CS2AI | Artificial Intelligence (Year 2) | `university_courseworks/year2/modules/CS2AI~0022~20267.htm` |
| CS2ON | Operating Systems and Computer Networking (Year 2) | `university_courseworks/year2/modules/CS2ON~0022~20267.htm` |
| CS2PP | Python Programming (Year 2) | `university_courseworks/year2/modules/CS2PP~0022~20267.htm` |
| CS2SD | Software Systems Design (Year 2) | `university_courseworks/year2/modules/CS2SD~0022~20267.htm` |
| CS2SE | Software Engineering (Year 2) | `university_courseworks/year2/modules/CS2SE~0022~20267.htm` |
| CS3IP | Individual Project (Year 3) | `university_courseworks/year3/year3-briefing-2025.txt` |
| CS3AM | Artificial Intelligence and Machine Learning (Year 3) | `university_courseworks/year3/year3-briefing-2025.txt` |
| CS3 elective group | DV/VR (S1), BC/CS/IV/TM (S2) - Year 3 | `university_courseworks/year3/year3-briefing-2025.txt` |

### Assessed Coursework Scripts (marked work — handle with care)

| Module | Folder | What is in it |
| --- | --- | --- |
| CS1IP | `university_courseworks/year1/semester1/cs1ip/coursework1/` | The marked scripts: `average_grades.py`, `hello.py`, `ice_cream.py`, `seven_segment.py`, `volume.py`, each with a `.java` counterpart |
| CS1IP | `university_courseworks/year1/semester1/cs1ip/coursework2/` | `sort10.txt` and its sorting script |

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
> three years: see `university_courseworks/university_modules/UNIVERSITY_MODULES.md`. Official BSc Computer Science
> (UCAS G400) course pages: 2025/26, 2026/27 and 2027/28 entry (the 2025 page
> redirects to 2026/27; the 2027 page is not live yet).

