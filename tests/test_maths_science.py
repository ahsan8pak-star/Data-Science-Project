"""
Pytest suite for every script under Python/maths_science_projects/.

Covers the standalone calculators (Area, Volume, Pythagoras, Sine/Cosine
Rule, etc.) as well as the composite scripts that import their siblings
directly (area_volume_calculator.py, circle_calculator.py,
triangle_calculator.py) - exercising the real cross-file behaviour rather
than testing each formula in isolation.
"""

import math
import pytest
import sys

from unittest.mock import patch
from tests.conftest import run_script

FOLDER = "imperitive_programming/maths_science_projects"


# ---------------------------------------------------------------------------
# area.py
# ---------------------------------------------------------------------------
class TestArea:
    FILE = f"{FOLDER}/area.py"

    def test_valid_area(self):
        _, out = run_script(self.FILE, inputs=["10", "5"])
        assert "Area: 50.0 cm^2" in out

    def test_non_numeric_input(self):
        _, out = run_script(self.FILE, inputs=["abc", "5"])
        assert "Numbers only" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["1", "1"])
        assert mod.area(3, 7) == 21

    def test_zero_length_gives_zero_area(self):
        _, out = run_script(self.FILE, inputs=["0", "5"])
        assert "Area: 0.0 cm^2" in out

    def test_decimal_dimensions_are_rounded(self):
        _, out = run_script(self.FILE, inputs=["3.333", "2"])
        assert "Area: 6.67 cm^2" in out

    def test_negative_dimension_is_not_rejected(self):
        
        """
        No explicit positivity check exists, so a negative width just
        flows through the multiplication.
        """
        
        _, out = run_script(self.FILE, inputs=["10", "-5"])
        assert "Area: -50.0 cm^2" in out

    def test_second_non_numeric_input_also_caught(self):
        _, out = run_script(self.FILE, inputs=["10", "abc"])
        assert "Numbers only" in out


# ---------------------------------------------------------------------------
# area_of_circle.py
# ---------------------------------------------------------------------------
class TestAreaOfCircle:
    FILE = f"{FOLDER}/area_of_circle.py"

    def test_running_directly_produces_no_output_at_all(self):
        
        """
        Genuine bug / asymmetry: unlike circumference_of_circle.py, this
        file defines calculate_area() and area_of_circle() but has NO
        `if __name__ == "__main__":` guard calling area_of_circle() at
        module level. So simply running/loading the script does nothing
        whatsoever - no prompt, no output - even though the file otherwise
        looks like a complete, runnable script.
        """
        
        _, out = run_script(self.FILE, inputs=["5"])
        assert out == ""

    def test_calculate_area_function_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.calculate_area(2) == pytest.approx(math.pi * 4)

    def test_area_of_circle_valid_radius(self, capsys):
        mod, _ = run_script(self.FILE)
        with patch("builtins.input", return_value="5"):
            mod.area_of_circle()
        captured = capsys.readouterr()
        expected = math.pi * 5 * 5
        assert f"Area of Circle: {expected:.2f}" in captured.out

    def test_area_of_circle_zero_radius_rejected(self, capsys):
        mod, _ = run_script(self.FILE)
        with patch("builtins.input", return_value="0"):
            mod.area_of_circle()
        captured = capsys.readouterr()
        assert "Enter a valid radius" in captured.out

    def test_area_of_circle_negative_radius_rejected(self, capsys):
        mod, _ = run_script(self.FILE)
        with patch("builtins.input", return_value="-3"):
            mod.area_of_circle()
        captured = capsys.readouterr()
        assert "Enter a valid radius" in captured.out

    def test_area_of_circle_non_numeric_radius(self, capsys):
        mod, _ = run_script(self.FILE)
        with patch("builtins.input", return_value="abc"):
            mod.area_of_circle()
        captured = capsys.readouterr()
        assert "Numbers only" in captured.out

    def test_area_of_circle_type_error_branch(self, capsys):
        
        """
        The `except TypeError:` clause can't actually be reached through
        any normal string input - float(radius) only ever raises
        ValueError for bad text, never TypeError, since input() always
        returns a str. Exercised here by making input() itself raise
        TypeError, purely to confirm the except clause's own message.
        """
        mod, _ = run_script(self.FILE)
        with patch("builtins.input", side_effect=TypeError):
            mod.area_of_circle()
        captured = capsys.readouterr()
        assert "Positive Numbers only. Meaning numbers greater than 0." in captured.out

    def test_area_of_circle_keyboard_interrupt_branch(self, capsys):
        mod, _ = run_script(self.FILE)
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            mod.area_of_circle()
        captured = capsys.readouterr()
        assert "Unusual Crash Detected." in captured.out

    def test_area_of_circle_output_uses_boxed_format(self, capsys):
        mod, _ = run_script(self.FILE)
        with patch("builtins.input", return_value="5"):
            mod.area_of_circle()
        captured = capsys.readouterr()
        assert "-----------------------------------------" in captured.out

    def test_calculate_area_large_radius(self):
        mod, _ = run_script(self.FILE)
        assert mod.calculate_area(1000) == pytest.approx(math.pi * 1000 * 1000)


# ---------------------------------------------------------------------------
# area_of_triangle.py
# ---------------------------------------------------------------------------
class TestAreaOfTriangle:
    FILE = f"{FOLDER}/area_of_triangle.py"

    def test_valid_area(self):
        _, out = run_script(self.FILE, inputs=["10", "4"])
        assert "Result: Area is 20.0 cm^2" in out

    def test_blank_input_skips_calculation(self):
        _, out = run_script(self.FILE, inputs=["", "4"])
        assert "Result" not in out

    def test_non_numeric_input_shows_message(self):
        _, out = run_script(self.FILE, inputs=["abc", "4"])
        assert "Invalid input. Numbers only." in out

    def test_get_float_input_directly(self):
        mod, _ = run_script(self.FILE, inputs=["10", "4"])
        assert mod.get_float_input.__name__ == "get_float_input"

    def test_zero_base_skips_result(self):
        
        """
        0 is falsy in Python, so `if b and h:` treats a zero base the
        same as a missing one and silently skips the calculation.
        """
        
        _, out = run_script(self.FILE, inputs=["0", "4"])
        assert "Result" not in out

    def test_decimal_dimensions_rounded_correctly(self):
        _, out = run_script(self.FILE, inputs=["7.5", "4"])
        assert "Result: Area is 15.0 cm^2" in out

    def test_both_blank_skips_calculation(self):
        _, out = run_script(self.FILE, inputs=["", ""])
        assert "Result" not in out


