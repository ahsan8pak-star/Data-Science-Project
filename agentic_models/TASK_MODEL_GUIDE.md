# TASK_MODEL_GUIDE.md — which model for which task, and at what effort

**Read this before starting a task, not after a failure.** It answers the
question the rotation tables in `AGENTS.md` only imply: given a *task*, which
model do you pick, and at which reasoning-effort level.

Companion to `AGENTS.md` (the rotation, ceilings and pre-flight) and
`MODEL_ALLOWANCE.md` (the supply side). This file is the demand side: the task
is the input, the model and its effort level are the output.

Retrieved and cross-checked 14 October 2026.

## 1. The context-first rule (mirrors AGENTS.md rule 14)

Before executing any task, the model reads the relevant context — the target
file(s), the applicable rule, and the `Verify:` command — to confirm it is the
right model for *this* task. If the model can do the task but not optimally
(wrong level, wrong window, logged route), it says so and asks A.I.M whether
to proceed, rather than forcing a mediocre patch. This applies at every
capability level: a 1M model is not automatically the right model, and a 200K
model is not automatically the wrong one.

The three pre-flight questions in `AGENTS.md` still gate every run. This rule
adds a fourth check that is easy to skip: *fit for this specific task, at this
specific effort level.*

## 2. Effort levels, low to high (the `/variants` list)

Each model exposes reasoning-effort **variants**. Higher effort means more
thinking before the answer: better on hard reasoning, slower and dearer on
trivial work. The levels below are the model's own declared set, ordered low to
high. A model with no selectable variant runs at a fixed reasoning effort.

| Model | Effort levels (low to high) | Notes |
| --- | --- | --- |
| Space Bunny Free | `low` → `medium` → `high` → `xhigh` → `max` | Widest range in the rotation; `max` is the default trap. |
| Muse Spark 1.3 Contributor Free | `minimal` → `low` → `medium` → `high` → `xhigh` | `xhigh` is the shipping tier; `max` was gated at launch. |
| LongCat 2.5 Preview Free | `low` → `medium` → `high` | No `max`; unscored on capability. |
| Step 5 Preview Free | `low` → `medium` → `high` | Not in the repo's rotation; listed for completeness. |
| Big Pickle Free | *(none — fixed)* | No selectable variant; runs at its own reasoning. |
| Nemotron 3.5 Lightning Free | *(none — fixed)* | Output ceiling equals its window (262,144). |
| Nemotron 3 Ultra Free | *(none — fixed)* | 128K output ceiling caps long patches. |
| MiMo-V2.6-Flash Free | *(none — fixed)* | 200K / 32K; mechanical text only. |
| Fledge Alpha Free | `low` → `high` → `max` | Not in the current Zen catalog (see §6). |
| Ling 3.0 Flash Fin Free | `high` (observed) | Not in the current Zen catalog (see §6). |
| Ling 3.1 Flash Free | `high` (observed) | Not in the current Zen catalog (see §6). |
| MiMo-V2.5 Free | *(none — fixed)* | Not in the current Zen catalog (see §6). |

**How to read a level.** `low`/`minimal` is for mechanical, well-specified work
where thinking is overhead. `high` is the default for most tasks. `xhigh`/`max`
is for hard reasoning, root-cause debugging and architecture — and is the
level that turns a fast model into a slow one. Pick the lowest level that
solves the task; the pre-flight's "speed is the last consideration" cuts both
ways.

## 3. Task → model matrix

For each task: **primary model (fallback) · effort · in-party cite · third-party
cite · pros / cons · authentic user note.**

