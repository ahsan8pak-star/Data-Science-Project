"""
Guards for the file-ranking markdown pair and the figures quoted from it.

The score sheet was reconciled by hand once: 167 headings for 161 real files
(one folder was written out twice), 112 headings that had drifted away from
their own tables, and 9 entries whose Final rounded an exact .5 weighted sum
downwards while the other 50 rounded it upwards. A hand audit is not a
control - it fixes today's file and does nothing about tomorrow's edit - so
the invariants live here instead and fail the suite if the sheet drifts again.

Three things are guarded:

1. FILE_SCORES.md covers every non-`__init__` module under python/ exactly
   once, and no path that does not exist.
2. Every number in the sheet is self-consistent: the Weighted cell is the
   criterion score times its weight, the Final is that sum rounded half away
   from zero, the heading repeats the Final, and the band label matches.
3. The figures AGENTS.md and NOTES.md quote from the sheet (overall average,
   how many files fall below 70, the weakest pair, the top three) are still
   true, and FILE_RANKING_GUIDE.md's pre-verified table agrees with the sheet
   rather than carrying a second, older set of numbers.

Nothing here writes to the repository; every check is a read.
"""

import math
import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORES_MD = REPO_ROOT / "FILE_SCORES.md"
GUIDE_MD = REPO_ROOT / "FILE_RANKING_GUIDE.md"
AGENTS_MD = REPO_ROOT / "AGENTS.md"
NOTES_MD = REPO_ROOT / "NOTES.md"

"""
The two-tier weighting from FILE_RANKING_GUIDE.md. A learning script is
judged on whether a reader can learn from it; an applied project on whether
a user can rely on it. The same file therefore carries different weights
depending on which question it is being asked to answer.
"""
TIER_WEIGHTS = {
    "Learning": {
        "Readability": 35, "Fixability": 25, "Robustness": 15,
        "Risk": 15, "Durability": 10,
    },
    "Applied": {
        "Readability": 20, "Fixability": 30, "Robustness": 30,
        "Risk": 10, "Durability": 10,
    },
}
CRITERIA = ("Readability", "Fixability", "Robustness", "Risk", "Durability")

"""
Band table from FILE_RANKING_GUIDE.md: inclusive (low, high) per band letter.

E's lower bound is 0 rather than 50, so the ranges tile 0-100 with no gap and
no overlap. The contiguity check walks the bands in order and requires each to
start one above the previous one's top.
"""
BANDS = {
    "A": (90, 100, "Exemplary"),
    "B": (80, 89, "Strong"),
    "C": (70, 79, "Serviceable"),
    "D": (60, 69, "Weak"),
    "E": (0, 59, "Broken"),
}

"""
[AI] The three patterns below are matched line-by-line against the sheet, so
they are anchored with ^...$ and pre-compiled once at import. CRITERION_RE
carries re.M because findall() scans the whole worked-example block in the
guide, where ^/$ must anchor per line rather than per string.
"""
HEADING_RE = re.compile(
    r"^### (?P<rel>[\w./]+\.py) — \*\*(?P<score>\d+)/100\*\* "
    r"\((?P<band>[A-F]) — (?P<label>[^)]*)\)\s*$"
)
CRITERION_RE = re.compile(
    r"^\| (?P<name>Readability|Fixability|Robustness|Risk|Durability) \| "
    r"(?P<score>\d+) \| (?P<pct>\d+)% \| (?P<weighted>[\d.]+) \|$",
    re.M,
)
TIER_RE = re.compile(r"^Tier: \*\*(?P<tier>Learning|Applied)\*\*$", re.M)
FINAL_RE = re.compile(r"^\| \*\*Final\*\* \| \| \| \*\*(?P<final>\d+)\*\* \|$")


class Entry:
    """
    One scored file, parsed out of FILE_SCORES.md.

    [AI] criteria holds the raw criterion scores keyed by name, while
    weighted_cells keeps the *printed* cell beside the criterion it came from.
    Keeping both is what lets one entry be checked two ways - the printed cells
    must agree with the criteria, and the Final must agree with their sum -
    without re-parsing the table. A doc that disagreed with itself would
    otherwise pass whichever half was read first.
    """

    def __init__(self, path, score, band, label, criteria, weighted_cells,
                 final, tier="Learning"):
        self.path = path
        self.tier = tier
        self.score = score
        self.band = band
        self.label = label
        self.criteria = criteria
        self.weighted_cells = weighted_cells
        self.final = final
        self.tier = tier

    @property
    def name(self):
        """Basename, for matching against a doc that names files without paths."""
        return self.path.rsplit("/", 1)[-1]

    def weighted_total(self):
        """
        The five criteria recombined on the 0-100 scale, unrounded, using the
        weights for this entry's own tier.
        """
        table = TIER_WEIGHTS[self.tier]
        return math.fsum(
            score * table[name] for name, score in self.criteria.items()
        ) / 100

    def __repr__(self):
        # Without this, a failing parametrised run prints 161 identical-looking
        # objects and the useful path never reaches the terminal.
        return f"<Entry {self.path} final={self.final}>"


