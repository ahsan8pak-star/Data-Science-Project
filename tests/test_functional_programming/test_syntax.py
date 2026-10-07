"""
Pytest suite for the applied programs under python/functional_programming/syntax_fundamentals/.

Each script is executed for real via run_script() (see conftest.py). These are
the basic applied programs built from the functional fundamental topics, so the
tests assert against the exact lines each program prints.
"""

import pytest

from tests.test_functional_programming.conftest import run_script

FOLDER = "functional_programming/syntax_fundamentals"


"""
---------------------------------------------------------------------------
shopping_receipt.py
---------------------------------------------------------------------------
"""

class TestShoppingReceipt:
    """
    reduce() totalling a shopping basket in shopping_receipt.py, plus the
    printed receipt lines.
    """
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


    def test_total_price_handles_an_empty_basket_and_a_single_line(self):

            """
            total_price() passes 0 as reduce()'s initial value, which is what
            makes an empty basket legal. The existing case only ever supplies one
            three-item basket, so neither the empty case nor the one-line case was
            reached, and a reduce() written without that initial value would still
            have passed everything above.
            """

            mod, _ = run_script(self.FILE)

            assert mod.total_price([]) == 0
            assert mod.total_price([("Milk", 1.05, 1)]) == pytest.approx(1.05)

    def test_zero_quantity_line_contributes_nothing_to_the_total(self):

        """
        The accumulator multiplies price by quantity per line, so a zero-quantity
        line must leave the total unchanged while still being a real line. This
        is the input that separates a genuine per-line product from a sum of
        prices, which would add the unit price regardless of quantity.
        """

        mod, _ = run_script(self.FILE)

        basket = [("Apple", 0.50, 4), ("Water", 1.20, 0)]
        assert mod.total_price(basket) == pytest.approx(2.00)

    def test_format_item_rounds_to_two_decimal_places(self):

        """
        format_item() formats price * quantity with a .2f spec, so a product
        that does not land on a clean cent is rounded in the printed line. The
        committed basket multiplies out to exact cents in every case, so the
        format spec was never actually load-bearing.
        """

        mod, _ = run_script(self.FILE)

        assert mod.format_item(("Apple", 0.333, 3)) == "Apple: $1.00"
        assert mod.format_item(("Bread", 1.00, 3)) == "Bread: $3.00"


"""
--------------------------------------------------------------------------
grade_summary.py
--------------------------------------------------------------------------
"""

class TestGradeSummary:
    """
    Helper functions behind the grade summary in grade_summary.py and the
    printed summary output.
    """
    FILE = f"{FOLDER}/grade_summary.py"

    def test_helpers_behave_as_expected(self):
        mod, _ = run_script(self.FILE)
        assert mod.pass_grade(40) is True
        assert mod.pass_grade(39) is False
        assert mod.average([10, 20]) == 15.0

    def test_pass_grade_threshold_holds_for_fractional_and_negative_scores(self):

        """
        pass_grade() is a bare `score >= 40`, so the existing 39/40 pair fixes
        the boundary but says nothing about the type of the score. A
        half-mark below the threshold must fail and a half-mark above must
        pass, which is what a threshold written as `> 40` instead of `>= 40`
        would get wrong at 40 but not at 39 or 41.
        """

        mod, _ = run_script(self.FILE)

        assert mod.pass_grade(39.5) is False
        assert mod.pass_grade(40.0) is True
        assert mod.pass_grade(-5) is False
        assert mod.pass_grade(0) is False

    def test_average_of_one_score_is_that_score_and_odd_lengths_are_a_real_mean(self):

        """
        average() divides a reduce() sum by len(), so a single score has to come
        back unchanged and a three-score list has to divide by three. Neither
        shape appeared before: the existing case used exactly two scores, which
        an off-by-one in the divisor would still satisfy.
        """

        mod, _ = run_script(self.FILE)

        assert mod.average([55]) == 55
        assert mod.average([10, 20, 30]) == pytest.approx(20.0)
        assert mod.average([10, 20, 31]) == pytest.approx(20.3333333, rel=1e-6)
        assert mod.average([1.5, 2.5]) == pytest.approx(2.0)

    def test_printed_summary_lines(self):
        _, out = run_script(self.FILE)
        assert "Passed: [45, 62, 78, 91, 58]" in out
        assert "Failed: [33]" in out
        assert "Average: 61.17" in out
        assert "Everyone passed? False" in out


"""
---------------------------------------------------------------------------
word_frequency.py
---------------------------------------------------------------------------
"""

class TestWordFrequency:
    """
    Counter-based word tallies in word_frequency.py.
    """
    FILE = f"{FOLDER}/word_frequency.py"

    def test_printed_word_tallies(self):
        _, out = run_script(self.FILE)
        assert "python: 3" in out
        assert "java: 2" in out
        assert "go: 1" in out
        assert "kotlin: 1" in out


"""
---------------------------------------------------------------------------
number_pipeline.py
---------------------------------------------------------------------------
"""

class TestNumberPipeline:
    """
    A functional pipeline over numbers in number_pipeline.py.
    """
    FILE = f"{FOLDER}/number_pipeline.py"

    def test_printed_pipeline_lines(self):
        _, out = run_script(self.FILE)
        assert "Evens: [2, 4, 6, 8, 10]" in out
        assert "Squares of evens: [4, 16, 36, 64, 100]" in out
        assert "Sum of squares: 220" in out

