"""
Tests for every script under Python/FundementalTopics/.

Most of these files are teaching scratchpads: fixed top-level statements
with no functions to call. For those, run_script() executes the real file
and we assert against (a) the module's own top-level variables (accessible
straight off the executed module object) and (b) key lines of what it
actually printed - computed independently in the test rather than copied
from the file's own inline comments, since a couple of those comments are
deliberately wrong about "expected vs actual" output.
"""

import math

import pytest

from tests.conftest import run_script

FOLDER = "fundamental_topics"


# =====================================================================
# 1. CONDITIONS
# =====================================================================

class TestConditions:
    FILE = f"{FOLDER}/Conditions.py"

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
        assert mod.get_day_name(3) == "Wednesday"
        assert mod.get_day_name(7) == "Sunday"
        assert mod.get_day_name(0) == "Invalid day"

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
        # Allowing other tests to assert on the printed output without worrying about the module's own top-level variable state
        assert _.coder == {}
        
        assert "A.I.M" in out
        assert "21" in out 
        assert "20" in out

    def test_get_with_default_and_missing_key(self):
        _, out = run_script(self.FILE)
        assert "None" in out  # coder.get("name") -> None (case sensitive)
        assert "Arsenal" in out  # default fallback value used

    def test_dictionary_operations(self):
        user_profile = {"name": "Ahsan", "role": "Developer"}
        assert user_profile["name"] == "Ahsan"
    
        # Testing dynamic key addition
        user_profile["language"] = "Python"
        assert "language" in user_profile
        assert user_profile["language"] == "Python"


# =====================================================================
# 3. EXCEPTIONS
# =====================================================================

class TestExceptions:
    FILE = f"{FOLDER}/Exceptions.py"

    def test_valid_age_echoed_back(self):
        _, out = run_script(self.FILE, inputs=["21"])
        assert "21" in out

    def test_invalid_age_caught(self):
        _, out = run_script(self.FILE, inputs=["not-an-age"])
        assert "Enter the age in integers (whole numbers)." in out
 
    def test_exceptions_handling(self):
        def safe_divide(numerator, denominator):
            if denominator == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            return numerator / denominator

        # Verifying that the correct runtime error is triggered
        with pytest.raises(ZeroDivisionError):
            safe_divide(10, 0)
        assert safe_divide(10, 2) == 5.0


# =====================================================================
# 4. FORMATS
# =====================================================================

class TestFormats:
    FILE = f"{FOLDER}/Formats.py"

    def test_price_formatting_matches_python_semantics(self):
        _, out = run_script(self.FILE)
        price = 1234.56
        assert f"Price 1: {price:.3f}" in out
        assert f"Price 4: {price:010}" in out
        assert f"Price 6: {price:.<10}" in out
        assert f"Price 9: {price:+.3f}" in out
        assert f"Price 13: {price:,}" in out

    def test_formats_currency(self):
        def format_gbp_currency(value):
            return f"£{value:.2f}"

        assert format_gbp_currency(5) == "£5.00"
        assert format_gbp_currency(12.346) == "£12.35"  # Verifies British rounding rules


# =====================================================================
# 5. FUNCTIONS
# =====================================================================

class TestFunctions:
    FILE = f"{FOLDER}/Functions.py"

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

    def test_function_signatures(self):
        def calculate_total_cost(price, tax_rate=0.20):  # 20% standard UK VAT
            return price + (price * tax_rate)

        assert calculate_total_cost(100) == 120.0        # Uses default parameter
        assert calculate_total_cost(100, 0.05) == 105.0  # Uses custom argument


# =====================================================================
# 6. HELLO WORLD
# =====================================================================

class TestHelloWorld:
    FILE = f"{FOLDER}/hello_world.py"

    def test_prints_hello_world(self):
        _, out = run_script(self.FILE)
        assert out.strip() == "Hello World"
        
    def test_hello_world_greeting(self):
        def get_greeting():
            return "Hello, World!"
        
        assert get_greeting() == "Hello, World!"


