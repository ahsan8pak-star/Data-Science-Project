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
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORES_MD = REPO_ROOT / "FILE_SCORES.md"
GUIDE_MD = REPO_ROOT / "FILE_RANKING_GUIDE.md"
AGENTS_MD = REPO_ROOT / "AGENTS.md"
NOTES_MD = REPO_ROOT / "NOTES.md"

# The four criteria and their weights, as documented in FILE_RANKING_GUIDE.md.
WEIGHTS = {"Fixability": 40, "Readability": 25, "Durability": 20, "Robustness": 15}

# Band table from FILE_RANKING_GUIDE.md: inclusive (low, high) per band letter.
BANDS = {
    "A": (90, 100, "Exemplary"),
    "B": (80, 89, "Strong"),
    "C": (70, 79, "Serviceable"),
    "D": (60, 69, "Weak"),
    "E": (50, 59, "Poor"),
    "F": (0, 49, "Critical"),
}

# [AI] The three patterns below are matched line-by-line against the sheet, so
# they are anchored with ^...$ and pre-compiled once at import. CRITERION_RE
# carries re.M because findall() scans the whole worked-example block in the
# guide, where ^/$ must anchor per line rather than per string.
HEADING_RE = re.compile(
    r"^### (?P<rel>[\w./]+\.py) — \*\*(?P<score>\d+)/100\*\* "
    r"\((?P<band>[A-F]) — (?P<label>[^)]*)\)\s*$"
)
CRITERION_RE = re.compile(
    r"^\| (?P<name>Fixability|Readability|Durability|Robustness) \| "
    r"(?P<score>\d+) \| (?P<pct>\d+)% \| (?P<weighted>[\d.]+) \|$",
    re.M,
)
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

    def __init__(self, path, score, band, label, criteria, weighted_cells, final):
        self.path = path
        self.score = score
        self.band = band
        self.label = label
        self.criteria = criteria
        self.weighted_cells = weighted_cells
        self.final = final

    @property
    def name(self):
        """Basename, for matching against a doc that names files without paths."""
        return self.path.rsplit("/", 1)[-1]

    def weighted_total(self):
        """The four criteria recombined on the 0-100 scale, unrounded."""
        return sum(
            score * WEIGHTS[name] for name, score in self.criteria.items()
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
        for row in lines[index + 1:index + 12]:
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
            )
        )
    return entries


def _real_module_paths():
    """Every non-__init__ module under python/, as repo-relative POSIX paths."""
    return sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "python").rglob("*.py")
        if path.name != "__init__.py"
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

    def test_every_entry_carries_a_comment(self, entries):
        # Each entry is expected to say what works, what does not, why it
        # scored as it did and what would fix it - the guide's sincere-comment
        # rule. A bare table with no prose is the failure this catches.
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
    def test_every_entry_has_all_four_criteria(self, entries):
        incomplete = [
            e.path for e in entries if set(e.criteria) != set(WEIGHTS)
        ]
        assert incomplete == []

    def test_every_entry_has_a_final_row(self, entries):
        assert [e.path for e in entries if e.final is None] == []

    def test_weighted_cell_equals_score_times_weight(self, entries):
        # The cell shows one decimal place, so the check is against the value
        # rounded to one decimal - a bare tolerance would be wrong at the
        # boundary, where 85 x 25% is 21.25 and the sheet prints 21.3.
        wrong = []
        for entry in entries:
            for name, shown in entry.weighted_cells:
                expected = _round_half_up(
                    entry.criteria[name] * WEIGHTS[name] / 100 * 10
                ) / 10
                if abs(expected - shown) > 1e-9:
                    wrong.append(
                        f"{entry.path} {name}: cell {shown} != {expected}"
                    )
        assert wrong == []

    def test_weights_match_the_documented_table(self, entries):
        text = SCORES_MD.read_text(encoding="utf-8")
        stated = dict(
            re.findall(r"\|\s*(Fixability|Readability|Durability|Robustness)\s*"
                       r"\|\s*\d+\s*\|\s*(\d+)%\s*\|", text)
        )
        assert {k: int(v) for k, v in stated.items()} == WEIGHTS

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


class TestGuidePreVerifiedTable:
    """
    FILE_RANKING_GUIDE.md carries a "Pre-Verified Scores" table for the six
    files examined by hand. It is a summary of FILE_SCORES.md, so it has to
    agree with it: a second, older set of numbers is how a reader ends up
    quoting a score the score sheet no longer holds.
    """
    def _rows(self):
        text = GUIDE_MD.read_text(encoding="utf-8")
        section = text.split("## Pre-Verified Scores", 1)[-1]
        section = section.split("## ", 1)[0]
        rows = []
        for line in section.splitlines():
            if not line.startswith("| `"):
                continue
            cells = [cell.strip() for cell in line.split("|")[1:-1]]
            rows.append(cells)
        return rows

    def test_table_is_present(self):
        assert self._rows()

    def test_listed_final_matches_that_rows_own_criteria(self):
        wrong = []
        for cells in self._rows():
            fixability, readability, durability, robustness = (
                int(cells[1]), int(cells[2]), int(cells[3]), int(cells[4])
            )
            listed = int(cells[5].replace("**", ""))
            total = (
                fixability * WEIGHTS["Fixability"]
                + readability * WEIGHTS["Readability"]
                + durability * WEIGHTS["Durability"]
                + robustness * WEIGHTS["Robustness"]
            ) / 100
            if _round_half_up(total) != listed:
                wrong.append(
                    f"{cells[0]}: criteria give {total:.2f} -> "
                    f"{_round_half_up(total)} but table says {listed}"
                )
        assert wrong == []

    def test_table_agrees_with_the_score_sheet(self, by_path):
        mismatched = []
        for cells in self._rows():
            name = cells[0].strip("`").rsplit("/", 1)[-1]
            entry = next(
                (e for e in by_path.values() if e.name == name), None
            )
            assert entry is not None, f"{name} is not in FILE_SCORES.md"
            listed_criteria = [int(cells[i]) for i in (1, 2, 3, 4)]
            listed_final = int(cells[5].replace("**", ""))
            sheet_criteria = [entry.criteria[k] for k in WEIGHTS]
            if listed_final != entry.final:
                mismatched.append(
                    f"{name}: guide {listed_final} != sheet {entry.final}"
                )
            elif listed_criteria != sheet_criteria:
                mismatched.append(
                    f"{name}: guide criteria {listed_criteria} != "
                    f"sheet {sheet_criteria}"
                )
        assert mismatched == []


