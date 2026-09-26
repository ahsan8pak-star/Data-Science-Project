"""
Circle calculator, presenting area and circumference together.

Imports area_of_circle() from the sibling script and computes the
circumference itself, so the two results sit side by side for comparison. The
ValueError handler is not reachable through normal input, since the guarded
body performs no numeric conversion; a test reaches it artificially.
"""

from area_of_circle import area_of_circle
from circumference_of_circle import circumference


try:
    print("\n=====================")
    print("| CIRCLE CALCULATOR |")
    print("=====================")

    print("\nOption Menu: ")
    print("1. Area of Circle")
    print("2. Circumference of Circle")

    choice = input("\nEnter your option: ")

    if choice.isdigit() and int(choice) == 1:
        print("\n==================")
        print("| AREA OF CIRCLE |")
        print("==================")

        area_of_circle()

    elif choice.isdigit() and int(choice) == 2:
        print("\n===========================")
        print("| CIRCUMFERENCE OF CIRCLE |")
        print("===========================")

        circumference()

    else:
        print("Invalid Option. Try Again.")

except ValueError:
    print("Positive Numbers Only.")

except KeyboardInterrupt:
    print("\nWe apologise for any inconvenience.")
    print("We reccomend that you enter your answers quickly.")
    print("Thank you for reading. Run the program again.")