| # | Task | Primary (fallback) | Effort | In-party cite | Third-party cite | Pros | Cons | Authentic user note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Factual Q&A / knowledge accuracy** | Big Pickle (Nemotron 3 Ultra) | fixed | AGENTS.md "Knowledge: Big Pickle (Omniscience +43, HLE 38, 0 unanswered)" | [Fellipe Soares battery](https://fellipesoares.com.br/en/opencode-stealth-models-benchmarks/) | Answered every question; top knowledge of five models tested | 200K window; served 202% of ceiling; verbose; sometimes ignores AGENTS.md | "Big Pickle knows the most… answered every question" (Soares); Reddit: mixed, deleted files once |
| 2 | **Code review / spot checks** | Big Pickle | fixed | AGENTS.md pick-a-model "Quick code review, pattern matching" | [Tenzler blog](https://daniel-tenzler.de/blog/opencodeexperiences/) | Reliable pattern matching; stays on plan | Edits fail / invent code 50–70K in; partly reads 400–500-line files | "Useful for reading a codebase, writing docs… without subagents it falls apart" |
| 3 | **Long-document reading / research synthesis** | Space Bunny (LongCat 2.5 Preview · Muse Spark) | `high`–`max` | AGENTS.md "Large multi-file refactors and long-document reading" | [buildfastwithai Space Bunny](https://blog.buildfastwithai.com/space-bunny-review); [orcarouter LongCat](https://www.orcarouter.ai/blog/longcat-2-5) | 1M context; fast (~90 tok/s); zero-retention on the OpenCode route | Space Bunny loses the thread ~100K in; LongCat unscored | "Extremely fast… but loses the thread starting ~100K" (Reddit); LongCat: "no benchmark… the state of it" |
| 4 | **Test writing / verification** | Nemotron 3.5 Lightning | fixed | AGENTS.md "Test writing, verification" | [Thoughtworks Nemotron 3.5](https://www.thoughtworks.com/en-us/insights/blog/generative-ai/putting-nvidia-nemotron-3-5-lightning-test) | Output = window (262K); fast (~670 tok/s); emits a long test file in one turn | NVIDIA trial endpoint **logs use**; mid window | "Fastest task completion… 1.5–2x faster generation" (Thoughtworks) |
| 5 | **Complex debugging / root-cause** | Muse Spark 1.3 Contributor (Nemotron 3 Ultra) | `high`–`xhigh` | AGENTS.md "Root-cause debugging, architecture" | [chat-o.chat Muse](https://chat-o.chat/blog/muse-spark-1-3-opencode) | Stays on task across tool calls; 1M window; strong on layered tracing | Contributor route **trains on your data**; weaker language skills | "Genuinely interesting coding model… stayed oriented across layers" (chat-o); "around Opus 4.8" (Aetos) |
| 6 | **Whole-repo architecture / multi-file refactor** | Space Bunny (Muse Spark · LongCat) | `high`–`max` | AGENTS.md "Large multi-file refactors" | [pgupai Space Bunny review](https://www.pgupai.com/guides/space-bunny-code-review-github-actions); [Fellipe Fledge](https://fellipesoares.com.br/en/fledge-alpha-stealth-model/) | 1M window + 524K output; Fledge fixed 15/15 bugs | Space Bunny forgets; Fledge one tool/turn, cache hiccups | "High effort found 6.5/27 issues, 251s median" (pgupai); "15 out of 15, fastest" (Fellipe) |
| 7 | **Quick fixes / single-file edits / lookups** | Ling 3.0 Flash Fin (Ling 3.1 Flash) | `high` | AGENTS.md "Single-file edits and small lookups" | *(thin — finance-specialised, dropped from top-18)* | Fast, cheap; fits a single-file edit | 32K output; finance specialisation, not general reasoning | "Above its own generalist parent (21)" (AA index) |
| 8 | **Boilerplate / docs / commit messages** | MiMo-V2.6-Flash (MiMo-V2.5) | fixed | AGENTS.md "Boilerplate, docs and commit messages only" | *(thin)* | Cheap; ample for mechanical text | 32K output; weak on careful reasoning | In-party only — treat as cheap/default, not proven |
| 9 | **Agentic / multi-step tool use** | Nemotron 3 Ultra (Muse Spark · Space Bunny) | fixed / `high` | AGENTS.md "Agentic / multi-step tool use" | [Fellipe battery](https://fellipesoares.com.br/en/opencode-stealth-models-benchmarks/) | PinchBench 90, TauBench avg 70.9; 1M window | 128K output caps long patches; NVIDIA trial logs use | "Nemotron 3 Ultra (PinchBench 90)" (AGENTS.md) |
| 10 | **Long-context retrieval** | Space Bunny (Muse Spark · LongCat) | `high`–`max` | AGENTS.md "Long context (1M)" | [buildfastwithai](https://blog.buildfastwithai.com/space-bunny-review) | Recovered three hidden codes from ~200K input | Not a full benchmark | "Retrieved all three in correct order" |
| 11 | **Private / confidential work** | Space Bunny (LongCat 2.5 Preview) | `high`–`max` | AGENTS.md privacy override | [OpenCode Zen docs](https://opencode.ai/docs/zen/) | Only two **zero-retention** routes | Everything else may train on data | "The privacy list is unchanged: Space Bunny, LongCat" (AGENTS.md) |

## 4. Choosing the effort level for a task

| Task shape | Effort | Why |
| --- | --- | --- |
| Mechanical edit, lookup, boilerplate | `low` / `minimal` / fixed | Thinking is overhead; the answer is known. |
| Default coding, test writing, review | `high` | The sweet spot for most work. |
| Hard reasoning, root-cause, architecture | `xhigh` / `max` | The task needs depth, not speed. |
| Long-context retrieval | `high`–`max` | Retrieval improves with effort, but the window is the real constraint. |

When in doubt, start at `high`. Drop to `low` if the task is trivial; raise to
`xhigh`/`max` only when `high` has failed. Never spend `max` on a task `low`
would solve.

## 5. Privacy override

If the prompt contains anything personal, confidential or credential-bearing —
a `.env` value, an API key, an email address, a university identifier — only
the two zero-retention routes are eligible: **Space Bunny Free** and **LongCat
2.5 Preview Free**. Every other route is out: the two Nemotrons are logged
trial endpoints, Muse Spark trains future Meta models on prompts, and Big
Pickle, Fledge Alpha, both MiMos and both Lings may train on free-period data.
Rule 6 already forbids putting `.env` in a prompt on any model.

## 6. Catalog status — confirm via `/models`

The Zen catalog is live and changes. As of 14 October 2026 it lists 85 models,
of which the free set is: Big Pickle, Cat Jam Free, LongCat 2.5 Preview Free,
MiMo-V2.6-Flash Free, Muse Spark 1.3 Contributor Free, Nemotron 3.5 Lightning
Free, Space Bunny Free, Step 5 Preview Free and Jev 1.13 Free.

**Five of the eleven models in the repo's rotation are not in the current Zen
free list:** `nemotron-3-ultra-free`, `fledge-alpha-free`,
`ling-3.0-flash-fin-free`, `ling-3.1-flash-free` and `mimo-v2.5-free`. They
appear in `AGENTS.md` and `MODEL_ALLOWANCE.md` and in the recorded usage
table, so the rotation docs have drifted from the live catalog. Confirm what
your console actually offers with `/models` before relying on this guide, and
treat a missing model as a reason to pick the next-best row in §3, not as a
reason to force a removed route.

## 7. Sources

**In-party (this repository):**
- `agentic_models/AGENTS.md` — rotation tables, pick-a-model, pros/cons, hand-off, capability evidence, privacy.
- `agentic_models/MODEL_ALLOWANCE.md` — route ceilings, recorded usage, largest-context table, allowance.

**Third-party (retrieved 14 October 2026):**
- [OpenCode Zen docs](https://opencode.ai/docs/zen/) — free-model list, privacy exceptions, pricing.
- [OpenCode models docs](https://opencode.ai/docs/models/) — variants, effort levels, custom variants.
- [Fellipe Soares — OpenCode stealth models battery](https://fellipesoares.com.br/en/opencode-stealth-models-benchmarks/) — Big Pickle / Space Bunny / Fledge Alpha vs two paid references.
- [Fellipe Soares — Fledge Alpha](https://fellipesoares.com.br/en/fledge-alpha-stealth-model/) — 15/15 bug-fix battery, cost per task.
- [buildfastwithai — Space Bunny review](https://blog.buildfastwithai.com/space-bunny-review) — 1M context, speed, retrieval test.
- [pgupai — Space Bunny code review](https://www.pgupai.com/guides/space-bunny-code-review-github-actions) — effort levels, issue-finding yield.
- [orcarouter — LongCat 2.5](https://www.orcarouter.ai/blog/longcat-2-5) — what is documented and what is absent.
- [chat-o.chat — Muse Spark 1.3](https://chat-o.chat/blog/muse-spark-1-3-opencode) — multi-file debugging, Contributor trade.
- [Thoughtworks — Nemotron 3.5 Lightning](https://www.thoughtworks.com/en-us/insights/blog/generative-ai/putting-nvidia-nemotron-3-5-lightning-test) — speed, customisation.
- [Tenzler — Big Pickle experiences](https://daniel-tenzler.de/blog/opencodeexperiences/) — real-project use, context failure point.
- [AIScroll — Muse Spark 1.3](https://aiscroll.io/article/reviews/muse-spark-13-contributor/) — best-value coding worker, Contributor terms.
- [stealthmodels.com — Fledge Alpha](https://stealthmodels.com/fledge-alpha/) — speed, router hypothesis.
- [Reddit r/opencodeCLI](https://www.reddit.com/r/opencodeCLI/comments/1qr1jm6/anyone_tried_the_big_pickle_model_on_opencode/) and [r/opencode](https://www.reddit.com/r/opencode/comments/1wqi4a8/my_honest_opinion_about_spacebunny/) — authentic user reports.
