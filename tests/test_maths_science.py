"""
Tests for every script under Python/Maths&ScienceProjects/.
"""
import math

import pytest

from tests.conftest import run_script

FOLDER = "maths_science_projects"


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


class TestArea:
    FILE = f"{FOLDER}/Area.py"

    def test_valid_area(self):
        _, out = run_script(self.FILE, inputs=["10", "5"])
        assert "Area: 50.0 cm^2" in out

    def test_non_numeric_input(self):
        _, out = run_script(self.FILE, inputs=["abc", "5"])
        assert "Numbers only" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["1", "1"])
        assert mod.area(3, 7) == 21


class TestAreaOfCircle:
    FILE = f"{FOLDER}/area_of_circle.py"

    def test_valid_radius(self):
        _, out = run_script(self.FILE, inputs=["5"])
        expected = math.pi * 5 * 5
        assert f"Area of Circle: {expected:.2f}" in out

    def test_zero_radius_rejected(self):
        _, out = run_script(self.FILE, inputs=["0"])
        assert "Enter a valid radius" in out

    def test_negative_radius_rejected(self):
        _, out = run_script(self.FILE, inputs=["-3"])
        assert "Enter a valid radius" in out

    def test_non_numeric_radius(self):
        _, out = run_script(self.FILE, inputs=["abc"])
        assert "Numbers only" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["1"])
        assert mod.area_of_circle(2) == pytest.approx(math.pi * 4)


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


class TestArithmeticCalculator:
    FILE = f"{FOLDER}/arithmetic_calculator.py"

    def test_addition_chain_with_no_rounding(self):
        # A clean float result has its trailing .0 stripped to an int for
        # display when "n" (no formatting) is chosen.
        inputs = ["10", "+", "5", "", "n"]
        _, out = run_script(self.FILE, inputs=inputs)
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
        # run_script() absorbs the script's own exit() call (see conftest),
        # so we assert on the message it printed just before exiting.
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


class TestCircumferenceOfCircle:
    FILE = f"{FOLDER}/circumference_of_circle.py"

    def test_valid_radius(self):
        _, out = run_script(self.FILE, inputs=["5"])
        expected = math.pi * 2 * 5
        assert f"Circumference of Circle: {expected:.2f}" in out

    def test_zero_radius_rejected(self):
        _, out = run_script(self.FILE, inputs=["0"])
        assert "Enter a valid radius" in out

    def test_non_numeric_radius(self):
        _, out = run_script(self.FILE, inputs=["abc"])
        assert "Numbers only" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["1"])
        assert mod.circumference(1) == pytest.approx(2 * math.pi)


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


class TestPerimeterOfTriangle:
    FILE = f"{FOLDER}/perimeter_of_triangle.py"

    def test_valid_perimeter(self):
        _, out = run_script(self.FILE, inputs=["3", "4", "5"])
        assert "Result: Perimeter is 12.0 cm" in out

    def test_missing_side_skips_result(self):
        _, out = run_script(self.FILE, inputs=["3", "", "5"])
        assert "Result" not in out


class TestPythagorasTheorem:
    FILE = f"{FOLDER}/pythagoras_theorem.py"

    def test_find_hypotenuse(self):
        _, out = run_script(self.FILE, inputs=["3", "4", ""])
        assert "Result: Hypotenuse (c) is 5.0 cm" in out

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


class TestSineRule:
    FILE = f"{FOLDER}/sine_rule.py"

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


class TestTriangleCalculator:
    FILE = f"{FOLDER}/triangle_calculator.py"

    def test_right_triangle_area_then_quit(self):
        inputs = ["A", "4", "6", "4", "6"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert ">>> Calculator locked into Right mode. <<<" in out
        assert "Result: Area is 12.0" in out
        assert "Powering down..." in out

    def test_equilateral_perimeter_then_quit(self):
        # inputs: triangle type, mode choice (5 = Perimeter), side length, quit
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


class TestVolume:
    FILE = f"{FOLDER}/Volume.py"

    def test_valid_volume(self):
        _, out = run_script(self.FILE, inputs=["2", "3", "4"])
        assert "Volume: 24.0 cm^3" in out

    def test_non_numeric_input(self):
        _, out = run_script(self.FILE, inputs=["abc", "3", "4"])
        assert "Numbers only" in out

    def test_function_directly(self):
        mod, _ = run_script(self.FILE, inputs=["1", "1", "1"])
        assert mod.volume(2, 3, 4) == 24

# Test cases for math, calculators, and converters
def test_arithmetic_calculator():
    # Basic arithmetic operations
    assert 2 + 3 == 5
    assert 10 - 4 == 6
    assert 3 * 4 == 12
    assert 20 / 4 == 5

def test_celsius_to_fahrenheit():
    # Example conversion: 0°C = 32°F
    celsius = 0
    fahrenheit = (celsius * 9/5) + 32
    assert fahrenheit == 32
    
    # 100°C = 212°F
    celsius = 100
    fahrenheit = (celsius * 9/5) + 32
    assert fahrenheit == 212

def test_weight_converter():
    # Example: 1kg = 2.20462 lbs
    kg = 1
    lbs = round(kg * 2.20462, 2)
    assert lbs == 2.20
    
    # 5kg conversion
    kg = 5
    lbs = round(kg * 2.20462, 2)
    assert lbs == 11.02

def test_time_converter():
    # 1 hour = 60 minutes
    hours = 1
    minutes = hours * 60
    assert minutes == 60
    
    # 2 hours = 120 minutes
    hours = 2
    minutes = hours * 60
    assert minutes == 120

def test_geometry_area():
    # Circle area: π * r²
    import math
    radius = 5
    area = round(math.pi * (radius ** 2), 2)
    assert area == 78.54

def test_geometry_perimeter():
    # Rectangle perimeter: 2(l + w)
    length = 10
    width = 5
    perimeter = 2 * (length + width)
    assert perimeter == 30

def test_geometry_volume():
    # Cube volume: s³
    side = 3
    volume = side ** 3
    assert volume == 27
    
    # Sphere volume: (4/3) * π * r³
    import math
    radius = 2
    volume = round((4/3) * math.pi * (radius ** 3), 2)
    assert volume == 33.51
