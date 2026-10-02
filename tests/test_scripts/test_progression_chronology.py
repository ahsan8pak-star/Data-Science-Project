"""
The OpenCode usage chronology inside PROGRESSION's section 4.7 is a
hand-maintained table, so the rules that make it a record rather than a wall
of prose have to be checked by a test the same way the rotation table is.
"""

import re
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRESSION_MD = REPO_ROOT / "PROGRESSION.md"


def _chronology_rows():
    """Return the pipe-table body rows of the section-4 chronology table."""
    text = PROGRESSION_MD.read_text(encoding="utf-8")
    start = text.index("### 4.7 Chronology")
    lines = text[start:].splitlines()
    section_lines = []
    for i, line in enumerate(lines[1:], start=1):
        if line.startswith("## "):
            break
        section_lines.append(line)
    rows = []
    for line in section_lines:
        if line.startswith("| ") and line[2:3].isdigit():
            rows.append(line)
    return rows


class TestChronologyTable:

    def test_the_table_exists_and_has_rows(self):
        rows = _chronology_rows()
        assert len(rows) >= 8, f"expected at least 8 milestones, found {len(rows)}"

    def test_each_row_has_a_parseable_date(self):
        for row in _chronology_rows():
            cells = [c.strip() for c in row.split("|")[1:-1]]
            assert len(cells) == 3, f"row is not three cells: {row}"
            try:
                datetime.strptime(cells[0], "%d %b %Y")
            except ValueError:
                raise AssertionError(f"row has an unparseable date: {cells[0]!r}")

    def test_dates_are_chronological(self):
        dates = []
        for row in _chronology_rows():
            cells = [c.strip() for c in row.split("|")[1:-1]]
            dates.append(datetime.strptime(cells[0], "%d %b %Y"))
        assert dates == sorted(dates), "chronology rows are out of order"

    def test_model_names_are_in_MODELS(self):
        """
        Model names that appear anywhere in the table must be canonically
        present in MODELS - catches a mistyped or stale name.
        """
        import sys, os
        sys.path.insert(0, os.path.dirname(__file__))
        try:
            from test_model_rotation_docs import MODELS
        finally:
            sys.path.pop(0)
        text = PROGRESSION_MD.read_text(encoding="utf-8")
        start = text.index("### 4.7 Chronology")
        lines = text[start:].splitlines()
        section_lines = []
        for line in lines[1:]:
            if line.startswith("## "):
                break
            section_lines.append(line)
        found = set()
        for row in section_lines:
            for name in MODELS:
                if name in row:
                    found.add(name)
        assert found, "no model name was found in the chronology table"
        for name in found:
            assert name in MODELS, f"{name!r} is not in MODELS"

    def test_each_row_has_evidence(self):
        for row in _chronology_rows():
            cells = [c.strip() for c in row.split("|")[1:-1]]
            backticks = re.findall(r"`([0-9a-f]{7})`", cells[2])
            assert backticks, f"row lacks commit evidence: {cells[1]!r}"

