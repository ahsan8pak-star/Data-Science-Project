# Exceptions are mainly used for Error Catching
# That means it'll allow the error message to be outputted without crashing the program

try: # Used for the actual executable code to be run underneath
    age = int(input("Enter your age: "))
    print(age)

except ValueError: # Very common example
    print("Enter the age in integers (whole numbers).")

""" Another Example """

# Exception = An event that interrupts the flow of a program
# (e.g. ZeroDivisionError, TypeError, ValueError)
# Main methods for exception handling / error catching:
# 1.try, 2.except, 3.finally

try:
    number = int(input("Enter an integer for the reciprocal as a decimal: "))
    print(1 / number)

except ZeroDivisionError:
    print("Error: Undefined. Zero (0) can't be as a divider.")

except ValueError:
    print("Enter Valid Numerical Values")

except KeyboardInterrupt:
    print("Unexpected Crash.\nImmense Apologies.")

except Exception as e:
    print(f"Unexpected Error: {e}")

finally:
    print("Proceed Data Cleanup.")

