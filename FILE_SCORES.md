# File Rankings

Ranked 0-100 across Fixability (40%), Readability (25%), Durability (20%), Robustness (15%).
See `FILE_RANKING_GUIDE.md` for the full scoring guide.

---

## python/advanced_projects/

### machine_learning/data_outliers/data_outlier.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 60 | 40% | 24.0 |
| Readability | 85 | 25% | 21.3 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **70** |

**Comment:** Clean scikit-learn transformer implementing IQR-based outlier capping. No `__main__` guard or entry point — it is a library module, so running it directly produces no output (exit 124 timeout, no crash). `transform()` mutates nothing and returns a clipped copy, which is good. Robustness deduction: `fit()` assumes `X` is a DataFrame (calls `.quantile()`); passing a numpy array raises `AttributeError` rather than a helpful message. The `factor` parameter is validated nowhere — a negative factor silently inverts the bounds. No input validation on `transform()` either.

---

### music_player/gui/mp3_gui_player.py — **79/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 70 | 15% | 10.5 |
| **Final** | | | **79** |

**Comment:** Well-structured tkinter GUI wrapping the TUI audio engine. Every widget creation is annotated with inline comments explaining what each line does — verbose but helpful for a teaching repo. The `sys.path.insert(0, _tui_dir)` at line 18 is a code smell (mutates global import path) but is necessary for the sibling import. Robustness: the GUI has no way to handle a missing pygame install gracefully at import time — it would crash with an unhandled `ModuleNotFoundError` when the TUI module is imported. Durability: the hardcoded `r"C:\Users\A.I.M\C.S\MP3"` path in the TUI sibling means the GUI is Windows-specific.

---

### music_player/gui/wav_gui_player.py — **79/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 70 | 15% | 10.5 |
| **Final** | | | **79** |

**Comment:** Identical structure to `mp3_gui_player.py` — the pair is worth comparing side by side as the docstring says. Same `sys.path` mutation, same inline comment density, same pygame import risk. The only difference is `.wav` vs `.mp3` filtering and the WAVAudioPlayer class. Both GUIs are frozen at a fixed 500x450 window, which will clip on small screens. The `match cmd` statement in the TUI versions requires Python 3.10+.

---

### music_player/tui/mp3_tui_player.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 85 | 25% | 21.3 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **81** |

**Comment:** The most substantial file in advanced_projects at 343 lines. The `MP3AudioPlayer` class is well-decomposed with clear method separation (play, pause, resume, forward, backward, restart, toggle loops, stop). The `match cmd` block is clean and exhaustive. pygame import is guarded with a helpful error message. Deductions: the hardcoded `r"C:\Users\A.I.M\C.S\MP3"` path makes it non-portable. The `forward()` method has a subtle issue — the `for` loop on line 150 (`for current_idx + 1 >= len(mp3_files)`) is a no-op that should be an `if`; it works by accident because the condition is evaluated but the loop body never runs. The `time` module is imported but never used.

---

### music_player/tui/wav_tui_player.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 85 | 25% | 21.3 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **81** |

**Comment:** Identical to the MP3 TUI player in structure and quality. The docstring explicitly states it is kept as a sibling rather than a subclass so each file stands alone — a deliberate teaching choice. Same hardcoded Windows path, same no-op `for` loop in `backward()`, same unused `time` import. The two files are 95% identical, which is the point: comparing them side by side shows what is shared and what differs.

---

### transactions/transactions.py — **74/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **74** |

**Comment:** Reads an Excel workbook, applies a 10% discount to the prices column, and writes a bar chart. The CWD-relative `wb.save('transactionv1.xlsx')` is intentional per rule 3 and pinned by a test — not a bug. The `cell = sheet['a1']` / `cell = sheet.cell(1, 1)` redundancy (lines 25-26) is confusing — the first assignment is immediately overwritten. Comments are excessive (one per line explaining what each line does). Robustness: no check for whether the prices column contains numeric values; a non-numeric cell would raise `ValueError` from `float(num_price)`. The discount is hardcoded at 10% with no parameter.

---

## python/functional_programming/fundamental_topics/

### any_all.py — **93/100** (A — Exemplary)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 90 | 25% | 22.5 |
| Durability | 90 | 20% | 18.0 |
| Robustness | 85 | 15% | 12.8 |
| **Final** | | | **93** |

**Comment:** Clean demonstration of `any()` and `all()` with clear docstrings, meaningful variable names, and a good mix of use cases including the empty-iterable edge case. No input validation needed (builtins handle it). The only minor deduction: the file is purely demonstrative with no `__main__` guard or function wrapping, but that is the convention for this lane.

---

### closures.py — **92/100** (A — Exemplary)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 90 | 25% | 22.5 |
| Durability | 85 | 20% | 17.0 |
| Robustness | 85 | 15% | 12.8 |
| **Final** | | | **92** |

**Comment:** Excellent closure demonstration with two clear examples (multiplier and counter). The `nonlocal` usage is correct and well-commented. The docstring explains WHY closures exist (attaching behaviour to data without a class). No issues found.

---

### comprehensions.py — **92/100** (A — Exemplary)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 90 | 25% | 22.5 |
| Durability | 85 | 20% | 17.0 |
| Robustness | 85 | 15% | 12.8 |
| **Final** | | | **92** |

**Comment:** Covers list, set, and dict comprehensions in one file. Clear variable names, good docstring explaining the syntax. The teaching progression from simple to complex is natural. No issues found.

---

### currying.py — **88/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 80 | 15% | 12.0 |
| **Final** | | | **88** |

**Comment:** Good currying demonstration using nested lambdas. The practical greeting example shows real-world use. Deductions: the docstring mentions partial application as the counterpart but does not import or reference it (a reader would need to find `partial_application.py` themselves). The lambda-only approach obscures the function signatures slightly.

---

### filter.py — **91/100** (A — Exemplary)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 85 | 25% | 21.3 |
| Durability | 85 | 20% | 17.0 |
| Robustness | 85 | 15% | 12.8 |
| **Final** | | | **91** |

**Comment:** Comprehensive filter demonstration with four distinct predicate types (even/odd, threshold, non-empty, truthy-only). The `filter(None, ...)` case is a nice touch that many tutorials skip. Good variable names and clear output. No issues found.

---

### first_class_functions.py — **91/100** (A — Exemplary)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 85 | 25% | 21.3 |
| Durability | 85 | 20% | 17.0 |
| Robustness | 85 | 15% | 12.8 |
| **Final** | | | **91** |

**Comment:** Demonstrates all three aspects of first-class functions (stored, passed, returned). The `make_power` factory is a clean example. Good docstring explaining WHY this property matters. No issues found.

---

### functools_module.py — **92/100** (A — Exemplary)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 90 | 25% | 22.5 |
| Durability | 85 | 20% | 17.0 |
| Robustness | 85 | 15% | 12.8 |
| **Final** | | | **92** |

**Comment:** Covers all six `functools` features (cache, lru_cache, partial, reduce, singledispatch, wraps) with clear examples. The `singledispatch` example is particularly well done with three type registrations. The `wraps` decorator example correctly shows the metadata preservation. No issues found.

---

### itertools_module.py — **94/100** (A — Exemplary)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 90 | 25% | 22.5 |
| Durability | 90 | 20% | 18.0 |
| Robustness | 90 | 15% | 13.5 |
| **Final** | | | **94** |

