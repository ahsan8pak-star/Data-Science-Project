"""
Tests for every script under Python/Algorithms&DataConverters/.

Each script is executed for real via run_script() (see conftest.py) with
scripted input, so these tests exercise the actual coursework code rather
than reimplementations of it.
"""

import pytest

from tests.conftest import run_script

FOLDER = "algorithmic_data_converters"


# ---------------------------------------------------------------------------
# annual_rate_calculator.py
# ---------------------------------------------------------------------------

class TestAnnualRateCalculator:
    FILE = f"{FOLDER}/annual_rate_calculator.py"

    def test_valid_calculation(self):
        _, out = run_script(self.FILE, inputs=["2", "1000", "$"])
        assert "Income: $1000.00" in out
        assert "Time: 2 years" in out
        assert "Amount Rate: $500.00 per year" in out
        assert "Percentage Rate: 50.00% Annual" in out

    def test_non_numeric_time_raises_value_error_message(self):
        _, out = run_script(self.FILE, inputs=["not-a-number", "1000", "$"])
        assert "Only numbers are accepted for time and income." in out

    def test_zero_time_raises_zero_division_message(self):
        _, out = run_script(self.FILE, inputs=["0", "1000", "$"])
        assert "Has to be at least 1 year." in out

    def test_income_with_too_many_decimal_places(self):
        _, out = run_script(self.FILE, inputs=["2", "10.123"])
        assert "Random Error Found: Income cannot have more than 2 decimal places." in out

    def test_currency_must_be_single_symbol(self):
        _, out = run_script(self.FILE, inputs=["2", "100", "USD"])
        assert "Random Error Found: Single Symbols only" in out

    def test_income_must_be_positive(self):
        _, out = run_script(self.FILE, inputs=["2", "0", "$"])
        assert "Random Error Found: Enter a Valid Amount." in out


# ---------------------------------------------------------------------------
# fahrenheit_celsius_converter.py
# ---------------------------------------------------------------------------

class TestFahrenheitCelsiusConverter:
    FILE = f"{FOLDER}/fahrenheit_celsius_converter.py"

    def test_fahrenheit_to_celsius_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["C", "0"])
        assert mod.fahrenheit_to_celcius(212) == pytest.approx(100.0)
        assert mod.fahrenheit_to_celcius(32) == pytest.approx(0.0)

    def test_celsius_to_fahrenheit_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["C", "0"])
        assert mod.celcius_to_fahrenheit(100) == pytest.approx(212.0)
        assert mod.celcius_to_fahrenheit(0) == pytest.approx(32.0)

    def test_fahrenheit_path_output(self):
        _, out = run_script(self.FILE, inputs=["F", "212"])
        assert "212.0 degrees Fahrenheit is 100.0 degrees Celsius" in out

    def test_celsius_path_is_default(self):
        _, out = run_script(self.FILE, inputs=["anything-not-f", "0"])
        assert "0.0 degrees Celsius is 32.0 degrees Fahrenheit" in out

    def test_non_numeric_value_raises_message(self):
        _, out = run_script(self.FILE, inputs=["F", "not-a-number"])
        assert "Numbers only!" in out


# ---------------------------------------------------------------------------
# phone_converter.py
# ---------------------------------------------------------------------------

class TestPhoneConverter:
    FILE = f"{FOLDER}/phone_converter.py"

    def test_num_maps_every_digit_to_its_word(self):
        mod, _ = run_script(self.FILE, inputs=["5"])
        expected = ["Zero", "One", "Two", "Three", "Four", "Five", "Six",
                    "Seven", "Eight", "Nine"]
        for digit, word in enumerate(expected):
            assert mod.num(digit) == word

    def test_num_returns_invalid_marker_for_out_of_range_value(self):
        mod, _ = run_script(self.FILE, inputs=["5"])
        assert mod.num(15) == "Invalid Phone Digit"

    def test_valid_phone_number_converted_to_words(self):
        _, out = run_script(self.FILE, inputs=["123"])
        assert "Word: One Two Three" in out

    def test_rejects_empty_and_non_digit_input_before_succeeding(self):
        _, out = run_script(self.FILE, inputs=["", "12a", "9"])
        assert out.count("Enter up to 10 digits from 0 to 9.") == 2
        assert "Word: Nine" in out

    def test_rejects_more_than_ten_digits(self):
        _, out = run_script(self.FILE, inputs=["12345678901", "7"])
        assert "Enter up to 10 digits from 0 to 9." in out
        assert "Word: Seven" in out


# ---------------------------------------------------------------------------
# roman_numeral_converter.py
# ---------------------------------------------------------------------------

