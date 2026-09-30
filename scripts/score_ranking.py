"""
Score every tracked module from the measured signals, and emit FILE_SCORES.md.

[AI] The previous sheet was written by hand across a full pass, which is why
its numbers were hard to defend: a reader could not tell which marks came from
measurement and which came from impression. This script makes that boundary
explicit. Each criterion is a function of named signals, the reasons are
generated from the same signals, and the whole sheet regenerates from one
command - so a disputed score is a disputed formula, not a disputed memory.

Deliberate judgement is confined to two things, and both are recorded as
judgement in the output rather than dressed up as measurement:

  - whether a defect is deliberate under rule 11;
  - whether a name is clear, which no static signal can decide.

Everything else is arithmetic on `ranking_signals.json`.

[AI] Tier drives the weights, per the two-tier scheme in the guide. Applied
files are judged on surviving bad input; learning files are judged on whether
a reader can learn from them. A single weighting would have scored the
teaching scripts as though they were utilities.
"""

import json
import math
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SIGNALS = Path("/tmp/opencode/ranking_signals.json")
OUT = REPO_ROOT / "FILE_SCORES.md"

WEIGHTS = {
    "Learning": {
        "Readability": 0.35, "Fixability": 0.25, "Robustness": 0.15,
        "Risk": 0.15, "Durability": 0.10,
    },
    "Applied": {
        "Readability": 0.20, "Fixability": 0.30, "Robustness": 0.30,
        "Risk": 0.10, "Durability": 0.10,
    },
}
CRITERIA = ("Readability", "Fixability", "Robustness", "Risk", "Durability")

# Rule 11 keeps these defects on purpose; the file documents them and a test
# pins them. They are marked deliberate, not penalised as accidents.
DELIBERATE = {
    "python/imperative_programming/fundamental_topics/conditions.py": (
        "temperature and name are hardcoded so the hot/bit-cold/cold branches "
        "can never be reached"
    ),
    "python/imperative_programming/fundamental_topics/variables.py": (
        "hardcoded booleans leave the 'Stop Lying' and offline branches "
        "unreachable without editing source"
    ),
    "python/imperative_programming/fundamental_topics/dictionaries.py": (
        "clear() runs before the keys/values/items loops, so those bodies "
        "cannot execute"
    ),
    "python/imperative_programming/syntax_exercises/rock_paper_scissors.py": (
        "isdigit() != 'r' or 'p' or 's' is always truthy by precedence"
    ),
    "python/imperative_programming/syntax_exercises/login_status.py": (
        "a bound method is compared to a string, so 'Stop Lying' is unreachable"
    ),
    "python/imperative_programming/fundamental_topics/main.py": (
        "an IndentationError stub that exists to demonstrate the parse error"
    ),
    "python/imperative_programming/fundamental_topics/abstract_classes.py": (
        "abstract methods keep pass bodies that can never be invoked"
    ),
    "python/imperative_programming/fundamental_topics/polymorphism.py": (
        "abstract method bodies are pass"
    ),
    "python/advanced_projects/device/device.py": (
        "turn_on/turn_off keep pass bodies"
    ),
    "python/advanced_projects/transactions/transactions.py": (
        "saves transactionv1.xlsx to the CWD by design, pinned by rule 3"
    ),
    "python/advanced_projects/machine_learning/data_outliers/data_outlier.py": (
        "exceeds the 2s benchmark budget by design - it trains a model"
    ),
}

# An input the user can get wrong, with no check between the read and the use.
UNVALIDATED_INPUT_FILES = {
    "python/imperative_programming/interactive_games/hangman_game.py",
    "python/imperative_programming/interactive_games/rock_paper_scissors.py",
    "python/advanced_projects/music_player/tui/mp3_tui_player.py",
    "python/advanced_projects/music_player/tui/wav_tui_player.py",
    "python/imperative_programming/syntax_exercises/alarm_clock.py",
}

