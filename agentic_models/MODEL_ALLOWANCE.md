# MODEL_ALLOWANCE.md — the supply side of the pre-flight

**Read this file before switching models, and before starting a long run.**
It answers questions 1 and 2 of the pre-flight in
`agentic_models/AGENTS.md`. Question 3
(applicability) is answered from the tables in `agentic_models/AGENTS.md`, not
from here.

Companion to the rotation tables in `agentic_models/AGENTS.md`; both files live
in `agentic_models/`, and this file is the one an
agent opens first.

## The rule

Before any model is changed, or a long run is started, confirm all three:

1. **Token fit.** Does the task fit the target model's route ceilings — the
   context it can read and the output it can emit? A patch larger than the
   output ceiling is a truncated patch.
2. **Percentage left.** How much of the allowance is unspent? **Read the
   "Allowance remaining" table below. If it is stale, empty, or says
   "unknown", the check has NOT passed — stop and ask A.I.M.** An agent cannot
   read the console, so a blank cell is a failed check, never a silent pass.
3. **Applicability.** Is this the model's job at all? See the pre-flight and
   the pick-a-model table in `AGENTS.md`. Correctness and context drive the
   choice; speed is the last consideration.

If (1) or (3) fails, hand off — the ranked-three table in `AGENTS.md` is the
mechanism. If (2) is unknown or low, ask A.I_M before burning the remainder on
a long run.

The context-first rule (AGENTS.md rule 14) applies on top of this, in both Plan
and Build mode: read the task context before acting, and ask when the fit is
suboptimal. The task-to-model mapping and effort levels live in
`TASK_MODEL_GUIDE.md`.

## Route ceilings

OpenCode's free route limits, from the `models.dev` registry entries for the
`opencode` provider (`https://models.dev/api.json`, retrieved 8 October 2026).
These are **route** limits, not the model's full capability — the same MiMo
release is 1,048,576 everywhere else and 200,000 on this route.

| Model | Route context | Route output |
| --- | --- | --- |
| Big Pickle Free | 200,000 | 32,000 |
| Space Bunny Free | 1,048,576 | 524,288 |
| Nemotron 3.5 Lightning Free | 262,144 | 262,144 |
| Nemotron 3 Ultra Free | 1,000,000 | 128,000 |
| Ling 3.0 Flash Fin Free | 262,144 | 32,768 |
| Ling 3.1 Flash Free | 262,144 | 32,768 |
| Muse Spark 1.3 Contributor Free | 1,048,576 | 131,072 |
| MiMo-V2.6-Flash Free | 200,000 | 32,000 |
| MiMo-V2.5 Free | 200,000 | 32,000 |
| LongCat 2.5 Preview Free | 1,000,000 | 131,072 |
| Fledge Alpha Free | 1,048,576 | 131,072 |
| Beam Free | 1,048,576 | 131,072 |

### Keeping this table current

The catalog moves. On 17 October 2026 the registry listed **44 zero-cost
models** on the `opencode` provider, against the twelve rotated here, and it
also listed **Exo Free** — still present, still 1,048,576 / 131,072 — which
this project removed from its rotation on 11 October 2026. So the removal was
a decision about *this* rotation, not an upstream discontinuation, and the two
are worth keeping distinct when the history is read.

Three sources, three different questions:

| Source | Answers | Not authoritative for |
| --- | --- | --- |
| `/models` in the OpenCode console | What this console can actually select | Route ceilings for a model you cannot see |
| `models.dev` registry | Route context and output per provider | Whether the route is served to you today |
| `AGENTS.md` §Free-tier model rotation | What this project chooses to rotate | Anything current |

Refresh the table and its date together, from the registry, and say which
figure is a measurement and which is an observation. Nothing here is fetched
by the test suite: a guard that reaches the network fails for reasons that
have nothing to do with the repository. The protection is the offline kind —
the stated ceilings are pinned against this recorded snapshot, so both are
refreshed together and neither drifts alone.

## Token usage — measurable locally

This half **is** locally verifiable, so an agent reads it rather than asking.
Two commands, both run from the repo root in WSL:

```bash
# Per-model totals, most recent activity first
opencode stats --days 7 --models

# Per-model totals for this project, from the session database
opencode db --format json "select json_extract(m.data,'$.modelID') as model,
  json_extract(m.data,'$.variant') as variant, count(*) as messages,
  sum(json_extract(m.data,'\$.tokens.input')) as input_tokens,
  sum(json_extract(m.data,'\$.tokens.output')) as output_tokens,
  sum(json_extract(m.data,'\$.tokens.cache.read')) as cache_read,
  max(json_extract(m.data,'\$.tokens.input')
    + coalesce(json_extract(m.data,'\$.tokens.cache.read'),0)) as max_context
  from message m join session s on s.id = m.session_id
  where json_extract(m.data,'\$.role') = 'assistant'
  and s.directory like '%Data-Science-Project%'
  group by 1, 2 order by (input_tokens + cache_read) desc"
```