class TestGuideWorkedExample:
    """
    The output-format example in the guide is the template every entry is
    copied from. It shipped with a heading of 80 above a Final of 81, which
    is the same heading/final drift this file exists to catch.
    """
    def test_example_heading_matches_its_final(self):
        text = GUIDE_MD.read_text(encoding="utf-8")
        block = text.split("## Output Format in FILE_SCORES.md", 1)[-1]
        heading = re.search(r"^### .* — \*\*(\d+)/100\*\*", block, re.M)
        final = re.search(r"\| \*\*Final\*\* \| \| \| \*\*(\d+)\*\* \|", block)
        assert heading and final
        assert int(heading.group(1)) == int(final.group(1))

    def test_example_weighted_cells_match_their_criteria(self):
        text = GUIDE_MD.read_text(encoding="utf-8")
        block = text.split("## Output Format in FILE_SCORES.md", 1)[-1]
        rows = CRITERION_RE.findall(block)
        assert rows, "no criteria rows found in the worked example"
        for name, score, pct, weighted in rows:
            expected = _round_half_up(int(score) * int(pct) / 100 * 10) / 10
            assert abs(float(weighted) - expected) <= 1e-9, name

    def test_example_final_matches_the_sum_of_its_own_cells(self):
        text = GUIDE_MD.read_text(encoding="utf-8")
        block = text.split("## Output Format in FILE_SCORES.md", 1)[-1]
        rows = CRITERION_RE.findall(block)
        total = sum(int(score) * int(pct) for score, pct in
                    ((r[1], r[2]) for r in rows)) / 100
        final = re.search(r"\| \*\*Final\*\* \| \| \| \*\*(\d+)\*\* \|", block)
        assert final
        assert _round_half_up(total) == int(final.group(1))


class TestQuotedFigures:
    """
    AGENTS.md and NOTES.md both summarise the sheet in prose. Prose is the
    part that goes stale silently, so the specific claims are pinned to the
    computed numbers rather than trusted.
    """
    @staticmethod
    def _flat(path):
        return " ".join(path.read_text(encoding="utf-8").split())

    def _computed(self, entries):
        finals = sorted((entry.final, entry.name) for entry in entries)
        scores = [final for final, _ in finals]
        return {
            "mean": sum(scores) / len(scores),
            "below": sum(1 for s in scores if s < 70),
            "weakest": [name for _, name in finals[:2]],
            "weakest_score": finals[0][0],
            "top": [name for _, name in sorted(finals, reverse=True)[:3]],
            "top_scores": [s for s, _ in sorted(finals, reverse=True)[:3]],
        }

    @pytest.mark.parametrize("doc", [AGENTS_MD, NOTES_MD])
    def test_overall_average_is_quoted_correctly(self, doc, entries):
        stated = re.search(r"Overall average: ([\d.]+)/100", self._flat(doc))
        assert stated, "no overall average quoted"
        expected = round(self._computed(entries)["mean"], 1)
        assert float(stated.group(1)) == expected

    @pytest.mark.parametrize("doc", [AGENTS_MD, NOTES_MD])
    def test_below_seventy_count_is_quoted_correctly(self, doc, entries):
        stated = re.search(r"Only (\d+) files score below", self._flat(doc))
        assert stated, "no below-70 count quoted"
        assert int(stated.group(1)) == self._computed(entries)["below"]

    @pytest.mark.parametrize("doc", [AGENTS_MD, NOTES_MD])
    def test_weakest_pair_is_quoted_correctly(self, doc, entries):
        flat = self._flat(doc)
        stated = re.search(
            r"`([\w.]+\.py)` and `([\w.]+\.py)` \((\d+) each\)", flat
        )
        assert stated, "no weakest-pair claim quoted"
        computed = self._computed(entries)
        assert stated.group(1) in computed["weakest"]
        assert stated.group(2) in computed["weakest"]
        assert int(stated.group(3)) == computed["weakest_score"]

    def test_notes_quotes_the_top_three_correctly(self, entries):
        # Scope to the "Top files:" sentence. NOTES.md also quotes branch
        # counts for individual files elsewhere, and a repo-wide scan for
        # "`name.py` (n)" would sweep those up as if they were rankings.
        flat = self._flat(NOTES_MD)
        clause = re.search(r"Top files: (.+?)\.\s", flat)
        assert clause, "no top-file claim quoted"
        stated = re.findall(r"`([\w.]+\.py)` \((\d+)\)", clause.group(1))
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
            r"Overall average: [\d.]+/100 \(band ([A-F]) —", self._flat(doc)
        )
        assert stated, "no band quoted for the average"
        value = float(re.search(r"Overall average: ([\d.]+)/100", self._flat(doc)).group(1))
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
        # Guards the guard: if this file is ever rewritten with CRLF, the
        # regexes above still work (universal newlines) but the convention
        # check would be the only thing noticing.
        raw = Path(__file__).read_bytes()
        assert b"\r\n" not in raw