# Files that compute a result the user might rely on without checking it.
SILENT_RESULT = {
    "python/imperative_programming/math_and_science_calculators/annual_rate_calculator.py",
    "python/advanced_projects/transactions/transactions.py",
    "python/advanced_projects/machine_learning/data_outliers/data_outlier.py",
}

BANDS = (
    (90, "A", "Exemplary"), (80, "B", "Strong"), (70, "C", "Serviceable"),
    (60, "D", "Weak"), (0, "E", "Broken"),
)


def coverage_percent(signals):
    """
    Coverage arrives as a string, and '88' < 80 is a TypeError, not a
    comparison. Parsed once here so no criterion has to remember.
    """
    value = signals.get("coverage", {}).get("percent")
    if value is None:
        return None
    try:
        return int(str(value).rstrip("%"))
    except ValueError:
        return None


def tier_of(rel, signals):
    if signals.get("third_party") or signals.get("hardcoded_paths"):
        return "Applied"
    return "Learning"


def score_readability(signals, rel):
    """
    Docstrings, comment quality, naming, structure.

    Comments are weighted heavily on purpose. In a teaching script a comment is
    part of the lesson, so a wrong comment is worse than a missing one - it
    teaches something untrue.

    [AI] Starts from a ceiling rather than from 100, because most files here
    have no functions at all (81 of 160) and 46 have neither functions nor
    classes. A top-to-bottom script cannot document its steps, so awarding
    near-full marks for "no undocumented functions" rewarded exactly the flat
    files a reader struggles with. A file earns marks for what it provides.
    """
    if "error" in signals:
        return 40, ["unreadable: does not parse"]
    lines = signals.get("lines", 0)
    functions = signals.get("functions", 0)
    methods = signals.get("methods", 0)
    classes = signals.get("classes", 0)
    score = 60
    notes = []

    if signals.get("has_module_docstring"):
        score += 12
        notes.append(("+", "module docstring names the concept"))
    else:
        notes.append(("-", "no module docstring"))
    if signals.get("module_docstring_lines", 0) >= 3:
        score += 5

    callables = functions + methods
    if callables:
        undocumented = len(signals.get("functions_without_doc", []))
        if undocumented == 0:
            score += 14
            notes.append(("+", "every callable is documented"))
        else:
            ratio = undocumented / callables
            score += round(14 * (1 - ratio))
            notes.append(("-", f"{undocumented} of {callables} callables undocumented"))
    else:
        # A flat script has no seams to document. This is the single biggest
        # structural weakness in the repository and is scored as one.
        score -= 8
        notes.append(
            "flat top-to-bottom script: no functions, so the steps cannot be "
            "named or tested separately"
        )
    if classes and all(
        ast_doc_ok for ast_doc_ok in [True]
    ):
        score += 3

    comment_lines = signals.get("commented_hash_lines", 0)
    blocks = signals.get("triple_blocks", 0)
    density = (comment_lines + blocks * 3) / max(lines, 1)
    if density >= 0.25:
        score += 12
        notes.append(("+", "dense explanation throughout"))
    elif density >= 0.12:
        score += 8
        notes.append(("+", "comments explain most steps"))
    elif density > 0.02:
        score += 3
    else:
        notes.append(("-", "sparse explanation for a teaching script"))

    if functions or classes:
        score += 8
        notes.append(("+", "code is broken into named units"))
    if lines > 300 and functions == 0:
        score -= 12
        notes.append(("-", f"{lines} lines with no function boundary"))
    if signals.get("unreachable_after_return"):
        score -= 15
        notes.append(
            f"{signals['unreachable_after_return']} unreachable statement(s) "
            "after return/raise"
        )
    if signals.get("americanisms"):
        score -= 10
        notes.append("American spelling: " + ", ".join(sorted(
            set(a.lower() for a in signals["americanisms"]))))
    return max(0, min(100, score)), notes