# ---------------------------------------------------------------------------
# area_volume_calculator.py
# ---------------------------------------------------------------------------
class TestAreaAndVolumeCalculator:
    FILE = f"{FOLDER}/area_volume_calculator.py"

    def test_area_choice(self):
        _, out = run_script(self.FILE, inputs=["1", "10", "5"])
        assert "Area: 50.0 cm\u00b2" in out

    def test_volume_choice(self):
        _, out = run_script(self.FILE, inputs=["2", "2", "3", "4"])
        assert "Volume: 24.0 cm\u00b3" in out

    def test_invalid_choice(self):
        _, out = run_script(self.FILE, inputs=["9"])
        assert "Invalid choice. Please run the program again." in out

    def test_non_numeric_dimension(self):
        _, out = run_script(self.FILE, inputs=["1", "abc", "5"])
        assert "Error: Numbers only." in out

    def test_functions_directly(self):
        mod, _ = run_script(self.FILE, inputs=["1", "1", "1"])
        assert mod.area(4, 5) == 20
        assert mod.volume(2, 3, 4) == 24

    def test_menu_is_shown_before_choice(self):
        _, out = run_script(self.FILE, inputs=["1", "1", "1"])
        assert "Geometry Calculator" in out
        assert "1: Calculate Area" in out
        assert "2: Calculate Volume" in out

    def test_volume_non_numeric_third_dimension(self):
        _, out = run_script(self.FILE, inputs=["2", "2", "3", "abc"])
        assert "Error: Numbers only." in out

    def test_empty_choice_is_invalid(self):
        _, out = run_script(self.FILE, inputs=[""])
        assert "Invalid choice. Please run the program again." in out