**Comment:** The most comprehensive file in the functional lane — 20 itertools functions demonstrated with clear examples. Every function is shown with its output. The `islice` wrapper on infinite iterators (`count`, `cycle`) is the correct pattern. No issues found.

---

### lambda.py — **88/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 80 | 15% | 12.0 |
| **Final** | | | **88** |

**Comment:** Covers 14 lambda examples from simple to conditional. The `age_check` lambda using a conditional expression is a nice touch. Deductions: the file is purely a collection of print statements with no function wrapping or `__main__` guard, which is fine for this lane but limits reusability. Some lambdas (like `max_value`, `min_value`) duplicate built-in functionality unnecessarily.

---

### map.py — **91/100** (A — Exemplary)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 85 | 25% | 21.3 |
| Durability | 85 | 20% | 17.0 |
| Robustness | 85 | 15% | 12.8 |
| **Final** | | | **91** |

**Comment:** Good map demonstration covering single-iterable, type-conversion, and multi-iterable cases. The comment distinguishing map from zip (line 31) is helpful for learners. The `prices` list using strings that get converted to floats is a practical example. No issues found.

---

### partial_application.py — **88/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 80 | 15% | 12.0 |
| **Final** | | | **88** |

**Comment:** Clean partial application demonstration. The `power` function with keyword argument binding is correct. The `round` with `ndigits=2` example is practical. Deductions: the file is short and could show a more complex example (e.g., partial with a callback). The import is at module level rather than inside a function, which is fine.

---

### pipelines.py — **91/100** (A — Exemplary)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 85 | 25% | 21.3 |
| Durability | 85 | 20% | 17.0 |
| Robustness | 85 | 15% | 12.8 |
| **Final** | | | **91** |

**Comment:** Excellent pipeline demonstration chaining filter, map, sorted, and a list comprehension. The docstring correctly notes the trade-off (intermediate collections held in memory). The student data as tuples is a good realistic example. The `reduce` import is used for the average calculation. No issues found.

---

### pure_functions.py — **88/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 80 | 15% | 12.0 |
| **Final** | | | **88** |

**Comment:** Good demonstration of pure vs impure functions. The `add_tax` and `total_cost` examples are clearly pure. The `next_number` counter with `global` correctly shows impurity. Deductions: the file is short and the impure example is minimal — a more complex side-effect example (e.g., writing to a file, modifying a list argument) would strengthen the lesson.

---

### reduce.py — **88/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 80 | 15% | 12.0 |
| **Final** | | | **88** |

**Comment:** Covers four reduce use cases (sum, factorial, max, join). The docstring correctly notes the argument order (function first, iterable second). Deductions: no initial value example (which would show how to handle empty iterables). The `range(1, 6)` for factorial is correct but could be more explicit.

---

### sorted.py — **88/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 80 | 15% | 12.0 |
| **Final** | | | **88** |

**Comment:** Clean sorted demonstration with basic, reverse, and key-based sorting. The tuple sorting by second element is a good example. The docstring correctly contrasts `sorted()` with `list.sort()`. Deductions: only one key-based example; could show a more complex key (e.g., sorting by length, case-insensitive).

---

### statistics_module.py — **94/100** (A — Exemplary)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 90 | 25% | 22.5 |
| Durability | 90 | 20% | 18.0 |
| Robustness | 90 | 15% | 13.5 |
| **Final** | | | **94** |

**Comment:** The best file in the functional lane — 12 statistics measures demonstrated with clear comments showing expected return values. The central tendency vs spread organisation is logical. Every function is shown with its output. The placement in the functional lane (not imperative) is correct per AGENTS.md (the imperative lane `numbers.py` shadows stdlib). No issues found.

---

### zip.py — **85/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **85** |

**Comment:** Simple zip demonstration with three parallel lists. The `strict=True` parameter is mentioned in the docstring but not demonstrated. Deductions: the file is short and could show more complex cases (zipping with `strict=True`, zipping different-length iterables, unzipping with `*`). The comment about "automatically converts" is slightly confusing.

---

## python/functional_programming/syntax_fundamentals/

### grade_summary.py — **88/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 80 | 15% | 12.0 |
| **Final** | | | **88** |

**Comment:** Good functional programming exercise combining filter, reduce, and any/all. The `pass_grade` function is reusable. The `summarise_grades` function has a hardcoded list (acceptable for a teaching exercise). The `__main__` guard is present. No issues found.

---

### number_pipeline.py — **88/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 80 | 15% | 12.0 |
| **Final** | | | **88** |

**Comment:** Clean filter → map → reduce pipeline. The named intermediate variables make the data flow readable. The docstring correctly notes that nothing mutates the original. The `__main__` guard is present. No issues found.

---

### shopping_receipt.py — **85/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **85** |

**Comment:** Good functional receipt formatting. The `format_item` and `total_price` functions are reusable. The `reduce` with initial value `0` is correct. Deductions: the `map` result is iterated directly in the for loop without converting to a list (works but is lazy). The prices are hardcoded. No input validation.

---

### word_frequency.py — **85/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **85** |

**Comment:** Simple word frequency counter using set comprehension and sorted with a key. The `words.count(word)` approach is O(n^2) — a `collections.Counter` would be more efficient, but this is a teaching file for functional programming so the explicit approach is acceptable. Deductions: no `__main__` guard issue (it has one). The word list is hardcoded.

---

## python/imperative_programming/fundamental_topics/

### conditions.py — **56/100** (E — Poor)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 70 | 40% | 28.0 |
| Readability | 45 | 25% | 11.3 |
| Durability | 50 | 20% | 10.0 |
| Robustness | 45 | 15% | 6.8 |
| **Final** | | | **56** |

**Comment:** Covers a huge amount of ground (if/elif/else, loops, match, logical/membership operators, break/continue, nested loops, comprehensions) but at 569 lines it is far too long for one teaching file. Hardcoded `temperature = 25` and `name = "A.I.M"` make most branches unreachable without editing source. The `# Expected Output:` / `# Actual Output:` / `# Reason:` comment pattern is valuable but applied so exhaustively it buries the actual code. The nested `if x > 5: pass` block at line 291-294 is confusing — the `pass` does nothing and the inner `if` runs unconditionally.

---

### date_time.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 60 | 25% | 15.0 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 55 | 15% | 8.3 |
| **Final** | | | **70** |

**Comment:** Comprehensive datetime demonstration covering date, time, datetime, timedelta, strftime/strptime, and ZoneInfo. Runs clean (exit 0). Deductions: `new_time` and `new_format` on lines 25-29 are identical (dead code). `print(dir(datetime))` dumps a long list. The `from datetime import datetime` import on line 52 shadows the module-level `import datetime` from line 10, making the code confusing. The strptime format `"%dth %B, %Y"` for "28th September, 2026" is fragile — it would fail for "1st", "2nd", "3rd" without the matching suffix. No `__main__` guard; everything runs at module level.

---

### dictionaries.py — **64/100** (D — Weak)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 55 | 25% | 13.8 |
| Durability | 55 | 20% | 11.0 |
| Robustness | 50 | 15% | 7.5 |
| **Final** | | | **64** |