def _round_half_up(value):
    """
    Round to the nearest whole number, sending an exact half upwards.

    [AI-authored fix] The sheet has always been predominantly half-up (50 of
    its 59 exact-.5 weighted sums), and the nine exceptions disagreed with
    entries of an identical sum - rock_paper_scissors.py at 74.5 became 75
    while qrcode_generator.py at 74.5 became 74 - so half-up is the intended
    convention and the minority was the defect; this helper is what the nine
    were corrected with. Python's built-in round() is not usable here because
    it breaks ties to even, which would send 74.5 down as well as 76.5.
    """
    return int(math.floor(value + 0.5))


def _parse_scores_sheet():
    """Read FILE_SCORES.md into a list of Entry, one per ### heading."""
    entries = []
    section = None
    lines = SCORES_MD.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        if line.startswith("## "):
            section = line[3:].strip().rstrip("/")
        heading = HEADING_RE.match(line)
        if heading is None:
            continue

        criteria, weighted_cells, final = {}, [], None
        tier = "Learning"
        for row in lines[index + 1:index + 12]:
            tier_row = TIER_RE.match(row)
            if tier_row is not None:
                tier = tier_row.group("tier")
                continue
            criterion = CRITERION_RE.match(row)
            if criterion is not None:
                criteria[criterion.group("name")] = int(criterion.group("score"))
                weighted_cells.append(
                    (criterion.group("name"), float(criterion.group("weighted")))
                )
                continue
            final_row = FINAL_RE.match(row)
            if final_row is not None:
                final = int(final_row.group("final"))
                break

        entries.append(
            Entry(
                path=f"{section}/{heading.group('rel')}",
                score=int(heading.group("score")),
                band=heading.group("band"),
                label=heading.group("label"),
                criteria=criteria,
                weighted_cells=weighted_cells,
                final=final,
                tier=tier,
            )
        )
    return entries