# ---------------------------------------------------------------------------
# arithmetic_calculator.py
# ---------------------------------------------------------------------------
class TestArithmeticCalculator:
    FILE = f"{FOLDER}/arithmetic_calculator.py"

    def test_addition_chain_with_no_rounding(self):
        inputs = ["10", "+", "5", "", "n"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "| Result: 15 |" in out

    def test_floor_division_by_zero_shows_error(self):
        inputs = ["10", "//", "0", ""]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Undefined. You can't divide anything by 0." in out

    def test_modulo_by_zero_shows_error(self):
        inputs = ["10", "%", "0", ""]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Undefined. You can't divide anything by 0." in out

    def test_blank_next_number_breaks_the_chain_early(self):
        
        """
        Distinct from a blank *operator* (which breaks earlier, at a
        separate `if not op: break`): providing a valid operator but then
        pressing Enter for the next number hits its own break a few lines
        later, before that dangling operator can ever be applied.
        """
        
        inputs = ["10", "+", "5", "*", "", "n"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "| Result: 15 |" in out

    def test_invalid_rounding_choice_shows_message(self):
        inputs = ["10", "+", "5", "", "z"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Invalid choice. Try again." in out
        assert "| Result: 15 |" in out
        assert "| Result: 15 |" in out

    def test_division_by_zero_shows_error_string_result(self):
        inputs = ["10", "/", "0", ""]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Undefined. You can't divide anything by 0." in out

    def test_decimal_place_rounding(self):
        inputs = ["10", "/", "3", "", "d", "2"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "| Result: 3.33 |" in out

    def test_no_first_number_exits_immediately(self):
        _, out = run_script(self.FILE, inputs=[""])
        assert "No input provided. Exiting." in out

    def test_arithmetic_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["1", "+", "1", "", "n"])
        assert mod.arithmetic(2, "+", 3) == 5
        assert mod.arithmetic(2, "-", 3) == -1
        assert mod.arithmetic(2, "*", 3) == 6
        assert mod.arithmetic(6, "/", 3) == 2
        assert mod.arithmetic(6, "//", 4) == 1
        assert mod.arithmetic(6, "%", 4) == 2
        assert mod.arithmetic(2, "**", 3) == 8
        assert mod.arithmetic(1, "/", 0) == "Error: Undefined. You can't divide anything by 0."

    def test_significant_figures_rounding(self):
        inputs = ["123.456", "+", "0", "", "s", "4"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "| Result: 123.5 |" in out

    def test_floor_division_chain(self):
        inputs = ["17", "//", "5", "", "n"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "| Result: 3 |" in out

    def test_invalid_first_number_raises_message(self):
        _, out = run_script(self.FILE, inputs=["not-a-number"])
        assert "Incorrect Format. Enter valid numbers." in out

    def test_chained_operations_of_three_numbers(self):
        inputs = ["2", "+", "3", "*", "4", "", "n"]
        _, out = run_script(self.FILE, inputs=inputs)
        # (2 + 3) = 5, then 5 * 4 = 20
        assert "| Result: 20 |" in out

# ---------------------------------------------------------------------------
# banking_program.py
# ---------------------------------------------------------------------------
class TestBankingProgram:
    FILE = f"{FOLDER}/banking_program.py"

    def test_show_balance_direct(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        mod.show_balance(123.4)
        captured = capsys.readouterr()
        assert "Balance: £123.40" in captured.out

    def test_deposit_valid_amount_returned(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="50"):
            result = mod.deposit()
        assert result == 50.0

    def test_deposit_produces_no_confirmation_message(self, capsys):
        
        """
        Asymmetry worth flagging: withdraw() prints two confirmation
        lines ("You have withdrew..."/"You have ... left.") on success,
        but deposit() has no equivalent - it silently just returns the
        amount with no printed confirmation at all.
        """
        
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="50"):
            mod.deposit()
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_deposit_negative_amount_rejected(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="-10"):
            result = mod.deposit()
        captured = capsys.readouterr()
        assert result == 0
        assert "Enter Positive Deposits." in captured.out

    def test_deposit_more_than_two_decimals_rejected(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="10.999"):
            result = mod.deposit()
        captured = capsys.readouterr()
        assert result == 0
        assert "Funds have to be within 2 decimal places." in captured.out

    def test_deposit_exactly_two_decimals_accepted(self):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="10.99"):
            result = mod.deposit()
        assert result == 10.99

    def test_deposit_non_numeric_rejected(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="abc"):
            result = mod.deposit()
        captured = capsys.readouterr()
        assert result == 0
        assert "Invalid Input. Numbers Only." in captured.out

    def test_withdraw_valid_amount(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="30"):
            result = mod.withdraw(100)
        captured = capsys.readouterr()
        assert result == 30.0
        assert "You have withdrew £30.00." in captured.out
        assert "You have £70.00 left." in captured.out

    def test_withdraw_insufficient_funds(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="150"):
            result = mod.withdraw(100)
        captured = capsys.readouterr()
        assert result == 0
        assert "Insufficient Funds." in captured.out
        assert "You need £50.00 to complete transaction." in captured.out

    def test_withdraw_negative_amount_rejected(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="-5"):
            result = mod.withdraw(100)
        captured = capsys.readouterr()
        assert result == 0
        assert "No Negative Amounts." in captured.out

    def test_withdraw_non_numeric_rejected(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="abc"):
            result = mod.withdraw(100)
        captured = capsys.readouterr()
        assert result == 0
        assert "Invalid Input. Numbers Only." in captured.out

    def test_full_session_deposit_then_withdraw_then_check_balance(self):
        inputs = ["2", "100", "3", "30", "1", "4"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "You have withdrew £30.00." in out
        assert "Balance: £70.00" in out
        assert ">>> Shutting Down... <<<" in out

    def test_invalid_menu_choice_shows_message(self):
        inputs = ["9", "4"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Invalid Choice." in out
        assert "Try Again." in out

    def test_menu_banner_shown(self):
        _, out = run_script(self.FILE, inputs=["4"])
        assert "Banking Program" in out
        assert "Main Menu" in out


# ---------------------------------------------------------------------------
# card_validator.py
# ---------------------------------------------------------------------------
class TestCardValidator:
    FILE = f"{FOLDER}/card_validator.py"

# ---------------------------------------------------------------------------
# circle_calculator.py
# ---------------------------------------------------------------------------
class TestCircleCalculator:
    FILE = f"{FOLDER}/circle_calculator.py"

    def test_option_1_delegates_to_area_of_circle(self):
        _, out = run_script(self.FILE, inputs=["1", "5"])
        expected = math.pi * 5 * 5
        assert "AREA OF CIRCLE" in out
        assert f"Area of Circle: {expected:.2f}" in out

    def test_option_2_delegates_to_circumference(self):
        _, out = run_script(self.FILE, inputs=["2", "5"])
        expected = math.pi * 2 * 5
        assert "CIRCUMFERENCE OF CIRCLE" in out
        assert f"Circumference of Circle: {expected:.2f}" in out

    def test_invalid_numeric_option_rejected(self):
        _, out = run_script(self.FILE, inputs=["9"])
        assert "Invalid Option. Try Again." in out

    def test_non_digit_option_falls_to_invalid_branch_not_a_crash(self):
        
        """
        `choice.isdigit() and int(choice) == 1` short-circuits safely
        for non-digit text - no ValueError, just the else branch.
        """
        
        _, out = run_script(self.FILE, inputs=["abc"])
        assert "Invalid Option. Try Again." in out

    def test_empty_option_is_invalid(self):
        _, out = run_script(self.FILE, inputs=[""])
        assert "Invalid Option. Try Again." in out

    def test_menu_banner_and_options_shown(self):
        _, out = run_script(self.FILE, inputs=["1", "5"])
        assert "CIRCLE CALCULATOR" in out
        assert "1. Area of Circle" in out
        assert "2. Circumference of Circle" in out

    def test_keyboard_interrupt_on_choice_prompt_uses_own_except(self):
        
        """
        A KeyboardInterrupt during the outer `choice = input(...)` call
        is caught by circle_calculator.py's own except block.
        """
        
        kb = patch("builtins.input", side_effect=KeyboardInterrupt)
        _, out = run_script(self.FILE, patches=[kb])
        assert "We apologise for any inconvenience." in out
        assert "Run the program again." in out

    def test_keyboard_interrupt_on_delegated_radius_prompt_is_swallowed_inside(self):
        
        """
        Genuine, subtle nesting behaviour: if the KeyboardInterrupt
        instead happens on the radius prompt *inside* the delegated
        area_of_circle() call, it's caught by that inner function's own
        `except KeyboardInterrupt` ("Unusual Crash Detected.") - circle_
        calculator.py's own outer except never even fires for that case.
        """
        
        call_count = {"n": 0}

        def fake_input(prompt=""):
            call_count["n"] += 1
            if call_count["n"] == 1:
                return "1"  # choose Area of Circle
            raise KeyboardInterrupt

        kb = patch("builtins.input", side_effect=fake_input)
        _, out = run_script(self.FILE, patches=[kb])
        assert "Unusual Crash Detected." in out
        assert "We apologise for any inconvenience." not in out

    def test_own_value_error_except_is_effectively_unreachable_in_practice(self):
        
        """
        circle_calculator.py's own `except ValueError:` can't actually be
        triggered by any real typed input: the choice prompt is a plain
        input() (never raises ValueError on its own), `int(choice)` is
        guarded by `choice.isdigit()` first, and the only real float()
        parsing happens inside the delegated functions, which already
        catch their own ValueError internally. This except clause is only
        reachable at all by making input() itself raise ValueError
        artificially, as done here - it's defensive code with no natural
        trigger path.
        """
        
        val_err = patch("builtins.input", side_effect=ValueError)
        _, out = run_script(self.FILE, patches=[val_err])
        assert "Positive Numbers Only." in out


# ---------------------------------------------------------------------------
# circumference_of_circle.py
# ---------------------------------------------------------------------------
class TestCircumferenceOfCircle:
    FILE = f"{FOLDER}/circumference_of_circle.py"

    def test_valid_radius_when_run_directly(self):
        
        """
        Unlike area_of_circle.py, this file DOES have a working
        `if __name__ == "__main__": circumference()` guard, so running it
        directly correctly prompts and prints a result.
        """
        
        _, out = run_script(self.FILE, inputs=["5"])
        expected = math.pi * 2 * 5
        assert f"Circumference of Circle: {expected:.2f}" in out

    def test_zero_radius_rejected(self):
        _, out = run_script(self.FILE, inputs=["0"])
        assert "Enter a valid radius" in out

    def test_negative_radius_rejected(self):
        _, out = run_script(self.FILE, inputs=["-5"])
        assert "Enter a valid radius" in out

    def test_non_numeric_radius(self):
        _, out = run_script(self.FILE, inputs=["abc"])
        assert "Numbers only" in out

    def test_calculate_circumference_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["1"])
        assert mod.calculate_circumference(1) == pytest.approx(2 * math.pi)

    def test_calculate_circumference_larger_radius(self):
        mod, _ = run_script(self.FILE, inputs=["1"])
        assert mod.calculate_circumference(10) == pytest.approx(20 * math.pi)

    def test_decimal_radius(self):
        _, out = run_script(self.FILE, inputs=["2.5"])
        expected = math.pi * 2 * 2.5
        assert f"Circumference of Circle: {expected:.2f}" in out

    def test_type_error_branch(self):
        
        """
        Same as area_of_circle.py: except TypeError is unreachable via
        normal string input, exercised here by making input() itself
        raise it.
        """
        
        type_err = patch("builtins.input", side_effect=TypeError)
        _, out = run_script(self.FILE, patches=[type_err])
        assert "Positive Numbers only. Meaning greater than 0." in out

    def test_keyboard_interrupt_branch(self):
        kb = patch("builtins.input", side_effect=KeyboardInterrupt)
        _, out = run_script(self.FILE, patches=[kb])
        assert "Unusual Crash Detected." in out

    def test_output_uses_boxed_format(self):
        _, out = run_script(self.FILE, inputs=["5"])
        assert "-----------------------------------------" in out


# ---------------------------------------------------------------------------
# compound_debt_calculator.py
# ---------------------------------------------------------------------------
class TestCompoundDebtCalculator:
    FILE = f"{FOLDER}/compound_debt_calculator.py"

    def test_negative_amount_computes_debt(self):
        inputs = ["-1000", "5", "2"]
        _, out = run_script(self.FILE, inputs=inputs)
        expected = -1000 * ((1 + 5 / 100) ** 2)
        assert f"Total Amount: £{expected:.2f}" in out

    def test_positive_amount_rejected(self):
        _, out = run_script(self.FILE, inputs=["1000"])
        assert "This is only for negative (-) values." in out

    def test_zero_amount_rejected(self):
        _, out = run_script(self.FILE, inputs=["0"])
        assert "Result will be 0" in out

    def test_non_numeric_input(self):
        _, out = run_script(self.FILE, inputs=["abc"])
        assert "Enter a valid input." in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["0"])
        assert mod.compound_debt(-1000, 5, 2) == pytest.approx(-1102.5)

    def test_zero_rate_leaves_amount_unchanged(self):
        inputs = ["-500", "0", "3"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Total Amount: £-500.00" in out

    def test_zero_time_leaves_amount_unchanged(self):
        inputs = ["-500", "10", "0"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Total Amount: £-500.00" in out

    def test_non_numeric_rate_raises_message(self):
        _, out = run_script(self.FILE, inputs=["-1000", "abc"])
        assert "Enter a valid input." in out


# ---------------------------------------------------------------------------
# compound_interest_rate.py
# ---------------------------------------------------------------------------
class TestCompoundInterestRate:
    FILE = f"{FOLDER}/compound_interest_rate.py"

    def test_positive_amount_computes_interest(self):
        inputs = ["1000", "5", "2"]
        _, out = run_script(self.FILE, inputs=inputs)
        expected = 1000 * ((1 + 5 / 100) ** 2)
        assert f"Total Amount: £{expected:.2f}" in out

    def test_negative_amount_rejected(self):
        _, out = run_script(self.FILE, inputs=["-1000"])
        assert "Amount can't be negative (-)." in out

    def test_zero_amount_rejected(self):
        _, out = run_script(self.FILE, inputs=["0"])
        assert "Result will be 0" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["0"])
        assert mod.compound_interest(1000, 5, 2) == pytest.approx(1102.5)

    def test_non_numeric_input(self):
        _, out = run_script(self.FILE, inputs=["abc"])
        assert "Enter a valid input." in out

    def test_ten_year_projection(self):
        inputs = ["2000", "3", "10"]
        _, out = run_script(self.FILE, inputs=inputs)
        expected = 2000 * ((1 + 3 / 100) ** 10)
        assert f"Total Amount: £{expected:.2f}" in out

    def test_number_of_years_echoed_back(self):
        inputs = ["1000", "5", "7"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "# of years: 7" in out


# ---------------------------------------------------------------------------
# cosine_rule.py
# ---------------------------------------------------------------------------
class TestCosineRule:
    FILE = f"{FOLDER}/cosine_rule.py"

    def test_find_side_c_given_ab_and_angle(self):
        inputs = ["side", "ab", "3", "4", "90"]
        _, out = run_script(self.FILE, inputs=inputs)
        expected = math.sqrt(3**2 + 4**2 - 2 * 3 * 4 * math.cos(math.radians(90)))
        assert f"Result: Side c is {round(expected, 2)}" in out

    def test_find_angle_given_three_sides(self):
        inputs = ["angle", "3", "4", "5", "C"]
        _, out = run_script(self.FILE, inputs=inputs)
        cos_C = ((3**2) + (4**2) - (5**2)) / (2 * 3 * 4)
        expected = round(math.degrees(math.acos(cos_C)), 2)
        assert f"Result: Angle C is {expected} degrees" in out

    def test_impossible_triangle_angle(self):
        inputs = ["angle", "1", "1", "100", "A"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Impossible triangle. These sides cannot connect." in out

    def test_invalid_side_combination(self):
        inputs = ["side", "zz"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Invalid combination." in out

    def test_find_side_b_given_ac_and_angle(self):
        inputs = ["side", "ac", "5", "6", "60"]
        _, out = run_script(self.FILE, inputs=inputs)
        expected = math.sqrt(5**2 + 6**2 - 2 * 5 * 6 * math.cos(math.radians(60)))
        assert f"Result: Side b is {round(expected, 2)}" in out

    def test_find_angle_a_given_three_sides(self):
        inputs = ["angle", "3", "4", "5", "A"]
        _, out = run_script(self.FILE, inputs=inputs)
        cos_A = ((4**2) + (5**2) - (3**2)) / (2 * 4 * 5)
        expected = round(math.degrees(math.acos(cos_A)), 2)
        assert f"Result: Angle A is {expected} degrees" in out

    def test_neither_side_nor_angle_prints_nothing_extra(self):
        inputs = ["neither"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Result" not in out

    def test_find_side_a_given_bc_and_angle(self):
        inputs = ["side", "bc", "4", "5", "60"]
        _, out = run_script(self.FILE, inputs=inputs)
        expected = math.sqrt(4**2 + 5**2 - 2 * 4 * 5 * math.cos(math.radians(60)))
        assert f"Result: Side a is {round(expected, 2)}" in out

    def test_find_angle_b_impossible_triangle(self):
        inputs = ["angle", "1", "1", "100", "B"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Impossible triangle. These sides cannot connect." in out

    def test_find_angle_c_impossible_triangle(self):
        inputs = ["angle", "1", "1", "100", "C"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Impossible triangle. These sides cannot connect." in out

    def test_find_angle_b_success_case(self):
        
        """
        Success (non-impossible) path for angle B specifically, as
        distinct from the impossible-triangle case above.
        """
        
        inputs = ["angle", "3", "4", "5", "B"]
        _, out = run_script(self.FILE, inputs=inputs)
        cos_B = ((3**2) + (5**2) - (4**2)) / (2 * 3 * 5)
        expected = round(math.degrees(math.acos(cos_B)), 2)
        assert f"Result: Angle B is {expected} degrees" in out

    def test_blank_input_returns_none_without_crashing(self):
        
        """
        Pressing Enter with no value hits get_float_input's own blank
        check, distinct from the try/except numeric-parsing path below.
        """
        
        inputs = ["side", "ab", "", "4", "90"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Result" not in out

    def test_non_numeric_side_length_caught(self):
        inputs = ["side", "ab", "abc", "4", "90"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Invalid input. Numbers only." in out

    def test_cosine_rule_silently_produces_nothing_when_imported_via_triangle_calculator(self):
        
        """
        Genuine, subtle bug: cosine_rule.py's own get_float_input() checks
        `if __name__ == "__main__":` - but that checks *cosine_rule's own*
        module-level __name__, not the top-level script's. When
        triangle_calculator.py does `import cosine_rule` and calls
        `cosine_rule.calculate()`, cosine_rule's __name__ is "cosine_rule",
        not "__main__", so that guard is always False and
        get_float_input() silently returns None for every value - meaning
        the Cosine Rule mode inside the triangle calculator can never
        actually produce a result, even with perfectly valid input.
        """
        
        inputs = ["A", "2", "side", "ab", "3", "4", "90", "6"]
        _, out = run_script("imperitive_programming/maths_science_projects/triangle_calculator.py", inputs=inputs)
        assert "Result: Side c is 5.0" in out

    def test_sine_rule_unaffected_by_the_same_pattern_when_imported(self):
        
        """
        Contrast case: sine_rule.py's get_float_input has no such nested
        guard, so Sine Rule mode works correctly through
        triangle_calculator.py, unlike Cosine Rule mode above.
        """
        
        inputs = ["A", "1", "angle", "ab", "3", "4", "A", "40", "6"]
        _, out = run_script("imperitive_programming/maths_science_projects/triangle_calculator.py", inputs=inputs)
        assert "Result: Angle B is" in out


# ---------------------------------------------------------------------------
# perimeter_of_triangle.py
# ---------------------------------------------------------------------------
class TestPerimeterOfTriangle:
    FILE = f"{FOLDER}/perimeter_of_triangle.py"

    def test_valid_perimeter(self):
        _, out = run_script(self.FILE, inputs=["3", "4", "5"])
        assert "Result: Perimeter is 12.0 cm" in out

    def test_missing_side_skips_result(self):
        _, out = run_script(self.FILE, inputs=["3", "", "5"])
        assert "Result" not in out

    def test_non_numeric_side_shows_message(self):
        _, out = run_script(self.FILE, inputs=["abc", "4", "5"])
        assert "Invalid input. Numbers only." in out

    def test_decimal_sides_rounded(self):
        _, out = run_script(self.FILE, inputs=["1.111", "2.222", "3.333"])
        assert "Result: Perimeter is 6.67 cm" in out

    def test_zero_side_skips_result(self):
        _, out = run_script(self.FILE, inputs=["0", "4", "5"])
        assert "Result" not in out

    def test_all_sides_equal(self):
        _, out = run_script(self.FILE, inputs=["5", "5", "5"])
        assert "Result: Perimeter is 15.0 cm" in out


# ---------------------------------------------------------------------------
# pythagoras_theorem.py
# ---------------------------------------------------------------------------
class TestPythagorasTheorem:
    FILE = f"{FOLDER}/pythagoras_theorem.py"

    def test_find_hypotenuse(self):
        _, out = run_script(self.FILE, inputs=["3", "4", ""])
        assert "Result: Hypotenuse (c) is 5.0 cm" in out

    def test_non_numeric_side_caught(self):
        _, out = run_script(self.FILE, inputs=["abc", "4", ""])
        assert "Invalid input. Numbers only." in out

    def test_find_missing_side_a(self):
        _, out = run_script(self.FILE, inputs=["", "4", "5"])
        assert "Result: Side (a) is 3.0 cm" in out

    def test_find_missing_side_b(self):
        _, out = run_script(self.FILE, inputs=["3", "", "5"])
        assert "Result: Side (b) is 4.0 cm" in out

    def test_invalid_hypotenuse_less_than_other_side(self):
        _, out = run_script(self.FILE, inputs=["", "10", "5"])
        assert "Error: Hypotenuse (c) MUST be strictly greater than side (b)." in out

    def test_must_provide_exactly_two_values(self):
        _, out = run_script(self.FILE, inputs=["3", "4", "5"])
        assert "Error: You must provide exactly TWO known values." in out

    def test_all_blank_also_rejected(self):
        _, out = run_script(self.FILE, inputs=["", "", ""])
        assert "Error: You must provide exactly TWO known values." in out

    def test_invalid_hypotenuse_less_than_side_a(self):
        _, out = run_script(self.FILE, inputs=["10", "", "5"])
        assert "Error: Hypotenuse (c) MUST be strictly greater than side (a)." in out

    def test_classic_five_twelve_thirteen_triangle(self):
        _, out = run_script(self.FILE, inputs=["5", "12", ""])
        assert "Result: Hypotenuse (c) is 13.0 cm" in out


# ---------------------------------------------------------------------------
# simple_debt_calculator.py
# ---------------------------------------------------------------------------
class TestSimpleDebtCalculator:
    FILE = f"{FOLDER}/simple_debt_calculator.py"

    def test_negative_amount_computes_debt(self):
        inputs = ["-1000", "5", "2"]
        _, out = run_script(self.FILE, inputs=inputs)
        expected = -1000 * (1 + (5 * 2) / 100)
        assert f"Total Amount: £{expected:.2f}" in out

    def test_positive_amount_rejected(self):
        _, out = run_script(self.FILE, inputs=["1000"])
        assert "This is only for negative (-) values." in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["0"])
        assert mod.simple_debt(-1000, 5, 2) == pytest.approx(-1100.0)

    def test_zero_amount_rejected(self):
        _, out = run_script(self.FILE, inputs=["0"])
        assert "Result will be 0" in out

    def test_non_numeric_input(self):
        _, out = run_script(self.FILE, inputs=["abc"])
        assert "Enter a valid input." in out

    def test_annual_rate_echoed_with_two_decimals(self):
        inputs = ["-1000", "5.5", "2"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Annual Rate: 5.50%" in out

    def test_one_year_term(self):
        inputs = ["-2000", "10", "1"]
        _, out = run_script(self.FILE, inputs=inputs)
        expected = -2000 * (1 + (10 * 1) / 100)
        assert f"Total Amount: £{expected:.2f}" in out


# ---------------------------------------------------------------------------
# simple_interest_rate.py
# ---------------------------------------------------------------------------
class TestSimpleInterestRate:
    FILE = f"{FOLDER}/simple_interest_rate.py"

    def test_positive_amount_computes_interest(self):
        inputs = ["1000", "5", "2"]
        _, out = run_script(self.FILE, inputs=inputs)
        expected = 1000 * (1 + (5 * 2) / 100)
        assert f"Total Amount: £{expected:.2f}" in out

    def test_negative_amount_rejected(self):
        _, out = run_script(self.FILE, inputs=["-1000"])
        assert "Amount can't be negative (-)." in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["0"])
        assert mod.simple_interest(1000, 5, 2) == pytest.approx(1100.0)

    def test_zero_amount_rejected(self):
        _, out = run_script(self.FILE, inputs=["0"])
        assert "Result will be 0" in out

    def test_non_numeric_input(self):
        _, out = run_script(self.FILE, inputs=["abc"])
        assert "Enter a valid input." in out

    def test_initial_amount_echoed_with_two_decimals(self):
        inputs = ["999.999", "5", "2"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Initial Amount: £1000.00" in out

    def test_five_year_term(self):
        inputs = ["500", "4", "5"]
        _, out = run_script(self.FILE, inputs=inputs)
        expected = 500 * (1 + (4 * 5) / 100)
        assert f"Total Amount: £{expected:.2f}" in out


# ---------------------------------------------------------------------------
# sine_rule.py
# ---------------------------------------------------------------------------
class TestSineRule:
    FILE = f"{FOLDER}/sine_rule.py"

    def test_blank_input_returns_none_without_crashing(self):
        inputs = ["angle", "ab", "", "4", "A", "40"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Result" not in out

    def test_non_numeric_side_length_caught(self):
        inputs = ["angle", "ab", "abc", "4", "A", "40"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Invalid input. Numbers only." in out

    def test_find_angle_a_given_ab_and_angle_b(self):
        
        """
        The known_ang == 'B' branch for the ab combo (as distinct from
        the 'A' branch already covered below).
        """
        
        inputs = ["angle", "ab", "3", "4", "B", "40"]
        _, out = run_script(self.FILE, inputs=inputs)
        sin_A = (3 * math.sin(math.radians(40))) / 4
        expected = round(math.degrees(math.asin(sin_A)), 2)
        assert f"Result: Angle A is {expected} degrees" in out

    def test_ab_domain_error_for_impossible_dimensions(self):
        inputs = ["angle", "ab", "1", "10", "A", "80"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Impossible dimensions (Domain Error)." in out

    def test_ab_domain_error_via_the_b_known_branch(self):
        
        """
        Same error, but reached through the sibling known_ang == 'B'
        branch rather than 'A' above - a separate code path entirely.
        """
        
        inputs = ["angle", "ab", "10", "1", "B", "80"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Impossible dimensions (Domain Error)." in out

    def test_find_angle_c_given_ac_and_angle_a(self):
        inputs = ["angle", "ac", "3", "5", "A", "30"]
        _, out = run_script(self.FILE, inputs=inputs)
        sin_C = (5 * math.sin(math.radians(30))) / 3
        expected = round(math.degrees(math.asin(sin_C)), 2)
        assert f"Result: Angle C is {expected} degrees" in out

    def test_ac_domain_error_via_the_a_known_branch(self):
        
        """
        Distinct from test_ac_domain_error_for_impossible_dimensions
        below, which goes through the sibling known_ang == 'C' branch.
        """
        
        inputs = ["angle", "ac", "1", "10", "A", "80"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Impossible dimensions (Domain Error)." in out

    def test_ac_domain_error_for_impossible_dimensions(self):
        inputs = ["angle", "ac", "10", "1", "C", "80"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Impossible dimensions (Domain Error)." in out

    def test_ac_unknown_angle_shows_error(self):
        inputs = ["angle", "ac", "3", "5", "Z"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: For sides a and c, you must know angle A or C." in out

    def test_find_angle_c_given_bc_and_angle_b(self):
        inputs = ["angle", "bc", "4", "6", "B", "35"]
        _, out = run_script(self.FILE, inputs=inputs)
        sin_C = (6 * math.sin(math.radians(35))) / 4
        expected = round(math.degrees(math.asin(sin_C)), 2)
        assert f"Result: Angle C is {expected} degrees" in out

    def test_bc_domain_error_via_the_b_known_branch(self):
        
        """
        Distinct from test_bc_domain_error_for_impossible_dimensions
        below, which goes through the sibling known_ang == 'C' branch.
        """
        
        inputs = ["angle", "bc", "1", "10", "B", "80"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Impossible dimensions (Domain Error)." in out

    def test_bc_domain_error_for_impossible_dimensions(self):
        inputs = ["angle", "bc", "10", "1", "C", "80"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Impossible dimensions (Domain Error)." in out

    def test_bc_unknown_angle_shows_error(self):
        inputs = ["angle", "bc", "4", "6", "Z"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: For sides b and c, you must know angle B or C." in out

    def test_find_side_a_given_ab_and_side_b(self):
        
        """
        The known_side == 'b' branch for the AB combo (finds side a),
        distinct from the known_side == 'a' branch (finds side b).
        """
        
        inputs = ["side", "AB", "30", "60", "b", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        a = (6 * math.sin(math.radians(30))) / math.sin(math.radians(60))
        assert f"Result: Side a is {round(a, 2)}" in out

    def test_find_side_a_given_ac_and_side_c(self):
        inputs = ["side", "AC", "40", "70", "c", "9"]
        _, out = run_script(self.FILE, inputs=inputs)
        a = (9 * math.sin(math.radians(40))) / math.sin(math.radians(70))
        assert f"Result: Side a is {round(a, 2)}" in out

    def test_find_side_c_given_bc_and_side_b(self):
        inputs = ["side", "BC", "50", "60", "b", "7"]
        _, out = run_script(self.FILE, inputs=inputs)
        c = (7 * math.sin(math.radians(60))) / math.sin(math.radians(50))
        assert f"Result: Side c is {round(c, 2)}" in out

    def test_find_angle_b_given_ab_and_angle_a(self):
        inputs = ["angle", "ab", "3", "4", "A", "40"]
        _, out = run_script(self.FILE, inputs=inputs)
        sin_B = (4 * math.sin(math.radians(40))) / 3
        expected = round(math.degrees(math.asin(sin_B)), 2)
        assert f"Result: Angle B is {expected} degrees" in out

    def test_find_side_given_two_angles(self):
        inputs = ["side", "AB", "30", "60", "a", "5"]
        _, out = run_script(self.FILE, inputs=inputs)
        b = (5 * math.sin(math.radians(60))) / math.sin(math.radians(30))
        assert f"Result: Side b is {round(b, 2)}" in out

    def test_invalid_side_combination(self):
        inputs = ["angle", "zz"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Invalid side combination." in out

    def test_invalid_angle_combination(self):
        inputs = ["side", "zz"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Invalid angle combination." in out

    def test_find_angle_c_given_ac_and_angle_c(self):
        inputs = ["angle", "ac", "5", "7", "C", "50"]
        _, out = run_script(self.FILE, inputs=inputs)
        sin_A = (5 * math.sin(math.radians(50))) / 7
        expected = round(math.degrees(math.asin(sin_A)), 2)
        assert f"Result: Angle A is {expected} degrees" in out

    def test_find_side_c_given_ac_angles(self):
        inputs = ["side", "AC", "40", "70", "a", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        c = (6 * math.sin(math.radians(70))) / math.sin(math.radians(40))
        assert f"Result: Side c is {round(c, 2)}" in out

    def test_unknown_angle_for_ab_sides_shows_error(self):
        inputs = ["angle", "ab", "3", "4", "Z"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: For sides a and b, you must know angle A or B." in out

    def test_find_angle_b_given_bc_and_angle_c(self):
        inputs = ["angle", "bc", "5", "6", "C", "50"]
        _, out = run_script(self.FILE, inputs=inputs)
        sin_B = (5 * math.sin(math.radians(50))) / 6
        expected = round(math.degrees(math.asin(sin_B)), 2)
        assert f"Result: Angle B is {expected} degrees" in out

    def test_find_side_b_given_bc_and_two_angles(self):
        inputs = ["side", "BC", "40", "70", "c", "8"]
        _, out = run_script(self.FILE, inputs=inputs)
        b = (8 * math.sin(math.radians(40))) / math.sin(math.radians(70))
        assert f"Result: Side b is {round(b, 2)}" in out


# ---------------------------------------------------------------------------
# triangle_calculator.py
# ---------------------------------------------------------------------------
class TestTriangleCalculator:
    FILE = f"{FOLDER}/triangle_calculator.py"

    def test_right_triangle_area_then_quit(self):
        inputs = ["A", "4", "6", "4", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert ">>> Calculator locked into Right mode. <<<" in out
        assert "Result: Area is 12.0" in out
        assert "Powering down..." in out

    def test_equilateral_perimeter_then_quit(self):
        inputs = ["B", "5", "5", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert ">>> Calculator locked into Equilateral mode. <<<" in out
        assert "Result: Perimeter is 15.0" in out

    def test_pythagoras_rejected_for_non_right_triangle(self):
        inputs = ["D", "3", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Pythagoras ONLY works on Right-Angled triangles. You selected Scalene." in out

    def test_invalid_menu_selection_reported(self):
        inputs = ["A", "9", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Invalid selection." in out

    def test_invalid_triangle_type_defaults_to_scalene(self):
        inputs = ["Z", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert ">>> Calculator locked into Scalene mode. <<<" in out

    def test_isosceles_perimeter_choice(self):
        inputs = ["C", "5", "3", "6", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert ">>> Calculator locked into Isosceles mode. <<<" in out
        assert "Result: Perimeter is 12.0" in out

    def test_equilateral_area_choice(self):
        inputs = ["B", "4", "10", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        expected = round((math.sqrt(3) / 4) * (10 ** 2), 2)
        assert f"Result: Area is {expected}" in out

    def test_right_triangle_pythagoras_choice(self):
        inputs = ["A", "3", "3", "4", "", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Result: Hypotenuse (c) is 5.0" in out

    def test_pythagoras_requires_exactly_two_known_values(self):
        
        """
        triangle_calculator.py has its own separate pythagoras()
        function (distinct from the standalone pythagoras_theorem.py) -
        exercising its own "all three provided" guard clause.
        """
        
        inputs = ["A", "3", "3", "4", "5", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: You must provide exactly TWO known values." in out

    def test_pythagoras_finds_side_a_given_b_and_c(self):
        inputs = ["A", "3", "", "3", "5", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Result: Adjacent side (a) is 4.0" in out

    def test_pythagoras_finds_side_b_given_a_and_c(self):
        inputs = ["A", "3", "3", "", "5", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Result: Opposite side (b) is 4.0" in out

    def test_pythagoras_side_a_impossible_when_c_not_greater_than_b(self):
        inputs = ["A", "3", "", "10", "5", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Hypotenuse (c) MUST be strictly greater than side (b)." in out

    def test_pythagoras_side_b_impossible_when_c_not_greater_than_a(self):
        inputs = ["A", "3", "10", "", "5", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Error: Hypotenuse (c) MUST be strictly greater than side (a)." in out

    def test_pythagoras_own_get_float_input_rejects_non_numeric(self):
        
        """
        triangle_calculator.py's pythagoras() uses its own local
        get_float_input(), separate from the one in pythagoras_theorem.py
        - confirms its error message specifically.
        """
        
        inputs = ["A", "3", "abc", "4", "5", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Invalid input. Please enter numbers only." in out

    def test_pythagoras_blocked_message_names_the_selected_type(self):
        inputs = ["D", "3", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "You selected Scalene." in out

    def test_scalene_perimeter_uses_three_sides(self):
        
        """
        Scalene is the match-statement's default case for perimeter()
        (unlike equilateral/isosceles, it takes 3 independent sides).
        """
        
        inputs = ["D", "5", "3", "4", "5", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert ">>> Calculator locked into Scalene mode. <<<" in out
        assert "Result: Perimeter is 12.0" in out

    def test_scalene_area_uses_base_height_formula(self):
        
        """
        Scalene is also area()'s default case, using the plain
        base * height / 2 formula rather than the right/equilateral
        specific ones.
        """
        
        inputs = ["D", "4", "10", "4", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Result: Area is 20.0" in out


# ---------------------------------------------------------------------------
# Volume.py
# ---------------------------------------------------------------------------
class TestVolume:
    FILE = f"{FOLDER}/volume.py"

    def test_valid_volume(self):
        _, out = run_script(self.FILE, inputs=["2", "3", "4"])
        assert "Volume: 24.0 cm^3" in out

    def test_non_numeric_input(self):
        _, out = run_script(self.FILE, inputs=["abc", "3", "4"])
        assert "Numbers only" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["1", "1", "1"])
        assert mod.volume(2, 3, 4) == 24

    def test_zero_depth_gives_zero_volume(self):
        _, out = run_script(self.FILE, inputs=["5", "5", "0"])
        assert "Volume: 0.0 cm^3" in out

    def test_decimal_dimensions_rounded(self):
        _, out = run_script(self.FILE, inputs=["1.5", "2", "2"])
        assert "Volume: 6.0 cm^3" in out

    def test_third_non_numeric_input_caught(self):
        _, out = run_script(self.FILE, inputs=["2", "3", "abc"])
        assert "Numbers only" in out

    def test_negative_dimension_not_rejected(self):
        _, out = run_script(self.FILE, inputs=["-2", "3", "4"])
        assert "Volume: -24.0 cm^3" in out

    def test_function_direct_with_all_equal_sides(self):
        mod, _ = run_script(self.FILE, inputs=["1", "1", "1"])
        assert mod.volume(5, 5, 5) == 125

    def test_first_non_numeric_input_caught(self):
        _, out = run_script(self.FILE, inputs=["abc", "3", "4"])
        assert "Numbers only" in out
        # only the length field triggers the try/except before it aborts
        assert "Volume:" not in out

