"""
Pytest suite for every script under Python/syntax_fundamentals/.

This is the largest and most varied folder - one-off utility scripts,
countdown timers, and a couple of files (math_module.py/math_file.py) that
only work correctly once run_script() replicates a directly-run script's
sys.path and __name__ behaviour (see conftest.py).
"""

import pytest
import sys

from unittest.mock import patch
from tests.conftest import run_script
from imperitive_programming.syntax_fundamentals.factorials import factorial # Unique case since this is the only file to occur a NameError
from imperitive_programming.syntax_fundamentals.food_script_example import favourite_food # This is to resolve ModuleNotFoundError
from imperitive_programming.syntax_fundamentals.drink_script_example import favourite_drink # This is to resolve ModuleNotFoundError



FOLDER = "imperitive_programming/syntax_fundamentals"


# ---------------------------------------------------------------------------
# add.py
# ---------------------------------------------------------------------------
class TestAdd:
    FILE = f"{FOLDER}/add.py"

    def test_output(self):
        _, out = run_script(self.FILE)
        assert _.result == 8
        assert "8" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.add(-2, 2) == 0

    def test_add_with_two_negatives(self):
        mod, _ = run_script(self.FILE)
        assert mod.add(-5, -5) == -10

    def test_add_with_floats(self):
        mod, _ = run_script(self.FILE)
        assert mod.add(1.5, 2.5) == 4.0

    def test_add_is_commutative(self):
        mod, _ = run_script(self.FILE)
        assert mod.add(3, 7) == mod.add(7, 3)

    def test_add_zero_identity(self):
        mod, _ = run_script(self.FILE)
        assert mod.add(9, 0) == 9

    def test_add_large_numbers(self):
        mod, _ = run_script(self.FILE)
        assert mod.add(999999, 1) == 1000000


# ---------------------------------------------------------------------------
# checkout_system.py
# ---------------------------------------------------------------------------
class TestCheckoutSystem:
    FILE = f"{FOLDER}/checkout_system.py"

    def test_zero_quantity(self):
        _, out = run_script(self.FILE, inputs=["Apple", "1.50", "0"])
        assert "You bought nothing. See you later!" in out

    def test_single_item(self):
        _, out = run_script(self.FILE, inputs=["Apple", "1.50", "1"])
        assert "You bought only 1 Apple" in out
        assert "Price: £1.50" in out

    def test_multiple_items(self):
        _, out = run_script(self.FILE, inputs=["Apple", "1.50", "4"])
        assert "You bought 4 Apples" in out
        assert "Total: £6.00" in out

    def test_non_numeric_price_raises_uncaught_value_error(self):
        with pytest.raises(ValueError):
            run_script(self.FILE, inputs=["Apple", "abc", "1"])

    def test_non_numeric_quantity_raises_uncaught_value_error(self):
        with pytest.raises(ValueError):
            run_script(self.FILE, inputs=["Apple", "1.50", "abc"])

    def test_negative_quantity_falls_into_else_branch(self):
        
        """
        Only 0 and 1 have dedicated branches; a negative quantity is
        neither, so it flows into the general multi-item branch.
        """
        
        _, out = run_script(self.FILE, inputs=["Apple", "1.50", "-2"])
        assert "You bought -2 Apples" in out
        assert "Total: £-3.00" in out

    def test_total_rounds_to_two_decimal_places(self):
        _, out = run_script(self.FILE, inputs=["Widget", "1.111", "3"])
        assert "Total: £3.33" in out

    def test_item_name_with_spaces_preserved(self):
        _, out = run_script(self.FILE, inputs=["Green Apple", "2.00", "2"])
        assert "You bought 2 Green Apples" in out


# ---------------------------------------------------------------------------
# count_up_timer.py
# ---------------------------------------------------------------------------
class TestCountUpTimer:
    FILE = f"{FOLDER}/count_up_timer.py"

    def test_ten_calls_all_print_times_up(self):
        _, out = run_script(self.FILE)
        assert out.count("TIMES UP!") == 10

    def test_none_printed_after_each_call(self):
        
        """
        count() has no return statement, so wrapping every call in
        print() also prints the literal word 'None' each time.
        """
        
        _, out = run_script(self.FILE)
        assert out.count("None") == 10

    def test_first_call_counts_from_zero_to_one(self):
        _, out = run_script(self.FILE)
        assert out.startswith("0\n1\nTIMES UP!\nNone\n")

    def test_last_call_reaches_thirty(self):
        _, out = run_script(self.FILE)
        assert "29\n30\nTIMES UP!\nNone" in out

    def test_default_start_argument_is_zero(self):
        mod, _ = run_script(self.FILE)
        assert mod.count.__defaults__ == (0,)

    def test_count_function_returns_none(self):
        mod, _ = run_script(self.FILE)
        with patch("time.sleep", return_value=None):
            assert mod.count(0) is None

    def test_custom_start_value_direct_call(self, capsys):
        mod, _ = run_script(self.FILE)
        with patch("time.sleep", return_value=None):
            mod.count(5, start=3)
        captured = capsys.readouterr()
        assert "3\n4\n5\nTIMES UP!\n" in captured.out

    def test_start_greater_than_end_prints_no_numbers(self):
        
        """
        range(start, end + 1) is empty when start > end, so the loop
        body never executes - only the trailing 'TIMES UP!' prints.
        """
        
        mod, _ = run_script(self.FILE)
        with patch("time.sleep", return_value=None):
            import io
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                mod.count(2, start=5)
            assert buf.getvalue() == "TIMES UP!\n"