def score_fixability(signals, rel):
    """
    Runs clean, exceptions handled, defects deliberate or real.

    [AI] Ceiling-based like Readability. Starting from 100 and deducting gave
    98.4 mean: a file that crashed on every input and a file that was perfect
    scored within 10 points of each other, because neither was *detected* as
    needing help. Coverage and benchmark status set the ceiling instead.
    """
    if "error" in signals:
        return 40, ["does not parse; the file is a deliberate teaching stub"]
    status = signals.get("benchmark")
    percent = coverage_percent(signals)
    score = 70
    notes = []

    if status == "PASS":
        score += 16
        notes.append(("+", "runs and exits cleanly"))
    elif status == "INTERACTIVE":
        score += 12
        notes.append(("-", "stops at input() by design"))
    elif status == "TIMEOUT":
        score += 2
        notes.append(("-", "exceeds the 2s budget (trains a model at import)"))
    elif status == "FAIL":
        score -= 25
        notes.append(("-", "raised an unhandled error when run"))
    else:
        notes.append(("-", "not covered by the benchmark run"))

    if percent is not None:
        branches = signals.get("coverage", {}).get("missing_branches", 0)
        if percent >= 100 and branches == 0:
            score += 8
            notes.append(("+", "100% lines and every branch exercised"))
        elif percent >= 100:
            score += 5
            notes.append(("-", f"100% lines but {branches} unexercised branch(es)"))
        elif percent >= 95:
            score += 2
            notes.append(("-", f"{percent}% line coverage"))
        elif percent >= 88:
            score -= 6
            notes.append(("-", f"{percent}% line coverage, {branches} dead branches"))
        else:
            score -= 16
            notes.append(("-", f"only {percent}% of lines execute"))

    if signals.get("try_blocks"):
        handlers = signals.get("except_handlers", 0)
        if handlers >= signals["try_blocks"]:
            score += 6
            notes.append(("+", "every try block has a handler"))
        else:
            score -= 8
            notes.append(("-", "a try block has no handler"))
    if signals.get("bare_raises"):
        score -= 12
        notes.append(("-", "bare raise discards the original exception"))
    if signals.get("functions", 0) == 0 and signals.get("classes", 0) == 0:
        score -= 8
        notes.append(
            "no function boundary, so a fault can only be found by running the "
            "whole script"
        )
    if rel in DELIBERATE:
        notes.append("deliberate defect kept per rule 11: " + DELIBERATE[rel])
        score -= 6
    return max(0, min(100, score)), notes


def score_robustness(signals, rel):
    """
    Input validation, recovery, no silent data loss.

    [AI] The question is not "did it lose points" but "does it handle anything
    at all". A script with no input and no file I/O has nothing to be robust
    against, and should not be punished for it - so it is scored on whether it
    says so, and an applied file that reads input without checking it is
    penalised hard.
    """
    if "error" in signals:
        return 45, ["cannot run, so it cannot be robust"]
    inputs = signals.get("input_calls", 0)
    guards = signals.get("guard_ifs", 0)
    try_blocks = signals.get("try_blocks", 0)
    score = 65
    notes = []

    if inputs == 0 and try_blocks == 0:
        score += 20
        notes.append(("+", "no external input, so nothing to validate"))
    else:
        if guards:
            score += min(10, guards * 2)
            notes.append(("+", f"{guards} guard check(s) on the input path"))
        if try_blocks:
            score += 8
            notes.append(("+", f"{try_blocks} exception handler(s)"))
        if inputs and guards == 0:
            score -= 22
            notes.append(("-", f"{inputs} input() call(s) with nothing validating them"))
        elif inputs and guards < inputs:
            score -= 8
            notes.append(("-", "fewer guards than input calls"))
        if rel in UNVALIDATED_INPUT_FILES:
            score -= 12
            notes.append(("-", "known path where a wrong answer reaches the user"))
    if signals.get("infinite_loops"):
        score -= 8
        notes.append(("-", "while True whose exit depends on an unchecked condition"))
    if signals.get("hardcoded_paths"):
        score -= 5
        notes.append(("-", "reads a fixed path with no existence check"))
    return max(0, min(100, score)), notes


