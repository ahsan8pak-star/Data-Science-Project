"""
Sibling-import example, importing favourite_food from food_script_example.py.

Should run ONLY standalone, and the comment at the top says so. Kept as the
pairing to food_script_example.py: the two together show the difference
between a module safe to import and one that assumes it owns the terminal.
"""

# This file should run ONLY standalone 

# [AI-authored fix] The bare `imperative_programming....` path only resolves
# when python/ happens to be on sys.path, which pytest arranges via
# pythonpath = ["python"] but a plain `python <file>` run does not. The
# try/except below is the fallback idiom already used by
# arithmetic_expressions.py and arithmetic_iteration.py: the package path
# first, the bare sibling second, so the file runs both ways.
try:
    from imperative_programming.syntax_exercises.food_script_example import favourite_food # from [FOLDER NAME]...[FILENAME] import [FUNCTION]

except ImportError:
    from food_script_example import favourite_food


def favourite_drink(drink):
    print(f"\nYour favourite drink is '{drink.upper()}'!")

# Ordering matters when outputting certain functions

favourite_food("rice") # 1st
favourite_drink("tea") # 2nd

print("\nThis is SCRIPT 2!")
print("\nPython is decent, but idk kinda mid")
print("\nImma sleep chat.")