# ---------------------------------------------------------------------------
# distance_calculator.py
# ---------------------------------------------------------------------------
class TestDistanceCalculator:
    FILE = f"{FOLDER}/distance_calculator.py"

    def test_positive_distance(self):
        _, out = run_script(self.FILE, inputs=["0", "100"])
        assert "You travelled 100.0km!" in out

    def test_negative_distance_if_reversed(self):
        _, out = run_script(self.FILE, inputs=["100", "0"])
        assert "You travelled -100.0km!" in out

    def test_non_numeric_input_raises_uncaught_value_error(self):
        with pytest.raises(ValueError):
            run_script(self.FILE, inputs=["abc", "100"])

    def test_decimal_inputs_rounded_to_two_places(self):
        _, out = run_script(self.FILE, inputs=["1.111", "5.555"])
        assert "You travelled 4.44km!" in out

    def test_identical_points_gives_zero_distance(self):
        _, out = run_script(self.FILE, inputs=["50", "50"])
        assert "You travelled 0.0km!" in out


# ---------------------------------------------------------------------------
# divide.py
# ---------------------------------------------------------------------------
class TestDivide:
    FILE = f"{FOLDER}/divide.py"

    def test_output(self):
        _, out = run_script(self.FILE)
        assert _.result == 4.0
        assert "4.0" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.divide(10, 2) == 5

    def test_division_by_zero_raises(self):
        mod, _ = run_script(self.FILE)
        with pytest.raises(ZeroDivisionError):
            mod.divide(1, 0)

    def test_divide_negative_numbers(self):
        mod, _ = run_script(self.FILE)
        assert mod.divide(-10, 2) == -5

    def test_divide_returns_float(self):
        mod, _ = run_script(self.FILE)
        assert isinstance(mod.divide(4, 2), float)


# ---------------------------------------------------------------------------
# drink_script_example.py
# ---------------------------------------------------------------------------
class TestDrinkScriptExample:
    FILE = "imperitive_programming/syntax_fundamentals/drink_script_example.py" # Full path for the module cache cleaner
    MODULE_PATH = "imperitive_programming.syntax_fundamentals.drink_script_example"

    @pytest.fixture(autouse=True)
    def _clean_module_cache(self):
        """
        Reset the specific module path before/after each test.
        """
        sys.modules.pop(self.MODULE_PATH, None)
        yield
        sys.modules.pop(self.MODULE_PATH, None)

    def test_drink_script_imports_and_calls_foods_function(self):
        _, out = run_script(self.FILE)
        assert "Your favourite food is 'RICE'!" in out
        assert "Your favourite drink is 'TEA'!" in out

    def test_drink_script_has_no_guard_and_always_executes(self, monkeypatch, capsys):
        
        """
        Importing the module via its full package path to verify
        the lack of a guard clause.
        """
        
        import imperitive_programming.syntax_fundamentals.drink_script_example as drink_script_example # noqa: F401
        
        captured = capsys.readouterr()
        assert "Your favourite food is 'RICE'!" in captured.out
        assert "This is SCRIPT 2!" in captured.out

    def test_drink_script_output_follows_comment_order(self):
        _, out = run_script(self.FILE)
        # Using string find to verify order of execution
        assert out.find("RICE") < out.find("TEA") < out.find("This is SCRIPT 2!")


# ---------------------------------------------------------------------------
# email_slicer.py
# ---------------------------------------------------------------------------
class TestEmailSlicer:
    FILE = f"{FOLDER}/email_slicer.py"

    def slice_email(email):
        if "@" not in email:
            raise ValueError("Invalid email: missing @ symbol")

    def test_username_and_domain_split(self):
        _, out = run_script(self.FILE, inputs=["ahsan@gmail.com"])
        assert "Username: ahsan" in out
        assert "Email Domain: gmail.com" in out

    def test_no_at_symbol_raises_uncaught_value_error(self):
        with pytest.raises(ValueError):
            run_script(self.FILE, inputs=["not-an-email", "q"])

    def test_multiple_at_symbols_uses_the_first_one(self):
        _, out = run_script(self.FILE, inputs=["a@b@c.com"])
        assert "Username: a" in out
        assert "Email Domain: b@c.com" in out

    def test_email_with_dots_in_username(self):
        _, out = run_script(self.FILE, inputs=["ahsan.iqbal@gmail.com"])
        assert "Username: ahsan.iqbal" in out

    def test_full_email_is_echoed_back(self):
        _, out = run_script(self.FILE, inputs=["test@test.co.uk"])
        assert "Email: test@test.co.uk" in out


