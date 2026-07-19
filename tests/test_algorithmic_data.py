"""
Pytest suite for every script under Python/algorithmic_data_converters/.

Each script is executed for real via run_script() (see tests/conftest.py) with
scripted input, so these tests exercise the actual coursework code rather
than reimplementations of it. Covers fundamental/happy paths as well as
error-catching (invalid input, boundary, and exception) cases.
"""

from unittest.mock import patch
from tests.conftest import run_script

import pytest

FOLDER = "imperitive_programming/algorithmic_data_converters"


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

    def test_income_with_exactly_two_decimals_is_accepted(self):
        _, out = run_script(self.FILE, inputs=["1", "99.99", "£"])
        assert "Income: £99.99" in out
        assert "Random Error Found" not in out

    def test_empty_currency_rejected(self):
        _, out = run_script(self.FILE, inputs=["2", "100", ""])
        assert "Random Error Found: Single Symbols only" in out

    def test_negative_time_produces_negative_rate_without_crashing(self):

        """
        int(time) accepts negatives happily (no explicit guard), so a
        negative time just flows through the rate formula rather than
        raising or being rejected.
        """
        
        _, out = run_script(self.FILE, inputs=["-2", "1000", "$"])
        expected_rate = 1000 / -2
        assert f"Amount Rate: ${expected_rate:.2f} per year" in out

    def test_whole_number_time_with_decimal_income(self):
        _, out = run_script(self.FILE, inputs=["4", "999.50", "€"])
        assert "Income: €999.50" in out
        assert "Time: 4 years" in out


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

    def test_empty_first_prompt_defaults_to_celsius_path(self):
        
        """
        An empty string is falsy, so `i and i[0].upper() == "F"` skips
        straight to the else (Celsius) branch.
        """
        
        _, out = run_script(self.FILE, inputs=["", "0"])
        assert "0.0 degrees Celsius is 32.0 degrees Fahrenheit" in out

    def test_lowercase_f_is_still_accepted(self):
        _, out = run_script(self.FILE, inputs=["f", "32"])
        assert "32.0 degrees Fahrenheit is 0.0 degrees Celsius" in out

    def test_negative_forty_is_the_equal_point(self):
        """-40 is the famous point where Fahrenheit and Celsius meet."""
        _, out = run_script(self.FILE, inputs=["F", "-40"])
        assert "-40.0 degrees Fahrenheit is -40.0 degrees Celsius" in out

    def test_non_numeric_celsius_value_raises_message(self):
        _, out = run_script(self.FILE, inputs=["C", "not-a-number"])
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

    def test_single_digit_zero_converted(self):
        _, out = run_script(self.FILE, inputs=["0"])
        assert "Word: Zero" in out

    def test_ten_digit_number_is_accepted(self):
        _, out = run_script(self.FILE, inputs=["1234567890"])
        assert "Word: One Two Three Four Five Six Seven Eight Nine Zero" in out

    def test_num_returns_invalid_marker_for_negative_value(self):
        mod, _ = run_script(self.FILE, inputs=["1"])
        assert mod.num(-1) == "Invalid Phone Digit"


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

    def test_empty_string_returns_zero(self):
        _, out = run_script(self.FILE, inputs=[""])
        assert "Arabic Numerals: 0" in out

    def test_single_numeral_returns_its_value(self):
        _, out = run_script(self.FILE, inputs=["M"])
        assert "Arabic Numerals: 1000" in out

    def test_repeated_numerals_sum_correctly(self):
        _, out = run_script(self.FILE, inputs=["III"])
        assert "Arabic Numerals: 3" in out

    def test_mixed_case_numeral_still_converts(self):
        _, out = run_script(self.FILE, inputs=["mCmXciV"])
        assert "Arabic Numerals: 1994" in out

    def test_get_value_for_all_seven_symbols_covers_full_dict(self):
        mod, _ = run_script(self.FILE, inputs=["I"])
        values = {mod.get_value(s) for s in "MDCLXVI"}
        assert values == {1000, 500, 100, 50, 10, 5, 1}


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

    def test_get_unit_info_middle_cases(self):
        """Cases 5-9 (weeks/months/years/decades/centuries) weren't
        exercised by any other test."""
        mod, _ = run_script(self.FILE, inputs=["1", "1", "1"])
        assert mod.get_unit_info(5) == (604800, "Weeks")
        assert mod.get_unit_info(6) == (2629746, "Months")
        assert mod.get_unit_info(7) == (31557600, "Years")
        assert mod.get_unit_info(8) == (315576000, "Decades")
        assert mod.get_unit_info(9) == (3155760000, "Centuries")

    def test_keyboard_interrupt_handled(self):
        kb = patch("builtins.input", side_effect=KeyboardInterrupt)
        _, out = run_script(self.FILE, patches=[kb])
        assert "Program Stopped." in out

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

    def test_same_unit_conversion_is_identity(self):
        _, out = run_script(self.FILE, inputs=["4", "4", "10"])
        assert "There are 10.0 Days in 10.0 Days." in out

    def test_non_numeric_amount_after_valid_choices(self):
        _, out = run_script(self.FILE, inputs=["1", "1", "not-a-number"])
        assert "Numbers only." in out

    def test_menu_is_displayed(self):
        _, out = run_script(self.FILE, inputs=["1", "1", "1"])
        assert "The Time Converter:" in out
        assert "10. Millenniums" in out


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

    def test_uppercase_unit_letters_accepted(self):
        _, out = run_script(self.FILE, inputs=["150", "L"])
        assert "You weigh 67.5 kilograms." in out

    def test_negative_weight_is_not_rejected_by_the_zero_check(self):
        
        """
        Only `== 0` or empty is rejected; a negative value slips through
        to the float()/unit conversion path.
        """
        
        _, out = run_script(self.FILE, inputs=["-10", "k"])
        expected = -10 / 0.45
        assert f"You weigh {expected} pounds." in out

    def test_empty_unit_rejected(self):
        _, out = run_script(self.FILE, inputs=["10", ""])
        assert "Only pounds and kilos." in out