The database is `~/.local/share/opencode/opencode.db` (`opencode db path` prints
it). It is **read-only for this purpose** — open it with `mode=ro`, never
write to it, and never read `account`, `control_account` or `credential` rows,
which hold the console's access and refresh tokens. **Rule 6 still applies:
never put a token in a prompt, on any model.**

### Recorded usage

Snapshot measured 10 October 2026: every assistant message in this project's
sessions (31 sessions), grouped by model and variant. `Cost` is $0.00 on every
free route, so cost cannot be used as a proxy for allowance consumed. The
database is live and these totals move as sessions run; the query above
reproduces them.

| Model | Messages | Input | Output | Cache read | Last used |
| --- | --- | --- | --- | --- | --- |
| Space Bunny Free (`max`) | 2,499 | 46.5M | 747.5K | 557.5M | 10 Oct 2026 |
| Big Pickle Free | 4,100 | 34.7M | 3.2M | 296.4M | 8 Oct 2026 |
| LongCat 2.5 Preview Free (`high`) | 418 | 5.3M | 115.3K | 144.2M | 9 Oct 2026 |
| Fledge Alpha Free (`max`) | 327 | 12.4M | 242.4K | 81.8M | 6 Oct 2026 |
| Ling 3.0 Flash Fin Free (`high`) | 83 | 1.5M | 50.6K | 6.5M | 26 Sep 2026 |
| Nemotron 3.5 Lightning Free | 61 | 3.3M | 19.2K | 3.9M | 9 Oct 2026 |
| Nemotron 3 Ultra Free | 22 | 424.6K | 5.5K | 2.7M | 26 Sep 2026 |
| Muse Spark 1.3 Contributor Free (`xhigh`) | 15 | 286.2K | 3.3K | 747.6K | 10 Oct 2026 |

No local messages on record for Ling 3.1 Flash Free, MiMo-V2.6-Flash Free or
MiMo-V2.5 Free. One further Space Bunny message
outside any variant carries zero tokens likewise.

### Largest context seen vs the route ceiling

`Max context` is input plus cache-read on the largest single assistant turn per
model — the closest local measure of how much window a run has actually needed.
The share column divides it by the published route ceiling above.

| Model | Route context | Largest context seen | Share of route ceiling |
| --- | --- | --- | --- |
| Space Bunny Free | 1,048,576 | 504.3K | 48% |
| Big Pickle Free | 200,000 | 403.6K | 202% — over the published ceiling |
| LongCat 2.5 Preview Free | 1,000,000 | 546.5K | 55% |
| Fledge Alpha Free | 1,048,576 | 520.0K | 50% |
| Ling 3.0 Flash Fin Free | 262,144 | 180.0K | 69% |
| Nemotron 3.5 Lightning Free | 262,144 | 357.2K | 136% — over the published ceiling |
| Nemotron 3 Ultra Free | 1,000,000 | 148.6K | 15% |
| Muse Spark 1.3 Contributor Free | 1,048,576 | 218.0K | 21% |

Two routes have served turns **larger** than their published ceilings, verified
turn by turn (Big Pickle's largest carries 403,621 input tokens with zero
cache-read; Nemotron 3.5 Lightning's 357,250 the same way, with further turns
above 262,144 behind it). So the ceilings table is the documented limit and
this table is what was actually served. Pre-flight question one is answered
against the ceiling — the conservative figure — and the two over-ceiling rows
are flagged here rather than silently trusted, because a limit the route does
not enforce is a limit that can start being enforced without warning.

**Read the table for what it is.** It shows which routes this project has
*used*, which is not the same as which routes are *good* — popularity is not
suitability, and `AGENTS.md` records why Space Bunny at 36.6% of listed
platform traffic is the default trap rather than the right answer.

## Allowance remaining — A.I.M only

**No agent can read this.** The remaining allowance lives in the OpenCode
console, not on this machine. What is observable locally is only the *failure*:
`Rate limit exceeded. Please try again later.` appears in
`~/.local/share/opencode/log/*.log`, timestamped, naming the model it hit. Eleven
such failures are recorded across four models — `big-pickle` six times on
26 September, `muse-spark-1.3-contributor-free` three times the same day,
`mimo-v2.6-flash-free` once the same day, and `longcat-2.5-preview-free` once on
1 October — and none since.

