import pytest

# =====================================================================
# 1. CONDITIONS
# =====================================================================
def test_conditions_admission():
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
def test_dictionary_operations():
    user_profile = {"name": "Ahsan", "role": "Developer"}
    assert user_profile["name"] == "Ahsan"
    
    # Testing dynamic key addition
    user_profile["language"] = "Python"
    assert "language" in user_profile
    assert user_profile["language"] == "Python"


# =====================================================================
# 3. EXCEPTIONS
# =====================================================================
def test_exceptions_handling():
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
def test_formats_currency():
    def format_gbp_currency(value):
        return f"£{value:.2f}"

    assert format_gbp_currency(5) == "£5.00"
    assert format_gbp_currency(12.346) == "£12.35"  # Verifies British rounding rules


# =====================================================================
# 5. FUNCTIONS
# =====================================================================
def test_function_signatures():
    def calculate_total_cost(price, tax_rate=0.20):  # 20% standard UK VAT
        return price + (price * tax_rate)

    assert calculate_total_cost(100) == 120.0        # Uses default parameter
    assert calculate_total_cost(100, 0.05) == 105.0  # Uses custom argument


# =====================================================================
# 6. HELLO WORLD
# =====================================================================
def test_hello_world_greeting():
    def get_greeting():
        return "Hello, World!"
        
    assert get_greeting() == "Hello, World!"


# =====================================================================
# 7. LISTS
# =====================================================================
def test_list_mutability():
    shopping_cart = ["bread", "milk"]
    shopping_cart.append("tea")
    
    assert len(shopping_cart) == 3
    assert shopping_cart[-1] == "tea"  # Checks end of array sequence


# =====================================================================
# 8. NUMBERS
# =====================================================================
def test_numbers_maths_operators():
    # Modulo remainder logic
    assert 10 % 3 == 1
    # Exponent logic
    assert 2 ** 3 == 8


# =====================================================================
# 9. SETS
# =====================================================================
def test_set_uniqueness():
    unique_ids = {101, 102, 102, 103}
    assert len(unique_ids) == 3  # Verifies duplicate removal
    assert 101 in unique_ids


# =====================================================================
# 10. STRINGS
# =====================================================================
def test_string_methods():
    text = "Python Workspace"
    assert text.upper() == "PYTHON WORKSPACE"
    assert text.lower() == "python workspace"
    assert text.startswith("Py")


# =====================================================================
# 11. TUPLES
# =====================================================================
def test_tuple_immutability():
    london_coordinates = (51.5074, -0.1278)
    assert london_coordinates[0] == 51.5074
    
    # Confirming that altering an immutable sequence raises a TypeError
    with pytest.raises(TypeError):
        london_coordinates[0] = 52.0000


# =====================================================================
# 12. TYPE CONVERSION & TYPE CASTING
# =====================================================================
def test_type_casting():
    assert int("42") == 42
    assert float("3.14") == 3.14
    assert str(2026) == "2026"


# =====================================================================
# 13. VARIABLES
# =====================================================================
def test_variable_reassignment():
    primary_score = 100
    backup_score = primary_score
    
    primary_score = 250
    
    # Confirms backup value points safely to the original integer assignment
    assert backup_score == 100
    assert primary_score == 250