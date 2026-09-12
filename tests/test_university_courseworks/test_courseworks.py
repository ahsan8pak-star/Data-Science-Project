"""
Pytest suite for the Python coursework programs under
`university_courseworks/year1/cs1ip/`.

Every module is loaded with conftest.load_module() so its function body is
available without triggering any `if __name__ == "__main__":` interaction.
Interactive scripts (ice_cream.py) drive their input()/print() loop through
mocked builtins instead of a live terminal.
"""

from unittest.mock import patch

import math
from pathlib import Path

import pytest

from tests.test_university_courseworks.conftest import (
    COURSEWORK1,
    COURSEWORK2,
    load_module,
)

AVERAGE_GRADES = COURSEWORK1 / "average_grades.py"
ICE_CREAM = COURSEWORK1 / "ice_cream.py"
SEVEN_SEGMENT = COURSEWORK1 / "seven_segment.py"
VOLUME = COURSEWORK1 / "volume.py"
HELLO = COURSEWORK1 / "hello.py"


# ---------------------------------------------------------------------------
# average_grades.py
# ---------------------------------------------------------------------------
class TestAverageGrades:

    @pytest.fixture(scope="class")
    @classmethod
    def mod(cls):
        return load_module(AVERAGE_GRADES)

    def test_textbook_example_returns_expected_averages(self, mod):
        grades = [[51, 83, 28], [0, 38, 95]]
        weights = [30, 40, 30]
        assert mod.AverageGrades(grades, weights) == [56, 43]

    def test_single_student_single_component(self, mod):
        assert mod.AverageGrades([[80]], [100]) == [80]

    def test_none_inputs_return_empty(self, mod):
        assert mod.AverageGrades(None, {}) == []
        assert mod.AverageGrades({}, None) == []

    def test_empty_grades_return_empty(self, mod):
        assert mod.AverageGrades([], [30, 70]) == []

    def test_weighted_math_verified_manually(self, mod):
        grades = [[10, 90]]
        weights = [50, 50]
        # (10*50 + 90*50) // 100 = 50
        assert mod.AverageGrades(grades, weights) == [50]

    def test_result_uses_integer_flooring(self, mod):
        grades = [[10, 10]]
        weights = [33, 33]
        # (330 + 330) // 100 = 6
        assert mod.AverageGrades(grades, weights) == [6]


# ---------------------------------------------------------------------------
# ice_cream.py
# ---------------------------------------------------------------------------
class TestIceCream:

    @pytest.fixture(scope="class")
    @classmethod
    def mod(cls):
        return load_module(ICE_CREAM)

    def test_pricing_constants_defined(self, mod):
        assert mod.CONE_PRICE == 100
        assert mod.VANILLA_PRICE == 19
        assert mod.CHOCOLATE_PRICE == 34
        assert mod.STRAWBERRY_PRICE == 0

    def test_two_vanilla_scoops(self, mod, capsys):
        with patch("builtins.input", side_effect=["v", "2"]):
            mod.IceCream()
        assert "£1.38" in capsys.readouterr().out

    def test_one_chocolate_scoop(self, mod, capsys):
        with patch("builtins.input", side_effect=["c", "1"]):
            mod.IceCream()
        assert "£1.34" in capsys.readouterr().out

    def test_three_strawberry_scoops_free_flavour(self, mod, capsys):
        with patch("builtins.input", side_effect=["s", "3"]):
            mod.IceCream()
        assert "£1.00" in capsys.readouterr().out

    def test_zero_scoops_rejected_and_retries(self, mod, capsys):
        with patch("builtins.input", side_effect=["v", "0", "v", "1"]):
            mod.IceCream()
        out = capsys.readouterr().out
        assert "We don't sell just a cone." in out
        assert "£1.19" in out

    def test_unknown_flavour_rejected_and_retries(self, mod, capsys):
        with patch("builtins.input", side_effect=["x", "v", "1"]):
            mod.IceCream()
        out = capsys.readouterr().out
        assert "We don't have that flavour." in out
        assert "£1.19" in out

    def test_non_numeric_scoops_rejected_and_retries(self, mod, capsys):
        with patch("builtins.input", side_effect=["v", "abc", "v", "2"]):
            mod.IceCream()
        out = capsys.readouterr().out
        assert "Please enter a valid number." in out
        assert "£1.38" in out

    def test_too_many_scoops_rejected(self, mod, capsys):
        with patch("builtins.input", side_effect=["c", "4", "c", "2"]):
            mod.IceCream()
        out = capsys.readouterr().out
        assert "That's too many scoops to fit in a cone." in out
        assert "£1.68" in out


