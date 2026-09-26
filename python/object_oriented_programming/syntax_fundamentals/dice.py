"""
Dice - a die that rolls, and the ASCII art in a sibling module.

Imports its art from the imperative dice_game module, a deliberate
cross-paradigm import to show a reusable component moving between folders.
Part of the frozen OOP lane, so the sys.path setup and the import are left
exactly as they are.
"""

import os
import sys

# Tells Python to look 2 folders up in the 'Python' root directory
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
)

import random
from imperative_programming.interactive_games.dice_game import dice_art

# 1. Roll a random integer (whole number) from 1 to 6
roll = random.randint(1, 6)

# 2. Print the roll and join the tuple lines with newlines
print(f"You rolled a {roll}:\n")
print("\n".join(dice_art[roll]))