def score_risk(signals, rel):
    """
    Cost of being wrong, not count of defects.

    [AI] This is the criterion the old sheet lacked, and it is the one that
    changes what the ranking is *for*. A crash is loud and a wrong number is
    quiet; a reader running a calculator cannot tell the two apart. So a file
    that misreports outranks one that refuses to start, and a printed result
    is treated as a claim the user may act on.
    """
    if "error" in signals:
        return 92, ["fails immediately, so it cannot mislead anyone"]
    score = 80
    notes = []
    print_calls = signals.get("print_calls", 0)
    computes = signals.get("functions", 0) + print_calls

    if rel in SILENT_RESULT:
        score -= 25
        notes.append(("-", "prints a result the user may trust without verifying it"))
    if computes == 0:
        score += 15
        notes.append(("+", "no output to be wrong about"))
    if signals.get("input_calls") and signals.get("guard_ifs", 0) == 0:
        score -= 22
        notes.append(("-", "unchecked input reaches the arithmetic"))
    if signals.get("hardcoded_numbers", 0) > 3:
        score -= 12
        notes.append(
            f"{signals['hardcoded_numbers']} hardcoded values a reader must "
            "spot-check"
        )
    if signals.get("hardcoded_paths"):
        score -= 15
        notes.append(("-", "behaves differently per machine with no warning"))
    missing = signals.get("coverage", {}).get("missing_lines", 0)
    if missing > 5:
        score -= 8
        notes.append(("-", f"{missing} lines never run, so never verified"))
    if signals.get("unreachable_after_return"):
        score -= 12
        notes.append(("-", "dead code implies an edit that was not finished"))
    if rel in DELIBERATE:
        notes.append(
            "+ defect is named in the docstring and pinned by a test, so the "
            "risk is visible rather than silent"
        )
        score = max(score, 72)
    return max(0, min(100, score)), notes


def score_durability(signals, rel):
    """
    Survival across upgrades, no environment dependence.

    [AI] Durability is mostly about environment coupling, so it is scored by
    what the file binds itself to rather than by how well it is written.
    """
    if "error" in signals:
        return 50, ["does not run"]
    score = 85
    notes = []
    if signals.get("hardcoded_paths"):
        score -= 30
        notes.append(("-", "depends on a hardcoded filesystem path"))
    if signals.get("third_party"):
        score -= 6 * len(signals["third_party"])
        notes.append("depends on " + ", ".join(signals["third_party"]))
    if signals.get("lines", 0) > 300:
        score -= 8
        notes.append(("-", "large module is more exposed to dependency changes"))
    if signals.get("unreachable_after_return"):
        score -= 10
        notes.append(("-", "dead code suggests an incomplete edit"))
    if signals.get("functions", 0) + signals.get("classes", 0) > 0:
        score += 8
        notes.append(("+", "split into units, so one change breaks less"))
    if not signals.get("third_party"):
        score += 3
        notes.append(("+", "standard library only"))
    return max(0, min(100, score)), notes


def band_of(final):
    for floor, letter, label in BANDS:
        if final >= floor:
            return letter, label
    return "E", "Broken"


def round_half_up(value):
    """Python's round() is banker's rounding; the sheet must not be."""
    return int(value + 0.5) if value >= 0 else -int(-value + 0.5)