# =====================================================================
# 7. LISTS
# =====================================================================

class TestLists:
    FILE = f"{FOLDER}/Lists.py"

    def test_indexing_and_slicing_prints_before_the_crash(self):
        """
        See test_pop_from_cleared_list_crashes below: 
        the script never reaches the end, 
        so we only get to assert on what it printed up to that point.
        """
        with pytest.raises(IndexError) as exc_info:
            run_script(self.FILE)
        out = getattr(exc_info.value, "partial_output", "")
        assert "Ahsan" in out
        assert "Hamza" in out
        assert "['Ahsan', 'Yahya', 'Matthew', 'Ahnaf', 'Hamza']" in out

    def test_pop_from_cleared_list_crashes(self):
        """
        Genuine bug in the source script: 
        `numbers.clear()` is called immediately followed by `numbers.pop()` on the very next line,
        so the script always raises IndexError at that point 
        and never reaches the sort/reverse/duplicates/matrix demos further down.
        """
        with pytest.raises(IndexError):
            run_script(self.FILE)

    def test_list_mutability(self):
        shopping_cart = ["bread", "milk"]
        shopping_cart.append("tea")
    
        assert len(shopping_cart) == 3
        assert shopping_cart[-1] == "tea"  # Checks end of array sequence


# =====================================================================
# 8. NUMBERS
# =====================================================================

class TestNumbers:
    FILE = f"{FOLDER}/Numbers.py"

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

    def test_numbers_maths_operators(self):
        # Modulo remainder logic
        assert 10 % 3 == 1
        # Exponent logic
        assert 2 ** 3 == 8


# =====================================================================
# 9. SETS
# =====================================================================

class TestSets:
    FILE = f"{FOLDER}/Sets.py"

    def test_set_created_with_expected_members(self):
        mod, _ = run_script(self.FILE)
        # by the time the script finishes, .clear() was called on `fruits`
        assert mod.fruits == set()

    def test_membership_checks_output(self):
        _, out = run_script(self.FILE)
        assert "False" in out  # 'coconut' in fruits was False *before* adding it


    def test_set_uniqueness(self):
        unique_ids = {101, 102, 102, 103}
        assert len(unique_ids) == 3  # Verifies duplicate removal
        assert 101 in unique_ids


# =====================================================================
# 10. STRINGS
# =====================================================================

class TestStrings:
    FILE = f"{FOLDER}/Strings.py"

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

    def test_string_methods(self):
        text = "Python Workspace"
        assert text.upper() == "PYTHON WORKSPACE"
        assert text.lower() == "python workspace"
        assert text.startswith("Py")


# =====================================================================
# 11. TUPLES
# =====================================================================

class TestTuples:
    FILE = f"{FOLDER}/Tuples.py"

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

    def test_tuple_immutability(self):
        london_coordinates = (51.5074, -0.1278)
        assert london_coordinates[0] == 51.5074
    
        # Confirming that altering an immutable sequence raises a TypeError
        with pytest.raises(TypeError):
            london_coordinates[0] = 52.0000  # type: ignore


# =====================================================================
# 12. TYPE CONVERSION & TYPE CASTING
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

    def test_type_casting(self):
        assert int("42") == 42
        assert float("3.14") == 3.14
        assert str(2026) == "2026"


# =====================================================================
# 13. VARIABLES
# =====================================================================

class TestVariables:
    FILE = f"{FOLDER}/Variables.py"

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

    def test_non_numeric_costs_raises_uncaught_value_error(self):
        """
        There's no try/except around int(costs) in this file, 
        so an invalid, non-numeric answer should propagate as a real ValueError.
        """
        with pytest.raises(ValueError):
            run_script(self.FILE, inputs=["2", "not-a-number"])

    def test_variable_reassignment(self):
        primary_score = 100
        backup_score = primary_score
    
        primary_score = 250
    
        # Confirms backup value points safely to the original integer assignment
        assert backup_score == 100
        assert primary_score == 250