# ---------------------------------------------------------------------------
# seven_segment.py
# ---------------------------------------------------------------------------
class TestSevenSegment:

    @pytest.fixture(scope="class")
    @classmethod
    def mod(cls):
        return load_module(SEVEN_SEGMENT)

    @pytest.mark.parametrize(
        "digit,line,segment",
        [
            (0, 1, " -- "), (0, 2, "|  |"), (0, 3, "    "),
            (1, 1, "    "), (1, 2, "   |"), (1, 5, "    "),
            (4, 2, "|  |"), (7, 2, "   |"), (8, 1, " -- "),
            (9, 5, " -- "), (0, 4, "|  |"),
        ],
    )
    def test_known_segments(self, mod, digit, line, segment):
        assert mod.ssd(digit, line) == segment

    def test_blank_falls_through_to_default(self, mod):
        # digit 1 has no top/middle/bottom segments -> those rows are blank
        assert mod.ssd(1, 1) == "    "
        assert mod.ssd(1, 3) == "    "
        assert mod.ssd(1, 5) == "    "
        # ...whereas its supporting rows are populated
        assert mod.ssd(1, 2) == "   |"

    def test_display_zero_renders_five_lines(self, mod, capsys):
        mod.display(0)
        out = capsys.readouterr().out.splitlines()
        assert len(out) == 5

    def test_display_single_digit_first_line_is_top_segment(self, mod, capsys):
        mod.display(8)
        out = capsys.readouterr().out.splitlines()
        assert out[0] == " -- "

    def test_display_multidigit_renders_each_row_in_full(self, mod, capsys):
        mod.display(42)
        out = capsys.readouterr().out.splitlines()

        assert len(out) == 5
        # digit 4's top is blank, digit 2's top is " -- ", joined by one space
        assert out[0] == "      -- "
        # digit 4's sides are "|  |", digit 2's upper-right is "   |"
        assert out[1] == "|  |    |"


# ---------------------------------------------------------------------------
# volume.py
# ---------------------------------------------------------------------------
class TestVolume:

    @pytest.fixture(scope="class")
    @classmethod
    def mod(cls):
        return load_module(VOLUME)

    def test_sphere_volume_matches_analytic_formula(self, mod):
        diameter = 20.24
        radius = diameter / 2.0
        expected = (4.0 / 3.0) * math.pi * radius ** 3
        assert mod.Volume(diameter) == pytest.approx(expected)

    def test_volume_of_unit_sphere(self, mod):
        assert mod.Volume(2) == pytest.approx((4.0 / 3.0) * math.pi)

    def test_zero_diameter_gives_zero_volume(self, mod):
        assert mod.Volume(0) == 0.0


# ---------------------------------------------------------------------------
# hello.py
# ---------------------------------------------------------------------------
class TestHello:

    @pytest.fixture(scope="class")
    @classmethod
    def run_hello(cls):
        import io
        import runpy

        buf = io.StringIO()
        with patch("sys.stdout", buf):
            runpy.run_path(str(HELLO), run_name="__main__")
        return buf.getvalue()

    def test_greeting_mentions_student_number(self, run_hello):
        assert "Hello, student 34001219." in run_hello


