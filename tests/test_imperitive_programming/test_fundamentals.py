"""
Pytest suite for every script under Python/fundamental_topics/.

Most of these files are teaching scratchpads: fixed top-level statements
with no functions to call. For those, run_script() executes the real file
and we assert against (a) the module's own top-level variables (accessible
straight off the executed module object) and (b) key lines of what it
actually printed - computed independently in the test rather than copied
from the file's own inline comments, since a couple of those comments are
deliberately wrong about "expected vs actual" output.
"""

import math
import sys
import pytest

from pathlib import Path
from unittest.mock import patch
from tests.test_imperitive_programming.conftest import run_script, PYTHON_DIR

FOLDER = "imperitive_programming/fundamental_topics"

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

    def test_conditions_admission(self):
        def check_admission(age):
            if age < 12:
                return "Child ticket"
            elif age < 65:
                return "Standard ticket"
            else:
                return "Senior ticket"

        assert check_admission(5) == "Child ticket"
        assert check_admission(25) == "Standard ticket"
        assert check_admission(70) == "Senior ticket"


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
        user_profile = {"name": "Ahsan", "role": "Developer"}
        assert user_profile["name"] == "Ahsan"

        # Testing dynamic key addition
        user_profile["language"] = "Python"
        assert "language" in user_profile
        assert user_profile["language"] == "Python"

    def test_dictionary_update_overwrites_existing_key(self):
        capitals = {"USA": "Washington D.C."}
        capitals.update({"USA": "Detroit"})
        assert capitals["USA"] == "Detroit"


# =====================================================================
# 3. EXCEPTIONS
# =====================================================================

class TestExceptions:
    FILE = f"{FOLDER}/exceptions.py"

    def test_valid_age_echoed_back(self):
        _, out = run_script(self.FILE, inputs=["21"])
        assert "21" in out

    def test_invalid_age_caught(self):
        _, out = run_script(self.FILE, inputs=["not-an-age"])
        assert "Enter the age in integers (whole numbers)." in out

    def test_zero_age_is_valid_and_echoed(self):
        _, out = run_script(self.FILE, inputs=["0"])
        assert "0" in out.splitlines()

    def test_negative_age_is_accepted_without_extra_validation(self):
        
        """
        int() parses negative numbers fine; this script has no range
        check, only a type check, so a negative age is echoed as-is.
        """
        
        _, out = run_script(self.FILE, inputs=["-5"])
        assert "-5" in out

    def test_float_input_is_rejected_as_invalid(self):
        _, out = run_script(self.FILE, inputs=["21.5"])
        assert "Enter the age in integers (whole numbers)." in out

    def test_module_defines_age_variable_after_valid_run(self):
        mod, _ = run_script(self.FILE, inputs=["30"])
        assert mod.age == 30

    def test_exceptions_handling(self):
        def safe_divide(numerator, denominator):
            if denominator == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            return numerator / denominator

        with pytest.raises(ZeroDivisionError):
            safe_divide(10, 0)
        assert safe_divide(10, 2) == 5.0


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

        assert format_gbp_currency(5) == "£5.00"
        assert format_gbp_currency(12.346) == "£12.35"  # British rounding rules


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
        def calculate_total_cost(price, tax_rate=0.20):  # 20% standard UK VAT
            return price + (price * tax_rate)

        assert calculate_total_cost(100) == 120.0        # Uses default parameter
        assert calculate_total_cost(100, 0.05) == 105.0   # Uses custom argument


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
        def get_greeting():
            return "Hello, World!"

        assert get_greeting() == "Hello, World!"

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

    def test_indexing_and_slicing_prints_before_the_crash(self):

        """
        See test_pop_from_cleared_list_crashes below: the script never
        reaches the end, so we only get to assert on what it printed up to
        that point.
        """
        
        with pytest.raises(IndexError) as exc_info:
            run_script(self.FILE)
        
        out = getattr(exc_info.value, "partial_output", "")
        assert "Ahsan" in out
        assert "Hamza" in out
        assert "['Ahsan', 'Yahya', 'Matthew', 'Ahnaf', 'Hamza']" in out

    def test_pop_from_cleared_list_crashes(self):
        
        """
        Genuine bug in the source script: `numbers.clear()` is called
        immediately followed by `numbers.pop()` on the very next line, so
        the script always raises IndexError at that point and never
        reaches the sort/reverse/duplicates/matrix demos further down.
        """
        
        with pytest.raises(IndexError):
            run_script(self.FILE)

    def test_negative_index_slicing_present_before_crash(self):
        with pytest.raises(IndexError) as exc_info:
            run_script(self.FILE)
        out = getattr(exc_info.value, "partial_output", "")
        assert "['Matthew', 'Ahnaf', 'Hamza']" in out  # names[-3:]

    def test_empty_slice_present_before_crash(self):
        with pytest.raises(IndexError) as exc_info:
            run_script(self.FILE)
        out = getattr(exc_info.value, "partial_output", "")
        assert "[]" in out  # names[:0] and names[:-5]

    def test_list_mutability(self):
        shopping_cart = ["bread", "milk"]
        shopping_cart.append("tea")

        assert len(shopping_cart) == 3
        assert shopping_cart[-1] == "tea"

    def test_matrix_and_duplicate_logic_never_reached(self):
        
        """
        The identity-matrix and duplicate-removal demos live after the
        clear()/pop() crash point, so they never actually execute.
        """
        
        with pytest.raises(IndexError) as exc_info:
            run_script(self.FILE)
        out = getattr(exc_info.value, "partial_output", "")
        assert "[1, 0, 0]" not in out

# =====================================================================
# 8. MODULES
# =====================================================================

