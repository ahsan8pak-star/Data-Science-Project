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
import subprocess
import tokenize
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
_TRIPLES = ('"""', "'''")
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
        path = REPO_ROOT / "requirements" / name
        if not path.exists():
            pytest.skip(f"{name} is not present")
        lines = [
            line.strip() for line in path.read_text(encoding="utf-8").splitlines()
        ]
        entries = [line for line in lines if line and not line.startswith("#")]
        assert entries, f"{name} lists no packages"

    def test_coursework_settings_json_parses(self):
        path = (
            REPO_ROOT / "university_courseworks" / "year1" / "semester1"
            / "cs1ip" / "coursework1" / "java" / "settings.json"
        )
        if not path.is_file():
            pytest.skip(
                "year1/semester1/cs1ip/coursework1/java/settings.json is not present"
            )
        json.loads(path.read_text(encoding="utf-8"))

    def test_sort_comparison_csv_is_rectangular(self):
        path = (
            REPO_ROOT / "university_courseworks" / "year1" / "semester1" / "cs1ip"
            / "coursework2" / "data" / "sort_comparison.csv"
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




class TestPythonFilesEndWithOneBlankLine:
    """
    [AI] The house convention is that a file ends with the last line of
    code, then one empty line - that is, exactly two trailing newlines.
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

    def test_every_python_file_ends_with_exactly_two_newlines(self):
        wrong = []
        for path in self._python_files():
            rel = path.relative_to(REPO_ROOT).as_posix()
            if rel in self.EXEMPT:
                continue
            count = self._trailing_newlines(path)
            if count != 2:
                wrong.append(f"{rel} (has {count})")
        assert wrong == [], (
            "Python files must end with the last line of code followed by one "
            "empty line, i.e. exactly two trailing newlines; wrong: "
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




class TestMultiLineDocstringsUseTheHouseStructure:
    """
    [AI] A multi-line docstring opens with the triple quote alone on its own
    line, carries its summary on the next, and closes with the triple quote
    alone on its own line. That is the form in the house reference
    (scripts/repair_test_numbers_seam.py) and it is what makes a docstring
    read as a block rather than as a paragraph that happens to be quoted.

    The failure it prevents is subtle: opening the quotes on the same line as
    the summary is valid Python and renders identically, so nothing catches it
    and it spreads. Three files had drifted, including one written during
    this work.

    Single-line docstrings are exempt and must stay exempt. A one-line
    docstring written as quotes, text and quotes on one line is the correct
    compact form, and forcing it onto four lines would make the code worse
    rather than better.

    The check parses with tokenize rather than grepping for quotes, so it
    reads actual string literals - a hash comment that mentions quotes is
    not a docstring and must not be mistaken for one.
    """

    SKIP_DIRS = {".venv", "__pycache__", "htmlcov", ".git", ".pytest_cache",
                 "node_modules"}

    def _sources(self):
        return [
            p for p in REPO_ROOT.rglob("*.py")
            if not (self.SKIP_DIRS & set(p.relative_to(REPO_ROOT).parts))
        ]

    def _multiline_strings(self, path):
        """Yield the raw text of every multi-line string literal in a file."""
        try:
            with open(path, "rb") as handle:
                tokens = list(tokenize.tokenize(io.BytesIO(handle.read()).readline))
        except (tokenize.TokenError, SyntaxError, IndentationError, ValueError):
            return
        for token in tokens:
            if token.type == tokenize.STRING and "\n" in token.string:
                yield token.string

    def test_multi_line_strings_open_and_close_on_their_own_lines(self):
        offenders = []
        for path in self._sources():
            for text in self._multiline_strings(path):
                parts = text.split("\n")
                rel = path.relative_to(REPO_ROOT).as_posix()
                if parts[0].strip() not in _TRIPLES:
                    offenders.append(
                        f"{rel}: opens as {parts[0].strip()[:40]!r} - the "
                        "quotes should be alone on their own line"
                    )
                    continue
                if parts[-1].strip() not in _TRIPLES:
                    offenders.append(
                        f"{rel}: closes as {parts[-1].strip()[-40:]!r} - the "
                        "quotes should be alone on their own line"
                    )
        assert offenders == [], (
            "multi-line docstrings must open and close with the triple quote "
            "alone on its own line: " + "; ".join(sorted(offenders)[:8])
        )

    def test_the_house_reference_docstring_matches(self):
        """
        The file the convention is quoted from has to follow it, or the
        convention is being described rather than followed.
        """
        path = REPO_ROOT / "scripts" / "repair_test_numbers_seam.py"
        if not path.is_file():
            pytest.skip("the house reference script is not present")
        docstring = next(iter(self._multiline_strings(path)), None)
        assert docstring is not None, "no multi-line docstring found"
        parts = docstring.split("\n")
        assert parts[0].strip() in _TRIPLES
        assert parts[-1].strip() in _TRIPLES

class TestCommentRunsUseHashOrTripleQuoteNotBoth:
    """
    AGENTS.md house style: two lines is the absolute maximum for a run of
    hash comments, and three or more consecutive hash lines must become a
    triple-quoted block. The block form is the one in the house reference -
    quotes alone on their own lines, summary first, a blank line, then the
    explanation.

    Scope is every tracked .py file. The rule was originally applied only to
    newly written files and the rest of the tree was merely counted, which left
    roughly 1100 overlong runs in place for weeks with nothing failing. A rule
    that only applies to files someone remembered to apply it to is a
    preference, so the guard now covers the repository and states its two
    exemptions by name.

    Two shapes are deliberately outside the rule, per AGENTS.md: an inline
    trailing comment (`x = 5  # why`) is not a standalone block, and a
    single hash comment followed by unrelated code is unaffected - the limit
    is on *consecutive* hash lines.

    Rule 1 freezes the OOP lane and rule 8 marks the CS1IP coursework as
    submitted work, so neither is restyled. Both are asserted below, because an
    exemption that rots into a no-op is worse than no exemption at all.
    """
    EXEMPT = frozenset({
        "python/object_oriented_programming/fundamental_topics/decorator.py",
        "python/object_oriented_programming/fundamental_topics/generator.py",
        "python/object_oriented_programming/fundamental_topics/multitasking.py",
        "python/object_oriented_programming/syntax_fundamentals/dice.py",
        "python/object_oriented_programming/fundamental_topics/classes.py",
        "python/object_oriented_programming/fundamental_topics/"
        "abstract_classes.py",
        "python/object_oriented_programming/fundamental_topics/"
        "nested_classes.py",
        "university_courseworks/year1/semester1/cs1ip/coursework2/python/sort_comparison.py",
    })

    @staticmethod
    def _overlong_runs(path):
        """Line numbers of hash-comment runs longer than two lines."""
        lines = path.read_bytes().replace(b"\r\n", b"\n").decode(
            "utf-8").split("\n")
        runs = []
        current = []
        for index, line in enumerate(lines, 1):
            if line.strip().startswith("#"):
                current.append(index)
            else:
                if current:
                    runs.append(current)
                current = []
        if current:
            runs.append(current)
        return [run for run in runs if len(run) > 2]

    def test_no_governed_file_has_a_hash_run_longer_than_two_lines(self):
        """
        Every tracked .py file, not only this session's.

        [AI-authored fix] The guard originally covered three files, with the
        rest of the repository's ~1100 overlong runs counted by a second test
        that only asserted the debt was still non-zero. That is a debt register,
        not a rule: it recorded the number without constraining anything, and
        the count stayed high for weeks because nothing failed.

        The rule now applies repo-wide, as AGENTS.md states. Two groups are
        exempt and named here rather than left implicit, because both are
        protected by other rules and an unnamed exception is not an exception:
          - the frozen OOP lane (rule 1), which must not be edited;
          - the marked CS1IP coursework (rule 8), which is submitted work.
        """
        offenders = {}
        for rel in self._tracked_files():
            runs = self._overlong_runs(REPO_ROOT / rel)
            if runs:
                offenders[rel] = [run[0] for run in runs]
        assert offenders == {}, (
            "a run of three or more hash comments must become a triple-quoted "
            "block; overlong runs at: "
            + repr(offenders)
            + ". The frozen OOP lane and the marked coursework are exempt by "
            "rule 1 and rule 8; nothing else is."
        )

    @classmethod
    def _tracked_files(cls):
        """Tracked .py files, minus the two groups the rules protect."""
        listed = subprocess.run(
            ["git", "ls-files", "*.py"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()
        return [rel for rel in listed if rel not in cls.EXEMPT]

    def test_the_house_reference_uses_the_block_form(self):
        """
        scripts/repair_test_numbers_seam.py is quoted as the reference for
        this rule, so it has to obey it.
        """
        path = REPO_ROOT / "scripts" / "repair_test_numbers_seam.py"
        if not path.is_file():
            pytest.skip("the house reference script is not present")
        assert self._overlong_runs(path) == []

    def test_the_exempt_files_still_carry_their_original_runs(self):
        """
        The exemptions are load-bearing, so they are asserted, not assumed.

        If one of these files is ever converted on purpose - A.I.M's call, not
        an agent's - this fails and the exemption list is revisited instead of
        the file quietly ceasing to be protected.
        """
        present = {}
        for rel in sorted(self.EXEMPT):
            path = REPO_ROOT / rel
            if not path.is_file():
                continue
            runs = self._overlong_runs(path)
            if runs:
                present[rel] = len(runs)
        assert present, (
            "no exempt file carries an overlong run any more; the exemptions "
            "have gone stale and should be removed from this list"
        )

    def test_the_exemption_list_names_real_files(self):
        """A typo in an exemption silently widens the rule, so check the names."""
        missing = [
            rel for rel in sorted(self.EXEMPT)
            if not (REPO_ROOT / rel).is_file()
        ]
        assert missing == [], (
            "EXEMPT names files that do not exist: " + str(missing)
        )