# ---------------------------------------------------------------------------
# coursework2/sort_comparison.py
# ---------------------------------------------------------------------------
class TestSortComparison:

    @pytest.fixture(scope="class")
    @classmethod
    def mod(cls):
        return load_module(COURSEWORK2 / "sort_comparison.py")

    @pytest.fixture()
    def mod_at(self, tmp_path):
        """
        A *copy* of sort_comparison.py living in a throwaway folder, so
        read_file()/write_results_to_csv() (which resolve paths relative to
        __file__) operate on temporary files instead of the real sources.
        """
        import shutil

        clone_dir = tmp_path / "coursework2"
        clone_dir.mkdir()
        files = ("sort_comparison.py", "sort10.txt", "sort100.txt", "sort10000.txt")
        for name in files:
            shutil.copy2(COURSEWORK2 / name, clone_dir / name)

        return load_module(clone_dir / "sort_comparison.py")

    @pytest.mark.parametrize(
        "suit,priority",
        [("H", 0), ("C", 1), ("D", 2), ("S", 3), ("X", -1)],
    )
    def test_get_suit_priority(self, mod, suit, priority):
        assert mod.get_suit_priority(suit) == priority

    def test_card_compare_same_suit_by_number(self, mod):
        assert mod.card_compare("4H", "3H") == 1

    def test_card_compare_different_suits_priority_wins(self, mod):
        # suit beats number: '4H' (H=0) sorts before '3S' (S=3)
        assert mod.card_compare("4H", "3S") == -1

    def test_card_compare_identical_cards(self, mod):
        assert mod.card_compare("7D", "7D") == 0

    def test_card_compare_ten_plus_ranks(self, mod):
        assert mod.card_compare("10C", "9C") == 1

    def test_bubble_sort_sorts_hand(self, mod):
        hand = ["4H", "3S", "7S", "8C", "2D", "3H"]
        # H < C < D < S, then face value within a suit
        expected = ["3H", "4H", "8C", "2D", "3S", "7S"]
        assert mod.bubble_sort(hand) == expected

    def test_merge_sort_matches_bubble_sort(self, mod):
        hand = ["4H", "3S", "7S", "8C", "2D", "3H"]
        assert mod.merge_sort(hand) == mod.bubble_sort(hand)

    def test_sorts_do_not_mutate_input(self, mod):
        hand = ["4H", "3S", "7S", "8C", "2D", "3H"]
        snapshot = hand[:]
        mod.bubble_sort(hand)
        mod.merge_sort(hand)
        assert hand == snapshot

    def test_empty_and_singleton_lists(self, mod):
        assert mod.bubble_sort([]) == []
        assert mod.merge_sort([]) == []
        assert mod.bubble_sort(["5D"]) == ["5D"]
        assert mod.merge_sort(["5D"]) == ["5D"]

    def test_read_file_returns_one_card_per_line(self, mod):
        cards = mod.read_file("sort10.txt")
        assert len(cards) == 10
        assert cards[0] == "10C"
        assert all(len(card) >= 2 for card in cards)

    def test_read_file_missing_raises_file_not_found(self, mod):
        with pytest.raises(FileNotFoundError):
            mod.read_file("sort_missing.txt")

    def test_write_results_to_csv_format(self, mod_at):
        csv_path = Path(mod_at.__file__).parent / "sort_comparison.csv"
        mod_at.write_results_to_csv([10, 100], [1, 2], [3, 4])

        assert csv_path.read_text() == (
            ", 10, 100\n"
            "bubbleSort, 1, 2\n"
            "mergeSort, 3, 4\n"
        )

    def test_sort_comparison_runs_and_produces_csv(self, mod_at):
        mod_at.sort_comparison(["sort10.txt"])

        csv_path = Path(mod_at.__file__).parent / "sort_comparison.csv"
        assert csv_path.exists()