# ---------------------------------------------------------------------------
# even_odd_detector.py
# ---------------------------------------------------------------------------
class TestEvenOddLoopDetector:
    FILE = f"{FOLDER}/even_odd_detector.py"

    def test_even_and_odd_counts(self):
        _, out = run_script(self.FILE)
        assert "We have 6 even numbers" in out
        assert "We have 5 odd numbers" in out

    def test_individual_numbers_present(self):
        _, out = run_script(self.FILE)
        lines = out.splitlines()
        for n in (0, 2, 4, 6, 8, 10):
            assert str(n) in lines
        for n in (1, 3, 5, 7, 9):
            assert str(n) in lines

    def test_even_numbers_printed_before_odd_numbers(self):
        _, out = run_script(self.FILE)
        assert out.find("We have 6 even numbers") < out.find("We have 5 odd numbers")

    def test_no_input_required(self):
        
        """
        The script has no input() calls, so it should run identically
        with an empty inputs list.
        """
        
        _, out = run_script(self.FILE, inputs=[])
        assert "We have 6 even numbers" in out


# ---------------------------------------------------------------------------
# food_script_example.py
# ---------------------------------------------------------------------------
class TestFoodScriptExample:
    FILE = "imperitive_programming/syntax_fundamentals/food_script_example.py" # Full path for the module cache cleaner
    MODULE_PATH = "imperitive_programming.syntax_fundamentals.food_script_example"

    @pytest.fixture(autouse=True)
    def _clean_module_cache(self):
        
        """
        Reset the specific module path before/after each test to ensure
        fresh imports and no state pollution.
        """
        
        sys.modules.pop(self.MODULE_PATH, None)
        yield
        sys.modules.pop(self.MODULE_PATH, None)

    def test_food_script_runs_main_when_executed_directly(self):
        _, out = run_script(self.FILE)
        assert "You are seeing SCRIPT 1!" in out
        assert "Your favourite food is 'CHICKEN'!" in out
        assert "Bye Bye!" in out

    def test_food_script_stays_silent_on_a_plain_import(self, monkeypatch, capsys):
        
        # Importing the module via its full package path.
        import imperitive_programming.syntax_fundamentals.food_script_example as food_script_example # noqa: F401
        
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_food_script_favourite_food_function_direct(self, capsys):
        mod, _ = run_script(self.FILE)
        mod.favourite_food("pizza")
        
        captured = capsys.readouterr()
        assert "Your favourite food is 'PIZZA'!" in captured.out


# ---------------------------------------------------------------------------
# factorials.py
# ---------------------------------------------------------------------------
class TestFactorials:

    def test_factorial_of_five(self):
        assert factorial(5) == 120

    def test_factorial_of_zero_and_one(self):
        assert factorial(0) == 1
        assert factorial(1) == 1

    def test_non_numeric_input(self):
        with pytest.raises(TypeError):
            factorial("abc")

    def test_factorial_of_ten(self):
        assert factorial(10) == 3628800

    def test_factorial_is_recursive(self):
        assert factorial(6) == 6 * factorial(5)

    def test_negative_input_recurses_indefinitely_until_recursion_error(self):
        
        """
        There's no base case for negatives, so n never reaches 0 or 1
        and Python eventually raises a RecursionError.
        """
        
        with pytest.raises(RecursionError):
            factorial(-1)

    def test_script_block_valid_input(self):
        
        """
        factorials.py now also has an `if __name__ == "__main__":`
        block wrapping an input()/print() script, in addition to the bare
        function - exercise that too, not just factorial() directly.
        """
        
        _, out = run_script(f"{FOLDER}/factorials.py", inputs=["5"])
        assert out.strip() == "120"

    def test_script_block_non_numeric_input(self):
        _, out = run_script(f"{FOLDER}/factorials.py", inputs=["abc"])
        assert "Error: Invalid number format. Enter integers only (whole numbers)." in out

    def test_script_block_zero_input(self):
        _, out = run_script(f"{FOLDER}/factorials.py", inputs=["0"])
        assert out.strip() == "1"


# ---------------------------------------------------------------------------
# file_writer.py
# ---------------------------------------------------------------------------
class TestFileWriter:
    FILE = f"{FOLDER}/file_writer.py"

    def test_writes_greeting_to_file(self, tmp_path):
        run_script(self.FILE, cwd=tmp_path)
        written = (tmp_path / "AIM.txt").read_text()
        assert written == "A.I.M"

    def test_greet_function_directly(self, tmp_path):
        mod, _ = run_script(self.FILE, cwd=tmp_path)
        assert mod.greet("Test") == "Test"

    def test_greet_with_empty_string(self, tmp_path):
        mod, _ = run_script(self.FILE, cwd=tmp_path)
        assert mod.greet("") == ""

    def test_file_is_overwritten_not_appended(self, tmp_path):
        (tmp_path / "AIM.txt").write_text("OLD CONTENT")
        run_script(self.FILE, cwd=tmp_path)
        assert (tmp_path / "AIM.txt").read_text() == "A.I.M"