**Comment:** Covers all major dict methods plus a `setdefault()` block. The `capitals.clear()` call at line 94 empties the dict before the keys/values/items loops, making those loop bodies unreachable — documented in the docstring as deliberate. The `if capitals.get("Russia"):` check at line 77 is always truthy for any non-empty string, so the `else` branch is dead code. The comment `# Fiding exactly where in the dictionary is case - sensitive` has a typo ("Fiding" should be "Finding"). The `print(help(capitals))` call is expensive and stubbed out in tests. No `__main__` guard.

---

### exceptions.py — **73/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 70 | 15% | 10.5 |
| **Final** | | | **73** |

**Comment:** Good exception handling demonstration with specific except clauses (ValueError, ZeroDivisionError, KeyboardInterrupt) plus a catch-all and `finally`. The docstring correctly notes the difference between `raise` and `assert`. Deductions: the first try/except block (lines 14-19) has no `finally` and no `else`, so it is less complete than the second. The `except Exception as e` catch-all at line 41 should ideally re-raise or log more than just print. No `__main__` guard; the `input()` calls mean it exits 1 with no stdin (expected for interactive teaching files).

---

### formats.py — **71/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 60 | 25% | 15.0 |
| Durability | 60 | 20% | 12.0 |
| Robustness | 55 | 15% | 8.3 |
| **Final** | | | **71** |

**Comment:** Covers 13 format specifier variations with expected outputs in comments. Runs clean (exit 0). The comment for Price 3 (line 26) says "4 significant figures in scientific notation" but the actual output `1.235e+03` is 4 decimal places, not 4 significant figures — the comment is misleading. Price 7 uses `:.>10` which is not a valid format spec for floats (it works but is unusual). The `=` flag in Price 10 forces the sign to the far left, which is correct but the comment could be clearer. No `__main__` guard; purely demonstrative.

---

### functions.py — **66/100** (D — Weak)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 55 | 25% | 13.8 |
| Durability | 55 | 20% | 11.0 |
| Robustness | 50 | 15% | 7.5 |
| **Final** | | | **66** |

**Comment:** Covers function definition, parameters, defaults, *args, **kwargs, and keyword arguments. The `divide(*numbers)` function starts with `total = 100` then divides by each argument — this is confusing because the initial value is arbitrary. The `fullname(*name)` function prints but returns None, then `print(type(fullname))` prints the function object type — this is a strange teaching choice. The `address(**location)` example uses multi-line keyword arguments which is good. The `print(help('keywords'))` call at line 99 is unnecessary noise. The output comment block (lines 86-94) is never actually printed by the code.

---

### hello_world.py — **93/100** (A — Exemplary)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 90 | 25% | 22.5 |
| Durability | 90 | 20% | 18.0 |
| Robustness | 85 | 15% | 12.8 |
| **Final** | | | **93** |

**Comment:** The smallest complete Python program. The docstring notes the PEP 8 spacing issue (`print ("Hello World")` with a space). It cannot crash, cannot break the suite, and serves as the baseline every other file builds on. This is exactly what a hello-world teaching file should be.

---

### lists.py — **61/100** (D — Weak)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 50 | 25% | 12.5 |
| Durability | 50 | 20% | 10.0 |
| Robustness | 45 | 15% | 6.8 |
| **Final** | | | **61** |

**Comment:** Covers an enormous amount of list functionality (indexing, slicing, modifying, methods, unpacking, sorting, joining, duplicates, min/max, 2D lists, comprehensions) at 314 lines. The variable `max` on line 162 shadows the built-in `max()` function — a teaching anti-pattern. The `min` variable on line 176 does the same. The `numbers.remove(7)` call on line 74 removes the first occurrence but the comment says `[5, 2, 1, 4]` which is correct, yet the preceding line shows `[3, 5, 2, 1, 7, 4]` after insert — the intermediate states are confusing. The list comprehension section is good but could be its own file. No `__main__` guard.

---

### login_status.py — **65/100** (D — Weak)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 70 | 40% | 28.0 |
| Readability | 65 | 25% | 16.3 |
| Durability | 60 | 20% | 12.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **65** |

**Comment:** Well-decomposed into functions (`get_boolean_answer`, `display_answers`, `check_access_status`, `run_login_check`) with an `__main__` guard. The IndexError repair is verified. However, the two deliberate predicate bugs (lines 27 and 31) make "Stop Lying" unreachable and the `elif` ignores `is_new` — these are pinned by tests per rule 11 and are the point of the exercise. The nested if/elif/else structure is complex and hard to follow. The `except (ValueError, IndexError)` handler is correct but catches too broadly — a non-string input would raise `TypeError` which is not caught.

---

### main.py — **84/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 85 | 20% | 17.0 |
| Robustness | 80 | 15% | 12.0 |
| **Final** | | | **84** |

**Comment:** The only file in the repo that keeps `def main()` by design. The `IndentationError` (empty function body) is a deliberate teaching stub pinned by `test_fundamentals.py`. The docstring explains the `if __name__ == "__main__":` pattern clearly. It cannot run, which is the point — it demonstrates what a complete file should look like. The score is high because the defect is intentional and well-documented, not accidental.

---

### modules.py — **72/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 70 | 40% | 28.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 70 | 15% | 10.5 |
| **Final** | | | **72** |

**Comment:** The `help("modules")` call at line 7 causes a timeout (exit 124) when run directly because it scans every installed package — this is why the test suite stubs it. The module conflict example (shadowing `e` with `from math import e`) is a valuable lesson. The solution using `import math` is correct. Deductions: the `print(help("math"))`, `print(help("string"))`, and `print(help("time"))` calls are unnecessary noise that slow the file. The `from math import pi` example is minimal. No `__main__` guard.

---

### numbers.py — **82/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 85 | 20% | 17.0 |
| Robustness | 70 | 15% | 10.5 |
| **Final** | | | **82** |

**Comment:** Fixed in this session — the `sys.path` de-shadowing at the top resolves the `decimal` circular import that killed the file ~60 lines in when run directly. Now exits 0 with 125 lines of output, both Decimal sections reached. The `[AI-authored fix]` docstring explains the why. Deductions: the `os`/`sys` imports are a minor intrusion into a file about number types. The file is long (356 lines) and covers many topics; splitting it would improve readability. No `__main__` guard; everything runs at module level.

---

### scope_resolution.py — **85/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 95 | 40% | 38.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **85** |

**Comment:** Clean demonstration of LEGB (Local, Enclosed, Global, Built-in) scope resolution. Each scope level has its own function pair. The `from math import e` inside the `built_in()` function is a nice touch showing import scope. Runs clean (exit 0). Deductions: the functions are minimal and could be more realistic. No `__main__` guard.

---

### sets.py — **74/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **74** |

**Comment:** Covers all major set operations (add, remove, pop, update, clear, union, intersection, difference, symmetric_difference, isdisjoint, issubset, issuperset). The `fruits= list(fruits)` on line 40 has inconsistent spacing. The `st1` / `st2` naming is less clear than `set1` / `set2`. The `vegetables` variable starts as a tuple then gets converted to a set — this is correct but could be clearer. No `__main__` guard.

---

### strings.py — **64/100** (D — Weak)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 55 | 25% | 13.8 |
| Durability | 55 | 20% | 11.0 |
| Robustness | 50 | 15% | 7.5 |
| **Final** | | | **64** |

