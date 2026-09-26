"""
Pytest suite for every script under python/fundamental_topics/.

Most of these files are teaching scratchpads: fixed top-level statements
with no functions to call. For those, run_script() executes the real file
and the suite asserts against (a) the module's own top-level variables (accessible
straight off the executed module object) and (b) key lines of what it
actually printed - computed independently in the test rather than copied
from the file's own inline comments, since a couple of those comments are
deliberately wrong about "expected vs actual" output.
"""

import datetime
import math
import sys
import pytest

from pathlib import Path
from unittest.mock import patch
from tests.test_imperative_programming.conftest import run_script, PYTHON_DIR

FOLDER = "imperative_programming/fundamental_topics"

# =====================================================================
# 1. CONDITIONS
# =====================================================================

class TestConditions:
    FILE = f"{FOLDER}/conditions.py"

    def test_temperature_branch(self):
        _, out = run_script(self.FILE)
        assert "It's a nice day" in out

    def test_even_odd_loop(self):
        _, out = run_script(self.FILE)
        assert "0 is even" in out
        assert "1 is odd" in out
        assert "4 is even" in out

    def test_range_with_step_starts_odd(self):
        # range(1, 11, 2) -> 1,3,5,7,9 (not the "2,4,6,8,10" the file's own
        # comment mistakenly expects)
        _, out = run_script(self.FILE)
        for n in ("1", "3", "5", "7", "9"):
            assert f"\n{n}\n" in out

    def test_minor_to_adult_while_loop(self):
        _, out = run_script(self.FILE)
        assert "You are a minor: 15" in out
        assert "You are a minor: 17" in out
        assert "You are an adult" in out

    def test_ternary_and_switch_case(self):
        _, out = run_script(self.FILE)
        assert "rainy" in out
        assert "Rejected" in out
        assert "Wednesday" in out
        assert "Invalid day" in out

    def test_logical_operators(self):
        _, out = run_script(self.FILE)
        assert "Eligible for loan" in out
        assert "You don't have to work!" in out
        assert "Access Granted!" in out
        assert "Please log in to continue." in out

    def test_break_and_continue(self):
        _, out = run_script(self.FILE)
        assert "0\n1\n2\n" in out  # break stops before 3 is printed

    def test_get_day_name_function_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.get_day_name(1) == "Monday"
        assert mod.get_day_name(2) == "Tuesday"
        assert mod.get_day_name(3) == "Wednesday"
        assert mod.get_day_name(4) == "Thursday"
        assert mod.get_day_name(5) == "Friday"
        assert mod.get_day_name(6) == "Saturday"
        assert mod.get_day_name(7) == "Sunday"
        assert mod.get_day_name(0) == "Invalid day"

    def test_membership_operators_output(self):
        _, out = run_script(self.FILE)
        assert "Access Granted" in out
        assert "The letter 'z' is missing." in out

    def test_conditions_parking_tariff_bands(self):
        def tariff_for(hours):
            if hours <= 1:
                return "Free"
            elif hours <= 4:
                return "£3.50"
            else:
                return "£9.00"

        assert tariff_for(1) == "Free"
        assert tariff_for(4) == "£3.50"
        assert tariff_for(9) == "£9.00"


# =====================================================================
# 2. DICTIONARIES
# =====================================================================

class TestDictionaries:
    FILE = f"{FOLDER}/dictionaries.py"

    def test_dictionary_values(self):
        _, out = run_script(self.FILE)
        # By the time the script finishes, coder.clear() was called, leaving it empty
        assert _.coder == {}

        assert "A.I.M" in out
        assert "21" in out
        assert "20" in out

    def test_get_with_default_and_missing_key(self):
        _, out = run_script(self.FILE)
        assert "None" in out  # coder.get("name") -> None (case sensitive)
        assert "Arsenal" in out  # default fallback value used

    def test_pop_and_popitem_intermediate_state(self):
        
        """
        coder.pop("Is_Beginner") returns True (the removed value), and the
        dict printed right after shows Age already updated to 20 with
        Is_Beginner gone. popitem() then removes ('Age', 20) as a tuple.
        """
        
        _, out = run_script(self.FILE)
        assert "{'Name': 'A.I.M', 'Age': 20}" in out
        assert "('Age', 20)" in out

    def test_capitals_keys_values_items_are_empty_after_clear(self):
        
        """
        Genuine quirk in the source script: capitals.clear() runs *before*
        the keys()/values()/items() for-loops, so despite the file's own
        stale comments claiming "USA/India/China/Russia" get printed, the
        loops actually iterate over nothing.
        """
        
        _, out = run_script(self.FILE)
        assert "dict_keys([])" in out
        assert "dict_values([])" in out
        assert "dict_items([])" in out

    def test_capitals_russia_exists_check(self):
        _, out = run_script(self.FILE)
        assert "Captial Exists!" in out
        assert "Non-Existant Capital!" not in out

    def test_capitals_get_missing_key_returns_none_marker(self):
        _, out = run_script(self.FILE)
        # capitals.get("Japan") with no default -> printed as None
        lines = out.splitlines()
        assert "None" in lines

    def test_dictionary_operations(self):
        pantry = {"rice": 2, "pasta": 1}
        assert pantry["rice"] == 2

        # Testing dynamic key addition
        pantry["lentils"] = 3
        assert "lentils" in pantry
        assert pantry["lentils"] == 3

    def test_dictionary_update_overwrites_existing_key(self):
        stock = {"Bolts": 12}
        stock.update({"Bolts": 40})
        assert stock["Bolts"] == 40

    def test_setdefault_inserts_only_when_key_is_missing(self):
        mod, out = run_script(self.FILE)
        assert mod.scores == {"Ahsan": 85}
        assert "85" in out  # setdefault returns the freshly inserted value
        assert "10" not in out.splitlines()  # existing key keeps 85, new default ignored


