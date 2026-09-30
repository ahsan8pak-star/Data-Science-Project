"""
Structural validation for the non-Python data files in the repository.

[AI] Kept in its own module rather than folded into an existing suite, because
these are not Python programs: there is no module to import, no function to
call, and nothing for `run_script` to execute. The fixtures below are the
inputs and outputs that the teaching scripts read and write, and the only
thing that can be checked about them is that they are structurally valid -
that a JSON file parses, that every row of a CSV has the same number of
columns, that a header cell does not carry a stray leading space.

That last check exists because of a real defect. `syntax_exercises/input.csv`
had the header `gamertag, gamerscore, is_online, account_made`, where every
cell after the first carried a leading space. `file_reader.py` strips
whitespace from *data* rows but reads the header without stripping it, so the
leading spaces were invisible in the printed output and had never been
noticed. This module treats a header cell with surrounding whitespace as a
failure, so the same defect cannot be reintroduced by editing the data.

Scope is deliberately structural only. Asserting what a fixture *means* would
couple this file to the internals of a teaching script, so a future edit to
`file_reader.py` could fail a data test for no good reason. The one exception
is a light existence check: each fixture is asserted to be named by the script
that claims to use it, which catches a rename that would otherwise leave an
orphan behind. Nothing here writes to the repository, and nothing runs a
script - these are read-only queries against committed data.
"""

import csv
import io
import json
import re
import tokenize
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SYNTAX = REPO_ROOT / "python" / "imperative_programming" / "syntax_exercises"

# fixture filename -> the teaching script that references it by name.
# Used only for the "is it still referenced" check, never to assert behaviour.
FIXTURE_OWNERS = {
    "input.txt": "file_reader.py",
    "input.json": "file_reader.py",
    "input.csv": "file_reader.py",
    "output.txt": "file_writer.py",
    "output.json": "file_writer.py",
    "output.csv": "file_writer.py",
    "aim.txt": "file_writer.py",
    "activity_log.txt": "file_writer.py",
    "test.txt": "file_handling.py",
}

# The four columns file_reader.py reads positionally out of input.csv.
INPUT_CSV_COLUMNS = ("gamertag", "gamerscore", "is_online", "account_made")


def _rows(path):
    """Parse a CSV into a list of non-blank rows."""
    text = path.read_text(encoding="utf-8")
    return [row for row in csv.reader(io.StringIO(text)) if row]


class TestSyntaxExerciseFixtures:
    """
    The data that sits beside the file-handling teaching scripts. Each fixture
    is read the way its consumer reads it, so a structural fault surfaces
    here rather than as a confusing failure inside a script.
    """

    @pytest.mark.parametrize("name", sorted(FIXTURE_OWNERS))
    def test_fixture_exists_and_is_not_empty(self, name):
        path = SYNTAX / name
        assert path.is_file(), f"{name} is missing from {SYNTAX.name}/"
        assert path.stat().st_size > 0, f"{name} is empty"

    @pytest.mark.parametrize("name", sorted(FIXTURE_OWNERS))
    def test_fixture_is_utf8_text(self, name):
        raw = (SYNTAX / name).read_bytes()
        raw.decode("utf-8")  # raises UnicodeDecodeError if not UTF-8
        assert not raw.startswith(b"\xef\xbb\xbf"), f"{name} carries a BOM"

    @pytest.mark.parametrize("name", ["input.json", "output.json"])
    def test_json_fixture_parses_to_an_object(self, name):
        payload = json.loads((SYNTAX / name).read_text(encoding="utf-8"))
        assert isinstance(payload, (dict, list)), (
            f"{name} should hold a JSON object or array, "
            f"not {type(payload).__name__}"
        )

    @pytest.mark.parametrize("name", ["input.csv", "output.csv"])
    def test_csv_rows_all_have_the_same_column_count(self, name):
        rows = _rows(SYNTAX / name)
        assert len(rows) >= 2, f"{name} needs a header and at least one row"
        widths = {len(row) for row in rows}
        assert len(widths) == 1, (
            f"{name} is ragged: row widths {sorted(widths)}; every row must "
            "match the header's column count"
        )

    @pytest.mark.parametrize("name", ["input.csv", "output.csv"])
    def test_csv_header_cells_carry_no_surrounding_whitespace(self, name):
        """
        The defect this whole module exists for.

        `csv.reader` preserves the space in `' gamerscore'`, so a header
        written as `a, b, c` parses to three cells where the second and third
        are silently wrong. `file_reader.py` strips its *data* rows but not the
        header, so the mismatch never reached the output and nothing caught it.
        """
        header = _rows(SYNTAX / name)[0]
        padded = [cell for cell in header if cell != cell.strip()]
        assert padded == [], (
            f"{name} header cells {padded} have surrounding whitespace; write "
            "the header as 'a,b,c' with no space after each comma"
        )

    def test_input_csv_header_matches_the_columns_the_reader_expects(self):
        """
        The one semantic check in this module, and it is deliberately narrow:
        the four header names must be the four the reader pulls positionally,
        because a rename on either side would otherwise break the script with
        no test failing.
        """
        header = _rows(SYNTAX / "input.csv")[0]
        assert tuple(header) == INPUT_CSV_COLUMNS, (
            f"input.csv header is {header}, but file_reader.py reads "
            f"{list(INPUT_CSV_COLUMNS)} positionally"
        )

    @pytest.mark.parametrize("name", ["input.csv", "output.csv"])
    def test_csv_does_not_end_with_blank_rows(self, name):
        rows = _rows(SYNTAX / name)
        assert rows, f"{name} parsed to nothing"
        assert rows[-1] != [], f"{name} ends with a blank row"

    @pytest.mark.parametrize("name,owner", sorted(FIXTURE_OWNERS.items()))
    def test_fixture_is_still_referenced_by_its_owning_script(self, name, owner):
        """
        A rename that breaks the link leaves an orphan nobody notices, because
        the script still runs - it just reads a file that is no longer there.
        """
        source = (SYNTAX / owner).read_text(encoding="utf-8")
        assert name in source, (
            f"{owner} no longer references {name}; the fixture is now an "
            "orphan unless the script was renamed too"
        )

    def test_text_fixtures_are_readable_as_lines(self):
        for name in ("input.txt", "output.txt", "test.txt", "aim.txt"):
            lines = (SYNTAX / name).read_text(encoding="utf-8").splitlines()
            assert lines, f"{name} has no content lines"