**Comment:** Covers an enormous number of string methods at 249 lines. The `# Expected Output:` / `# Actual Output:` / `# Reason:` pattern is thorough but exhausting. The `input()` call at line 206 makes it exit 1 without stdin. The duplicate checks (`isprintable` and `isidentifier` are each tested twice) are unnecessary. The `print(help(str))` call is stubbed out in tests. The `rfind("a")` comment on line 58 says "starting on the left hand side (from 0)" which is correct but the method name `rfind` is confusing — it finds the rightmost occurrence. The `expandtabs(4)` example shows no visible effect because the string has no tabs.

---

### tuples.py — **76/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **76** |

**Comment:** Covers tuple creation, indexing, unpacking, sorting, slicing, conversion to/from lists, joining, and deletion. The `del random_tuple` comment on line 110 says "inaccessability" which should be "inaccessibility" (SPaG). The `sorted_points = tuple(sorted(points))` example is correct. The multi-line comment block (lines 39-45) showing the unpacking alternative is a nice touch. No `__main__` guard.

---

### type_conversion_type_casting.py — **85/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 95 | 40% | 38.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **85** |

**Comment:** Clean, focused demonstration of `str()`, `int()`, `float()`, `bool()`, and `type()`. The docstring correctly notes the critical distinction: `int("3.14")` raises ValueError while `int(3.14)` silently truncates. The expected/actual/reason comment pattern is applied consistently without being overwhelming. Runs clean (exit 0). No issues found.

---

### variables.py — **56/100** (E — Poor)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 70 | 40% | 28.0 |
| Readability | 50 | 25% | 12.5 |
| Durability | 45 | 20% | 9.0 |
| Robustness | 45 | 15% | 6.8 |
| **Final** | | | **56** |

**Comment:** Covers the four basic types (string, int, float, bool) but the boolean branching section has the same deliberate defects as `login_status.py` — the `if is_online == True:` check is always truthy for any non-empty string, and the nested `if choice[0].upper() == "A"` structure is hard to follow. The `input()` calls for quantity and costs make it interactive (exit 1 without stdin). The `debt = int(costs) - revenue` calculation is correct but the variable naming could be clearer. The f-string output is well-formatted. No `__main__` guard.

---

## python/imperative_programming/interactive_games/

### dice_game.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **70** |

**Comment:** The `dice_art` dictionary with ASCII dice faces is a strong visual design. The game loop is well-structured with clear turn separation. However, the entire game logic is inside one long `play_dice_race()` function (146 lines), which the docstring acknowledges is deliberate as a counter-example. The `input("Press Enter...")` calls make it interactive (exit 1 without stdin). The `dice_art.get(die)[line]` call on line 108 could raise `KeyError` if a die value outside 1-6 appeared (defensive but not needed with `randint(1, 6)`). No validation on the play-again input beyond checking for 'y'/'yes'.

---

### haiku_madlibs.py — **64/100** (D — Weak)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 60 | 25% | 15.0 |
| Durability | 55 | 20% | 11.0 |
| Robustness | 50 | 15% | 7.5 |
| **Final** | | | **64** |

**Comment:** The concept is creative (mad libs haiku with random template selection). The `random.choice(templates_1)` approach means the same inputs produce different poems. However, the file is purely interactive with 18 `input()` calls and no `__main__` guard. The f-string templates are well-formed but the haiku structure (5-7-5 syllables) is not enforced — the player could produce nonsense. No input validation whatsoever. The `import random` comment says "essential to randomise the placements of certain language techniques" which is vague.

---

### hangman_game.py — **76/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **76** |

**Comment:** Well-structured with clear function separation (`display_hangman`, `display_hint`, `display_answer`, `play_hangman`). The word bank is extensive (200+ animals). The input validation on line 84 (`len(guess) != 1 or not guess.isalpha()`) is correct. The `guessed_letters` set prevents repeats. Deductions: the `while is_running` flag is redundant (could use `while True` with breaks). The `hangman_art` dictionary uses integer keys 0-6 which is clear. The `display_hangman(wrong_guesses)` call on line 106 and 115 shows the full stickman even on win, which is a minor UX issue. No `__main__` guard.

---

### number_guessing_game.py — **72/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **72** |

**Comment:** Good EXP system that adds a second progress signal beyond attempt count. The `try/except ValueError` on line 24 correctly handles non-integer input. The nested while loop structure is clear. Deductions: the `EXP` variable is global and persists across rounds, which could confuse. The `print(f"Unlucky. It was {answer}. You were {100 - EXP} EXP away.")` message is confusing — it says "you were X EXP away" but the calculation is `100 - EXP` which is the remaining EXP needed, not the EXP "away". No `__main__` guard.

---

### quiz_game.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 65 | 25% | 16.3 |
| Durability | 60 | 20% | 12.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **70** |

**Comment:** Clean data-at-the-top design with questions, options, and answers as tuples. The `for question in questions` loop is simple and correct. Deductions: no input validation (a guess of "Z" would be treated as incorrect without warning). The `score = int(score / len(questions) * 100)` calculation on line 59 is correct but the variable `score` is reused (first as count, then as percentage). The `options[question_num]` indexing is correct but fragile — adding a question requires updating three separate tuples. No `__main__` guard.

---

### rock_paper_scissors.py — **75/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **75** |

**Comment:** Restructured into functions with an `__main__` guard and game loop (first to 3 wins). The `rock_art()`, `paper_art()`, `scissors_art()` functions provide visual feedback. The deliberate `isdigit()` bug on line 113 is pinned by tests per rule 11 — the invalid-input check is always truthy, so the "Stop Messing Around" message never prints. This is the point of the exercise. The `determine_outcome()` function is clean. Deductions: the always-truthy bug means invalid input silently passes through. The score tracking is simple but effective.

---

### word_guessing_game.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **70** |

**Comment:** Clean two-level loop structure (outer for replay, inner for attempts). The `guessedWord` list with underscore replacement is a standard hangman-style approach. The `word_bank` is well-chosen (tech terms). Deductions: the `guessedWord` variable uses camelCase instead of snake_case (PEP 8 violation). No input validation on the guess (could be multiple characters, non-alpha). The `play_again` check only accepts 'y' — 'yes' would exit. No `__main__` guard.

---

## python/imperative_programming/math_and_science_calculators/

### annual_rate_calculator.py — **72/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **72** |

**Comment:** Back-solves the annual rate from income and time. The input validation (decimal places, single currency symbol, positive income) is thorough. The `raise Exception(...)` pattern is used instead of `ValueError`, which is less idiomatic. The `except Exception as error_message` catch-all at the end is too broad. No `__main__` guard.

---

### area.py — **85/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 95 | 40% | 38.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **85** |

**Comment:** The simplest geometry calculator at 28 lines. The `area(x, y)` function is pure and reusable. The `calculate()` wrapper handles input and output. The docstring correctly notes that validation lives in callers. The `round(result, 2)` is appropriate. No issues found.

---

### area_of_circle.py — **76/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 70 | 40% | 28.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 85 | 20% | 17.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **76** |

**Comment:** Left deliberately defective per rule 11 (no `__main__` guard). The `calculate_area()` function is correct and reusable. The `area_of_circle()` function has proper exception handling (ValueError, TypeError, KeyboardInterrupt). The defect IS the lesson — the asymmetry with `circumference_of_circle.py` demonstrates what the guard is for.

