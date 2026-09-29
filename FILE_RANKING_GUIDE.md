# File Ranking Framework

**Purpose:** Rank every Python file under `python/` on a 0-100 scale across four criteria. Record results chunk-wise by subfolder in `FILE_SCORES.md`.

**Executor:** Any AI model with read/write access to this repo. Full context is in `AGENTS.md`, `NOTES.md`, `pyproject.toml`, and git history.

---

## Scoring Criteria

Each file is scored on four criteria, weighted as follows:

| Criterion | Weight | What It Measures |
|-----------|--------|------------------|
| **Fixability** | 40% | Does it run without crashing? Are exceptions handled? Is a defect deliberate (rule 11) or a real bug? |
| **Readability** | 25% | Variable naming, docstrings, comment quality, British English/SPaG, no Americanisms |
| **Durability** | 20% | Does it survive repo upgrades? Edge cases handled? Known breakage points? Does it survive `execution_time.py`? |
| **Robustness** | 15% | Input validation, error recovery, graceful degradation, no silent data corruption |

**Final score = sum of (criterion score x weight), rounded to integer.**

---

## Scoring Guide (0-100 per criterion)

### Fixability (40%)

| Score | Meaning |
|-------|---------|
| 90-100 | Runs clean; no crashes; all exceptions caught; no known defects |
| 70-89 | Minor defect that is documented and deliberate (rule 11); runs in tests but not standalone |
| 50-69 | A real bug exists; partially mitigated; crashes in some paths |
| 30-49 | Crashes frequently; multiple unhandled exceptions; core functionality broken |
| 0-29 | Cannot run at all; syntax error; import failure |

**Deductions:**
- Rule 11 documented defect (deliberate): start at 70, not lower — the defect IS the lesson
- Uncaught exception that crashes the script: -20 from baseline
- Import that shadows stdlib and breaks direct runs: -15
- Works under pytest but crashes standalone: -10 (pytest masks the issue)

### Readability (25%)

| Score | Meaning |
|-------|---------|
| 90-100 | Clear names, docstrings, British English, SPaG-clean, comments explain why |
| 70-89 | Mostly readable; minor SPaG issues; comments adequate |
| 50-69 | Readable but inconsistent; some Americanisms; sparse comments |
| 30-49 | Hard to follow; poor naming; no docstrings; comment noise |
| 0-29 | Unreadable; meaningless names; no documentation |

**Checks:**
- British English throughout (organise not organize, colour not color)
- Module docstring present and accurate
- Variable names are descriptive (`radius` not `r`, `exact_sum` not `x`)
- Comments explain WHY, not WHAT (per AGENTS.md house style)
- No Americanised spelling in comments/docstrings/print strings

### Durability (20%)

| Score | Meaning |
|-------|---------|
| 90-100 | Survives refactoring; no hardcoded paths; no CWD dependencies; handles edge cases |
| 70-89 | Mostly durable; minor CWD or path assumptions |
| 50-69 | Will break on some refactors; hardcoded values that should be parameters |
| 30-49 | Fragile; breaks on small changes; depends on specific environment |
| 0-29 | Brittle; breaks on any change; environment-specific hacks |

**Checks:**
- No hardcoded absolute paths
- No CWD-dependent file operations (unless documented per rules 3/4)
- Handles empty/zero/negative inputs gracefully
- No reliance on specific Python version internals
- Survives being imported as a module (has `__main__` guard or no side effects)

### Robustness (15%)

| Score | Meaning |
|-------|---------|
| 90-100 | Validates all input; recovers from errors; no silent failures |
| 70-89 | Validates most input; graceful degradation on edge cases |
| 50-69 | Some validation; crashes on unexpected input |
| 30-49 | No validation; crashes easily; silent data corruption possible |
| 0-29 | Dangerously unvalidated; corrupts data; crashes on any edge case |

**Checks:**
- Input validation (type, range, format)
- Exception handling (specific, not bare except)
- No silent failures (errors are logged or raised)
- No data corruption on error paths

---

## Execution Method

### Per Subfolder

1. List all `.py` files in the subfolder (excluding `__init__.py`)
2. For each file:
   - Read the source
   - Check its test file under `tests/`
   - Run it directly: `.venv/Scripts/python.exe <file>` (note crashes)
   - Run its tests: `.venv/Scripts/python.exe -m pytest tests/... -q`
   - Score each criterion
   - Calculate weighted final score
   - Write a sincere comment explaining the score
3. Append results to `FILE_SCORES.md`

### Direct Run Test

```bash
# From repo root, for each file:
timeout 10 .venv/Scripts/python.exe python/<subfolder>/<file>.py < /dev/null 2>&1 | tail -5
echo "exit: ${PIPESTATUS[0]}"
```

