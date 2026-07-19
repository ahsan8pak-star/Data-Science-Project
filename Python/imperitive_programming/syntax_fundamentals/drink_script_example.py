# This file should run ONLY standalone 

from food_script_example import favourite_food # from [FILE NAME] import [FUNCTION]


def favourite_drink(drink):
    print(f"\nYour favourite drink is '{drink.upper()}'!")

# Ordering matters when outputting certain functions

favourite_food("rice") # 1st
favourite_drink("tea") # 2nd

print("\nThis is SCRIPT 2!")
print("\nPython is decent, but idk kinda mid")
print("\nImma sleep chat.")

