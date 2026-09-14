"""
Pytest suite for every script under python/algorithmic_data_converters/.

Each script is executed for real via run_script() (see tests/conftest.py) with
scripted input, so these tests exercise the actual coursework code rather
than reimplementations of it. Covers fundamental/happy paths as well as
error-catching (invalid input, boundary, and exception) cases.
"""

import os
import pytest
import sys

from unittest.mock import patch
from tests.test_imperative_programming.conftest import run_script

FOLDER = "imperative_programming/algorithmic_data_converters"

# ---------------------------------------------------------------------------
# alarm_clock.py
# ---------------------------------------------------------------------------

class TestAlarmClock:

    """
    alarm_clock.py imports pygame at module level (SystemExit if missing),
    so pygame/pygame-ce must be installed to import this script at all. On
    a headless machine set SDL_AUDIODRIVER=dummy and SDL_VIDEODRIVER=dummy
    before running pytest so pygame.mixer.init() doesn't need a real device.
    The hardcoded sound_file path in set_alarm() never exists on a test
    machine, so every full-script run naturally lands on the
    "[X] FileNotFoundError: Audio file missing..." branch - the real
    playback branch is exercised separately below via mocks.
    """

    FILE = f"{FOLDER}/alarm_clock.py"

    @pytest.fixture(autouse=True)
    def _force_missing_sound_file(self):

        """
        CRITICAL: without this, any full-script test where the target
        time doesn't match the current second falls into set_alarm()'s
        REAL polling loop. run_script() already mocks time.sleep() to a
        no-op globally (for countdown-style scripts elsewhere), so on any
        machine where the hardcoded sound_file path genuinely exists
        (e.g. the original author's own machine), that "sleep" does
        nothing and the loop becomes a 100%-CPU busy-wait on the REAL
        system clock - it can spin for hours until the wall clock
        happens to hit the exact target second, making pytest appear to
        hang indefinitely. Forcing os.path.exists() to False here keeps
        every full-script-flow test deterministic and machine-independent.
        Tests that specifically exercise the playback branch patch
        os.path.exists themselves inside a narrower `with` block, which
        safely overrides this fixture for their own duration.

        The mock is scoped to the hardcoded sound_file path only (rather
        than returning False for every path): on Python 3.14+ pathlib's
        Path.exists() delegates to os.path.exists(), so an unconditional
        False would also break the test harness's own "Script not found"
        sanity check inside run_script().
        """

        real_exists = os.path.exists
        missing_sound_file = os.path.normcase(
            r"C:\Users\A.I.M\C.S\WAV\Ummati Qad Laha Fajrun.wav"
        )

        def _exists(path):
            if os.path.normcase(str(path)) == missing_sound_file:
                return False
            return real_exists(path)

        with patch("os.path.exists", side_effect=_exists):
            yield

    # --- valid_alarm_time(): 12-hour path ---

    def test_valid_12_hour_input(self):
        # Choice 1 (12-hr), Time input, Period input
        _, out = run_script(self.FILE, inputs=["1", "02:30:00", "PM"])
        assert "Mode        : 12-Hour Format (PM)" in out
        assert "Target Time : 02:30:00 PM (Internal: 14:30:00)" in out

    def test_valid_24_hour_input(self):
        # Choice 2 (24-hr), Time input
        _, out = run_script(self.FILE, inputs=["2", "14:30:00"])
        assert "Mode        : 24-Hour Format" in out
        assert "Target Time : 14:30:00" in out

    def test_invalid_mode_selection_retry(self):
        # Invalid selection '9', retried with valid choice '2', then valid time
        _, out = run_script(self.FILE, inputs=["9", "2", "14:30:00"])
        assert "[X] Invalid selection! Please enter choice '1' or '2'." in out
        assert "Target Time : 14:30:00" in out

    def test_blank_mode_selection_is_also_rejected(self):
        _, out = run_script(self.FILE, inputs=["", "2", "14:30:00"])
        assert "[X] Invalid selection! Please enter choice '1' or '2'." in out

    def test_invalid_12_hour_period_retry(self):

        """
        Genuine bug fixed here: the case "1" retry loop re-prompts BOTH
        time_input and period on failure (not just period alone), so the
        retry needs two fresh inputs, not one. The original single "AM"
        follow-up value was silently consumed as the retry's time_input,
        leaving period with no scripted answer and raising an EOFError
        from run_script() rather than exercising the retry path at all.
        """

        # Choice 1, Time '10:00:00', Invalid Period 'NOON', retried with time '10:00:00', period 'AM'
        _, out = run_script(self.FILE, inputs=["1", "10:00:00", "NOON", "10:00:00", "AM"])
        assert "[X] Error: Period must strictly be 'AM' or 'PM'." in out
        assert "Mode        : 12-Hour Format (AM)" in out

    def test_invalid_12_hour_time_format_retry(self):
        # Choice 1, Invalid Time '25:00:00', Period 'PM', retried with '05:00:00', Period 'PM'
        _, out = run_script(self.FILE, inputs=["1", "25:00:00", "PM", "05:00:00", "PM"])
        assert "[X] Error: Invalid 12-hour time format!" in out
        assert "(Hours: 01-12, Minutes: 00-59, Seconds: 00-59)" in out
        assert "Target Time : 05:00:00 PM (Internal: 17:00:00)" in out


    # --- valid_alarm_time(): 24-hour path ---

    def test_invalid_24_hour_time_format_retry(self):
        # Choice 2, Invalid Time '25:00:00', retried with valid time '14:30:00'
        _, out = run_script(self.FILE, inputs=["2", "25:00:00", "14:30:00"])
        assert "[X] Error: Invalid 24-hour time format!" in out
        assert "(Hours: 00-23, Minutes: 00-59, Seconds: 00-59)" in out
        assert "Target Time : 14:30:00" in out


    # --- top-level KeyboardInterrupt handling ---

    def test_keyboard_interrupt_handled_gracefully(self):
        # Simulates pressing Ctrl+C during initial input prompt
        kb = patch("builtins.input", side_effect=KeyboardInterrupt)
        _, out = run_script(self.FILE, patches=[kb])
        assert "[!] Alarm session cancelled by user." in out
        assert "Have a great day!" in out

    def test_keyboard_interrupt_prints_no_stack_trace(self):
        kb = patch("builtins.input", side_effect=KeyboardInterrupt)
        _, out = run_script(self.FILE, patches=[kb])
        assert "Traceback" not in out


    # --- missing pygame dependency ---

    def test_missing_pygame_prints_install_instructions_and_exits_cleanly(self):

        """
        Forces the module-level `import pygame` to fail regardless of
        whether pygame is actually installed in this environment, to
        confirm the fallback except-branch message and the immediate,
        clean SystemExit (already handled by run_script's own
        `except SystemExit: pass`).
        """

        import builtins
        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name == "pygame":
                raise ModuleNotFoundError("No module named 'pygame'")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=fake_import):
            _, out = run_script(self.FILE)

        assert out.strip() == (
            "Error: 'pygame' module is not installed. Please run 'pip install pygame-ce'."
        )


    # --- display_tui_banner() / display_info_box() directly ---

    def test_display_tui_banner_centres_title_across_40_chars(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["1", "02:30:00", "PM"])
        mod.display_tui_banner("TEST")
        captured = capsys.readouterr()
        lines = captured.out.strip("\n").splitlines()
        assert lines[0] == "=" * 40
        assert lines[1] == "TEST".center(40)
        assert lines[2] == "=" * 40

    def test_display_info_box_border_width_fits_longest_line(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["1", "02:30:00", "PM"])
        mod.display_info_box(["short", "a much longer line here"])
        captured = capsys.readouterr()
        longest = len("a much longer line here")
        expected_border = "-" * (longest + 4)
        assert captured.out.count(expected_border) == 2  # top and bottom
        assert f"| {'short'.ljust(longest)} |" in captured.out

    def test_total_width_constant_is_forty(self):
        mod, _ = run_script(self.FILE, inputs=["1", "02:30:00", "PM"])
        assert mod.TOTAL_WIDTH == 40


    # --- set_alarm() directly ---

    def test_set_alarm_missing_sound_file_returns_immediately(self, capsys):

        """
        os.path.exists() is checked before any pygame.mixer call, so this
        branch is safely testable without touching real audio at all.
        """

        mod, _ = run_script(self.FILE, inputs=["1", "02:30:00", "PM"])
        mod.set_alarm("14:30:00")
        captured = capsys.readouterr()
        assert "[X] FileNotFoundError: Audio file missing at path:" in captured.out
        assert r"Ummati Qad Laha Fajrun.wav" in captured.out

    def test_set_alarm_triggers_playback_when_clock_matches_target(self, capsys):

        """
        Mocks os.path.exists (file "found"), every pygame.mixer call (no
        real audio device needed), time.sleep (no real waiting), and
        datetime.datetime.now() (clock "matches" target immediately) -
        confirms the full TIMES UP! + playback + completion sequence
        without any real I/O.
        """

        mod, _ = run_script(self.FILE, inputs=["1", "02:30:00", "PM"])

        with patch("os.path.exists", return_value=True), \
             patch.object(mod.pygame.mixer, "init"), \
             patch.object(mod.pygame.mixer.music, "load"), \
             patch.object(mod.pygame.mixer.music, "play"), \
             patch.object(mod.pygame.mixer.music, "get_busy", return_value=False), \
             patch.object(mod.time, "sleep"), \
             patch.object(mod.datetime, "datetime") as mock_dt:

            mock_dt.now.return_value.strftime.return_value = "14:30:00"
            mod.set_alarm("14:30:00")

        captured = capsys.readouterr()
        assert "TIMES UP!" in captured.out
        assert "Alarm Time Reached: 14:30:00" in captured.out
        assert "Alarm session completed successfully." in captured.out

    def test_set_alarm_handles_pygame_mixer_init_failure(self, capsys):

        """
        Confirms the `except pygame.error` branch around mixer.init()/
        music.load() specifically, distinct from the FileNotFoundError
        and successful-playback paths above.
        """

        mod, _ = run_script(self.FILE, inputs=["1", "02:30:00", "PM"])

        with patch("os.path.exists", return_value=True), \
             patch.object(mod.pygame.mixer, "init", side_effect=mod.pygame.error("no audio device")):
            mod.set_alarm("14:30:00")

        captured = capsys.readouterr()
        assert "[X] Pygame Engine Error: Failed to initialise or load track" in captured.out


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

        # -40 is the famous point where Fahrenheit and Celsius meet.
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

        """
        Cases 5-9 (weeks/months/years/decades/centuries) weren't
        exercised by any other test.
        """
        
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

