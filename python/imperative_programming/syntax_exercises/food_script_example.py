"""
Sibling-import example - favourite_food() and favourite_drink() take a
parameter and return a sentence.

Should run standalone OR as an imported module, which is the import
arrangement drink_script_example.py depends on.
"""

# This file should run only standalone OR imported as a module

def favourite_food(food):
    print(f"\nYour favourite food is '{food.upper()}'!")

def show_food_script():
    print("\nYou are seeing SCRIPT 1!")

    favourite_food("chicken") # function being called
    
    print("\nBye Bye!")


if __name__ == "__main__":
    show_food_script()