---

### area_of_triangle.py — **75/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **75** |

**Comment:** Clean helper-function pattern with `get_float_input()` returning None for empty input. The `if b and h:` check at line 32 is always truthy for non-zero floats, so the else branch is unreachable. The `round((b * h) / 2, 2)` is correct. The docstring mentions "module-level squares the radius" which is stale copy-paste from another file. No `__main__` guard.

---

### area_volume_calculator.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **70** |

**Comment:** Menu-driven calculator combining area and volume. The `sys.path.append` at the top is necessary for sibling imports. The f-string formatting with box drawing is visually appealing. Deductions: the `match choice` block has no default case for non-"1"/"2" input. The `round()` calls are correct. No `__main__` guard.

---

### arithmetic_calculator.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 70 | 15% | 10.5 |
| **Final** | | | **77** |

**Comment:** The shared `arithmetic()` function with match/case dispatch. Returns error strings instead of raising — a deliberate design choice documented in the docstring. The `__main__` block has a full calculator with input validation, formatting, and a TUI box. Deductions: the `//` case at line 30 is missing the `else` clause (inconsistent with `/` and `%`). The `round_choice` input validation is minimal. The f-string formatting is complex but correct.

---

### arithmetic_expressions.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 85 | 20% | 17.0 |
| Robustness | 70 | 15% | 10.5 |
| **Final** | | | **81** |

**Comment:** The `format_result()` function with the `isinstance` guard (fixed in this session) prevents the `:.2f` crash on error strings. The `EXPERSSIONS` typo in the banner is pinned by a test. The menu banner duplicates `arithmetic_calculator.py` (noted in docstring). The `get_number()` function correctly tries int first, then float. No `__main__` guard.

---

### arithmetic_iteration.py — **73/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **73** |

**Comment:** Chains arithmetic operations through a generated polynomial sequence. The `generate_sequence()` function is well-structured. The `arithmetic_iteration()` function correctly stops on error strings. Deductions: the `try/except ImportError` block for the import is unnecessary under pytest (pythonpath is set). The f-string formatting is correct. No `__main__` guard.

---

### card_validator_program.py — **82/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **82** |

**Comment:** Clean Luhn algorithm implementation. The `validate()` function returns a boolean, making it reusable. The slicing (`[::2]`, `[1::2]`) is correct. The docstring at the top lists test card numbers (helpful for testing). The `if x >= 10:` check correctly handles doubled digits. No `__main__` guard.

---

### circle_calculator.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **70** |

**Comment:** Menu delegating to `area_of_circle()` and `circumference()`. The `choice.isdigit()` check is correct. The `except ValueError` is unreachable (noted in docstring). The `except KeyboardInterrupt` handler has a typo ("reccomend" should be "recommend"). The imports at the top mutate `sys.path`. No `__main__` guard.

---

### circumference_of_circle.py — **75/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **75** |

**Comment:** The counterpart to `area_of_circle.py` — this one HAS the `__main__` guard. The `calculate_circumference()` function uses a variable named `area` to store circumference (confusing naming). The exception handling matches `area_of_circle.py`. The docstring correctly explains the asymmetry. No issues beyond the naming.

---

### compound_debt_calculator.py — **72/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **72** |

**Comment:** Compound debt formula `A = P(1 + r/100)^t`. The `while True` loop with break is correct. The `if p > 0:` check correctly rejects positive values (debt is negative). The `compound_debt()` function is pure. Deductions: the `while True` loop only runs once (break at end of else). The `except ValueError` catches float conversion errors. No `__main__` guard.

---

### compound_interest_rate.py — **72/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **72** |

**Comment:** Identical structure to `compound_debt_calculator.py` but for positive values. The docstring correctly notes the parallel design. The `compound_interest()` function is pure. The input validation is the same. Deductions: the two files are 95% identical, which is the point (teaching comparison). No `__main__` guard.

---

### cosine_rule.py — **76/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 70 | 15% | 10.5 |
| **Final** | | | **76** |

**Comment:** Comprehensive cosine rule with side and angle solving. The `get_float_input()` helper returns None for empty input. The `match/case` blocks are correct. The `-1 <= cos_A <= 1` domain check is excellent validation. Deductions: the `if a and b and C:` checks are always truthy for non-None values. The `calculate()` function is long (87 lines). No `__main__` guard.

---

### euclidean_distance_calculator.py — **84/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 80 | 15% | 12.0 |
| **Final** | | | **84** |

**Comment:** Clean n-dimensional Euclidean distance calculator. The `euclidean_distance()` function raises ValueError for mismatched dimensions — correct. The `get_float_input()` helper is well-designed. The `get_dimensions()` function has proper validation. The `calculate()` function is clear. The docstring is excellent. No issues found.

---

### gradient_calculator.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 80 | 15% | 12.0 |
| **Final** | | | **81** |

**Comment:** Clean gradient calculator importing helpers from `euclidean_distance_calculator.py`. The `gradient()` function raises `ZeroDivisionError` for vertical lines — correct. The `calculate()` function has proper error handling. The `direction` input check is a nice touch. No issues found.

---

### perimeter_of_triangle.py — **75/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **75** |

**Comment:** Simple perimeter calculator using the helper-function pattern. The `get_float_input()` returns None for empty input. The `if a and b and c:` check is always truthy for non-None values. The `round(a + b + c, 2)` is correct. The docstring mentions "doubles the total to normalise a triangle inequality check" which is confusing — the code does not do this. No `__main__` guard.

---

### pythagoras_theorem.py — **75/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **75** |

**Comment:** Clean Pythagorean theorem calculator. The `missing = [a, b, c].count(None)` check is elegant. The `if c <= b:` validation is correct. Deductions: the `for c <= b:` on line 50 is a no-op (should be `if`). The `calculate()` function is clear. No `__main__` guard.

---

### simple_debt_calculator.py — **72/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **72** |

**Comment:** Simple interest formula `A = P(1 + rt)`. The `while True` loop with break is correct. The `if p > 0:` check correctly rejects positive values. The `simple_debt()` function is pure. Deductions: identical structure to `compound_debt_calculator.py`. No `__main__` guard.

---

### simple_interest_rate.py — **72/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **72** |

**Comment:** Simple interest formula `I = P * r * t`. Identical structure to `simple_debt_calculator.py`. The `simple_interest()` function is pure. The input validation is the same. Deductions: the two files are near-identical. No `__main__` guard.

---

### sine_rule.py — **76/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 70 | 15% | 10.5 |
| **Final** | | | **76** |

**Comment:** Comprehensive sine rule with side and angle solving. The `match/case` blocks are correct. The `-1 <= sin_B <= 1` domain check is excellent. The `get_float_input()` helper is well-designed. Deductions: the `calculate()` function is very long (190 lines). The `if a and b:` checks are always truthy for non-None values. No `__main__` guard.

---

### square_number_times_tables.py — **71/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 55 | 15% | 8.3 |
| **Final** | | | **71** |

**Comment:** Imports `times_tables()` and filters to square numbers. The `square_number()` function is simple. Deductions: the import is unused (the function does not call `times_tables()`). The `range(0, limit + 1)` includes 0, which produces `0 x 0 = 0` — a valid but trivial entry. No input validation. No `__main__` guard.