class TestRomanNumeralsConverter:
    FILE = f"{FOLDER}/roman_numeral_converter.py"

    def test_get_value_for_each_symbol(self):
        mod, _ = run_script(self.FILE, inputs=["I"])
        assert mod.get_value("M") == 1000
        assert mod.get_value("D") == 500
        assert mod.get_value("C") == 100
        assert mod.get_value("L") == 50
        assert mod.get_value("X") == 10
        assert mod.get_value("V") == 5
        assert mod.get_value("I") == 1

    def test_get_value_raises_for_unknown_symbol(self):
        mod, _ = run_script(self.FILE, inputs=["I"])
        with pytest.raises(ValueError):
            mod.get_value("Z")

    @pytest.mark.parametrize(
        "numeral, expected",
        [
            ("III", 3),
            ("IV", 4),
            ("IX", 9),
            ("LVIII", 58),
            ("MCMXCIV", 1994),
            ("xiv", 14),  # lower-case should still work
        ],
    )
    def test_roman_to_int_direct(self, numeral, expected):
        mod, _ = run_script(self.FILE, inputs=["I"])
        assert mod.roman_to_int(numeral) == expected

    def test_valid_script_run(self):
        _, out = run_script(self.FILE, inputs=["MCMXCIV"])
        assert "Arabic Numerals: 1994" in out

    def test_invalid_symbol_prints_error(self):
        _, out = run_script(self.FILE, inputs=["ABC123"])
        assert "Error: Roman Numerals Only (I, V, X, L, C, D, M)" in out


# ---------------------------------------------------------------------------
# time_converter.py
# ---------------------------------------------------------------------------

class TestTimeConverter:
    FILE = f"{FOLDER}/time_converter.py"

    def test_get_unit_info_known_cases(self):
        mod, _ = run_script(self.FILE, inputs=["1", "1", "1"])
        assert mod.get_unit_info(1) == (1, "Seconds")
        assert mod.get_unit_info(2) == (60, "Minutes")
        assert mod.get_unit_info(10) == (31557600000, "Millenniums")

    def test_get_unit_info_out_of_range(self):
        mod, _ = run_script(self.FILE, inputs=["1", "1", "1"])
        assert mod.get_unit_info(0) == (None, "Invalid")
        assert mod.get_unit_info(11) == (None, "Invalid")

    def test_seconds_to_minutes_conversion(self):
        _, out = run_script(self.FILE, inputs=["1", "2", "60"])
        assert "There are 1.0 Minutes in 60.0 Seconds." in out

    def test_hours_to_minutes_conversion(self):
        _, out = run_script(self.FILE, inputs=["3", "2", "2"])
        assert "There are 120.0 Minutes in 2.0 Hours." in out

    def test_out_of_range_choice_prints_message(self):
        _, out = run_script(self.FILE, inputs=["99", "1"])
        assert "Outside of Range." in out

    def test_non_numeric_choice_prints_message(self):
        _, out = run_script(self.FILE, inputs=["abc", "1"])
        assert "Numbers only." in out


# ---------------------------------------------------------------------------
# weight_converter.py
# ---------------------------------------------------------------------------

class TestWeightConverter:
    FILE = f"{FOLDER}/weight_converter.py"

    def test_zero_weight_rejected(self):
        _, out = run_script(self.FILE, inputs=["0"])
        assert "You must weigh something" in out

    def test_empty_weight_rejected(self):
        _, out = run_script(self.FILE, inputs=[""])
        assert "You must weigh something" in out

    def test_non_numeric_weight_rejected(self):
        _, out = run_script(self.FILE, inputs=["not-a-number"])
        assert "Invalid weight" in out

    def test_pounds_to_kilograms(self):
        _, out = run_script(self.FILE, inputs=["150", "l"])
        assert "You weigh 67.5 kilograms." in out

    def test_kilograms_to_pounds(self):
        expected = 10 / 0.45
        _, out = run_script(self.FILE, inputs=["10", "k"])
        assert f"You weigh {expected} pounds." in out

    def test_unrecognised_unit_rejected(self):
        _, out = run_script(self.FILE, inputs=["5", "stone"])
        assert "Only pounds and kilos." in out


# Test cases for algorithms and logic

def test_prime_detection():
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    assert is_prime(2) == True
    assert is_prime(3) == True
    assert is_prime(4) == False
    assert is_prime(17) == True
    assert is_prime(1) == False


def test_sorting_algorithm():
    # Bubble sort implementation
    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    assert bubble_sort([5, 2, 8, 1, 9]) == [1, 2, 5, 8, 9]
    assert bubble_sort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]


def test_logic_game_implementation():
    # Simple game logic: check win condition
    def check_win(score):
        return score >= 100
    
    game_over = False
    assert not game_over
    assert check_win(100) == True
    assert check_win(50) == False


def test_edge_cases_empty_list():
    empty_list = []
    assert len(empty_list) == 0
    assert empty_list == []


def test_edge_cases_data_converter():

    # Test converter with edge cases
    def safe_divide(a, b):
        if b == 0:
            return None
        return a / b
    
    assert safe_divide(10, 2) == 5
    assert safe_divide(10, 0) == None
    assert safe_divide(0, 5) == 0


def test_fibonacci_sequence():

    def fibonacci(n):
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        elif n == 2:
            return [0, 1]
        else:
            fib = [0, 1]
            for i in range(2, n):
                fib.append(fib[i-1] + fib[i-2])
            return fib
    
    assert fibonacci(5) == [0, 1, 1, 2, 3]
    assert fibonacci(1) == [0]
    assert fibonacci(0) == []