def _real_module_paths():
    """
    Every tracked non-__init__ module under python/, repo-relative POSIX.

    [AI] Tracked files, not whatever is on disk. The score sheet describes the
    repository, so an untracked practice file must not be counted as a module
    awaiting a score - sandbox/aim.py is gitignored on purpose, and reading it
    here would have let the sheet claim to rank a file the repo does not
    contain. rglob() also walked .pyc-adjacent scratch copies.
    """
    tracked = subprocess.run(
        ["git", "ls-files", "python"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    return sorted(
        path for path in tracked
        if path.endswith(".py") and not path.endswith("__init__.py")
    )


@pytest.fixture(scope="module")
def entries():
    return _parse_scores_sheet()


@pytest.fixture(scope="module")
def by_path(entries):
    return {entry.path: entry for entry in entries}


class TestScoreSheetCoverage:
    """
    The sheet must describe the tree, not a memory of it. The duplicate
    converter section that produced 167 headings for 161 files is the exact
    failure this class exists to prevent.
    """
    def test_one_entry_per_module_under_python(self, entries):
        assert len(entries) == len(_real_module_paths())

    def test_every_module_is_scored_exactly_once(self, entries):
        paths = [entry.path for entry in entries]
        assert len(paths) == len(set(paths))

    def test_no_entry_points_at_a_missing_file(self, entries):
        missing = [e.path for e in entries if not (REPO_ROOT / e.path).is_file()]
        assert missing == []

    def test_no_module_is_left_unscored(self, entries):
        scored = {entry.path for entry in entries}
        unscored = [p for p in _real_module_paths() if p not in scored]
        assert unscored == []

    def test_no_folder_section_is_repeated(self):
        sections = [
            line[3:].strip().rstrip("/")
            for line in SCORES_MD.read_text(encoding="utf-8").splitlines()
            if line.startswith("## ")
        ]
        duplicates = sorted({s for s in sections if sections.count(s) > 1})
        assert duplicates == []

    def test_no_comment_leaks_a_sign_or_a_stray_marker(self, entries):
        """
        A rendered comment must never show the machinery that built it.

        [AI] Implicit string concatenation looks identical to a (sign, text)
        tuple in source, so a note written as
        `notes.append(("- x " "y"))` parses as a plain string and is treated as
        a weakness. It shipped once, in main.py's entry, where a strength
        appeared under Weaknesses with a leading `+`. Nothing else catches it:
        the overlap assertion only fires on a phrase listed twice, and a
        mis-signed note appears exactly once.
        """
        text = SCORES_MD.read_text(encoding="utf-8")
        offenders = []
        for block in text.split("### ")[1:]:
            name = block.split(" \u2014")[0]
            for marker in ("Works", "Weaknesses"):
                clause = re.search(r"\*\*" + marker + r":\*\* ([^\n]*)", block)
                if clause is None:
                    continue
                if re.search(r"(^|; )[+-] ", clause.group(1)):
                    offenders.append(name + " under " + marker)
        assert offenders == [], (
            "a rendered comment leaks a + or - sign, which means the note was "
            "written as a plain string rather than a (sign, text) tuple: "
            + str(offenders)
        )

    def test_every_entry_carries_a_comment(self, entries):
        """
        Each entry is expected to say what works, what does not, why it
        scored as it did and what would fix it - the guide's sincere-comment
        rule. A bare table with no prose is the failure this catches.
        """
        blocks = re.split(
            r"(?m)^(?=### )", SCORES_MD.read_text(encoding="utf-8")
        )
        headed = [b for b in blocks if b.startswith("### ")]
        assert len(headed) == len(entries)
        silent = [
            b.splitlines()[0] for b in headed if "**Comment:**" not in b
        ]
        assert silent == []


class TestScoreSheetArithmetic:
    """
    The sheet is a computed artefact: criterion score x weight, summed, then
    rounded. Each of those three steps is checked, because a reader who adds
    the column by hand must land on the number printed above it.
    """
    def test_every_entry_has_all_five_criteria(self, entries):
        """
        Five criteria, not four: Risk was added because "is it broken" and
        "what happens if it is" are different questions, and collapsing them
        hid every failure that produces a wrong answer quietly.
        """
        incomplete = [
            e.path for e in entries if set(e.criteria) != set(CRITERIA)
        ]
        assert incomplete == []

    def test_every_entry_declares_a_known_tier(self, entries):
        unknown = [
            e.path for e in entries if e.tier not in TIER_WEIGHTS
        ]
        assert unknown == []

    def test_every_entry_has_a_final_row(self, entries):
        assert [e.path for e in entries if e.final is None] == []

    def test_weighted_cell_equals_score_times_weight(self, entries):
        """
        The cell shows one decimal place, so the check is against the value
        rounded to one decimal - a bare tolerance would be wrong at the
        boundary, where 85 x 25% is 21.25 and the sheet prints 21.3.
        """
        wrong = []
        for entry in entries:
            table = TIER_WEIGHTS[entry.tier]
            for name, shown in entry.weighted_cells:
                expected = _round_half_up(
                    entry.criteria[name] * table[name] / 100 * 10
                ) / 10
                if abs(expected - shown) > 1e-9:
                    wrong.append(
                        f"{entry.path} {name}: cell {shown} != {expected}"
                    )
        assert wrong == []

    def test_weights_match_the_documented_table(self, entries):
        """
        The weights are per tier, so the guide is checked tier by tier rather
        than as one flat table. A single dict was what stopped the old sheet
        from saying that a teaching script and an application need different
        questions asked of them.

        [AI] Two tables in the guide start with "| Tier |": the definition
        table and the weighting table. The first attempt at this check matched
        the definition table and read a sentence as a percentage, so the
        search is anchored on the weighting header and the rows are looked for
        only below it.
        """
        guide = GUIDE_MD.read_text(encoding="utf-8")
        header = re.search(
            r"^\|\s*Tier\s*\|\s*Files\s*\|\s*Readability([^\n]*)$",
            guide, re.M,
        )
        assert header, "the guide's tier weighting table has no header"
        after = guide[header.end():]
        names = ["Readability"] + [
            c.strip() for c in header.group(1).split("|") if c.strip()
        ]
        for tier, table in TIER_WEIGHTS.items():
            row = re.search(
                rf"^\|\s*\*\*{tier}\*\*\s*\|([^\n]*)$", after, re.M
            )
            assert row, f"the guide has no weighting row for {tier}"
            values = [c.strip() for c in row.group(1).split("|")]
            stated = {}
            # values[0] is the file count; the percentages follow it.
            for name, cell in zip(names, values[1:]):
                match = re.match(r"(\d+)%", cell)
                if match:
                    stated[name] = int(match.group(1))
            assert stated == table, (
                f"the guide states {stated} for {tier}, the sheet uses {table}"
            )

    def test_final_is_the_weighted_sum_rounded_half_up(self, entries):
        wrong = [
            f"{e.path}: weighted {e.weighted_total():.2f} -> "
            f"{_round_half_up(e.weighted_total())} but sheet says {e.final}"
            for e in entries
            if _round_half_up(e.weighted_total()) != e.final
        ]
        assert wrong == []

    def test_heading_repeats_the_final(self, entries):
        wrong = [
            f"{e.path}: heading {e.score} != final {e.final}"
            for e in entries
            if e.score != e.final
        ]
        assert wrong == []


class TestScoreSheetBands:
    """
    A band is a range, so the label is derivable rather than editorial. A
    score of 56 carrying "D — Weak" was a real defect: D starts at 60.
    """
    def test_band_letter_matches_the_final(self, entries):
        wrong = [
            f"{e.path}: final {e.final} labelled {e.band}"
            for e in entries
            if not BANDS[e.band][0] <= e.final <= BANDS[e.band][1]
        ]
        assert wrong == []

    def test_label_matches_the_band(self, entries):
        wrong = [
            f"{e.path}: band {e.band} labelled '{e.label}', "
            f"expected '{BANDS[e.band][2]}'"
            for e in entries
            if e.label != BANDS[e.band][2]
        ]
        assert wrong == []

    def test_bands_are_contiguous_and_cover_0_to_100(self):
        covered = []
        for low, high, _ in BANDS.values():
            covered.extend(range(low, high + 1))
        assert sorted(covered) == list(range(101))


class TestGuideWorkedExample:
    """
    The worked example in the guide is the template every entry is copied
    from, so it has to obey the same arithmetic as the sheet it documents.

    [AI] Rewritten for the two-tier scheme. It previously read a pre-verified
    table of four criteria and an "Output Format" section, both of which the
    rescore replaced. The example is now checked against a real file in the
    sheet, which is a stronger test: the guide cannot drift from the artefact
    it is describing, because the numbers come from the artefact.
    """

    EXAMPLE = "python/advanced_projects/music_player/tui/mp3_tui_player.py"

    def _example_block(self):
        text = GUIDE_MD.read_text(encoding="utf-8")
        assert text.count("## Worked example") == 1, (
            "the guide must carry exactly one worked example, so the checks "
            "below cannot pass against an unrelated table"
        )
        return text.split("## Worked example", 1)[1]

    def test_example_heading_matches_its_final(self, by_path):
        block = self._example_block()
        heading = re.search(r"^### .* — \*\*(\d+)/100\*\*", block, re.M)
        final = re.search(r"\| \*\*Final\*\* \| \| \| \*\*(\d+)\*\* \|", block)
        assert heading and final, "the example has no heading or no Final row"
        assert int(heading.group(1)) == int(final.group(1))

    def test_example_criteria_match_the_real_file(self, by_path):
        """
        The example must be a real entry, not an illustration.

        A worked example invented for the guide drifts from reality within one
        edit, and then teaches the wrong thing. Taking the numbers from the
        file it names makes that impossible to do by accident.
        """
        entry = by_path.get(self.EXAMPLE)
        assert entry is not None, (
            f"the worked example names {self.EXAMPLE}, which is not in "
            "FILE_SCORES.md"
        )
        block = self._example_block()
        rows = {m.group("name"): int(m.group("score"))
                for m in CRITERION_RE.finditer(block)}
        assert rows == entry.criteria, (
            f"the guide shows {rows}, the sheet has {entry.criteria} for "
            f"{self.EXAMPLE}"
        )

    def test_example_weighted_cells_match_their_criteria(self, by_path):
        block = self._example_block()
        entry = by_path[self.EXAMPLE]
        table = TIER_WEIGHTS[entry.tier]
        rows = CRITERION_RE.findall(block)
        assert rows, "no criteria rows found in the worked example"
        assert [name for name, _, _, _ in rows] == list(CRITERIA)
        for name, score, pct, weighted in rows:
            assert int(pct) == table[name], (
                f"{name}: the example shows {pct}%, the {entry.tier} tier "
                f"weights it {table[name]}%"
            )
            expected = (int(score) * table[name] + 5) // 10 / 10
            assert abs(float(weighted) - expected) <= 1e-9, name

    def test_example_final_matches_the_sum_of_its_own_cells(self, by_path):
        block = self._example_block()
        entry = by_path[self.EXAMPLE]
        final = re.search(r"\| \*\*Final\*\* \| \| \| \*\*(\d+)\*\* \|", block)
        assert final
        assert int(final.group(1)) == entry.final, (
            f"the example's Final is {final.group(1)}, the sheet says "
            f"{entry.final}"
        )


class TestQuotedFigures:
    """
    AGENTS.md and NOTES.md both summarise the sheet in prose. Prose is the
    part that goes stale silently, so the specific claims are pinned to the
    computed numbers rather than trusted.
    """
    @staticmethod
    def _flat(path):
        return " ".join(path.read_text(encoding="utf-8").split())

    def _current_claims(self, path):
        """
        The figures a document is currently claiming.

        [AI] NOTES.md is an append-only maintenance log and the ranking has
        been done twice, so it carries two sets of figures and only one is
        live. Reading the whole file compares the sheet against the *oldest*
        row every time, which is a check that cannot pass and teaches nothing.
        A row marked SUPERSEDED is history and is excluded, case-insensitively
        so the marker can be shouted in the table; what remains is the set of
        claims that must agree with the sheet.
        """
        flat = self._flat(path)
        if path != NOTES_MD:
            return flat
        rows = re.split(r"\|\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+\d", flat)
        live = [
            row for row in rows
            if "superseded" not in row.lower()
        ]
        assert live, "every NOTES.md row is marked superseded"
        return " ".join(live)

    def _computed(self, entries):
        finals = sorted(
            (entry.final, entry.name, entry.path) for entry in entries
        )
        scores = [final for final, _, _ in finals]
        return {
            "mean": sum(scores) / len(scores),
            "below": sum(1 for s in scores if s < 70),
            "weakest": [name for _, name, _ in finals[:2]],
            "weakest_scores": [score for score, _, _ in finals[:2]],
              "top": [
                  name for _, name, _ in
                  sorted(finals, key=lambda f: (-f[0], f[2]))[:3]
              ],
              "top_scores": [
                  s for s, _, _ in
                  sorted(finals, key=lambda f: (-f[0], f[2]))[:3]
              ],
        }

    @pytest.mark.parametrize("doc", [AGENTS_MD, NOTES_MD])
    def test_overall_average_is_quoted_correctly(self, doc, entries):
        stated = re.search(r"Overall average: ([\d.]+)/100", self._current_claims(doc))
        assert stated, "no overall average quoted"
        expected = round(self._computed(entries)["mean"], 1)
        assert float(stated.group(1)) == expected

    @pytest.mark.parametrize("doc", [AGENTS_MD, NOTES_MD])
    def test_below_seventy_count_is_quoted_correctly(self, doc, entries):
        stated = re.search(r"Only (\d+) files score below", self._current_claims(doc))
        assert stated, "no below-70 count quoted"
        assert int(stated.group(1)) == self._computed(entries)["below"]

    @pytest.mark.parametrize("doc", [AGENTS_MD, NOTES_MD])
    def test_weakest_pair_is_quoted_correctly(self, doc, entries):
        flat = self._current_claims(doc)
        """
        The weakest two need not tie. They tied when main.py scored 50 on its
        own, but after it was repaired the lowest two sit at 64 and 69, so
        the "(n each)" phrasing no longer applies. Both the names and the
        numbers are checked independently of how the sentence is worded.
        """
        pair = re.search(
            r"`([\w.]+\.py)` \((\d+)\) and `([\w.]+\.py)` \((\d+)\)", flat
        )
        tied = re.search(
            r"`([\w.]+\.py)` and `([\w.]+\.py)` \((\d+) each\)", flat
        )
        stated = pair or tied
        assert stated, (
            "no weakest-pair claim quoted; expected either two separately "
            "scored files or two tied ones"
        )
        computed = self._computed(entries)
        groups = stated.groups()
        if len(groups) == 4:
            names, scores = [groups[0], groups[2]], [groups[1], groups[3]]
        else:
            names, scores = [groups[0], groups[1]], [groups[2]] * 2
        for name, score in zip(names, scores):
            assert name in computed["weakest"], (
                f"{name} is not one of the two weakest files; the sheet says "
                f"{computed['weakest']}"
            )
            assert int(score) == dict(
                zip(computed["weakest"], computed["weakest_scores"])
            )[name], f"{name} is quoted at {score}, the sheet says otherwise"

    def test_notes_quotes_the_top_three_correctly(self, entries):
        """
        Scope to the "Top files:" sentence. NOTES.md also quotes branch
        counts for individual files elsewhere, and a repo-wide scan for
        "`name.py` (n)" would sweep those up as if they were rankings.
        """
        # _current_claims has already dropped the superseded pass, so the only
        # remaining "Top files:" clause is the live one.
        flat = self._current_claims(NOTES_MD)
        clauses = re.findall(r"Top files: (.+?)\.\s", flat)
        assert len(clauses) == 1, (
            f"expected exactly one live top-files claim, found {len(clauses)}; "
            "a superseded pass was not marked as one"
        )
        newest = clauses[0]
        stated = re.findall(r"`([\w.]+\.py)` \((\d+)\)", newest)
        assert stated, "no top-file claim quoted"
        computed = self._computed(entries)
        for name, score in stated:
            assert name in computed["top"], f"{name} is not a top-three file"
            assert int(score) == dict(
                zip(computed["top"], computed["top_scores"])
            )[name]

    @pytest.mark.parametrize("doc", [AGENTS_MD, NOTES_MD])
    def test_named_average_band_matches_its_value(self, doc):
        stated = re.search(
            r"Overall average: [\d.]+/100 \(band ([A-F]) —", self._current_claims(doc)
        )
        assert stated, "no band quoted for the average"
        value = float(re.search(r"Overall average: ([\d.]+)/100", self._current_claims(doc)).group(1))
        expected = next(
            band for band, (low, high, _) in BANDS.items()
            if low <= value <= high
        )
        assert stated.group(1) == expected


class TestRenamedRankingFilesAreReferencedLive:
    """
    The pair was renamed (FILE_RANKING_FRAMEWORK.md -> FILE_RANKING_GUIDE.md,
    RANKINGS.md -> FILE_SCORES.md). A stale reference reads as a broken link
    to anyone who follows it.
    """
    STALE = ("RANKINGS.md", "FILE_RANKING_FRAMEWORK.md")

    @pytest.mark.parametrize(
        "doc",
        [AGENTS_MD, NOTES_MD, REPO_ROOT / "README.md", SCORES_MD, GUIDE_MD],
    )
    def test_no_reference_to_a_pre_rename_filename(self, doc):
        text = doc.read_text(encoding="utf-8")
        found = [name for name in self.STALE if name in text]
        assert found == [], f"{doc.name} still references {found}"

    @pytest.mark.parametrize("doc", [AGENTS_MD, NOTES_MD, REPO_ROOT / "README.md"])
    def test_named_ranking_files_exist(self, doc):
        text = doc.read_text(encoding="utf-8")
        for name in ("FILE_SCORES.md", "FILE_RANKING_GUIDE.md"):
            if name in text:
                assert (REPO_ROOT / name).is_file(), f"{doc.name} names missing {name}"


class TestRankingDocsUseLfLineEndings:
    """
    .gitattributes pins `* text=auto eol=lf`, so the canonical form of these
    files is LF. The trap is that a rewrite through the Windows venv
    interpreter re-emits CRLF: pathlib's write_text leaves newline=None, and
    on Windows that translates every \\n to \\r\\n, so a file fixed to LF goes
    back to CRLF the next time a script rewrites it. Git then normalises on
    commit and the working copy quietly disagrees with the index, which shows
    up as churn in `git diff` on a file that "has not changed".
    """
    @pytest.mark.parametrize(
        "doc",
        [SCORES_MD, GUIDE_MD, AGENTS_MD, NOTES_MD, REPO_ROOT / "README.md"],
    )
    def test_no_carriage_returns(self, doc):
        raw = doc.read_bytes()
        crlf = raw.count(b"\r\n")
        bare_cr = raw.count(b"\r") - crlf
        assert crlf == 0, f"{doc.name} has {crlf} CRLF endings, expected LF"
        assert bare_cr == 0, f"{doc.name} has {bare_cr} bare CR characters"

    def test_this_test_file_is_lf(self):
        """
        Guards the guard: if this file is ever rewritten with CRLF, the
        regexes above still work (universal newlines) but the convention
        check would be the only thing noticing.
        """
        raw = Path(__file__).read_bytes()
        assert b"\r\n" not in raw