class TestRepoLevelDataFiles:
    """
    Data that belongs to the repository rather than to one teaching script:
    editor settings, pinned requirement lists, and the coursework sort
    fixture. These are grouped separately because they are checked on a
    different basis - they must simply be well-formed for the tooling that
    reads them.
    """

    @pytest.mark.parametrize(
        "name", ["launch.json", "settings.json", "tasks.json"]
    )
    def test_vscode_json_parses(self, name):
        path = REPO_ROOT / ".vscode" / name
        assert path.is_file(), f".vscode/{name} is missing"
        json.loads(path.read_text(encoding="utf-8"))

    @pytest.mark.parametrize(
        "name",
        ["requirements.txt", "requirements-win_dev.txt", "requirements.in",
         "requirements-win_dev.in"],
    )
    def test_requirements_file_is_populated_and_pinned(self, name):
        path = REPO_ROOT / name
        if not path.exists():
            pytest.skip(f"{name} is not present")
        lines = [
            line.strip() for line in path.read_text(encoding="utf-8").splitlines()
        ]
        entries = [line for line in lines if line and not line.startswith("#")]
        assert entries, f"{name} lists no packages"

    def test_coursework_settings_json_parses(self):
        path = REPO_ROOT / "university_courseworks" / "year1" / "settings.json"
        if not path.is_file():
            pytest.skip("year1/settings.json is not present")
        json.loads(path.read_text(encoding="utf-8"))

    def test_sort_comparison_csv_is_rectangular(self):
        path = (
            REPO_ROOT / "university_courseworks" / "year1" / "cs1ip"
            / "coursework2" / "sort_comparison.csv"
        )
        if not path.is_file():
            pytest.skip("sort_comparison.csv is not present")
        rows = [r for r in csv.reader(io.StringIO(path.read_text(encoding="utf-8"))) if r]
        assert len(rows) >= 2, "sort_comparison.csv needs a header and data"
        widths = {len(r) for r in rows}
        assert len(widths) == 1, (
            f"sort_comparison.csv is ragged: row widths {sorted(widths)}"
        )


class TestDataFilesUseLfAndNoTrailingWhitespace:
    """
    [AI] The data files sit in the same tree as the source, and .gitattributes
    pins `* text=auto eol=lf` for everything, so a CRLF committed into a CSV
    would be a silent inconsistency with the rest of the repository - and a
    header cell ending in `\\r` is exactly the kind of defect the header check
    above is meant to catch, arriving by a different route.
    """

    @pytest.mark.parametrize("name", sorted(FIXTURE_OWNERS))
    def test_fixture_has_no_crlf(self, name):
        raw = (SYNTAX / name).read_bytes()
        assert b"\r\n" not in raw, f"{name} contains CRLF endings, expected LF"

    @pytest.mark.parametrize("name", sorted(FIXTURE_OWNERS))
    def test_fixture_has_no_trailing_whitespace_on_any_line(self, name):
        lines = (SYNTAX / name).read_text(encoding="utf-8").split("\n")
        padded = [i + 1 for i, line in enumerate(lines) if line != line.rstrip()]
        assert padded == [], (
            f"{name} has trailing whitespace on line(s) {padded}"
        )