# ---------------------------------------------------------------------------
# food_menu.py
# ---------------------------------------------------------------------------
class TestFoodMenu:
    FILE = f"{FOLDER}/food_menu.py"

    def test_menu_lists_all_nine_items_with_prices(self):
        _, out = run_script(self.FILE, inputs=["q"])
        assert "pizza      : £2.99" in out
        assert "lemonade   : £3.99" in out

    def test_ordering_same_item_twice_aggregates_quantity(self):
        _, out = run_script(self.FILE, inputs=["pizza", "pizza", "q"])
        assert "x2 pizza      : £5.98" in out
        assert "Total:  £5.98" in out

    def test_ordering_multiple_distinct_items(self):
        _, out = run_script(self.FILE, inputs=["pizza", "pizza", "tacos", "q"])
        assert "x2 pizza      : £5.98" in out
        assert "x1 tacos      : £5.99" in out
        assert "Total:  £11.97" in out

    def test_invalid_item_is_silently_ignored(self):
        
        """
        menu.get(food) is None for unknown items, so the elif branch is
        skipped entirely with no error message and no order entry.
        """
        
        _, out = run_script(self.FILE, inputs=["burger", "q"])
        assert "burger" not in out.split("======================")[1]
        assert "Total:  £0.00" in out

    def test_immediate_quit_shows_zero_total(self):
        _, out = run_script(self.FILE, inputs=["q"])
        assert "Total:  £0.00" in out
        assert "Thank you for your order!" in out

    def test_item_name_is_case_insensitive(self):
        
        """
        `food = input(...).lower()` normalises the entry before the
        menu lookup, so uppercase item names still match.
        """
        _, out = run_script(self.FILE, inputs=["PIZZA", "q"])
        assert "x1 pizza      : £2.99" in out

    def test_payment_prompt_always_shown_at_the_end(self):
        _, out = run_script(self.FILE, inputs=["q"])
        assert "Cash or Card?" in out

    def test_menu_dict_has_nine_items(self):
        mod, _ = run_script(self.FILE, inputs=["q"])
        assert len(mod.menu) == 9


# ---------------------------------------------------------------------------
# grade_boundary_calculator.py
# ---------------------------------------------------------------------------
class TestGradeBoundaryCalculator:
    FILE = f"{FOLDER}/grade_boundary_calculator.py"

    @pytest.mark.parametrize(
        "score, expected_phrase",
        [
            ("105", "HOW?! YOU ARE LYING!"),
            ("100", "Unbelievable!"),
            ("95", "Really Good."),
            ("85", "Solid."),
            ("75", "Decent!"),
            ("65", "Not bad!"),
            ("55", "Well done! You passed!"),
            ("45", "Better luck next time."),
            ("35", "You must have slept the exam"),
            ("25", "We can do way better"),
            ("15", "Did you forgot the exam?"),
            ("5", "SERIOUSLY?! THAT LOW?!! DO BETTER!!!"),
            ("0", "ARE YOU KIDDING ME???!!! GET OUT!!!"),
            ("-5", "HOW?! YOU ARE LYING!"),
        ],
    )
    def test_grade_boundaries(self, score, expected_phrase):
        _, out = run_script(self.FILE, inputs=[score])
        assert expected_phrase in out

    def test_score_over_100_flagged_as_lying(self):
        _, out = run_script(self.FILE, inputs=["150"])
        assert "HOW?! YOU ARE LYING!" in out

    def test_negative_score_flagged_as_lying(self):
        _, out = run_script(self.FILE, inputs=["-5"])
        assert "HOW?! YOU ARE LYING!" in out

    def test_non_numeric_score_raises_uncaught_value_error(self):
        with pytest.raises(ValueError):
            run_script(self.FILE, inputs=["not-a-number"])

    def test_score_out_of_100_line_is_always_printed_first(self):
        _, out = run_script(self.FILE, inputs=["50"])
        assert "50 / 100" in out

    def test_exact_boundary_of_90_gives_really_good(self):
        _, out = run_script(self.FILE, inputs=["90"])
        assert "Really Good." in out

    def test_exact_boundary_of_50_gives_passed_message(self):
        _, out = run_script(self.FILE, inputs=["50"])
        assert "Well done! You passed!" in out


# ---------------------------------------------------------------------------
# hour_clock.py
# ---------------------------------------------------------------------------
class TestHourClock:
    FILE = f"{FOLDER}/hour_clock.py"

    def test_value_error_except_branch(self):
        val_err = patch("builtins.input", side_effect=ValueError)
        _, out = run_script(self.FILE, patches=[val_err])
        assert "All inputs must be in the form of whole integers." in out

    def test_full_countdown_from_hms(self):
        _, out = run_script(self.FILE, inputs=["0", "0", "2"])
        assert "00:00:02" in out
        assert "00:00:01" in out
        assert "TIMES UP!" in out

    def test_minutes_60_or_more_rejected(self):
        _, out = run_script(self.FILE, inputs=["1", "60", "0"])
        assert "Minutes and seconds must be less than 60." in out

    def test_all_zero_rejected(self):
        _, out = run_script(self.FILE, inputs=["0", "0", "0"])
        assert "Enter a valid time." in out

    def test_non_digit_input(self):
        _, out = run_script(self.FILE, inputs=["a", "0", "0"])
        assert "Please enter a valid input." in out

    def test_countdown_function_directly_is_instant(self):
        _, out = run_script(self.FILE, inputs=["0", "0", "1"])
        assert "TIMES UP!" in out

    def test_seconds_60_or_more_rejected(self):
        _, out = run_script(self.FILE, inputs=["0", "0", "60"])
        assert "Minutes and seconds must be less than 60." in out

    def test_one_hour_countdown_shows_correct_padding(self):
        _, out = run_script(self.FILE, inputs=["1", "0", "0"])
        assert "01:00:00" in out
        assert "00:59:59" in out