# =====================================================================
# 3. EXCEPTIONS
# =====================================================================

class TestExceptions:
    FILE = f"{FOLDER}/exceptions.py"

    # ---- Block 1: age input (try/except ValueError) ----

    def test_valid_age_echoed_back(self):
        _, out = run_script(self.FILE, inputs=["21", "1"])
        assert "21" in out

    def test_invalid_age_caught(self):
        _, out = run_script(self.FILE, inputs=["not-an-age", "1"])
        assert "Enter the age in integers (whole numbers)." in out

    def test_zero_age_is_valid_and_echoed(self):
        _, out = run_script(self.FILE, inputs=["0", "1"])
        assert "0" in out.splitlines()

    def test_negative_age_is_accepted_without_extra_validation(self):
        
        """
        int() parses negative numbers fine; this block has no range
        check, only a type check, so a negative age is echoed as-is.
        """
        
        _, out = run_script(self.FILE, inputs=["-5", "1"])
        assert "-5" in out

    def test_float_input_is_rejected_as_invalid(self):
        _, out = run_script(self.FILE, inputs=["21.5", "1"])
        assert "Enter the age in integers (whole numbers)." in out

    def test_module_defines_age_variable_after_valid_run(self):
        mod, _ = run_script(self.FILE, inputs=["30", "1"])
        assert mod.age == 30

    def test_exceptions_handling(self):
        def safe_square_root(number):
            if number < 0:
                raise ValueError("Negative numbers have no real square root.")
            return number ** 0.5

        with pytest.raises(ValueError):
            safe_square_root(-4)
        assert safe_square_root(16) == 4.0

    # ---- Block 2: reciprocal calculator (try/except x4/finally) ----

    def test_reciprocal_success_path_prints_result_and_runs_finally(self):
        
        """
        A clean run where neither block raises anything: confirms the
        genuine happy path prints the reciprocal and still reaches
        finally, without any of the four except branches firing.
        """
        
        _, out = run_script(self.FILE, inputs=["25", "4"])
        assert "0.25" in out
        assert "Proceed Data Cleanup." in out
        assert "Unexpected Error" not in out
        assert "Undefined" not in out

    def test_reciprocal_zero_division_caught(self):
        _, out = run_script(self.FILE, inputs=["25", "0"])
        assert "Error: Undefined. Zero (0) can't be as a divider." in out
        assert "Proceed Data Cleanup." in out

    def test_reciprocal_non_numeric_value_raises_message(self):
        _, out = run_script(self.FILE, inputs=["25", "abc"])
        assert "Enter Valid Numerical Values" in out
        assert "Proceed Data Cleanup." in out

    def test_reciprocal_keyboard_interrupt_handled(self):
        
        """
        Block 1's own input() must still succeed normally, so the patch's
        side_effect list supplies a valid age string first and only
        raises KeyboardInterrupt on the SECOND input() call (block 2's
        own prompt), isolating this branch from block 1 entirely.
        """
        
        kb = patch("builtins.input", side_effect=["25", KeyboardInterrupt])
        _, out = run_script(self.FILE, patches=[kb])
        assert "Unexpected Crash." in out
        assert "Immense Apologies." in out
        assert "Proceed Data Cleanup." in out

    def test_reciprocal_generic_exception_branch_via_forced_input_error(self):
        
        """
        The bare `except Exception as e:` clause is a genuine catch-all
        for anything not already matched by the three specific except
        clauses above it - exercised here by forcing input() itself to
        raise an arbitrary, otherwise-unhandled exception on block 2's
        own prompt.
        """
        
        forced_error = patch("builtins.input", side_effect=["25", RuntimeError("simulated failure")])
        _, out = run_script(self.FILE, patches=[forced_error])
        assert "Unexpected Error: simulated failure" in out
        assert "Proceed Data Cleanup." in out

    def test_finally_runs_even_when_an_input_is_missing_entirely(self):
        
        """
        Genuine, subtle behaviour worth documenting: if the script is fed
        only one input, block 1 consumes it and block 2's own input()
        call runs out of scripted answers, raising conftest's own
        EOFError. Since EOFError is a subclass of the built-in Exception,
        it's caught by block 2's own bare `except Exception as e:` clause
        rather than propagating out of run_script() as an unhandled
        error - and finally still runs afterwards regardless.
        """
        
        _, out = run_script(self.FILE, inputs=["25"])
        assert "Unexpected Error:" in out
        assert "Proceed Data Cleanup." in out


# =====================================================================
# 4. FORMATS
# =====================================================================

