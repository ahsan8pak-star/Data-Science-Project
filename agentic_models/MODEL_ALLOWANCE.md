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
| Exo Free (`high`) | 1 | 0 | 0 | 0 | 9 Oct 2026 |

No local messages on record for Ling 3.1 Flash Free, MiMo-V2.6-Flash Free or
MiMo-V2.5 Free. Exo Free's single message carried zero tokens — a call that
produced nothing, matching its no-show pattern. One further Space Bunny message
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
| Exo Free | 1,048,576 | 0 | — (no real turn yet) |

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

- OpenCode Zen documentation — <https://opencode.ai/docs/zen/> (route
  availability and the privacy exceptions)
- `models.dev` registry — <https://models.dev/api.json> (route context and
  output ceilings, per provider)
- Local session database and CLI output — the token usage and largest-context
  tables (re-measured 10 October 2026) and the rate-limit log lines above
  (eleven failures, none since 1 October)