# ---------------------------------------------------------------------------
# leap_year.py
# ---------------------------------------------------------------------------
class TestLeapYear:
    FILE = f"{FOLDER}/leap_year.py"

    @pytest.mark.parametrize("year, expected", [("2024", "True"), ("2023", "False")])
    def test_leap_year_detection(self, year, expected):
        _, out = run_script(self.FILE, inputs=[year])
        assert expected in out

    def test_non_numeric_year(self):
        _, out = run_script(self.FILE, inputs=["abc"])
        assert "Integers only" in out

    def test_is_leap_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["2000"])
        assert mod.is_leap(2000) is True
        assert mod.is_leap(1900) is True  # this script's rule is "multiple of 4" only
        assert mod.is_leap(2001) is False

    def test_year_zero_is_treated_as_leap(self):
        _, out = run_script(self.FILE, inputs=["0"])
        assert "True" in out

    def test_negative_multiple_of_four_is_leap(self):
        _, out = run_script(self.FILE, inputs=["-8"])
        assert "True" in out


# ---------------------------------------------------------------------------
# math_module.py + math_file.py
# ---------------------------------------------------------------------------
class TestMathModuleAndMathFile:
    MODULE_FILE = f"{FOLDER}/math_module.py"
    IMPORTER_FILE = f"{FOLDER}/math_file.py"

    @pytest.fixture(autouse=True)
    def _clean_math_module_cache(self):
        
        """
        math_file.py's plain `import math_module` gets cached in
        sys.modules under the bare name 'math_module'; reset it before and
        after each test here so successes/failures in one test don't leak
        into another.
        """
        
        sys.modules.pop("math_module", None)
        yield
        sys.modules.pop("math_module", None)

    def test_math_module_constant_and_functions_directly(self):
        mod, _ = run_script(self.MODULE_FILE)
        assert mod.pi == 3.14159
        assert mod.square(2) == 4
        assert mod.cube(3) == 27
        assert mod.circumference(4) == pytest.approx(2 * 3.14159 * 4)
        assert mod.area(5) == pytest.approx(3.14159 * 5 ** 2)

    def test_square_of_negative_number(self):
        mod, _ = run_script(self.MODULE_FILE)
        assert mod.square(-3) == 9

    def test_cube_of_negative_number_stays_negative(self):
        mod, _ = run_script(self.MODULE_FILE)
        assert mod.cube(-2) == -8

    def test_math_file_sibling_import_resolves_automatically(self):
        """
        math_file.py does a plain `import math_module`, which only works
        when the running script's own directory is on sys.path (true when
        launched directly, e.g. from VS Code). run_script() now replicates
        that automatically for every script (mirroring runpy's own
        directly-run behaviour), so this sibling import just works without
        any special per-test handling.
        """
        _, out = run_script(self.IMPORTER_FILE)
        assert "3.14159" in out
        assert "4" in out
        assert "27" in out
        assert "25.13272" in out
        assert "78.53975" in out

    def test_math_file_output_is_in_call_order(self):
        _, out = run_script(self.IMPORTER_FILE)
        assert (
            out.find("3.14159")
            < out.find("4")
            < out.find("27")
            < out.find("25.13272")
            < out.find("78.53975")
        )

    def test_area_formula_matches_pi_r_squared(self):
        mod, _ = run_script(self.MODULE_FILE)
        assert mod.area(10) == pytest.approx(3.14159 * 100)

    def test_circumference_formula_matches_two_pi_r(self):
        mod, _ = run_script(self.MODULE_FILE)
        assert mod.circumference(1) == pytest.approx(2 * 3.14159)


# ---------------------------------------------------------------------------
# minute_timer.py
# ---------------------------------------------------------------------------
class TestMinuteTimer:
    FILE = f"{FOLDER}/minute_timer.py"

    def test_value_error_except_branch(self):
        val_err = patch("builtins.input", side_effect=ValueError)
        _, out = run_script(self.FILE, patches=[val_err])
        assert "Minutes and Seconds is in the form of integers." in out

    def test_full_countdown(self):
        _, out = run_script(self.FILE, inputs=["0", "2"])
        assert "00:02" in out
        assert "00:01" in out
        assert "TIMES UP!" in out

    def test_seconds_60_or_more_rejected(self):
        _, out = run_script(self.FILE, inputs=["1", "60"])
        assert "Can't be at least 60 seconds" in out

    def test_non_digit_input(self):
        _, out = run_script(self.FILE, inputs=["a", "0"])
        assert "Please enter a valid input." in out

    def test_one_minute_countdown_padding(self):
        _, out = run_script(self.FILE, inputs=["1", "0"])
        assert "01:00" in out
        assert "00:59" in out

    def test_zero_minutes_zero_seconds_still_runs_to_times_up(self):
        _, out = run_script(self.FILE, inputs=["0", "0"])
        assert "TIMES UP!" in out