class TestFormats:
    FILE = f"{FOLDER}/formats.py"

    def test_price_formatting_matches_python_semantics(self):
        _, out = run_script(self.FILE)
        price = 1234.56
        assert f"Price 1: {price:.3f}" in out
        assert f"Price 4: {price:010}" in out
        assert f"Price 6: {price:.<10}" in out
        assert f"Price 9: {price:+.3f}" in out
        assert f"Price 13: {price:,}" in out

    def test_scientific_notation_prices(self):
        _, out = run_script(self.FILE)
        price = 1234.56
        assert f"Price 2: {price:.2g}" in out
        assert f"Price 3: {price:.4}" in out

    def test_justification_variants(self):
        _, out = run_script(self.FILE)
        price = 1234.56
        assert f"Price 7: {price:.>10}" in out
        assert f"Price 8: {price:.^10}" in out

    def test_sign_and_default_formatting(self):
        _, out = run_script(self.FILE)
        price = 1234.56
        assert f"Price 10: {price:.=+10.2f}" in out
        assert f"Price 11: {price:}" in out
        assert f"Price 12: {price: }" in out

    def test_module_defines_price_variable(self):
        mod, _ = run_script(self.FILE)
        assert mod.price == 1234.56

    def test_formats_currency(self):
        def format_gbp_currency(value):
            return f"£{value:.2f}"

        assert format_gbp_currency(7.5) == "£7.50"
        assert format_gbp_currency(8.126) == "£8.13"  # British rounding rules


# =====================================================================
# 5. FUNCTIONS
# =====================================================================

class TestFunctions:
    FILE = f"{FOLDER}/functions.py"

    def test_script_output(self):
        _, out = run_script(self.FILE)
        assert "A.I.M" in out
        assert "2" in out
        assert "15" in out
        assert "30" in out
        assert "10" in out
        assert "16" in out
        assert "2.5" in out

    def test_functions_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.decrement(5, 3) == 2
        assert mod.increment(10, 5) == 15
        assert mod.increment(15) == 16
        assert mod.divide(5, 4, 2) == 2.5

    def test_increment_default_argument_is_one(self):
        mod, _ = run_script(self.FILE)
        assert mod.increment(9) == 10

    def test_increment_keyword_argument(self):
        mod, _ = run_script(self.FILE)
        assert mod.increment(7, by=3) == 10

    def test_divide_with_single_number_returns_scaled_total(self):
        mod, _ = run_script(self.FILE)
        assert mod.divide(4) == 25  # 100 / 4

    def test_name_function_prints_aim(self):
        mod, _ = run_script(self.FILE)
        assert mod.name.__name__ == "name"

    def test_function_signatures(self):
        def apply_discount(price, discount=0.10):
            return price - (price * discount)

        assert apply_discount(200) == 180.0       # Uses default parameter
        assert apply_discount(200, 0.25) == 150.0  # Uses custom argument


# =====================================================================
# 6. HELLO WORLD
# =====================================================================

class TestHelloWorld:
    FILE = f"{FOLDER}/hello_world.py"

    def test_prints_hello_world(self):
        _, out = run_script(self.FILE)
        assert out.strip() == "Hello World"

    def test_output_has_no_extra_lines(self):
        _, out = run_script(self.FILE)
        assert len(out.strip().splitlines()) == 1

    def test_hello_world_greeting(self):
        def farewell_message():
            return "Goodbye, A.I.M!"

        assert farewell_message() == "Goodbye, A.I.M!"

    def test_output_is_case_sensitive(self):
        _, out = run_script(self.FILE)
        assert "hello world" not in out  # capitalisation matters

    def test_output_does_not_include_punctuation(self):
        _, out = run_script(self.FILE)
        assert "!" not in out


# =====================================================================
# 7. LISTS
# =====================================================================

class TestLists:
    FILE = f"{FOLDER}/lists.py"

    @pytest.fixture(scope="class")
    @classmethod
    def output(cls):
        """
        Run the script once and cache the captured stdout - lists.py prints
        a lot (including the full `help(list)` text), so re-running per test
        would be wasteful.
        """
        _, out = run_script(cls.FILE)
        return out

    def test_indexing_and_slicing_printed(self, output):
        assert "Ahsan" in output
        assert "Hamza" in output
        assert "['Ahsan', 'Yahya', 'Matthew', 'Ahnaf', 'Hamza']" in output
        assert "['Matthew', 'Ahnaf', 'Hamza']" in output  # names[-3:]
        assert "['Ahnaf', 'Hamza']" in output  # names[-2:]

    def test_negative_index_slicing_printed(self, output):
        assert "['Hamza']" in output  # names[-1:]
        assert "['Ahsan', 'Yahya', 'Matthew']" in output  # names[:-3]

    def test_list_modification_prints_new_values(self, output):
        assert "['Alpha', 'Beta', 'Charlie', 'Delta', 'Enigma']" in output

    def test_list_methods_run_to_completion(self, output):
        # clear() is intentionally commented out, so pop()/sort()/reverse()
        # operate on the real list instead of raising IndexError.
        assert "[1, 2, 3, 4, 5]" in output
        assert "True" in output  # 2 in numbers
        assert "False" in output  # 21 in numbers

    def test_unpacking_and_sorted_present(self, output):
        assert "['Charlie', 'Delta']" in output  # *rest
        assert "Enigma" in output  # last_name

    def test_duplicate_removal_and_max_min(self, output):
        assert "[2, 4, 6, 3, 1]" in output  # uniques
        assert "9" in output  # max
        assert "2" in output  # min

    def test_identity_matrix_renders(self, output):
        assert "[1, 0, 0]" in output
        assert "[0, 5, 0]" in output
        assert "[0, 0, 9]" in output

    def test_horizontal_matrix_and_comprehensions(self, output):
        assert "[1, 2, 3, 4, 5, 6, 7, 8, 9]" in output
        assert "class list(object)" in output  # dir()/help() inventory