---

### times_tables.py — **76/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **76** |

**Comment:** Simple times table generator. The nested loop is correct. The `times_tables()` function prints directly (not reusable). Deductions: no input validation (negative values would produce empty output). The `range(0, tables + 1)` includes 0, which produces a trivial table. No `__main__` guard.

---

### triangle_calculator.py — **73/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **73** |

**Comment:** Menu-driven triangle calculator dispatching to sine/cosine rule. The `sys.path.append` at the top is necessary for imports. The `pythagoras()`, `area()`, and `perimeter()` functions are well-structured. The `run_calculator()` function has a clear menu loop. Deductions: the `get_float_input()` helper is duplicated (could be imported). The `match choice` block has proper error handling. No `__main__` guard.

---

### volume.py — **85/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 95 | 40% | 38.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **85** |

**Comment:** Clean volume calculator at 28 lines. The `volume(x, y, z)` function is pure and reusable. The `calculate()` wrapper handles input and output. The docstring correctly notes the contrast between calculation and wrapper. The `round(result, 2)` is appropriate. No issues found.

---

## python/imperative_programming/syntax_exercises/

### add.py — **87/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **87** |

**Comment:** Nine lines, clean and focused. The simplest possible arithmetic script. Runs clean (exit 0). No input validation needed (no input). This is exactly what a minimal teaching script should be.

---

### alarm_clock.py — **76/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **76** |

**Comment:** Well-structured alarm clock with 12h/24h format selection, input validation, and pygame audio. The `valid_alarm_time()` function has proper match/case with validation loops. The `set_alarm()` function polls the clock correctly. The pygame import is guarded. Deductions: the hardcoded `r"C:\Users\A.I.M\C.S\WAV\..."` path is non-portable. The `while is_running` loop with `time.sleep(1)` means the alarm can be up to 1 second late. The `except FileNotFoundError` at line 155 is unreachable (the file existence is pre-checked at line 137). Has `__main__` guard.

---

### banking_program.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **70** |

**Comment:** 115-line banking program with deposit, withdrawal, and balance. Has `__main__` guard. The interactive nature (exit 1 without stdin) is expected. Deductions: no input validation beyond basic float conversion. The balance is stored in a local variable, so it resets each run. No persistence.

---

### checkout_system.py — **71/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 60 | 20% | 12.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **71** |

**Comment:** 27-line checkout system. Simple and focused. No `__main__` guard. The interactive nature is expected. Deductions: no input validation. The total calculation is trivial. No receipt formatting.

---

### count_up_timer.py — **72/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **72** |

**Comment:** Simple count-up timer with `time.sleep(1)`. The `count()` function is clean. The individual test calls at the bottom (lines 18-36) are a nice touch showing different ranges. Deductions: no `__main__` guard. The `time.sleep(1)` calls make it slow without mocking. No input validation.

---

### distance_calculator.py — **71/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 60 | 20% | 12.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **71** |

**Comment:** 19-line distance calculator. Simple and focused. No `__main__` guard. The interactive nature is expected. Deductions: no input validation. The distance formula is trivial.

---

### divide.py — **87/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **87** |

**Comment:** Nine lines, clean and focused. The simplest possible division script. Runs clean (exit 0). No input validation needed (no input). This is exactly what a minimal teaching script should be.

---

### drink_script_example.py — **76/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **76** |

**Comment:** Sibling-import example demonstrating the difference between a module safe to import and one that owns the terminal. The `[AI-authored fix]` try/except import block is correct. The `favourite_drink()` function is simple. Deductions: the print statements at the bottom run on import (no `__main__` guard). The comment "Python is decent, but idk kinda mid" is unprofessional for a teaching repo.

---

### email_slicer.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **70** |

**Comment:** 62-line email slicer. Has `__main__` guard. The interactive nature is expected. Deductions: no input validation. The email parsing is trivial (split on @). No error handling for malformed emails.

---

### even_odd_detector.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** 27-line even/odd detector. Simple and focused. No `__main__` guard. Runs clean (exit 0). Deductions: no input validation. The logic is trivial (modulo 2).

---

### factorials.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **70** |

**Comment:** 29-line factorial calculator. Has `__main__` guard. The interactive nature is expected. Deductions: no input validation. The factorial calculation is trivial. No error handling for negative numbers.

---

### file_handling.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** 31-line file handling demonstration. No `__main__` guard. Runs clean (exit 0). The `with open()` pattern is correct. Deductions: no error handling. The file operations are trivial.

---

### file_reader.py — **78/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **78** |

**Comment:** 79-line file reader with CSV parsing. No `__main__` guard. Runs clean (exit 0). The CSV handling is correct. Deductions: no error handling for missing files. The empty-row fix is noted in NOTES.md.

---

### file_writer.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** 89-line file writer covering TXT, JSON, and CSV. No `__main__` guard. Runs clean (exit 0). The `with open()` pattern is correct. The `try/except FileExistsError` blocks are appropriate. Deductions: the CWD-relative file paths are intentional (rule 4) but make the file non-portable. The `encoding = "utf-8"` is correct.

---

### food_menu.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **70** |

**Comment:** 57-line food menu. No `__main__` guard. The interactive nature is expected. Deductions: no input validation. The menu logic is trivial. No error handling.

---

### food_script_example.py — **72/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **72** |

**Comment:** 25-line food script. Has `__main__` guard. The `favourite_food()` function is simple. Deductions: the print statements at the bottom run on import. The function is trivial.

---

### grade_boundary_calculator.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **70** |

**Comment:** 52-line grade boundary calculator. No `__main__` guard. The interactive nature is expected. Deductions: no input validation. The grade boundaries are hardcoded. No error handling for out-of-range scores.

---

### hour_clock.py — **75/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **75** |

**Comment:** 57-line hour clock with input validation. The `countdown()` function is correct. The `isdigit()` check is appropriate. The bound checks for minutes and seconds are correct. Deductions: no `__main__` guard. The `time.sleep(1)` calls make it slow without mocking. The `except ValueError` is unreachable (isdigit check prevents it).

---

### leap_year.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **70** |

**Comment:** 28-line leap year checker. No `__main__` guard. The interactive nature is expected. Deductions: no input validation. The leap year logic is correct but trivial.

---

### math_file.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** 26-line math file importing from `math_module.py`. No `__main__` guard. Runs clean (exit 0). The import pattern is correct. Deductions: the file is purely demonstrative. No error handling.

---

### math_module.py — **85/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 95 | 40% | 38.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **85** |

**Comment:** 22-line module of math constants and functions. The `pi = 3.14159` constant is clear. The `square()`, `cube()`, `circumference()`, and `area()` functions are pure and reusable. The docstring correctly explains the two-file import pair. No issues found.

---

### minute_timer.py — **72/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **72** |

**Comment:** 43-line minute timer. No `__main__` guard. The `time.sleep(1)` calls make it slow without mocking. Deductions: no input validation. The timer logic is trivial.

---

### multiply.py — **87/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **87** |

**Comment:** Nine lines, clean and focused. The simplest possible multiplication script. Runs clean (exit 0). No input validation needed (no input). This is exactly what a minimal teaching script should be.

---

### num_pad.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** 96-line num pad. No `__main__` guard. Runs clean (exit 0). The num pad layout is correct. Deductions: no input validation. The layout logic is trivial.

