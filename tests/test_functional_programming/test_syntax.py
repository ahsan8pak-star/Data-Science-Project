"""
Pytest suite for the applied programs under python/functional_programming/syntax_fundamentals/.

Each script is executed for real via run_script() (see conftest.py). These are
the basic applied programs built from the functional fundamental topics, so the
tests assert against the exact lines each program prints.
"""

from tests.test_functional_programming.conftest import run_script

FOLDER = "functional_programming/syntax_fundamentals"


# ---------------------------------------------------------------------------
# shopping_receipt.py
# ---------------------------------------------------------------------------

class TestShoppingReceipt:
    FILE = f"{FOLDER}/shopping_receipt.py"

    def test_total_price_reduces_the_basket(self):
        mod, _ = run_script(self.FILE)
        basket = [("Apple", 0.50, 4), ("Bread", 1.20, 2), ("Milk", 1.05, 1)]
        assert mod.total_price(basket) == 5.45

    def test_printed_receipt_lines(self):
        _, out = run_script(self.FILE)
        lines = out.strip().splitlines()
        assert lines == [
            "-- Shopping Receipt --",
            "Apple: $2.00",
            "Bread: $2.40",
            "Milk: $1.05",
            "-" * 20,
            "Total: $5.45",
        ]


# ---------------------------------------------------------------------------
# grade_summary.py
# ---------------------------------------------------------------------------

class TestGradeSummary:
    FILE = f"{FOLDER}/grade_summary.py"

    def test_helpers_behave_as_expected(self):
        mod, _ = run_script(self.FILE)
        assert mod.pass_grade(40) is True
        assert mod.pass_grade(39) is False
        assert mod.average([10, 20]) == 15.0

    def test_printed_summary_lines(self):
        _, out = run_script(self.FILE)
        assert "Passed: [45, 62, 78, 91, 58]" in out
        assert "Failed: [33]" in out
        assert "Average: 61.17" in out
        assert "Everyone passed? False" in out


# ---------------------------------------------------------------------------
# word_frequency.py
# ---------------------------------------------------------------------------

class TestWordFrequency:
    FILE = f"{FOLDER}/word_frequency.py"

    def test_printed_word_tallies(self):
        _, out = run_script(self.FILE)
        assert "python: 3" in out
        assert "java: 2" in out
        assert "go: 1" in out
        assert "kotlin: 1" in out


# ---------------------------------------------------------------------------
# number_pipeline.py
# ---------------------------------------------------------------------------

class TestNumberPipeline:
    FILE = f"{FOLDER}/number_pipeline.py"

    def test_printed_pipeline_lines(self):
        _, out = run_script(self.FILE)
        assert "Evens: [2, 4, 6, 8, 10]" in out
        assert "Squares of evens: [4, 16, 36, 64, 100]" in out
        assert "Sum of squares: 220" in out