# Python Assertions & Precondition Check

def divide(a, b):
    assert b != 0, "Denominator cannot be zero"  # Precondition check with error message
    return a / b


assert divide(10, 2) == 5.0  # Functional test verification

# Python Docstring Specification

def add(a, b):
    """
    Adds two integers and returns the result.

    :param a: the first integer
    :param b: the second integer
    :return: the sum of a and b
    """
    return a + b