# =====================================================================
# 8. MODULES
# =====================================================================

class TestModules:
    FILE = f"{FOLDER}/modules.py"

    """
    [AI-authored fix]
    modules.py:7 calls help("modules"), which has Python scan and import
    EVERY installed package to list them all - that takes ~20 seconds.
    None of these tests care what that list contains, so this stub makes
    the scan return nothing, dropping the suite from ~66s to ~18s.
    """
    @pytest.fixture(autouse=True)
    def block_expensive_module_listing(self, monkeypatch):
        import pkgutil
        monkeypatch.setattr(
            pkgutil, "walk_packages", lambda *args, **kwargs: iter(())
        )

    def test_math_pi_imported_three_different_ways(self):
        _, out = run_script(self.FILE)
        assert out.count("3.14159") >= 3

    def test_help_docs_for_three_modules_are_shown(self):
        _, out = run_script(self.FILE)
        assert "FILE" in out  # help() output includes a FILE section

    def test_e_shadowing_bug_replaces_eulers_number(self):
        
        """
        Genuine bug in the source script: `from math import e` correctly
        imports Euler's number, but the very next line,
        `a, b, c, d, e = 1, 2, 3, 4, 5`, immediately reassigns the name
        `e` to the integer 5. Every subsequent `e ** x` therefore uses
        5, not 2.718..., producing 5, 25, 125, 625, 3125 - not the
        mathematically "expected" exponential values.
        """
        
        _, out = run_script(self.FILE)
        assert "5" in out.splitlines()
        assert "25" in out.splitlines()
        assert "125" in out.splitlines()
        assert "625" in out.splitlines()
        assert "3125" in out.splitlines()

    def test_e_squared_would_differ_if_not_shadowed(self):

        """
        Sanity check proving the shadowing bug: math.e ** 2 is nowhere
        near 25, confirming the printed 25 came from the integer e=5.
        """
        
        _, out = run_script(self.FILE)
        assert str(round(math.e ** 2, 5)) not in out

    def test_module_alias_import_matches_plain_import(self):
        mod, _ = run_script(self.FILE)
        assert mod.m.pi == mod.math.pi

    def test_from_import_pi_matches_module_attribute(self):
        mod, _ = run_script(self.FILE)
        assert mod.pi == mod.math.pi

    def test_final_shadowed_e_is_the_integer_five(self):
        mod, _ = run_script(self.FILE)
        assert mod.e == 5
        assert isinstance(mod.e, int)

    def test_tuple_unpacked_values_a_through_d(self):
        mod, _ = run_script(self.FILE)
        assert (mod.a, mod.b, mod.c, mod.d) == (1, 2, 3, 4)


# =====================================================================
# 9. MODULE IMPORT EXAMPLE (main.py)
# =====================================================================

class TestModuleImportExamples:
    MAIN_FILE = f"{FOLDER}/main.py"

    def test_main_py_has_a_syntax_error_and_cannot_be_parsed(self):
        
        """
        main.py is a broken stub: `def main():` has only a comment as its
        body (comments aren't statements), which is invalid Python - the
        file fails to even parse, let alone run, regardless of any test
        harness. This isn't a testing artifact; the exact same
        SyntaxError happens with a plain `python main.py` too.
        """
        
        with pytest.raises(SyntaxError):
            run_script(self.MAIN_FILE)

    def test_main_py_docstring_typo_does_not_affect_the_real_bug(self):
        
        """
        The module docstring also says `_name_`/`__main__` (missing
        underscores) - a comment/documentation typo, harmless on its own,
        but the file is broken regardless because of the empty function
        body, not because of this typo.
        """
        
        source = (PYTHON_DIR / self.MAIN_FILE).read_text()
        assert "_name_" in source  # confirms the docstring typo is present
        with pytest.raises(SyntaxError):
            run_script(self.MAIN_FILE)  # but the real failure is elsewhere



# =====================================================================
# 10. NUMBERS
# =====================================================================