Record: exit code, whether it crashed, whether it produced expected output.

### Test Run

```bash
.venv/Scripts/python.exe -m pytest tests/<area>/<test_file>.py -q 2>&1 | tail -3
```

Record: passed/failed count, any errors.

---

## Pre-Verified Scores (by this session)

These files have been directly examined and fixed. Use as baseline. The
criteria and the resulting **Final** are the ones carried in
`FILE_SCORES.md`; the two documents are kept in step by
`tests/test_scripts/test_ranking_docs.py`, which fails if they drift apart.

| File | Fixability | Readability | Durability | Robustness | **Final** | Notes |
|------|-----------|-------------|------------|------------|-----------|-------|
| `fundamental_topics/numbers.py` | 90 | 75 | 85 | 70 | **82** | Fixed: sys.path de-shadowing. Minor: adds os/sys to teaching file |
| `math_and_science_calculators/arithmetic_expressions.py` | 90 | 70 | 85 | 70 | **81** | Fixed: .2f guard. EXPERSSIONS typo pinned by test (left) |
| `fundamental_topics/area_of_circle.py` | 70 | 80 | 85 | 75 | **76** | Left defective per rule 11 (asymmetry demo); adding guard breaks 8 tests |
| `fundamental_topics/main.py` | 90 | 75 | 85 | 80 | **84** | Intentional IndentationError; pinned by test; documented teaching stub |
| `fundamental_topics/login_status.py` | 70 | 65 | 60 | 60 | **65** | Predicates at 16/19 dead by design (rule 11); IndexError fixed |
| `interactive_games/rock_paper_scissors.py` | 80 | 75 | 70 | 65 | **75** | isdigit() always-truthy pinned (rule 11); restructured into functions |

The rounding convention is half away from zero, so an exact `.5` weighted sum
goes up. It has to be stated rather than left implicit, because the two
natural alternatives disagree: banker's rounding sends 74.5 down, and
truncation sends every 69.5 down instead of up.

---

## Ranking Categories

Group final scores into bands:

| Band | Range | Label |
|------|-------|-------|
| A | 90-100 | Exemplary — runs clean, well-documented, durable |
| B | 80-89 | Strong — minor issues, mostly clean |
| C | 70-79 | Serviceable — documented defects or minor fragility |
| D | 60-69 | Weak — real bugs, fragile, or hard to read |
| E | 50-59 | Poor — multiple issues, likely to break |
| F | 0-49 | Critical — cannot run, crashes, or unreadable |

---

## Sincere Comments Guide

For each file, write 2-4 sentences covering:
1. **What works** — be specific, not generic
2. **What doesn't** — name the exact issue
3. **Why the score** — connect the evidence to the number
4. **What would fix it** — actionable suggestion

Avoid: "good file", "needs work", "looks fine". Be specific.

---

## Subfolder Processing Order

Process in this order (alphabetical by subfolder):

1. `python/advanced_projects/`
2. `python/functional_programming/`
3. `python/imperative_programming/`
4. `python/object_oriented_programming/`

Within each subfolder, process sub-subfolders alphabetically.

---

## Output Format in FILE_SCORES.md

```markdown
## python/<subfolder>/<sub-subfolder>

### filename.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 85 | 20% | 17.0 |
| Robustness | 70 | 15% | 10.5 |
| **Final** | | | **81** |

**Comment:** What works, what doesn't, why scored here, what would fix it.

---

```

---

## Key Rules to Remember (from AGENTS.md)

- **Rule 11:** Documented defects stay defective unless crash/false result. Rule 11 defects: `isdigit()` in `rock_paper_scissors.py`, predicates in `login_status.py`, no `__main__` guard in `area_of_circle.py`.
- **Rule 2:** No comments unless asked. Don't strip existing comments.
- **Rule 9:** Entry points are content-named, not `def main()` (except `fundamental_topics/main.py`).
- **Rule 10:** LF line endings enforced by `.gitattributes`.
- **Rule 8:** Any file type may be committed; never commit `.env`.

---

## Verification Commands

After ranking each subfolder:

```bash
# Confirm no regressions
.venv/Scripts/python.exe -m pytest -q 2>&1 | tail -3

# Confirm benchmark status
.venv/Scripts/python.exe scripts/execution_time.py --all 2>&1 | grep -E "FAIL|ERROR" | grep -v "raised a real error\|harness could not"

# Confirm repo hygiene
.venv/Scripts/python.exe -m pytest tests/test_scripts/test_repo_hygiene.py -q 2>&1 | tail -3
```

Target: 1350 passed, 0 failed. Only `main.py` should be FAIL in benchmark.