# ---------------------------------------------------------------------------
# Multiply.py
# ---------------------------------------------------------------------------
class TestMultiply:
    FILE = f"{FOLDER}/multiply.py"

    def test_output(self):
        _, out = run_script(self.FILE)
        assert _.product == 24
        assert "24" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.multiply(7, 8) == 56

    def test_multiply_by_zero(self):
        mod, _ = run_script(self.FILE)
        assert mod.multiply(9, 0) == 0

    def test_multiply_negatives_gives_positive(self):
        mod, _ = run_script(self.FILE)
        assert mod.multiply(-3, -4) == 12


# ---------------------------------------------------------------------------
# num_pad.py
# ---------------------------------------------------------------------------
class TestNumPad:
    FILE = f"{FOLDER}/num_pad.py"

    def test_script_crashes_on_the_set_of_lists_assignment(self):
        """
        Genuine bug: despite the header comment saying to comment out the
        invalid variants, the "2D set of lists (NOT VALID)" assignment is
        left active and always raises TypeError (lists aren't hashable),
        well before the later frozenset-based assignment or the print
        loop are ever reached.
        """
        with pytest.raises(TypeError):
            run_script(self.FILE)

    def test_crash_is_specifically_about_unhashable_type(self):
        with pytest.raises(TypeError, match="unhashable"):
            run_script(self.FILE)

    def test_frozenset_variant_never_executes(self):
        
        """
        The valid frozenset-based num_pad assignment sits after the
        crash point, so it's never actually reached or printed.
        """
        
        with pytest.raises(TypeError) as exc_info:
            run_script(self.FILE)
        out = getattr(exc_info.value, "partial_output", "")
        assert out == ""  # nothing is printed before the crash


# ---------------------------------------------------------------------------
# prime_numbers.py
# ---------------------------------------------------------------------------
class TestPrimeNumbers:
    FILE = f"{FOLDER}/prime_numbers.py"

    @pytest.mark.parametrize("n, is_prime", [("2", True), ("17", True), ("1", False), ("4", False)])
    def test_prime_detection(self, n, is_prime):
        _, out = run_script(self.FILE, inputs=[n])
        if is_prime:
            assert f"The number {n} is a prime number!" in out
        else:
            assert f"The number {n} isn't prime." in out

    def test_non_numeric_input(self):
        _, out = run_script(self.FILE, inputs=["abc"])
        assert "Error: Invalid number format. Enter integers only (whole numbers)." in out

    def test_is_prime_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["2"])
        assert mod.is_prime(0) is False
        assert mod.is_prime(2) is True
        assert mod.is_prime(97) is True

    def test_zero_is_not_prime(self):
        _, out = run_script(self.FILE, inputs=["0"])
        assert "The number 0 isn't prime." in out

    def test_negative_number_is_reported_as_not_prime(self):
        
        """
        The special-case check only excludes 0 and 1; a negative number
        falls through the `while i < n` loop (which never executes since
        i=2 is not < a negative n), so `flag` stays True... except the
        function still returns based on that logic - verify actual
        behaviour rather than assuming.
        """
        
        mod, _ = run_script(self.FILE, inputs=["2"])
        assert mod.is_prime(-5) is True  # loop never runs, flag stays True

    def test_large_prime_is_correctly_detected(self):
        _, out = run_script(self.FILE, inputs=["7919"])
        assert "The number 7919 is a prime number!" in out


# ---------------------------------------------------------------------------
# random_cipher.py
# ---------------------------------------------------------------------------
class TestRandomCipher:
    FILE = f"{FOLDER}/random_cipher.py"

    @staticmethod
    def _reversed_key_patch():
        
        """
        Makes the substitution deterministic: the key is simply the
        character pool reversed, instead of randomly shuffled.
        """
        
        return patch("random.shuffle", side_effect=lambda lst: lst.reverse())

    def test_encryption_is_deterministic_with_a_reversed_key(self):
        _, out = run_script(
            self.FILE, inputs=["Hi 4!", "placeholder"], patches=[self._reversed_key_patch()]
        )
        assert "Encrypted Message: <aZoY" in out

    def test_decryption_reverses_a_matching_encryption(self):
        
        """
        Feeding the exact ciphertext produced above back in as the
        decrypt input should round-trip to the original plaintext.
        """
        
        _, out = run_script(
            self.FILE, inputs=["Hi 4!", "<aZoY"], patches=[self._reversed_key_patch()]
        )
        assert "Decrypted Message: Hi 4!" in out

    def test_unknown_characters_pass_through_unchanged(self):
        
        """
        Characters outside the tracked charset (like a tab) hit the
        fallback `else` branch and are copied over untouched.
        """
        
        _, out = run_script(
            self.FILE, inputs=["A\tB", "placeholder"], patches=[self._reversed_key_patch()]
        )
        assert "\t" in out

    def test_chars_pool_is_never_shuffled_itself(self):
        
        """
        Only `key` (a copy) is shuffled; the original `chars` list stays
        in its built, unshuffled order.
        """
        
        mod, _ = run_script(
            self.FILE, inputs=["A", "B"], patches=[self._reversed_key_patch()]
        )
        assert mod.chars[0] == " "

    def test_key_is_always_a_permutation_of_chars(self):
        mod, _ = run_script(
            self.FILE, inputs=["A", "B"], patches=[self._reversed_key_patch()]
        )
        assert sorted(mod.key) == sorted(mod.chars)
        assert len(mod.key) == len(mod.chars)

    def test_original_and_encrypted_labels_printed(self):
        _, out = run_script(
            self.FILE, inputs=["Hi", "x"], patches=[self._reversed_key_patch()]
        )
        assert "Original Message :" in out
        assert "Encrypted Message:" in out

    def test_empty_message_produces_empty_ciphertext(self):
        _, out = run_script(
            self.FILE, inputs=["", "x"], patches=[self._reversed_key_patch()]
        )
        assert "Encrypted Message: \n" in out

    def test_decrypt_fallback_for_characters_outside_the_charset(self):
        
        """
        The decrypt loop's own `else: decrypted_text += letter` branch,
        distinct from the encrypt-side fallback tested elsewhere - a tab
        in the ciphertext input passes through unchanged on decryption.
        """
        
        _, out = run_script(
            self.FILE, inputs=["A", "\t"], patches=[self._reversed_key_patch()]
        )
        assert "Decrypted Message: \t" in out

    def test_encrypted_and_decrypted_labels_printed(self):
        _, out = run_script(
            self.FILE, inputs=["Hi", "x"], patches=[self._reversed_key_patch()]
        )
        assert "Encrypted Input  :" in out
        assert "Decrypted Message:" in out


