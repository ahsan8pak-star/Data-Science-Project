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


def _write_workbook(path, prices, sheet_name="Sheet1"):
    """
    Build a minimal workbook shaped the way transactions() expects: column 1 is
    the transaction_id header, column 3 is the price. The sheet name matters
    because the script indexes wb['Sheet1'] directly.
    """

    wb = openpyxl.Workbook()
    sheet = wb[sheet_name] if sheet_name in wb.sheetnames else wb.active
    sheet.title = sheet_name
    sheet.cell(1, 1).value = "transaction_id"
    sheet.cell(1, 2).value = "product_id"
    sheet.cell(1, 3).value = "price"

    for offset, price in enumerate(prices):
        row = 2 + offset
        sheet.cell(row, 1).value = 9000 + offset
        sheet.cell(row, 2).value = offset + 1
        sheet.cell(row, 3).value = price

    wb.save(path)
    return path


class TestAlternateWorkbookInputs:
    """
    Method-first cases for transactions(file_path).

    The existing cases all feed the one committed workbook, so they prove the
    pipeline runs but not that the discount is actually computed from its
    input: a hardcoded "always 90%" would pass every one of them. Each case
    below hands the function a different workbook, so a fixed output cannot
    satisfy them all.
    """

    def _run_on(self, tmp_path, monkeypatch, prices, sheet_name="Sheet1"):

        monkeypatch.chdir(tmp_path)
        source = _write_workbook(tmp_path / "alt_input.xlsx", prices, sheet_name)
        mod, _ = run_script(FILE, cwd=str(tmp_path))
        mod.transactions(str(source))
        return openpyxl.load_workbook(tmp_path / "transactionv1.xlsx")["Sheet1"]

    def test_discount_follows_the_input_prices_not_a_fixed_value(
        self, tmp_path, monkeypatch
    ):
        """Three prices chosen so no single output could be hardcoded."""

        sheet = self._run_on(
            tmp_path, monkeypatch, ["\u00a31.00", "\u00a32.50", "\u00a399.99"]
        )

        assert sheet.cell(2, 4).value == pytest.approx(0.90)
        assert sheet.cell(3, 4).value == pytest.approx(2.25)
        assert sheet.cell(4, 4).value == pytest.approx(89.991)

    def test_numeric_price_cells_are_accepted_without_a_currency_symbol(
        self, tmp_path, monkeypatch
    ):
        """
        The pipeline casts each price with str(cell.value) before stripping the
        symbol, so a plain float cell must work even though the committed
        workbook stores prices as text. This is the branch that cast exists
        for, and nothing else here exercised it.
        """

        sheet = self._run_on(tmp_path, monkeypatch, [10.0, 2.5])

        assert sheet.cell(2, 4).value == pytest.approx(9.0)
        assert sheet.cell(3, 4).value == pytest.approx(2.25)

    def test_sub_penny_input_is_discounted_without_intermediate_rounding(
        self, tmp_path, monkeypatch
    ):

        """
        3.33 at 90% is 2.997, which is not a two-decimal figure. Checking the
        exact product with pytest.approx pins that the discount is applied to
        the parsed price and not rounded to pence on the way through.
        """

        sheet = self._run_on(tmp_path, monkeypatch, ["\u00a33.33"])

        assert sheet.cell(2, 4).value == pytest.approx(2.997)
        assert sheet.cell(2, 4).value != pytest.approx(3.0)

    def test_single_data_row_still_builds_the_chart_reference(
        self, tmp_path, monkeypatch
    ):

        """
        The boundary case where the sheet holds exactly one data row, so the
        Reference block collapses to min_row == max_row == 2. A header-only
        sheet would make that range empty, so this is the smallest input the
        pipeline is meant to accept.
        """

        monkeypatch.chdir(tmp_path)
        source = _write_workbook(tmp_path / "single.xlsx", ["\u00a34.00"])
        mod, _ = run_script(FILE, cwd=str(tmp_path))
        mod.transactions(str(source))

        wb = openpyxl.load_workbook(tmp_path / "transactionv1.xlsx")
        sheet = wb["Sheet1"]

        assert sheet.max_row == 2
        assert sheet.cell(2, 4).value == pytest.approx(3.6)
        assert len(sheet._charts) == 1

    def test_a_missing_sheet_name_raises_the_same_way_the_script_expects(
        self, tmp_path, monkeypatch
    ):

        """
        The script indexes wb['Sheet1'] directly and its own comment notes the
        sheet name is case-sensitive. A workbook whose active sheet is called
        "Sheet2" must therefore fail rather than silently produce an empty
        report, which is what makes the hard-coded name in the source a real
        contract rather than an incidental detail.
        """

        monkeypatch.chdir(tmp_path)
        source = _write_workbook(
            tmp_path / "wrong_sheet.xlsx", ["\u00a35.00"], sheet_name="Sheet2"
        )
        mod, _ = run_script(FILE, cwd=str(tmp_path))

        with pytest.raises(KeyError):
            mod.transactions(str(source))
    """Structural/consistency checks independent of the spreadsheet data."""

    def test_row_count_preserved(self, output_file, tmp_path):
        original = openpyxl.load_workbook(INPUT_WORKBOOK)["Sheet1"]
        saved = openpyxl.load_workbook(output_file)["Sheet1"]

        assert saved.max_row == original.max_row
        assert saved.max_column >= original.max_column