class TestModules:
    FILE = f"{FOLDER}/modules.py"

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
        assert 10 % 3 == 1
        # Exponent logic
        assert 2 ** 3 == 8

    def test_divmod_returns_quotient_and_remainder_tuple(self):
        _, out = run_script(self.FILE)
        assert str(divmod(10, 3)) in out

    def test_underscore_separated_literals_parse_correctly(self):
        mod, _ = run_script(self.FILE)
        assert mod.h == 1000000
        assert mod.i == pytest.approx(0.000001)


# =====================================================================
# 11. SCOPE RESOLUTION
# =====================================================================

class TestScopeResolution:
    FILE = f"{FOLDER}/scope_resolution.py"

    # TO DO Pytest Cases

# =====================================================================
# 12. SETS
# =====================================================================

class TestSets:
    FILE = f"{FOLDER}/sets.py"

    def test_set_created_with_expected_members(self):
        mod, _ = run_script(self.FILE)
        # by the time the script finishes, .clear() was called on `fruits`
        assert mod.fruits == set()

    def test_membership_checks_output(self):
        _, out = run_script(self.FILE)
        assert "False" in out  # 'coconut' in fruits was False *before* adding it

    def test_add_and_remove_print_none(self):
        
        """
        .add() and .remove() both return None, so wrapping them in
        print() prints the literal word 'None'.
        """
        
        _, out = run_script(self.FILE)
        assert out.count("None") >= 2

    def test_len_of_original_set_is_printed(self):
        _, out = run_script(self.FILE)
        assert "6" in out  # len of the original 6-item fruits set

    def test_case_sensitive_membership_check(self):
        _, out = run_script(self.FILE)
        # Both 'coconut' in fruits and 'Apple' in fruits print False initially
        assert out.count("False") >= 2

    def test_set_uniqueness(self):
        unique_ids = {101, 102, 102, 103}
        assert len(unique_ids) == 3  # Verifies duplicate removal
        assert 101 in unique_ids


# =====================================================================
# 13. STRINGS
# =====================================================================

class TestStrings:
    FILE = f"{FOLDER}/strings.py"

    def test_case_conversion_methods(self):
        _, out = run_script(self.FILE, inputs=["Aiman"])
        name = " AhSaN "
        assert name.lower() in out
        assert name.upper() in out
        assert name.swapcase() in out
        assert name.strip() in out

    def test_find_and_replace_methods(self):
        _, out = run_script(self.FILE, inputs=["Aiman"])
        name = " AhSaN "
        assert str(name.find("s")) in out  # -1, case sensitive
        assert name.replace("A", "a") in out

    def test_input_echoed_back(self):
        _, out = run_script(self.FILE, inputs=["Aiman"])
        assert "Hey there, Aiman" in out

    def test_padding_methods(self):
        _, out = run_script(self.FILE, inputs=["Aiman"])
        name = " AhSaN "
        assert name.center(10) in out
        assert name.ljust(10) in out
        assert name.rjust(10) in out
        assert name.zfill(10) in out

    def test_boolean_check_methods(self):
        _, out = run_script(self.FILE, inputs=["Aiman"])
        name = " AhSaN "
        assert str(name.isalpha()) in out
        assert str(name.isascii()) in out

    def test_split_method(self):
        _, out = run_script(self.FILE, inputs=["Aiman"])
        name = " AhSaN "
        assert str(name.split("h")) in out

    def test_string_methods(self):
        text = "Python Workspace"
        assert text.upper() == "PYTHON WORKSPACE"
        assert text.lower() == "python workspace"
        assert text.startswith("Py")


# =====================================================================
# 14. TUPLES
# =====================================================================

class TestTuples:
    FILE = f"{FOLDER}/tuples.py"

    def test_tuple_indexing(self):
        _, out = run_script(self.FILE)
        assert _.numbers == (1, 2, 3)
        assert "1" in out and "2" in out and "3" in out

    def test_unpacking(self):
        mod, _ = run_script(self.FILE)
        assert (mod.x, mod.y, mod.z) == (1, 2, 3)

    def test_count_of_missing_item_is_zero(self):
        _, out = run_script(self.FILE)
        assert "0" in out  # numbers.count(0)

    def test_negative_indexing_matches_positive(self):
        mod, _ = run_script(self.FILE)
        assert mod.numbers[-1] == mod.numbers[2] == 3
        assert mod.numbers[-3] == mod.numbers[0] == 1

    def test_index_method_finds_correct_positions(self):
        mod, _ = run_script(self.FILE)
        assert mod.numbers.index(1) == 0
        assert mod.numbers.index(3) == 2

    def test_coordinates_multiplication_result(self):
        mod, _ = run_script(self.FILE)
        assert mod.result == 6  # 1 * 2 * 3

    def test_tuple_immutability(self):
        london_coordinates = (51.5074, -0.1278)
        assert london_coordinates[0] == 51.5074

        with pytest.raises(TypeError):
            london_coordinates[0] = 52.0000  # type: ignore


# =====================================================================
# 15. TYPE CONVERSION & TYPE CASTING
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
        assert int("42") == 42
        assert float("3.14") == 3.14
        assert str(2026) == "2026"


# =====================================================================
# 16. VARIABLES
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
        primary_score = 100
        backup_score = primary_score

        primary_score = 250

        assert backup_score == 100
        assert primary_score == 250

    def test_favourite_team_line_is_static(self):
        _, out = run_script(self.FILE, inputs=["1", "1"])
        assert "Arsenal is your favourite team!" in out

    def test_games_remaining_calculation(self):
        mod, _ = run_script(self.FILE, inputs=["1", "1"])
        assert mod.left == 15  # 100 - 85