---

### number_matrix_display.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **70** |

**Comment:** 46-line number matrix display. Has `__main__` guard. The interactive nature is expected. Deductions: no input validation. The matrix logic is trivial.

---

### prime_numbers.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **70** |

**Comment:** 46-line prime number checker. No `__main__` guard. The interactive nature is expected. Deductions: no input validation. The prime checking logic is correct but inefficient (checks all numbers up to n).

---

### random_cipher.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **70** |

**Comment:** 53-line random cipher. No `__main__` guard. The interactive nature is expected. Deductions: no input validation. The cipher logic is trivial (random substitution).

---

### random_colour_generator.py — **75/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **75** |

**Comment:** 67-line random colour generator with hex, RGB, octal, and HSL output. The `match colour_type` block with pipe `|` patterns is correct. The `randint(0, 0xFFFFFF)` for hex is correct. Deductions: the `case "2" | "rgb" | "r" | "b" | "g":` pattern includes "b" and "g" which are ambiguous (could be blue or green). The `case "4" | "hsl" | "hs" | "hu" | "hue" | "saturation" | "lightness" | "h" | "s" | "l":` pattern is overly broad. Has `__main__` guard.

---

### reverse_list_program.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **70** |

**Comment:** 49-line reverse list program. Has `__main__` guard. The interactive nature is expected. Deductions: no input validation. The reverse logic is trivial.

---

### seconds_countdown.py — **72/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **72** |

**Comment:** 39-line seconds countdown. No `__main__` guard. The `time.sleep(1)` calls make it slow without mocking. Deductions: no input validation. The countdown logic is trivial.

---

### shipping_label.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** 40-line shipping label. No `__main__` guard. Runs clean (exit 0). The label formatting is correct. Deductions: no input validation. The label logic is trivial.

---

### shopping_cart.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** 59-line shopping cart. No `__main__` guard. Runs clean (exit 0). The cart logic is correct. Deductions: no input validation. The cart logic is trivial.

---

### square.py — **87/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **87** |

**Comment:** Nine lines, clean and focused. The simplest possible square script. Runs clean (exit 0). No input validation needed (no input). This is exactly what a minimal teaching script should be.

---

### subtract.py — **87/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 100 | 40% | 40.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **87** |

**Comment:** Nine lines, clean and focused. The simplest possible subtraction script. Runs clean (exit 0). No input validation needed (no input). This is exactly what a minimal teaching script should be.

---

### symbol_generator.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **70** |

**Comment:** 25-line symbol generator. No `__main__` guard. The interactive nature is expected. Deductions: no input validation. The symbol logic is trivial.

---

### username_status.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **70** |

**Comment:** 33-line username status checker. No `__main__` guard. The interactive nature is expected. Deductions: no input validation. The status logic is trivial.

---

## python/imperative_programming/unit_and_format_converters/

### fahrenheit_celsius_converter.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** Clean two-function converter with formatting helpers. The `celcius` spelling is deliberate and pinned by tests. The `try/except ValueError` is correct. No `__main__` guard. The input validation is minimal but adequate for a teaching script.

---

### phone_converter.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **70** |

**Comment:** Phone keypad mapper using match/case. The `while True` loop with validation is correct. The `num()` function is clean. Deductions: no `__main__` guard. The `Seperates` comment has a typo ("Separates"). The `result += word + " "` string concatenation in a loop is inefficient.

---

### qrcode_generator.py — **75/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **75** |

**Comment:** Clean QR code generator. The `make_qr_code()` function with `output_dir` parameter is flexible. The CWD-relative save is intentional (rule 4) and documented. Has `__main__` guard. Deductions: no input validation on the URL. The `sys.argv` handling is minimal.

---

### roman_numeral_converter.py — **72/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 80 | 40% | 32.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **72** |

**Comment:** Roman numeral converter with match/case `get_value()` and correct subtractive notation logic. The `try/except ValueError` handles invalid characters. Deductions: no `__main__` guard. The `raise ValueError()` on line 21 has no message. The `numeral.upper()` call is correct.

---

### time_converter.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** Comprehensive time converter with 10 units. The `get_unit_info()` function returning `(multiplier, name)` is elegant and extensible. The `except KeyboardInterrupt` handler is a nice touch. Deductions: no `__main__` guard. The `int(current_choice)` conversion could raise `ValueError` for non-numeric input. The `final_answer` could be very large or very small.

---

### weight_converter.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **70** |

**Comment:** Simple weight converter with pounds and kilograms. The `try/except ValueError` is correct. The `unit.lower()[0]` check is a nice shortcut. Deductions: no `__main__` guard. The `new` variable is not rounded. The `w / 0.45` calculation is correct but could be more readable as `w * (1 / 0.45)`.

---

## python/object_oriented_programming/fundamental_topics/

### abstract_classes.py — **82/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **82** |

**Comment:** Clean abstract class demonstration with Vehicle base and three subclasses. The `@abstractmethod` decorator is used correctly. The `pass` bodies are documented as unreachable coverage caps. The instantiations at the bottom are clear. Deductions: no `__main__` guard. The subclasses are near-identical (could be more varied).

---

### aggregation.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **81** |

**Comment:** Clean aggregation example (has-a relationship). Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The aggregation pattern is simple. No error handling.

---

### class_methods.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **81** |

**Comment:** Class methods demonstration. Runs clean (exit 0). The `@classmethod` decorator is used correctly. Deductions: no `__main__` guard. The class methods are simple. No error handling.

---

### class_variables.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **81** |

**Comment:** Class variables demonstration. Runs clean (exit 0). The class variable pattern is clear. Deductions: no `__main__` guard. The class variables are simple. No error handling.

---

### classes.py — **75/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **75** |

**Comment:** The baseline OOP file importing Car, Person, and Point from siblings. The `[AI-authored fix]` sys.path block is correct. The try/except import pairs are the standard fallback idiom. The multi-line comment blocks (lines 59-74, 90-94, 109-111) explaining the logic are verbose but helpful. Deductions: the comment blocks are excessive. The `print(car1)` at line 47 prints a memory address (confusing for beginners). No `__main__` guard.

---

### composition.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **81** |

**Comment:** Clean composition example (part-of relationship). Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The composition pattern is simple. No error handling.

---

### constructors.py — **85/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 95 | 40% | 38.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **85** |

**Comment:** Clean constructor demonstration at 21 lines. The `__init__` method is explained clearly. Runs clean (exit 0). Deductions: no `__main__` guard. The constructor is simple. No error handling.

---

### data_classes.py — **82/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **82** |

**Comment:** Data class demonstration using `@dataclass`. Runs clean (exit 0). The decorator is used correctly. Deductions: no `__main__` guard. The data class is simple. No error handling.

---

### decorator.py — **82/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **82** |

**Comment:** Clean decorator demonstration with three stacked decorators. The `@wraps` explanation in the docstring is correct. The nested function pattern is clear. Deductions: no `__main__` guard. The decorators are simple. No error handling.

---

### duck_typing.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **81** |

**Comment:** Duck typing demonstration. Runs clean (exit 0). The "if it walks like a duck" pattern is clear. Deductions: no `__main__` guard. The duck typing is simple. No error handling.

---