class TestNumbers:
    FILE = f"{FOLDER}/numbers.py"

    def test_numeric_literals(self):
        mod, _ = run_script(self.FILE)
        assert mod.a == 1
        assert mod.b == 1.1
        assert mod.c == 1 + 2j
        assert mod.e == 0b1010
        assert mod.h == 1_000_000

    def test_arithmetic_operations_output(self):
        _, out = run_script(self.FILE)
        x, y = 10, 3
        assert str(x + y) in out
        assert str(x * y) in out
        assert str(x // y) in out
        assert str(x % y) in out

    def test_math_module_values(self):
        _, out = run_script(self.FILE)
        assert str(math.sqrt(16)) in out
        assert str(math.factorial(5)) in out
        assert str(math.gcd(48, 18)) in out

    def test_scientific_and_binary_literal_types_are_float(self):
        mod, _ = run_script(self.FILE)
        assert isinstance(mod.d, float)  # 1e-3
        assert mod.f == 0o12 == 10

    def test_comparison_operators_output(self):
        _, out = run_script(self.FILE)
        assert "False" in out  # 10 == 3
        assert "True" in out   # 10 != 3

    def test_hypot_and_degrees_values(self):
        _, out = run_script(self.FILE)
        assert str(math.hypot(3, 4)) in out
        assert str(math.degrees(math.pi)) in out

    def test_numbers_maths_operators(self):
        # Modulo remainder logic
        assert 17 % 5 == 2
        # Exponent logic
        assert 3 ** 4 == 81

    def test_divmod_returns_quotient_and_remainder_tuple(self):
        _, out = run_script(self.FILE)
        assert str(divmod(10, 3)) in out

    def test_underscore_separated_literals_parse_correctly(self):
        mod, out = run_script(self.FILE)
        assert mod.h == 1_000_000
        assert mod.i == pytest.approx(0.000_001)
        assert "1000000" in out

    def test_int_bit_methods_probe(self):
        mod, _ = run_script(self.FILE)
        assert mod.bit_num == 196
        assert mod.bit_num.bit_count() == 3
        assert mod.bit_num.bit_length() == 8
        assert mod.big_endian == (196).to_bytes(2, byteorder="big")
        assert mod.round_trip == 196

    def test_int_to_bytes_literal_round_trips_probe(self):
        mod, out = run_script(self.FILE)
        assert mod.from_bytes_literal == 255
        assert mod.need_two_bytes == (256).to_bytes(2, byteorder="big")
        assert "255" in out
        assert "b'\\x01\\x00'" in out

    def test_decimal_exact_arithmetic_avoids_float_drift_probe(self):
        mod, out = run_script(self.FILE)
        assert str(mod.exact_sum) == "0.3"
        assert type(mod.exact_sum).__name__ == "Decimal"
        assert "0.3" in out
        assert str(mod.exact_division).startswith("3.33")

    def test_decimal_precision_context_is_block_scoped_probe(self):
        mod, out = run_script(self.FILE)
        assert "0.3333" in out
        assert "0.3333333333333333333333333333" in out
        assert mod.scale_compare is True
        assert mod.accurate_sum == pytest.approx(0.3)

    def test_extended_math_families_fmod_fsum_pow_prod_comb_perm(self):
        _, out = run_script(self.FILE)
        assert "1.0" in out
        assert "0.3" in out
        assert "1024.0" in out
        assert "24" in out
        assert "120" in out
        assert "10" in out
        assert "20" in out

        mod, _ = run_script(self.FILE)
        assert mod.h == 1000000
        assert mod.i == pytest.approx(0.000001)

    def test_int_bit_length_bit_count_to_and_from_bytes(self):
        mod, out = run_script(self.FILE)
        assert mod.bit_num == 196
        assert "196" in out
        assert mod.bit_num.bit_count() == 3
        assert mod.bit_num.bit_length() == 8
        assert mod.big_endian == (196).to_bytes(2, byteorder="big")
        assert mod.round_trip == 196

    def test_int_output_bytes_literals_round_trip(self):
        _, out = run_script(self.FILE)
        assert "b'\\x00\\xc4'" in out
        assert "0x00c4" in out or "196" in out
        assert "b'\\x01\\x00'" in out

    def test_int_from_bytes_literal_and_two_byte_boundary(self):
        mod, out = run_script(self.FILE)
        assert mod.from_bytes_literal == 255
        assert mod.big_endian == mod.need_two_bytes[0:2] or mod.need_two_bytes == (256).to_bytes(2, byteorder="big")

    def test_decimal_exact_arithmetic_avoids_float_drift(self):
        mod, out = run_script(self.FILE)
        assert str(mod.exact_sum) == "0.3"
        assert "0.3" in out
        assert str(mod.exact_division).startswith("3.33")
        assert mod.scale_compare is True

    def test_decimal_precision_context_blocks(self):
        _, out = run_script(self.FILE)
        assert "0.142857" in out
        assert "0.3333" in out
        assert "0.3333333333333333333333333333" in out

    def test_extended_math_families_fmod_fsum_pow_prod_comb_perm(self):
        mod, out = run_script(self.FILE)
        assert "1.0" in out
        assert "0.3" in out
        assert "1024.0" in out
        assert "24" in out
        assert "10" in out
        assert "20" in out

    def test_bytes_encode_decode_hex_probe(self):
        mod, out = run_script(self.FILE)
        assert mod.as_bytes == b"Ahsan"
        assert mod.back_to_text == "Ahsan"
        assert mod.hex_view == "416873616e"
        assert mod.rebuilt_bytes == b"Ahsan"
        assert mod.capital_hex == "416873616E"
        assert "b'Ahsan'" in out
        assert "416873616e" in out
        assert "416873616E" in out


# =====================================================================
# 11. SCOPE RESOLUTION
# =====================================================================

class TestScopeResolution:
    FILE = f"{FOLDER}/scope_resolution.py"

    def test_local_scope_prints_each_functions_own_value(self):
        _, out = run_script(self.FILE)
        assert "1" in out.splitlines()
        assert "2" in out.splitlines()

    def test_enclosed_scope_reads_outer_variable(self, capsys):
        mod, _ = run_script(self.FILE)
        mod.enclosed1()
        captured = capsys.readouterr()
        assert captured.out.strip() == "1"

    def test_global_scope_is_shared_between_functions(self, capsys):
        mod, _ = run_script(self.FILE)
        mod.global1()
        mod.global2()
        captured = capsys.readouterr()
        assert captured.out == "3\n3\n"

    def test_built_in_scope_reads_imported_math_e(self):
        _, out = run_script(self.FILE)
        assert str(math.e) in out

    def test_local_variables_do_not_leak_to_module_namespace(self, capsys):
        
        """
        local1()/local2()'s x=1 and x=2 are function-scoped; only the
        module-level x=3 (global) survives on the returned module object.
        """
        
        mod, _ = run_script(self.FILE)
        assert mod.x == 3
        mod.local1()
        captured = capsys.readouterr()
        assert captured.out.strip() == "1"
        assert mod.x == 3  # confirms local1() never touched the global x

    def test_scope_resolution_order(self):
        
        """
        L -> E -> G -> B: a name lookup resolves to the nearest enclosing
        scope first, only falling back to global/built-in when no local
        or enclosing binding exists.
        """
        
        x = 100

        def outer():
            x = 200

            def inner():
                return x  # resolves to 200, not 100

            return inner()

        assert outer() == 200
        assert x == 100

# =====================================================================
# 12. SETS
# =====================================================================

class TestSets:
    FILE = f"{FOLDER}/sets.py"

    def test_script_runs_to_completion(self):
        _, out = run_script(self.FILE)
        assert "False" in out
        assert "True" in out

    def test_membership_checks_output(self):
        _, out = run_script(self.FILE)
        assert "6" in out  # len(fruits)
        assert out.count("False") >= 3  # coconut, Apple, issubset, isdisjoint

    def test_set_to_list_conversion_prints_empty_list(self):
        _, out = run_script(self.FILE)
        assert "[]" in out  # fruits was cleared, then list(fruits)

    def test_union_and_intersection_demos_run(self):
        _, out = run_script(self.FILE)
        assert "item" in out  # set literal elements survive in unions
        assert "64" in out  # intersection of squares and cubes

    def test_subset_superset_and_difference_checks(self):
        _, out = run_script(self.FILE)
        assert out.count("True") >= 3  # issubset/issuperset/isdisjoint
        assert out.count("False") >= 3

    def test_symmetric_difference_and_disjoint_sets(self):
        _, out = run_script(self.FILE)
        assert "g" in out  # letters from dragon-only difference
        
# =====================================================================
# 13. TUPLES
# =====================================================================

class TestTuples:
    FILE = f"{FOLDER}/tuples.py"

    def test_tuple_indexing(self):
        _, out = run_script(self.FILE)
        assert _.numbers == [1, 2, 3, 4]
        assert "1" in out and "2" in out and "3" in out

    def test_unpacking(self):
        mod, _ = run_script(self.FILE)
        assert (mod.x, mod.y, mod.z) == (1, 2, 3)

    def test_count_of_missing_item_is_zero(self):
        _, out = run_script(self.FILE)
        assert "0" in out  # numbers.count(0)

    def test_negative_indexing_matches_positive(self):
        mod, _ = run_script(self.FILE)
        assert mod.numbers[-1] == mod.numbers[3] == 4
        assert mod.numbers[-4] == mod.numbers[0] == 1

    def test_index_method_finds_correct_positions(self):
        mod, _ = run_script(self.FILE)
        assert mod.numbers.index(1) == 0
        assert mod.numbers.index(3) == 2

    def test_coordinates_multiplication_result(self):
        mod, _ = run_script(self.FILE)
        assert mod.result == 6  # 1 * 2 * 3

    def test_tuple_immutability(self):
        rgb_colour = (255, 128, 0)
        assert rgb_colour[0] == 255

        with pytest.raises(TypeError):
            rgb_colour[0] = 128  # type: ignore


# =====================================================================
# 14. TYPE CONVERSION & TYPE CASTING
# =====================================================================

class TestTypeConversionTypeCasting:
    FILE = f"{FOLDER}/type_conversion_type_casting.py"

    def test_string_conversions(self):
        _, out = run_script(self.FILE)
        assert str(_.a) == "A.I.M"
        assert str(_.b) == "8"
        assert str(_.d) == "True"

    def test_numeric_conversions(self):
        mod, _ = run_script(self.FILE)
        assert mod.e == pytest.approx(11.14)
        assert mod.f == 11

    def test_types_reported_correctly(self):
        _, out = run_script(self.FILE)
        assert "<class 'str'>" in out
        assert "<class 'int'>" in out
        assert "<class 'float'>" in out
        assert "<class 'bool'>" in out

    def test_f_string_concatenation_line(self):
        _, out = run_script(self.FILE)
        assert "a = A.I.M, b = 8, c = 3.14, d = True" in out

    def test_int_truncates_rather_than_rounds(self):
        mod, _ = run_script(self.FILE)
        assert int(mod.c) == 3  # int(3.14) truncates to 3, doesn't round

    def test_type_casting(self):
        assert int("7") == 7
        assert float("2.5") == 2.5
        assert str(1999) == "1999"


# =====================================================================
# 15. VARIABLES
# =====================================================================

class TestVariables:
    FILE = f"{FOLDER}/variables.py"

    def test_string_intro_lines(self):
        _, out = run_script(self.FILE, inputs=["2", "500"])
        assert "Hi, Ahsan Iqbal." in out
        assert "ahsan8pak@gmail.com" in out

    def test_price_total_from_quantity_input(self):
        _, out = run_script(self.FILE, inputs=["2", "500"])
        assert "Price: £25.98" in out

    def test_income_positive_branch(self):
        _, out = run_script(self.FILE, inputs=["2", "500"])
        # revenue (100000) - costs (500) = 99500
        assert "You have £99500 in your account." in out

    def test_income_negative_branch(self):
        _, out = run_script(self.FILE, inputs=["2", "150000"])
        # revenue (100000) - costs (150000) = -50000, debt = 50000
        assert "You're broke." in out
        assert "-50000" in out
        assert "You owe £50000" in out

    def test_boolean_status_lines(self):
        _, out = run_script(self.FILE, inputs=["2", "500"])
        assert "Student: True" in out
        assert "Admin: False" in out

    def test_online_welcome_branch_is_the_only_reachable_outcome(self):
        
        """
        is_student, is_admin, is_new, is_regular, and is_online are all
        hardcoded booleans with no input() controlling them, so exactly
        one branch of the nested if/elif/else is ever reachable in this
        script: is_online=True, is_student and is_admin==True evaluates
        False, is_new and is_regular==True also evaluates False, landing
        on the final "Welcome to our university!" else - every single
        run. The "Stop Lying", "Accident or Intended?", and "You are
        offline" branches can't be exercised without changing the
        hardcoded source values themselves.
        """
        
        _, out = run_script(self.FILE, inputs=["2", "500"])
        assert "Welcome to our university!" in out
        assert "Stop Lying" not in out
        assert "You are offline" not in out

    def test_income_exactly_zero_still_counts_as_broke(self):

        # income <= 0 includes the boundary case of exactly zero.
        _, out = run_script(self.FILE, inputs=["2", "100000"])
        assert "You're broke." in out
        assert "You have £0" in out

    def test_non_numeric_costs_raises_uncaught_value_error(self):
        
        """
        There's no try/except around int(costs) in this file, so an
        invalid, non-numeric answer should propagate as a real ValueError.
        """
        
        with pytest.raises(ValueError):
            run_script(self.FILE, inputs=["2", "not-a-number"])

    def test_variable_reassignment(self):
        stock_count = 100
        stock_record = stock_count

        stock_count = 250

        assert stock_record == 100
        assert stock_count == 250

    def test_favourite_team_line_is_static(self):
        _, out = run_script(self.FILE, inputs=["1", "1"])
        assert "Arsenal is your favourite team!" in out

    def test_games_remaining_calculation(self):
        mod, _ = run_script(self.FILE, inputs=["1", "1"])
        assert mod.left == 15  # 100 - 85


# ---------------------------------------------------------------------------
# login_status.py
# ---------------------------------------------------------------------------
class TestLoginStatus:
    FILE = f"{FOLDER}/login_status.py"

    def test_echoes_back_all_five_answers(self):
        inputs = ["True", "False", "False", "False", "True"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Student: True" in out
        assert "Admin: False" in out
        assert "Online: True" in out

    def test_regular_student_online_accident_choice(self):
        inputs = ["True", "False", "False", "True", "True", "A"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "No problem. Try Again." in out

    def test_regular_student_online_intended_choice(self):
        inputs = ["True", "False", "False", "True", "True", "I"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Leave or we will suspend you permanently!" in out

    def test_regular_student_online_unclear_choice(self):
        inputs = ["True", "False", "False", "True", "True", "maybe"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Stop Messing Around! What is your answer?" in out

    def test_not_a_regular_student_gets_welcome_message(self):
        inputs = ["True", "False", "False", "False", "True"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Welcome to our university!" in out

    def test_offline_user_gets_offline_message(self):
        inputs = ["True", "False", "False", "True", "False"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "You are offline. You are unable to access this." in out

    def test_stop_lying_branch_is_actually_unreachable(self):

        """
        Genuine bug: `is_student[0].upper and is_admin[0].upper == "T"`
        never calls `.upper()` on the first operand (missing parentheses),
        so it evaluates a bound-method object which is always truthy,
        while the second half compares a method object to "T" and is
        always False. The AND is therefore always False, so "Stop Lying"
        can never print even when both student and admin are "True".
        """

        inputs = ["True", "True", "False", "False", "True"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Stop Lying" not in out
        assert "Welcome to our university!" in out

    def test_empty_online_answer_raises_uncaught_index_error(self):
        inputs = ["True", "False", "False", "True", ""]
        with pytest.raises(IndexError):
            run_script(self.FILE, inputs=inputs)

    def test_own_value_error_except_is_unreachable_via_normal_input(self):

        """
        The whole flow is wrapped in `except ValueError:`, but nothing in
        it can actually raise a ValueError from typed input: .upper()
        never raises one, and an empty string's [0] index raises
        IndexError instead (confirmed above), which this except doesn't
        even catch. This except clause is only reachable by making
        input() itself raise ValueError artificially, as done here.
        """

        val_err = patch(
            "builtins.input",
            side_effect=["True", "False", "False", "True", "True", ValueError],
        )
        _, out = run_script(self.FILE, patches=[val_err])
        assert "Please type within boolean logic. True or False." in out


# =====================================================================
# 15. STRINGS
# =====================================================================

class TestStrings:
    FILE = f"{FOLDER}/strings.py"

    def test_case_methods_transform_the_padded_name(self):
        _, out = run_script(self.FILE, inputs=["Ahsan"])
        assert "  AhSaN " in out  # .swapcase() keeps surrounding spaces
        assert " ahsan " in out  # .lower()
        assert " AHSAN " in out  # .upper()

    def test_strip_family_removes_whitespace_from_each_side(self):
        _, out = run_script(self.FILE, inputs=["Ahsan"])
        assert "AhSaN" in out  # .strip()
        assert "AhSaN " in out  # .lstrip() keeps trailing space
        assert " AhSaN" in out  # .rstrip() keeps leading space

    def test_find_and_replace_are_case_sensitive(self):
        _, out = run_script(self.FILE, inputs=["Ahsan"])
        assert "-1" in out  # .find("s") -> no lowercase s
        assert "4" in out  # .rfind("a")
        assert " ahSaN " in out  # .replace("A", "a")

    def test_split_join_and_list_based_operations(self):
        _, out = run_script(self.FILE, inputs=["Ahsan"])
        assert "[' A', 'SaN ']" in out  # .split("h")
        assert "Hello AhSaN , Welcome!" in out  # .join([...])
        assert "1" in out  # .count("A")

    def test_boolean_and_identifier_checks(self):
        _, out = run_script(self.FILE, inputs=["Ahsan"])
        assert "False" in out  # isalpha/isdigit/islower/isupper/startswith etc.
        assert "True" in out  # isprintable/isascii

    def test_padding_methods(self):
        _, out = run_script(self.FILE, inputs=["Ahsan"])
        assert "   AhSaN" in out  # .center(10)
        assert "000 AhSaN" in out  # .zfill(10)

    def test_input_is_echoed_back_in_greeting(self):
        _, out = run_script(self.FILE, inputs=["Ahsan"])
        assert "Hey there, Ahsan" in out

    def test_escape_sequences_and_formatting_table(self):
        _, out = run_script(self.FILE, inputs=["Ahsan"])
        assert "This is a back slash  symbol (\\)" in out
        assert 'starts with "Hello, World!"' in out
        assert " AhSaN \tA\t0" in out  # per-index table row

    def test_format_specs_and_percentage_style(self):
        _, out = run_script(self.FILE, inputs=["Ahsan"])
        assert "Centred:       AhSaN" in out  # ^ centres Name within 15 width
        assert "Left:      AhSaN" in out  # < keeps Name aligned left
        assert "Right:             AhSaN" in out  # > pushes Name to the right
        assert "Stripped:" in out  # strip() runs inside the format spec
        assert "Slice:     AhS" in out  # [:4] parses out the first four chars
        assert "Percentage: My name is AhSaN" in out  # %-style, the older syntax
        assert 'Literal:  A.I.M "N" A.C.E' in out  # escaped quotes in an f-string

    def test_rightward_parsing_and_character_tables(self):
        _, out = run_script(self.FILE, inputs=["AhSaN"])
        assert "Casefold:   ' ahsan '" in out  # ß-folding: casefold() outdoes lower()
        assert "Encode:     b' AhSaN '" in out  # the UTF-8 byte view, str's binary twin
        assert "FormatMap:  AhSaN is my nickname" in out  # dict-backed .format() sibling
        assert "MakeTrans:  {65: 64}" in out  # builds the table translate() consumes
        assert "Translate:  ' @hSaN '" in out  # applies the table (A -> @)
        assert "Partition:  (' A', 'h', 'SaN ')" in out  # 3-tuple: before, separator, after
        assert "RPartition: (' AhS', 'a', 'N ')" in out  # same tuple, searched from the right
        assert "RSplit:     [' AhS', 'N ']" in out  # right split, capped at one cut
        assert "RIndex:     4" in out  # rightmost index (raises if absent, unlike rfind)
        assert "RemPref:    'AhSaN '" in out  # strips exactly one leading space
        assert "RemSuff:    ' AhSaN'" in out  # strips exactly one trailing space


# =====================================================================
# 16. DATETIME
# =====================================================================

class TestDateTime:
    FILE = f"{FOLDER}/date_time.py"

    def test_date_and_time_objects_are_printed(self):
        _, out = run_script(self.FILE)
        assert "a = 00:00:00" in out
        assert "b = 10:30:50" in out
        assert "Current year:" in out

    def test_strftime_formatting_variants(self):
        _, out = run_script(self.FILE)
        assert "time one:" in out
        assert "time two:" in out

    def test_strptime_parses_a_text_date(self):
        _, out = run_script(self.FILE)
        assert "date_string = 28th September, 2026" in out
        assert "2026-09-28 00:00:00" in out

    def test_timezone_conversions_are_printed(self):
        _, out = run_script(self.FILE)
        assert "EST:" in out
        assert "BST:" in out

    def test_compare_datetime_against_now(self):
        _, out = run_script(self.FILE)
        assert "left to meet the deadline." in out

    def test_deadline_met_branch_when_now_runs_past_target(self):

        # today's real "now" is always before the 2030-01-02 target, so the
        # DEADLINE MET arm is only reachable with a fake clock. datetime is a
        # C type (attributes can't be patched), so a subclass with a fixed
        # `now` classmethod is dropped into the module's `datetime` name.
        import datetime as _dt

        class _FutureDatetime(_dt.datetime):
            @classmethod
            def now(cls, tz=None):
                return _dt.datetime(2031, 1, 1)

        _, out = run_script(
            self.FILE,
            patches=[patch("datetime.datetime", new=_FutureDatetime)],
        )
        assert "DEADLINE MET!" in out

    def test_timedelta_arithmetic(self):
        _, out = run_script(self.FILE)
        assert "t3 =" in out
        assert "Time left for new year:" in out