# ---------------------------------------------------------------------------
# seconds_countdown.py
# ---------------------------------------------------------------------------
class TestSecondsCountdown:
    FILE = f"{FOLDER}/seconds_countdown.py"

    def test_value_error_except_branch(self):
        val_err = patch("builtins.input", side_effect=ValueError)
        _, out = run_script(self.FILE, patches=[val_err])
        assert "Seconds is in the form of integers." in out

    def test_full_countdown(self):
        _, out = run_script(self.FILE, inputs=["3"])
        assert "03" in out
        assert "02" in out
        assert "01" in out
        assert "TIMES UP!" in out

    def test_60_or_more_rejected(self):
        _, out = run_script(self.FILE, inputs=["60"])
        assert "Can't be at least 60 seconds" in out

    def test_non_digit_input(self):
        _, out = run_script(self.FILE, inputs=["abc"])
        assert "Please enter a valid input." in out

    def test_single_digit_seconds_are_zero_padded(self):
        _, out = run_script(self.FILE, inputs=["1"])
        assert "01" in out

    def test_zero_seconds_still_hits_times_up(self):
        _, out = run_script(self.FILE, inputs=["0"])
        assert "TIMES UP!" in out


# ---------------------------------------------------------------------------
# shipping_label.py
# ---------------------------------------------------------------------------
class TestShippingLabel:
    FILE = f"{FOLDER}/shipping_label.py"

    def test_full_name_is_joined_uppercased_and_dot_free(self):
        _, out = run_script(self.FILE)
        assert "DR NOBODY KNOWS" in out

    def test_floor_is_prefixed_with_floor_label(self):
        _, out = run_script(self.FILE)
        assert "FLOOR 123" in out

    def test_street_dot_is_removed_with_no_prefix(self):
        _, out = run_script(self.FILE)
        assert "1 FAKE AV" in out

    def test_city_county_and_postcode_all_printed(self):
        _, out = run_script(self.FILE)
        assert "READING" in out
        assert "BERKSHIRE" in out
        assert "RD1 2AB" in out

    def test_output_follows_template_order(self):
        _, out = run_script(self.FILE)
        assert (
            out.find("FLOOR 123")
            < out.find("1 FAKE AV")
            < out.find("READING")
            < out.find("BERKSHIRE")
            < out.find("RD1 2AB")
        )

    def test_missing_keyword_is_silently_skipped(self, capsys):
        mod, _ = run_script(self.FILE)
        mod.shipping_label("Mr.", "John", "Smith", city="London")
        captured = capsys.readouterr()
        assert "MR JOHN SMITH" in captured.out
        assert "LONDON" in captured.out
        assert "FLOOR" not in captured.out

    def test_falsy_empty_value_is_treated_as_missing(self, capsys):
        
        """
        The walrus-operator guard `if value := location.get(key)` skips
        the line entirely when the value is empty, since "" is falsy.
        """
        
        mod, _ = run_script(self.FILE)
        mod.shipping_label("A.", "B", postcode="", city="Bristol")
        captured = capsys.readouterr()
        assert "BRISTOL" in captured.out
        assert captured.out.count("\n") == 2  # only the name and city lines

    def test_commas_are_stripped_from_values(self, capsys):
        mod, _ = run_script(self.FILE)
        mod.shipping_label("A.", "B", city="Reading, Berks")
        captured = capsys.readouterr()
        assert "READING BERKS" in captured.out

    def test_positional_args_are_joined_with_spaces(self, capsys):
        mod, _ = run_script(self.FILE)
        mod.shipping_label("Mrs.", "Jane", "Doe")
        captured = capsys.readouterr()
        assert captured.out.strip() == "MRS JANE DOE"