A rate-limit error is a **signal that the allowance ran out**, not a measure of
how much is left. It cannot be converted into a percentage.

| Checked on | Model | Context in use | % of context | Spent | Stated by | Note |
| --- | --- | --- | --- | --- | --- | --- |
| 8 Oct 2026 | Space Bunny Free | 242,366 | 23% | $0.00 | A.I.M | Read from the console. Verified against the session database: the largest assistant turn on this route then carried 242,366 total tokens, which is 23.1% of the 1,048,576 context ceiling — so this is the *conversation's* context fill, not an allowance remaining. See the distinction below. |
| 9 Oct 2026 | Space Bunny Free | 259,540 | 25% | $0.00 | A.I.M | Read from the console. 259,540 of 1,048,576 is 24.8% — the same conversation further in. Context fill again, not allowance remaining. |

### Two different "percentages", and they are not interchangeable

The latest figure above is **context consumed in this conversation** — 259,540
of 1,048,576 route context, which is 24.8%. It is verifiable here, and the
8 October row is kept as history showing the same conversation's earlier fill.

**Allowance remaining is a different number.** It is the share of the daily or
monthly quota still unspent, it lives in the console, and nothing in this
repository records it. A conversation can sit at 23% of its context window and
still be one request away from the allowance limit, because context fill and
quota consumption are measured against different ceilings.

So the honest reading of the rows above is: **question one answered (context fit
is fine at 25% of 1,048,576), question two not answered** (allowance remaining
unknown, $0.00 spent confirms this is a free route but says nothing about how
much of it is left). If A.I.M reads a remaining-percentage figure off the
console, it goes in the next table rather than in the `% of context` column.

| Checked on | Model run | Remaining % | Stated by | Note |
| --- | --- | --- | --- | --- |
| *(one row per check — empty means question two is unanswered)* | | | | |

**How to fill this in.** Before a long run or a model switch, A.I.M reads the
percentage off the console and states it. The agent records the row *before*
starting, so the next agent inherits a real answer instead of a blank.

**The empty-table case is the rule that matters.** With this table empty — as it
is now — question two of the pre-flight **fails**, and the correct behaviour on
any long run is to ask A.I.M for the remaining percentage rather than assume it
is fine. This mirrors `AGENTS.md`: a guard that silently passes is worse than no
guard, because it reads as coverage.

## What this file deliberately does not do

- **It does not predict or estimate a percentage.** A guess in this table would
  be a number with a table around it, which is exactly what
  `test_model_rotation_docs.py` forbids for the traffic shares.
- **It does not rank models.** Capability ranking lives in `AGENTS.md`
  (external evidence) and route limits live in the table above; this file only
  answers "can this route carry the task, and is there allowance left".
- **It does not read the console, or any credential store.** The `account`,
  `control_account` and `credential` tables in `opencode.db` hold live tokens
  and are never read here.
- **It does not report context fill as allowance remaining.** The 25% above is
  the conversation's share of its own window, measured against a ceiling this
  file can see; the quota is a different ceiling and lives in the console.

## Sources

- OpenCode Zen documentation — <https://opencode.ai/v2/docs/zen/> (route
  availability and the privacy exceptions)
- `models.dev` registry — <https://models.dev/api.json> (route context and
  output ceilings, per provider; last read 17 October 2026 for Beam Free and
  the 44-model free-set count)
- Local session database and CLI output — the token usage and largest-context
  tables (re-measured 10 October 2026) and the rate-limit log lines above
  (eleven failures, none since 1 October)

## Agentic LLM usage evaluation (11 Oct 2026)

### Over-concentration on certain files

The clearest concentration signal is the AI-authored-fix marker. `git grep`
finds `[AI-authored fix]` in 17 files, 46 markers total:

| File | AI-authored markers |
| --- | ---: |
| `tests/test_scripts/test_repo_doc_numbers.py` | 12 |
| `tests/test_imperative_programming/test_math_and_science_calculators.py` | 7 |
| `tests/test_object_oriented_programming/test_syntax.py` | 5 |
| `tests/test_imperative_programming/test_fundamentals.py` | 5 |
| `tests/test_university_courseworks/test_structure.py` | 4 |

`test_repo_doc_numbers.py` is the highest-AI-touched file — and the reason is
structural, not sloth. It is a doc-number guard: it recomputes module counts,
passing counts, coverage caps and the tier arithmetic so `AGENTS.md`,
`NOTES.md` and `FILE_SCORES.md` cannot drift from the tree silently. Its own
docstring records a live correction where the tree moved from 161 to 160
modules, leaving the assertion failing and tempting a maintainer to hard-code
around it. That is precisely the work that should be AI-heavy: cross-file
numeric reconciliation is mechanical, verifiable, and high-volume — exactly
the profile `AGENTS.md` assigns to cheap/fast models.