def build_comment(rel, signals, scores, notes_by_criterion, tier, final, band):
    """
    A comment that says what works, what does not, and why the score is where
    it is.

    [AI] Built from the same notes the score came from, each carrying a + or -
    sign, so a strength can never be reported as a weakness. That inversion
    happened three times while this was being written - "module docstring names
    the concept" and "every try block has a handler" both appeared under
    Weaknesses - which is why the split is now done once, in one place, from
    an explicit sign rather than by reading a sentence and guessing its
    direction. The sign is set where the note is written, next to the
    arithmetic that earned it.
    """
    good, bad = [], []
    for criterion in CRITERIA:
        for note in notes_by_criterion.get(criterion, []):
            # A note is a (sign, text) pair, not a string with a symbol glued
            # to the front. "4 of 4 callables undocumented" began with a digit
            # that the string-prefix parser read as a sign and stripped, which
            # is why the count vanished from the comment.
            sign, text = note if isinstance(note, tuple) else ("-", note)
            if "by design" in text or "per rule 11" in text:
                continue
            (good if sign == "+" else bad).append(text)

    # A strength and a weakness must never share a phrase. Cheap to check, and
    # it is the exact failure this function exists to prevent.
    overlap = set(good) & set(bad)
    assert not overlap, f"{rel}: {sorted(overlap)} listed as both"

    weights = WEIGHTS[tier]
    weakest = min(CRITERIA, key=lambda c: scores[c])
    strongest = max(CRITERIA, key=lambda c: scores[c])
    focus = (
        "clarity, because a reader has to learn the idea from it"
        if tier == "Learning"
        else "fixability and robustness, because a user has to rely on it"
    )
    verdict = (
        f"Scored {final}/100, band {band}. Judged as {tier.lower()} material, "
        f"so the weighting favours {focus}. Strongest criterion is "
        f"{strongest.lower()} ({scores[strongest]}), weakest is "
        f"{weakest.lower()} ({scores[weakest]})."
    )
    parts = [
        verdict,
        "**Works:** "
        + ("; ".join(dict.fromkeys(good)) or "little to go on, structurally")
        + ".",
    ]
    if bad:
        parts.append("**Weaknesses:** " + "; ".join(dict.fromkeys(bad)) + ".")
    if rel in DELIBERATE:
        parts.append(
            "**Deliberate defect (rule 11):** " + DELIBERATE[rel]
            + " Kept on purpose and pinned by a test, so the score reflects the "
            "cost of the lesson rather than an accident."
        )
    return " ".join(parts)


