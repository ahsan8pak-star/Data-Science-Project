import os
import sys

# Tells Python to look 2 folders up in the 'Python' root directory
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
)

import random
from imperitive_programming.logical_games.dice_game import dice_art

# 1. Roll a random integer (whole number) from 1 to 6
roll = random.randint(1, 6)

# 2. Print the roll and join the tuple lines with newlines
print(f"You rolled a {roll}:\n")
print("\n".join(dice_art[roll]))

