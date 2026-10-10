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
| Exo Free | 1,048,576 | 131,072 |
| Fledge Alpha Free | 1,048,576 | 131,072 |

## Token usage — measurable locally

This half **is** locally verifiable, so an agent reads it rather than asking.
Two commands, both run from the repo root in WSL:

```bash
# Per-model totals, most recent activity first
opencode stats --days 7 --models

# Per-model totals for this project only, from the session database
opencode db --format json "select json_extract(model,'\$.id') as model,
  count(*) as sessions, sum(tokens_input) as input_tokens,
  sum(tokens_output) as output_tokens, sum(tokens_cache_read) as cache_read
  from session where directory like '%Data-Science-Project%'
  group by 1 order by (input_tokens + cache_read) desc"
```

The database is `~/.local/share/opencode/opencode.db` (`opencode db path` prints
it). It is **read-only for this purpose** — open it with `mode=ro`, never
write to it, and never read `account`, `control_account` or `credential` rows,
which hold the console's access and refresh tokens. **Rule 6 still applies:
never put a token in a prompt, on any model.**

### Recorded usage

Snapshot taken 8 October 2026 for this project. `Cost` is $0.00 on every free
route, so cost cannot be used as a proxy for allowance consumed.

| Model | Sessions | Input | Output | Cache read | Last used |
| --- | --- | --- | --- | --- | --- |
| Space Bunny Free | 1 | 99.7M | 3.78M | 1.03B | 8 Oct 2026 |
| Ling 3.0 Flash Fin Free | 3 | 546,081 | 36,230 | 2,668,928 | 4 Oct 2026 |
| Big Pickle Free | 6 | 212,912 | 53,800 | — | 28 Sep 2026 |
| Fledge Alpha Free | 2 | 35,917 | 8,472 | 220,544 | 4 Oct 2026 |

Twenty further sessions in this project carry no model attribution in the
database, so they are excluded rather than guessed at.

**Read the table for what it is.** It shows which routes this project has
*used*, which is not the same as which routes are *good* — popularity is not
suitability, and `AGENTS.md` records why Space Bunny at 36.6% of listed
platform traffic is the default trap rather than the right answer.

## Allowance remaining — A.I.M only

**No agent can read this.** The remaining allowance lives in the OpenCode
console, not on this machine. What is observable locally is only the *failure*:
`Rate limit exceeded. Please try again later.` appears in
`~/.local/share/opencode/log/*.log`, timestamped, naming the model it hit. Six
such failures are recorded across three models in the last twelve days —
`big-pickle` (26 Sep, twice), `muse-spark-1.3-contributor-free` (26 Sep, twice),
`mimo-v2.6-flash-free` (26 Sep) and `longcat-2.5-preview-free` (1 Oct).

A rate-limit error is a **signal that the allowance ran out**, not a measure of
how much is left. It cannot be converted into a percentage.

| Checked on | Model | Context in use | % of context | Spent | Stated by | Note |
| --- | --- | --- | --- | --- | --- | --- |
| 8 Oct 2026 | Space Bunny Free | 242,366 | 23% | $0.00 | A.I.M | Read from the console. Verified against the session database: the largest assistant turn on this route carries 242,366 total tokens, which is 23.1% of the 1,048,576 context ceiling — so this is the *conversation's* context fill, not an allowance remaining. See the distinction below. |

### Two different "percentages", and they are not interchangeable

The figure above is **context consumed in this conversation** — 242,366 of
1,048,576 route context, which is 23.1%. It is verifiable here, and
independently confirmed against the session database.

**Allowance remaining is a different number.** It is the share of the daily or
monthly quota still unspent, it lives in the console, and nothing in this
repository records it. A conversation can sit at 23% of its context window and
still be one request away from the allowance limit, because context fill and
quota consumption are measured against different ceilings.

So the honest reading of the row above is: **question one answered (context fit
is fine at 23% of 1,048,576), question two not answered** (allowance remaining
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
- **It does not report context fill as allowance remaining.** The 23% above is
  the conversation's share of its own window, measured against a ceiling this
  file can see; the quota is a different ceiling and lives in the console.

## Sources

- OpenCode Zen documentation — <https://opencode.ai/docs/zen/> (route
  availability and the privacy exceptions)
- `models.dev` registry — <https://models.dev/api.json> (route context and
  output ceilings, per provider)
- Local session database and CLI output, measured 8 October 2026 — the token
  usage table and the rate-limit log lines above