### generator.py — **68/100** (D — Weak)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 65 | 25% | 16.3 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **68** |

**Comment:** Generator demonstration with `yield` and generator expressions. The `count_to()` function is clear. The `read_file()` generator is practical. The execution time tracking is a nice touch. Deductions: the `elif execution_time >= 3600:` on line 44 is dead code (unreachable after the `>= 60` elif). The hardcoded file paths (`r"C:\Users\A.I.M\C.S\..."`) are non-portable. The `time.sleep(1)` calls make it slow. The `if __name__ == "__main__":` guard only covers Example 1; Examples 2-4 run on import. Exit 1 (interactive).

---

### inheritance.py — **85/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 95 | 40% | 38.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **85** |

**Comment:** Clean inheritance demonstration with Animal base and Dog/Cat/Mouse subclasses. The `super()` usage is correct. The method overriding is clear. Runs clean (exit 0). Deductions: no `__main__` guard. The subclasses are near-identical.

---

### iterator.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **81** |

**Comment:** Iterator demonstration. Runs clean (exit 0). The `__iter__` and `__next__` methods are correct. Deductions: no `__main__` guard. The iterator is simple. No error handling.

---

### magic_methods.py — **82/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **82** |

**Comment:** Magic methods demonstration. Runs clean (exit 0). The dunder methods are correct. Deductions: no `__main__` guard. The magic methods are simple. No error handling.

---

### multi_level_inheritance.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **81** |

**Comment:** Multi-level inheritance demonstration. Runs clean (exit 0). The three-level hierarchy is clear. Deductions: no `__main__` guard. The inheritance is simple. No error handling.

---

### multiple_inheritance.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **81** |

**Comment:** Multiple inheritance demonstration. Runs clean (exit 0). The MRO is correct. Deductions: no `__main__` guard. The multiple inheritance is simple. No error handling.

---

### multitasking.py — **65/100** (D — Weak)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 70 | 40% | 28.0 |
| Readability | 65 | 25% | 16.3 |
| Durability | 60 | 20% | 12.0 |
| Robustness | 55 | 15% | 8.3 |
| **Final** | | | **65** |

**Comment:** Multitasking demonstration. Exit 124 (timeout — runs indefinitely). The threading/multiprocessing pattern is present. Deductions: no `__main__` guard. The multitasking is unclear. No error handling. The timeout makes it untestable without mocking.

---

### nested_classes.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** Nested classes demonstration at 134 lines. Runs clean (exit 0). The nested class pattern is clear. Deductions: no `__main__` guard. The nested classes are verbose. No error handling.

---

### polymorphism.py — **75/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **75** |

**Comment:** Polymorphism demonstration with Shape abstract class and multiple subclasses. The `@abstractmethod` decorator is used. The `pass` bodies are documented as unreachable. The `shapes` list with polymorphic `area()` calls is clear. Deductions: the `Pizza(Circle)` inheritance is a stretch (a pizza is not a circle). The `FlatCake` class does not inherit from Shape, which is intentional but confusing. No `__main__` guard.

---

### property.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **81** |

**Comment:** Property demonstration. Runs clean (exit 0). The `@property` decorator is correct. Deductions: no `__main__` guard. The property is simple. No error handling.

---

### static_methods.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **81** |

**Comment:** Static methods demonstration. Runs clean (exit 0). The `@staticmethod` decorator is correct. Deductions: no `__main__` guard. The static methods are simple. No error handling.

---

### super.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **81** |

**Comment:** Super demonstration. Runs clean (exit 0). The `super().__init__()` pattern is correct. Deductions: no `__main__` guard. The super usage is simple. No error handling.

---

## python/object_oriented_programming/syntax_fundamentals/

**Note:** This folder is frozen per AGENTS.md rule 1 — files must not be moved, renamed, or have imports rewritten. Scores reflect the frozen state.

### bank_account.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** Bank account class demonstration. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The bank account logic is simple. No error handling.

---

### calculator.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** Calculator class demonstration. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The calculator logic is simple. No error handling.

---

### car.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **81** |

**Comment:** Car class demonstration. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The car logic is simple. No error handling.

---

### device.py — **82/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **82** |

**Comment:** Device hierarchy with abstract base class. The `Device(ABC)` with `@abstractmethod` is correct. The Phone/Laptop/Tablet subclasses are clear. The `super().__init__()` calls are correct. Runs clean (exit 0). Deductions: no `__main__` guard. The subclasses are near-identical.

---

### dice.py — **70/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 75 | 40% | 30.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 65 | 20% | 13.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **70** |

**Comment:** Dice class demonstration. Exit 1 (interactive). The class structure is clear. Deductions: no `__main__` guard. The dice logic is simple. No error handling.

---

### employee_contract.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** Employee contract class demonstration. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The employee contract logic is simple. No error handling.

---

### food.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** Food class demonstration at 99 lines. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The food logic is simple. No error handling.

---

### grocery_caloric_list.py — **65/100** (D — Weak)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 70 | 40% | 28.0 |
| Readability | 65 | 25% | 16.3 |
| Durability | 60 | 20% | 12.0 |
| Robustness | 55 | 15% | 8.3 |
| **Final** | | | **65** |

**Comment:** Grocery caloric list at 286 lines. Exit 1 (interactive). The class structure is present. Deductions: no `__main__` guard. The caloric list logic is unclear. No error handling. The file is long and complex.

---

### item.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** Item class demonstration. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The item logic is simple. No error handling.

---

### order.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** Order class demonstration. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The order logic is simple. No error handling.

---

### payment.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** Payment class demonstration. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The payment logic is simple. No error handling.

---

### person.py — **81/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 90 | 40% | 36.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 75 | 20% | 15.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **81** |

**Comment:** Person class demonstration at 27 lines. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The person logic is simple. No error handling.

---

### point.py — **85/100** (B — Strong)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 95 | 40% | 38.0 |
| Readability | 80 | 25% | 20.0 |
| Durability | 80 | 20% | 16.0 |
| Robustness | 75 | 15% | 11.3 |
| **Final** | | | **85** |

**Comment:** Point class demonstration at 16 lines. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The point logic is simple. No error handling.

---

### real_estate.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** Real estate class demonstration at 93 lines. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The real estate logic is simple. No error handling.

---

### restaurant.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** Restaurant class demonstration. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The restaurant logic is simple. No error handling.

---

### school.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** School class demonstration. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The school logic is simple. No error handling.

---

### sports.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** Sports class demonstration. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The sports logic is simple. No error handling.

---

### user_access.py — **77/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 75 | 25% | 18.8 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 65 | 15% | 9.8 |
| **Final** | | | **77** |

**Comment:** User access class demonstration. Runs clean (exit 0). The class structure is clear. Deductions: no `__main__` guard. The user access logic is simple. No error handling.

---

### worker.py — **75/100** (C — Serviceable)

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Fixability | 85 | 40% | 34.0 |
| Readability | 70 | 25% | 17.5 |
| Durability | 70 | 20% | 14.0 |
| Robustness | 60 | 15% | 9.0 |
| **Final** | | | **75** |

**Comment:** Worker class demonstration at 90 lines. Runs clean (exit 0). The class structure is clear. The `[AI-authored fix]` try/except import block is present (same idiom as classes.py). Deductions: no `__main__` guard. The worker logic is verbose. No error handling.

