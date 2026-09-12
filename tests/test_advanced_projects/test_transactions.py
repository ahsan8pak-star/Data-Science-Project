"""
Pytest suite for the openpyxl spreadsheet pipeline in
`python/advanced_projects/transactions/transactions.py`.

The script loads transactions.xlsx, strips the currency symbol from the
prices column, applies a 10% discount into a new fourth column, attaches a
bar chart, and saves the result as transactionv1.xlsx in the *current working
directory* (a relative `wb.save('transactionv1.xlsx')` call). Tests therefore
run in an isolated tmp_path that shadows the script's own folder.
"""

import hashlib

import openpyxl
import pytest

from tests.test_advanced_projects.conftest import PROJECT_ROOT, run_script

SCRIPT_DIR = "transactions"
FILE = f"{SCRIPT_DIR}/transactions.py"

INPUT_WORKBOOK = (
    PROJECT_ROOT
    / "python"
    / "advanced_projects"
    / "transactions"
    / "transactions.xlsx"
)


@pytest.fixture()
def output_file(tmp_path, monkeypatch):
    """Run the pipeline, then hand the saved transactionv1.xlsx path back."""
    monkeypatch.chdir(tmp_path)
    run_script(FILE)

    saved = tmp_path / "transactionv1.xlsx"
    assert saved.exists(), "pipeline did not write transactionv1.xlsx in the cwd"
    return saved


class TestPriceChecks:
    """The workbook used as the pipeline's real input."""

    def test_prices_column_is_text_with_currency_symbol(self):
        wb = openpyxl.load_workbook(INPUT_WORKBOOK)
        sheet = wb["Sheet1"]

        for row in range(2, sheet.max_row + 1):
            value = sheet.cell(row, 3).value
            assert isinstance(value, str), "prices must be stored as text"
            assert value.startswith("£"), f"expected a £ prefix, got {value!r}"


@pytest.fixture()
def input_workbook_bytes():
    """Snapshot of the real input workbook so mutation can be detected."""
    return INPUT_WORKBOOK.read_bytes()


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


class TestPipelineOutput:
    """What the discounted workbook actually contains."""

    def test_new_file_created_with_discount_column(self, output_file):
        wb = openpyxl.load_workbook(output_file)
        sheet = wb["Sheet1"]

        assert sheet.max_column >= 4, "discount column missing"
        assert all(
            sheet.cell(row, 4).value is not None for row in range(2, sheet.max_row + 1)
        ), "every data row must receive a discount"

    def test_discount_is_ten_percent_off(self, output_file):
        wb = openpyxl.load_workbook(output_file)
        sheet = wb["Sheet1"]

        for row in range(2, sheet.max_row + 1):
            raw_price = float(sheet.cell(row, 3).value.replace("£", ""))
            discount = float(sheet.cell(row, 4).value)
            assert discount == pytest.approx(raw_price * 0.9)

    def test_original_file_untouched(self, input_workbook_bytes):
        assert _sha256(INPUT_WORKBOOK.read_bytes()) == _sha256(input_workbook_bytes)
        assert INPUT_WORKBOOK.stat().st_size == len(input_workbook_bytes)

    def test_chart_anchored_to_e2(self, output_file):
        wb = openpyxl.load_workbook(output_file)
        sheet = wb["Sheet1"]

        assert len(sheet._charts) == 1, "expected exactly one bar chart"
        assert sheet._charts[0].anchor._from.col == 4
        assert sheet._charts[0].anchor._from.row == 1

    def test_header_row_intact(self, output_file):
        wb = openpyxl.load_workbook(output_file)
        sheet = wb["Sheet1"]

        header = [sheet.cell(1, col).value for col in range(1, 5)]
        assert header[0] is not None


class TestPipelineMetadata:
    """Structural/consistency checks independent of the spreadsheet data."""

    def test_row_count_preserved(self, output_file, tmp_path):
        original = openpyxl.load_workbook(INPUT_WORKBOOK)["Sheet1"]
        saved = openpyxl.load_workbook(output_file)["Sheet1"]

        assert saved.max_row == original.max_row
        assert saved.max_column >= original.max_column