### Model usage vs suitability

Recorded usage — 31 sessions, live database:

| Model | Messages | Input | Largest turn | % of route ceiling |
| --- | ---: | ---: | ---: | ---: |
| Space Bunny Free | 2,499 | 46.5M | 504.3K | 48% |
| Big Pickle Free | 4,100 | 34.7M | 403.6K | 202% (over) |
| LongCat 2.5 | 418 | 5.3M | 546.5K | 55% |
| Fledge Alpha | 327 | 12.4M | 520.0K | 50% |
| Ling 3.0 Flash Fin | 83 | 1.5M | 180.0K | 69% |
| Nemotron 3.5 Lightning | 61 | 3.3M | 357.2K | 136% (over) |

**The over-use finding.** `AGENTS.md` states it plainly: "The rotation has
been over-used on two models. A.I.M reached for Big Pickle and Space Bunny by
default." Big Pickle logged the most messages (4,100) on the smallest window
(200K), and served a 403.6K turn — 202% of its published ceiling. Nemotron
3.5 Lightning likewise served a 357.2K turn at 136%. Meanwhile Ling (the
correct model for "the small, mechanical work that filled Big Pickle's
column") got 83 messages, and the one route since removed upstream managed a
single no-op turn before it went.

The repo's own correction is the right reading: Big Pickle is a review model,
not a default builder; Ling and Nemotron 3.5 are the right answer for
single-file mechanical edits. Popularity does not equal suitability.

### How context and prompts buy function, per file category

| File category | Model class | Prompt features that pay off | Why |
| --- | --- | --- | --- |
| Long single-owner docs (AGENTS.md 1,119 lines, NOTES.md 1,098, git_repo_progress/PROGRESSION.md 1,029, FILE_SCORES.md 2,931) | 1M-window models: Space Bunny, Fledge Alpha, LongCat, Muse Spark | "Long-document reading, research synthesis"; full detail | Four docs total ~6,200 lines of cross-linked state. A 256K model truncates mid-document and misses cross-references. |
| Numeric/doc-drift guards (test_repo_doc_numbers.py, test_ranking_docs.py, test_model_rotation_docs.py) | Cheap/fast models: Ling, Nemotron 3.5, MiMo | `Files: tests/test_scripts/` + `Verify: full suite` | Mechanical reconciliation; the model that writes it needs to run the suite, not hold the whole repo. |
| Big teaching/test lanes (test_math_and_science_calculators.py 305, test_syntax_programs.py 271) | Nemotron 3 Ultra / LongCat; probe-writing also fits Nemotron 3.5 | `Goal` + `Files:` + `Constraints: owner lane byte-frozen` | High case-count but each is small; the constraint block is load-bearing because rule 1/11 freeze the owner's files. |
| GUI/front-end (CS1OP tkinter screens) | Space Bunny / Fledge | multi-file `Files:` block, `Verify: -q` | Cross-file GUI refactor (the Java-to-Python translation used exactly this shape). |
| Docs / commit messages (README.md, REPORT.md, session logs) | MiMo-V2.6/2.5 | short `Goal` only | Cheap, fast, no repo context needed. |

### What is working

- Role assignment exists and is documented. The 11-model table with explicit
  Plan/Build use-cases is unusually disciplined.
- Privacy is tracked per-route (zero-retention defaults vs free-period
  training routes; Nemotron as NVIDIA trial endpoints) — a real
  portfolio-quality concern handled properly.
- Over-use is self-diagnosed. The repo records its own Big Pickle/Space
  Bunny default-trap rather than hiding it. The two "percentages" (context
  fill vs allowance remaining) are kept distinct, which is a subtle and
  correct epistemics.

### What needs adjusting

1. Route by task shape, not habit. Doc reading goes to 1M models; single-file
   edits to Ling/Nemotron 3.5; verification to whatever already holds the tree.
   Stop defaulting to Big Pickle/Space Bunny.
2. Do not switch models mid-task. `AGENTS.md`: "switching mid-task discards
   the analysis and pays for it twice." Keep Plan and Build on one model.
3. Treat the free routes as the route, not the model. MiMo is 200K here, 1M
   paid — a context figure from a model card will mislead pre-flight.
4. The free routes are not private uniformly, and this is a public repo —
   choose zero-retention routes (Space Bunny, LongCat) for anything personal.