class TestPythonFilesEndWithTwoBlankLines:
    """
    [AI] The house convention is that a Python file ends with the last line of
    code, then two empty lines - that is, exactly three trailing newlines.
    `scripts/repair_test_numbers_seam.py` documents the same invariant ("LF-only,
    exactly three trailing LF, no BOM, no trailing whitespace on any line, no
    CRLF"), so the rule already existed in prose and was not held anywhere.

    Ten files drifted from it when it was checked: four had no trailing newline
    at all, and six had one or two. The drift is invisible in a review because
    a missing trailing newline looks like nothing at all on screen, which is
    the reason it needs a test rather than a habit.

    Scope is Python only. The same rule is deliberately not applied to markdown:
    trailing blank lines do not render, and every document in the repo is
    already consistent at a single newline, so normalising them would be
    churn with no visible effect. `.pytest_cache/` is excluded because it is
    generated and gitignored.

    `scripts/repair_test_numbers_seam.py` is exempt: it is a one-shot repair
    script whose ending is part of what it was written to produce, and it
    currently carries an uncommitted edit that is not the author's to normalise
    from here.
    """

    EXEMPT = {"scripts/repair_test_numbers_seam.py"}
    SKIP_DIRS = {".venv", "__pycache__", "htmlcov", ".git", ".pytest_cache",
                 "node_modules"}

    def _python_files(self):
        return [
            p for p in REPO_ROOT.rglob("*.py")
            if not self.SKIP_DIRS & set(p.relative_to(REPO_ROOT).parts)
        ]

    @staticmethod
    def _trailing_newlines(path):
        raw = path.read_bytes().replace(b"\r\n", b"\n")
        count = 0
        while raw.endswith(b"\n"):
            count += 1
            raw = raw[:-1]
        return count

    def test_every_python_file_ends_with_exactly_three_newlines(self):
        wrong = []
        for path in self._python_files():
            rel = path.relative_to(REPO_ROOT).as_posix()
            if rel in self.EXEMPT:
                continue
            count = self._trailing_newlines(path)
            if count != 3:
                wrong.append(f"{rel} (has {count})")
        assert wrong == [], (
            "Python files must end with the last line of code followed by two "
            "empty lines, i.e. exactly three trailing newlines; wrong: "
            + "; ".join(sorted(wrong))
        )




class TestPythonSourceHasNoTrailingWhitespace:
    """
    [AI] Trailing whitespace is invisible in a review and in most editors, so
    it accumulates unnoticed: 103 files under the tree carried 853 such lines
    when this was first checked. The cleanup is deliberately conservative -
    only whitespace at the END of a line is removed, never leading indentation,
    so no code changes shape.

    Fifteen lines are exempt because they fall inside a multi-line string
    literal, where the whitespace is the content rather than an accident. Two
    of those are expected-output strings in
    test_math_and_science_calculators.py, where a stripped space would change
    what the test asserts. The rest are continuation lines of docstrings.

    The exemption is computed with tokenize rather than guessed, so it stays
    correct when a file is edited: a line moves in or out of a string literal
    and the guard follows it.
    """

    EXEMPT_FILES = set()
    # .venv is the pinned environment itself: its site-packages are third-party
    # code, not this repository's, and are never ours to reformat.
    SKIP_DIRS = {".venv", "__pycache__", "htmlcov", ".git", ".pytest_cache",
                 "node_modules"}

    @staticmethod
    def _multiline_string_lines(path):
        """
        Line numbers that fall inside a multi-line string literal.

        Returns an empty set for a file that will not tokenize, so an
        unparseable file such as the deliberate main.py stub is checked by the
        plain rule rather than silently skipped.
        """
        try:
            with open(path, "rb") as handle:
                tokens = list(tokenize.tokenize(io.BytesIO(handle.read()).readline))
        except (tokenize.TokenError, SyntaxError, IndentationError, ValueError):
            return set()
        inside = set()
        for token in tokens:
            if token.type == tokenize.STRING and token.end[0] > token.start[0]:
                inside.update(range(token.start[0], token.end[0] + 1))
        return inside

    def _sources(self):
        return [
            p for p in REPO_ROOT.rglob("*.py")
            if not (self.SKIP_DIRS & set(p.relative_to(REPO_ROOT).parts))
        ]

    def test_no_trailing_whitespace_outside_string_literals(self):
        offenders = []
        for path in self._sources():
            rel = path.relative_to(REPO_ROOT).as_posix()
            if rel in self.EXEMPT_FILES:
                continue
            try:
                lines = path.read_text(encoding="utf-8").split("\n")
            except UnicodeDecodeError:
                continue
            inside = self._multiline_string_lines(path)
            padded = [
                i for i, line in enumerate(lines, 1)
                if line != line.rstrip() and i not in inside
            ]
            if padded:
                offenders.append(f"{rel} ({len(padded)} line(s) from {padded[0]})")
        assert offenders == [], (
            "trailing whitespace found; strip it from the end of the line "
            "(leading indentation must stay): "
            + "; ".join(sorted(offenders)[:12])
        )