# ---------------------------------------------------------------------------
# shopping_cart.py
# ---------------------------------------------------------------------------
class TestShoppingCart:
    FILE = f"{FOLDER}/shopping_cart.py"

    def test_keyboard_interrupt_branch(self):
        kb = patch("builtins.input", side_effect=KeyboardInterrupt)
        _, out = run_script(self.FILE, patches=[kb])
        assert "Program Crashed!" in out

    def test_eof_error_branch(self):
        eof = patch("builtins.input", side_effect=EOFError)
        _, out = run_script(self.FILE, patches=[eof])
        assert "Program Completed." in out

    def test_checkout_via_fruit_prompt(self):
        inputs = ["apple", "1.50", "banana", "0.50", "c"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "apple: £1.50" in out
        assert "banana: £0.50" in out
        assert "Total: £2.00" in out

    def test_checkout_via_price_prompt(self):
        inputs = ["apple", "c"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Total: £0.00" in out

    def test_invalid_price_caught(self):
        inputs = ["apple", "abc"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Enter a valid number" in out

    def test_cart_function_directly(self):
        inputs = ["apple", "1.00", "c"]
        mod, _ = run_script(self.FILE, inputs=inputs)
        assert mod.cart.__name__ == "cart"

    def test_multiple_items_totalled_correctly(self):
        inputs = ["apple", "1.20", "banana", "0.80", "cherry", "2.00", "c"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Total: £4.00" in out

    def test_uppercase_c_also_checks_out(self):
        inputs = ["apple", "1.00", "C"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Total: £1.00" in out


# ---------------------------------------------------------------------------
# Square.py
# ---------------------------------------------------------------------------
class TestSquare:
    FILE = f"{FOLDER}/square.py"

    def test_output(self):
        _, out = run_script(self.FILE)
        assert _.result == 16
        assert "16" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.square(5) == 25

    def test_square_of_negative_number(self):
        mod, _ = run_script(self.FILE)
        assert mod.square(-4) == 16

    def test_square_of_zero(self):
        mod, _ = run_script(self.FILE)
        assert mod.square(0) == 0


# ---------------------------------------------------------------------------
# Subtract.py
# ---------------------------------------------------------------------------
class TestSubtract:
    FILE = f"{FOLDER}/subtract.py"

    def test_output(self):
        _, out = run_script(self.FILE)
        assert _.product == 6
        assert "6" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.subtract(3, 10) == -7

    def test_subtract_from_itself_is_zero(self):
        mod, _ = run_script(self.FILE)
        assert mod.subtract(8, 8) == 0

    def test_subtract_negative_number_adds(self):
        mod, _ = run_script(self.FILE)
        assert mod.subtract(5, -5) == 10


# ---------------------------------------------------------------------------
# symbol_generator.py
# ---------------------------------------------------------------------------
class TestSymbolGenerator:
    FILE = f"{FOLDER}/symbol_generator.py"

    def test_grid_of_symbols_printed(self):
        _, out = run_script(self.FILE, inputs=["2", "3", "*"])
        assert "***" in out
        assert out.count("***") == 2

    def test_letter_symbol_rejected(self):
        _, out = run_script(self.FILE, inputs=["2", "3", "a"])
        assert "Can't be a letter nor a number. Try again" in out

    def test_digit_symbol_rejected(self):
        _, out = run_script(self.FILE, inputs=["2", "3", "5"])
        assert "Can't be a letter nor a number. Try again" in out

    def test_non_numeric_rows_caught(self):
        _, out = run_script(self.FILE, inputs=["abc"])
        assert "Invalid Input. Try Again." in out

    def test_zero_rows_prints_nothing(self):
        _, out = run_script(self.FILE, inputs=["0", "3", "#"])
        assert "#" not in out

    def test_single_row_and_column(self):
        _, out = run_script(self.FILE, inputs=["1", "1", "$"])
        assert out.strip() == "$"


# ---------------------------------------------------------------------------
# username_status.py
# ---------------------------------------------------------------------------
class TestUsernameStatus:
    FILE = f"{FOLDER}/username_status.py"

    def test_valid_username_welcomed(self):
        _, out = run_script(self.FILE, inputs=["Ahsan"])
        assert "Welcome, Ahsan!" in out

    def test_username_with_space_rejected(self):
        _, out = run_script(self.FILE, inputs=["Ahsan Iqbal"])
        assert "Bye!" in out

    def test_username_with_digit_rejected(self):
        _, out = run_script(self.FILE, inputs=["Ahsan1"])
        assert "Bye!" in out

    def test_username_too_long_rejected(self):
        _, out = run_script(self.FILE, inputs=["a" * 13])
        assert "Bye!" in out

    def test_username_at_exactly_twelve_characters_is_accepted(self):
        _, out = run_script(self.FILE, inputs=["a" * 12])
        assert f"Welcome, {'a' * 12}!" in out

    def test_leading_and_trailing_whitespace_is_stripped_first(self):
        _, out = run_script(self.FILE, inputs=["  Ahsan  "])
        assert "Welcome, Ahsan!" in out


"""
Test for Python/aim.py, the single file directly under Python/ that isn't
part of any of the topic subfolders.
"""


def test_aim_py_is_currently_empty_and_imports_cleanly():
    
    """
    aim.py is a placeholder (intended as the main pipeline entry point,
    per the README) and is currently empty. This just guards against
    anything being silently added later that breaks on import.
    """
    
    _, out = run_script("aim.py")
    assert out == ""

