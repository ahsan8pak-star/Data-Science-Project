"""
Dice rolling with near-symmetrical ASCII faces.

Translation of ``DiceSystem.java``. Roll tables are preserved exactly:
1-2 maps to 50 HP (1x door bonus), 3-4 to 100 HP (2x), 5-6 to 200 HP (4x).
The ASCII faces below are the Java originals with trailing whitespace
stripped, which is invisible on screen but fails this repository's
no-trailing-whitespace guard.
"""

import random


class DiceSystem:
    """
    A six-sided die with game lookup tables and ASCII faces.
    """

    DICE_1 = [
        " ╔═════════════╗",
        " ║           ║",
        " ║           ║",
        " ║     ●     ║",
        " ║           ║",
        " ║           ║",
        " ╚═════════════╝",
    ]
    DICE_2 = [
        " ╔═════════════╗",
        " ║ ●         ║",
        " ║           ║",
        " ║           ║",
        " ║           ║",
        " ║        ●  ║",
        " ╚═════════════╝",
    ]
    DICE_3 = [
        " ╔═════════════╗",
        " ║  ●        ║",
        " ║           ║",
        " ║     ●     ║",
        " ║           ║",
        " ║        ●  ║",
        " ╚═════════════╝",
    ]
    DICE_4 = [
        " ╔═════════════╗",
        " ║ ●      ● ║",
        " ║           ║",
        " ║           ║",
        " ║           ║",
        " ║ ●      ● ║",
        " ╚═════════════╝",
    ]
    DICE_5 = [
        " ╔═════════════╗",
        " ║ ●      ● ║",
        " ║           ║",
        " ║     ●     ║",
        " ║           ║",
        " ║ ●      ● ║",
        " ╚═════════════╝",
    ]
    DICE_6 = [
        " ╔═════════════╗",
        " ║ ●      ● ║",
        " ║           ║",
        " ║ ●      ● ║",
        " ║           ║",
        " ║ ●      ● ║",
        " ╚═════════════╝",
    ]
    DICE_BLANK = [
        " ╔═════════════╗",
        " ║             ║",
        " ║             ║",
        " ║             ║",
        " ║             ║",
        " ║             ║",
        " ╚═════════════╝",
    ]

    def __init__(self, rng=None):
        self.last_roll = 0
        self.random = rng if rng is not None else random.Random()

    def roll(self):
        """
        Roll the die, returning a value from 1 to 6.
        """
        self.last_roll = self.random.randint(1, 6)
        return self.last_roll

    def get_last_roll(self):
        """
        The most recently rolled value, 0 before the first roll.
        """
        return self.last_roll

    def get_hp_from_roll(self, dice_value):
        """
        HP for a roll: 1-2 gives 50, 3-4 gives 100, 5-6 gives 200.
        """
        if dice_value <= 2:
            return 50
        if dice_value <= 4:
            return 100
        return 200

    def get_door_bonus_from_roll(self, dice_value, base_value):
        """
        Door bonus multiplier: 1x for 1-2, 2x for 3-4, 4x for 5-6.
        """
        if dice_value <= 2:
            return base_value
        if dice_value <= 4:
            return base_value * 2
        return base_value * 4

    def get_dice_face_array(self, face):
        """
        The ASCII face lines for a value, or the blank face otherwise.
        """
        return {
            1: self.DICE_1,
            2: self.DICE_2,
            3: self.DICE_3,
            4: self.DICE_4,
            5: self.DICE_5,
            6: self.DICE_6,
        }.get(face, self.DICE_BLANK)

    def get_current_dice_array(self):
        """
        The ASCII face lines for the most recent roll.
        """
        return self.get_dice_face_array(self.last_roll)

    def get_dice_face_ascii(self):
        """
        The current face as one newline-terminated string.
        """
        return "".join(line + "\n" for line in self.get_current_dice_array())

