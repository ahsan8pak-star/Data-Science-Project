# File Ranking Framework

**Purpose:** Rank every tracked Python file under `python/` on a 0-100 scale, and record the result per file in `FILE_SCORES.md` with a written reason for every score.

**Executor:** Any AI model with read/write access to this repo. Full context is in `AGENTS.md`, `NOTES.md`, `pyproject.toml`, and git history.

**How the marks are produced:** `scripts/measure_ranking_signals.py` measures what can be measured (coverage, exception handling, docstrings, comment style, hardcoded values, input handling, library use) into a JSON table. The scores are then assigned from that table, with judgement applied only where a number cannot decide: whether a defect is deliberate under rule 11, and whether a name is clear. This split matters — a score you cannot trace to a signal is a guess with a decimal point on it.

---

## The two tiers, and why they exist

A teaching script and an application are not the same kind of artefact, so they are not scored the same way. The distinction is not which folder a file sits in; `imperative_programming/` contains both a scratchpad and a spreadsheet pipeline. The distinction is **what the file is for**:

| Tier | What it is | How it is judged |
| --- | --- | --- |
| **Learning** | A script whose purpose is to demonstrate or drill a technique. It is read to be understood. | Can a reader learn the idea from it without being misled? |
| **Applied** | A program with a real interface — reads user input, drives a GUI, processes files. It is run to be used. | Does it survive contact with a real user who types nonsense? |

A file is **Applied** if it meets any of these, and **Learning** otherwise:

- it imports a third-party library (`numpy`, `pandas`, `sklearn`, `pygame`, `tkinter`, `openpyxl`, …), **or**
- it hardcodes a filesystem path, **or**
- it exposes a class-based interface to another module (`from mp3_tui_player import MP3AudioPlayer`).

That rule assigns **8 files to Applied and 152 to Learning**. The measurement is in `FILE_SCORES.md` under the *Tier* row of each file's table, so any single classification can be challenged without re-deriving the rest.

---

## Criteria

Five criteria. The two tiers weight them differently, because the questions are different.

| Criterion | Learning | Applied | What it measures |
| --- | --- | --- | --- |
| **Readability** | **35%** | 20% | Docstrings, comment quality, naming, structure, British English. *Comments count here* — they are a primary signal, not decoration. |
| **Fixability** | 25% | **30%** | Does it run? Are exceptions handled? Is a defect deliberate (rule 11) or a real bug? |
| **Robustness** | 15% | **30%** | Input validation, recovery from bad input, no silent data loss, graceful failure. |
| **Risk** | 15% | 10% | What is the cost if this is wrong? Silent wrong answers outrank crashes; crashes outrank nothing happening. |
| **Durability** | 10% | 10% | Survival across dependency upgrades, use of deprecated APIs, dependence on hardcoded environment specifics. |

Tier totals, which the suite checks against the sheet:

| Tier | Files | Readability | Fixability | Robustness | Risk | Durability |
| --- | --- | --- | --- | --- | --- | --- |
| **Learning** | 152 | 35% | 25% | 15% | 15% | 10% |
| **Applied** | 8 | 20% | 30% | 30% | 10% | 10% |

**Final score = Σ (criterion × tier weight), rounded half-up to an integer.**

### Why Risk is a separate criterion

Fixability asks *is it broken*. Risk asks *what happens if it is*. The two are not the same, and collapsing them hides the failures that matter most.

A crash is loud: the user sees it and nothing is silently wrong. A script that reports a wrong number is quiet and much worse — a portfolio reader running a calculator cannot tell a correct answer from a plausible one. So Risk is scored by **consequence, not by defect count**, and a file that misreports a result outranks one that refuses to start.

- **90–100** — Fails loudly, or is demonstrably correct. Crashes before doing damage, or cannot fail.
- **75–89** — Fails visibly on bad input; no path to a wrong answer.
- **60–74** — Can produce a wrong result on plausible input, but the user would have to be careless to get there.
- **40–59** — Silently wrong on common input. The failure mode is invisible to the user.
- **0–39** — Corrupts data, or reports a confident wrong answer in a normal path.

### Readability (35% Learning / 20% Applied)

Comments are scored as a first-class signal here, which is why this is the highest-weighted criterion for learning material: a teaching script whose comments are wrong is worse than one with none, because it teaches the error. Sub-signals, in order of weight:

- **Docstrings** — module docstring present, and function docstrings present. A missing function docstring costs more than a thin one.
- **Comment quality** — comments explain *why*, not *what*. A comment restating the next line is a penalty. Comment blocks that contradict the code are a heavy penalty, because a reader believes them.
- **Naming** — variables and functions named for what they hold (`total_price`, not `x1`).
- **Structure** — one idea per function, no unreachable code after a `return`.

### Fixability (25% Learning / 30% Applied)

- Does it run to completion? Cross-check against the benchmark status in `FILE_SCORES.md`.
- Are exceptions caught and handled, or merely caught and ignored?
- Is a known defect **deliberate** (rule 11) or a **real bug**? A deliberate defect is not penalised as heavily as a real one, because preserving it is the exercise — but it is still marked, and the docstring must name it.
- Unreachable statements after a `return` or `raise` are penalised. They are invisible to coverage by definition, since they never run.

### Robustness (15% Learning / 20% Applied)

- Is user input validated before it is used?
- What happens on empty input, a non-numeric answer, or `EOFError` from a closed stdin?
- Is data written to disk read back and verified?
- Does a failure leave partial or corrupt output?

### Durability (10% / 10%)

- Use of APIs that are deprecated or likely to be.
- Dependence on a hardcoded path, interpreter version, or console encoding.
- Does it survive being run from a different working directory?

---

## Scoring guide (0–100 per criterion)

| Score | Meaning |
| --- | --- |
| 90–100 | Exemplary. Would pass review unchanged. |
| 80–89 | Strong. Minor issues only. |
| 70–79 | Serviceable. Works, with real but non-blocking weaknesses. |
| 60–69 | Weak. Works only under conditions the user is likely to meet. |
| 40–59 | Poor. Likely to mislead or fail. |
| 0–39 | Dangerous. Misleads silently, or is a documented stub. |

Bands: **A** 90–100, **B** 80–89, **C** 70–79, **D** 60–69, **E** 0–59.

---

## Verifying a change to the sheet

Regenerate it, then run the suite. Target: the full suite green (1618 passed at the
time of writing) and 0 failed. The guards in
`tests/test_scripts/test_ranking_docs.py` recompute the arithmetic, the band
labels, the tier weights and the figures quoted in `AGENTS.md`, so a sheet that
disagrees with itself or with the docs fails rather than misleading quietly.

## Rules for filling the sheet

1. One entry per tracked non-`__init__.py` file under `python/`, no more and no fewer. The count is checked against `git ls-files`, not the filesystem, so an untracked practice file cannot move the total.
2. Every entry carries all five criterion scores, their weighted cells, a final, and a written comment.
3. The final must equal the sum of its own weighted cells, rounded half-up. A heading that disagrees with its table fails the suite.
4. The comment must name what is good, what is not, and why the score landed where it did. A comment that only restates the number is not a comment.
5. Deliberate defects are named as deliberate. Rule 11 keeps them in the code; the sheet is where the explanation lives.
6. Scores must be traceable to the measured signals. Where judgement is used instead, the comment says so.

---

## Worked example

### mp3_tui_player.py — **80/100** (B — Strong)

`python/advanced_projects/music_player/tui/mp3_tui_player.py` — Applied tier, because it imports `pygame` and is imported as a class by the GUI. The numbers below are copied from `FILE_SCORES.md` and the test suite checks they still match, so this example cannot drift into fiction:

| Criterion | Score | Weight | Weighted |
| --- | --- | --- | --- |
| Readability | 93 | 20% | 18.6 |
| Fixability | 96 | 30% | 28.8 |
| Robustness | 57 | 30% | 17.1 |
| Risk | 80 | 10% | 8.0 |
| Durability | 79 | 10% | 7.9 |
| **Final** | | | **80** |

Robustness is held at 57 while Fixability is 96, and the gap is the point of the two-tier scheme. The file runs cleanly and is fully covered, so nothing is broken. But it reads a path from the user and opens an audio file, and neither is checked: a missing directory or an unreadable `.wav` fails somewhere deeper, so the player works on the machine it was written on and not reliably on another. Under the Learning weighting — Readability at 35% — this file would have scored *higher* than it deserves, because its comments and structure are good. Under Applied, where Fixability and Robustness carry 30% each, the gap it cannot close is visible. That is what the tier is for.

