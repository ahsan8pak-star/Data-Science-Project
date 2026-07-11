"""
Tests for every script under Python/SyntaxFundementals/.
"""

import pytest

from tests.conftest import run_script
from syntax_fundamentals.factorials import factorial

FOLDER = "syntax_fundamentals"


class TestAdd:
    FILE = f"{FOLDER}/Add.py"

    def test_output(self):
        _, out = run_script(self.FILE)
        assert _.result == 8
        assert "8" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.add(-2, 2) == 0


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


class TestDivide:
    FILE = f"{FOLDER}/Divide.py"

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


class TestEmailSlicer:
    FILE = f"{FOLDER}/email_slicer.py"

    def test_username_and_domain_split(self):
        _, out = run_script(self.FILE, inputs=["ahsan@gmail.com"])
        assert "Username: ahsan" in out
        assert "Email Domain: gmail.com" in out

    def test_no_at_symbol_handles_error_gracefully(self):
        output = run_script(self.FILE, inputs=["not-an-email", "q"])
        assert "Invalid input" in output


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


class TestFactorials:

    def test_factorial_of_five(self):
        assert factorial(5) == 120

    def test_factorial_of_zero_and_one(self):
        assert factorial(0) == 1
        assert factorial(1) == 1

    def test_non_numeric_input(self):
        """Since the script's logic has been passed, we can test that
        passing a non-integer raises a TypeError (or add a specific
        test case in this function in here, if handled it correctly)."""
        with pytest.raises(TypeError):
            factorial("abc")


class TestFileWriter:
    FILE = f"{FOLDER}/file_writer.py"

    def test_writes_greeting_to_file(self, tmp_path):
        run_script(self.FILE, cwd=tmp_path)
        written = (tmp_path / "AIM.txt").read_text()
        assert written == "A.I.M"

    def test_greet_function_directly(self, tmp_path):
        mod, _ = run_script(self.FILE, cwd=tmp_path)
        assert mod.greet("Test") == "Test"


class TestHourClock:
    FILE = f"{FOLDER}/hour_clock.py"

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


class TestMinuteTimer:
    FILE = f"{FOLDER}/minute_timer.py"

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


class TestMultiply:
    FILE = f"{FOLDER}/Multiply.py"

    def test_output(self):
        _, out = run_script(self.FILE)
        assert _.product == 24
        assert "24" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.multiply(7, 8) == 56


class TestNumPad:
    FILE = f"{FOLDER}/num_pad.py"

    def test_script_crashes_on_the_set_of_lists_assignment(self):
        """
        Genuine bug in the source script: 
        despite the header comment saying to comment out the invalid variants, 
        the "2D set of lists (NOT VALID)" assignment is left active 
        and always raises TypeError (lists aren't hashable), 
        well before the later frozenset-based assignment 
        or the print loop are ever reached.
        """
        with pytest.raises(TypeError):
            run_script(self.FILE)


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


class TestSecondsCountdown:
    FILE = f"{FOLDER}/seconds_countdown.py"

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


class TestShoppingCart:
    FILE = f"{FOLDER}/shopping_cart.py"

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


class TestSquare:
    FILE = f"{FOLDER}/Square.py"

    def test_output(self):
        _, out = run_script(self.FILE)
        assert _.result == 16
        assert "16" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.square(5) == 25


class TestSubtract:
    FILE = f"{FOLDER}/Subtract.py"

    def test_output(self):
        _, out = run_script(self.FILE)
        assert _.product == 6
        assert "6" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.subtract(3, 10) == -7


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


"""
Test for Python/AIM.py, the single file directly under Python/ that isn't
part of any of the topic subfolders (those each have their own dedicated
test module: test_algorithms.py, test_fundamentals.py, test_logic_games.py,
test_math_science.py, test_syntax.py).

"""

def test_aim_py_is_currently_empty_and_imports_cleanly():
    """AIM.py is a placeholder (intended as the main pipeline entry point,
    per the README) and is currently empty. This just guards against
    anything being silently added later that breaks on import."""
    _, out = run_script("AIM.py")
    assert out == ""


"""
Sample test file to validate pytest configuration.
Replace with actual tests for your Python modules.

"""

def test_sample_pass():
    """Sample test that should pass."""
    assert 1 + 1 == 2


def test_sample_string():
    """Sample test for string operations."""
    result = "hello".upper()
    assert result == "HELLO"