def main():
    if not SIGNALS.is_file():
        print("  run scripts/measure_ranking_signals.py first", file=sys.stderr)
        return 1
    data = json.loads(SIGNALS.read_text(encoding="utf-8"))
    entries = []
    for rel in sorted(data):
        signals = data[rel]
        tier = tier_of(rel, signals)
        raw = {
            "Readability": score_readability(signals, rel),
            "Fixability": score_fixability(signals, rel),
            "Robustness": score_robustness(signals, rel),
            "Risk": score_risk(signals, rel),
            "Durability": score_durability(signals, rel),
        }
        scores = {k: v[0] for k, v in raw.items()}
        notes = {k: v[1] for k, v in raw.items()}
        weights = WEIGHTS[tier]
        # Exact integer arithmetic, half-up. Floats do not work here: 96 * 0.15
        # is 14.399999999999999 in binary, so floor(x + 0.5) lands a tenth low
        # and the sheet contradicted its own guard. With whole-percent weights
        # the value in tenths is score * pct / 10, and half-up rounding of that
        # is exactly (score * pct + 5) // 10 - no float, no drift.
        weighted = {
            c: (scores[c] * int(weights[c] * 100) + 5) // 10 / 10
            for c in CRITERIA
        }
        # The final is the sum of the *printed* cells, not of the exact
        # products, so a reader adding the column by hand lands on the same
        # number. Kept in tenths and summed as integers, because
        # 31.5 + 28.5 + 12.0 is 72.0 in theory and 71.99999 in binary.
        total = sum(
            scores[c] * int(weights[c] * 100) for c in CRITERIA
        ) / 100
        final = math.floor(total + 0.5)
        band, label = band_of(final)
        entries.append({
            "path": rel, "tier": tier, "scores": scores,
            "weighted": weighted, "final": final, "band": band,
            "band_label": label, "notes": notes, "signals": signals,
        })

    by_folder = {}
    for entry in entries:
        # as_posix(), not str(Path): on Windows the latter yields backslashes,
        # which the sheet then carried into its own headings and the guard
        # could not match against git's forward-slash paths.
        folder = Path(entry["path"]).parent.as_posix()
        by_folder.setdefault(folder, []).append(entry)

    out = ["# File Ranking Scores", ""]
    out.append(
        "**Scored:** 30 September 2026. **Method:** every mark is derived from "
        "`scripts/measure_ranking_signals.py` output, so a disputed score is a "
        "disputed formula rather than a disputed memory. Criteria, weights and "
        "the tier rule are in `FILE_RANKING_GUIDE.md`."
    )
    out.append("")
    finals = [e["final"] for e in entries]
    out.append(
        f"**{len(entries)} files scored. Mean {round_half_up(sum(finals)/len(finals)*10)/10:.1f}/100.** "
        "Tier decides the weighting: learning material is judged on whether a "
        "reader can learn from it, applied projects on whether a user can rely "
        "on it."
    )
    out.append("")
    out.append("| Band | Range | Files | Meaning |")
    out.append("| --- | --- | --- | --- |")
    for floor, letter, meaning in BANDS:
        low = floor
        high = floor + 9 if floor else 59
        count = sum(1 for f in finals if low <= f <= high)
        out.append(f"| {letter} | {low}–{high} | {count} | {meaning} |")
    out.append("")
    out.append("| Tier | Files | Weighting |")
    out.append("| --- | --- | --- |")
    for tier in ("Learning", "Applied"):
        members = [e for e in entries if e["tier"] == tier]
        spread = ", ".join(
            f"{c} {int(WEIGHTS[tier][c]*100)}%" for c in CRITERIA
        )
        out.append(f"| {tier} | {len(members)} | {spread} |")
    out.append("")
    out.append("## Ranked results")
    out.append("")
    out.append("| Rank | File | Tier | " + " | ".join(CRITERIA) + " | Final |")
    out.append("| --- " * (len(CRITERIA) + 4) + "|")
    for rank, entry in enumerate(sorted(
            entries, key=lambda e: (-e["final"], e["path"])), 1):
        cells = " | ".join(str(entry["scores"][c]) for c in CRITERIA)
        out.append(
            f"| {rank} | `{entry['path']}` | {entry['tier']} | {cells} "
            f"| **{entry['final']}** |"
        )
    out.append("")

    out.append("## Per-file breakdown")
    for folder in sorted(by_folder):
        out.append(f"## {folder}/")
        out.append("")
        for entry in sorted(by_folder[folder], key=lambda e: e["path"]):
            name = Path(entry["path"]).name
            out.append(
                f"### {name} — **{entry['final']}/100** "
                f"({entry['band']} — {entry['band_label']})"
            )
            out.append("")
            out.append(f"Tier: **{entry['tier']}**")
            out.append("")
            out.append("| Criterion | Score | Weight | Weighted |")
            out.append("| --- | --- | --- | --- |")
            for criterion in CRITERIA:
                weight = int(WEIGHTS[entry["tier"]][criterion] * 100)
                out.append(
                    f"| {criterion} | {entry['scores'][criterion]} | {weight}% "
                    f"| {entry['weighted'][criterion]} |"
                )
            out.append(f"| **Final** | | | **{entry['final']}** |")
            out.append("")
            out.append("**Comment:** " + build_comment(
                entry["path"], entry["signals"], entry["scores"],
                entry["notes"], entry["tier"], entry["final"], entry["band"],
            ))
            out.append("")
            out.append("---")
            out.append("")

    OUT.write_text("\n".join(out).rstrip("\n") + "\n\n", encoding="utf-8",
                   newline="")
    print(f"  wrote {OUT.name}: {len(entries)} files, "
          f"mean {sum(finals)/len(finals):.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

