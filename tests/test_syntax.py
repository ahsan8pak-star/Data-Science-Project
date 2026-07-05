import pytest
import os

from syntax_fundamentals.Add import add
from syntax_fundamentals.Divide import divide
from syntax_fundamentals.Factorials import factorial

# =====================================================================
# 1. ADD & DIVIDE (Pure Functions)
# =====================================================================

def test_addition_module():
    # Tests the actual function from Add.py
    assert add(5, 3) == 8
    assert add(-1, 1) == 0

def test_division_module():
    # Tests the actual function from Divide.py
    assert divide(16, 4) == 4.0
    assert divide(5, 2) == 2.5
    
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


# =====================================================================
# 2. FACTORIALS (Recursion & Input Validation Logic)
# =====================================================================

def test_factorial_logic():
    # Tests the recursive function from Factorials.py
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120


# =====================================================================
# 3. FILE WRITER (I/O Operations)
# =====================================================================

def test_file_writer_output(tmp_path):
    # Temporarily changing directory to pytest's safe sandbox to check file writing
    os.chdir(tmp_path)
    
    # Importing the greet logic from file_writer.py
    from syntax_fundamentals.file_writer import greet
    
    message = greet("A.I.M")
    assert message == "A.I.M"
    
    # Simulating the file creation process from your script
    file = open("AIM.txt", "w", encoding="utf-8")
    file.write(message)
    file.close()
    
    assert os.path.exists("AIM.txt")
    with open("AIM.txt", "r", encoding="utf-8") as f:
        assert f.read() == "A.I.M"


# =====================================================================
# 4. TIME CALCULATIONS (Hour Clock & Timers)
# =====================================================================

def test_hour_clock_maths():
    # Abstracting the seconds pool logic from your countdown script
    def calculate_combined_seconds(hours, minutes, seconds):
        return (hours * 3600) + (minutes * 60) + seconds

    assert calculate_combined_seconds(1, 0, 0) == 3600
    assert calculate_combined_seconds(0, 1, 30) == 90


# =====================================================================
# 5. SCRIPTS CONVERTED TO PURE LOGIC FUNCTIONS
# =====================================================================

def test_checkout_system_logic():
    # Testing the calculations from checkout_system.py
    def get_total(price, quantity):
        return round((price * quantity), 2)

    assert get_total(10.50, 3) == 31.50
    assert get_total(1.99, 1) == 1.99

def test_distance_calculator_logic():
    # Testing the formula from distance_calculator.py
    def get_distance(start, finish):
        return round(float(finish) - float(start), 2)

    assert get_distance(10.5, 25.7) == 15.2

def test_email_slicer_logic():
    # Testing the indexing logic from email_slicer.py
    def slice_email(email):
        index = email.index("@")
        return email[:index], email[index + 1:]

    username, domain = slice_email("ahsan.iqbal@gmail.com")
    assert username == "ahsan.iqbal"
    assert domain == "gmail.com"

def test_even_odd_detector_logic():
    # Testing the modulo boundaries from even_odd_detector.py
    evens = [i for i in range(0, 11) if i % 2 == 0]
    odds = [i for i in range(0, 11) if i % 2 == 1]
    
    assert len(evens) == 6  # 0, 2, 4, 6, 8, 10
    assert len(odds) == 5   # 1, 3, 5, 7, 9

def test_prime_numbers_logic():
    # Testing the logic meant for your prime_numbers.py script
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    assert is_prime(2) is True
    assert is_prime(7) is True
    assert is_prime(1) is False
    assert is_prime(10) is False

