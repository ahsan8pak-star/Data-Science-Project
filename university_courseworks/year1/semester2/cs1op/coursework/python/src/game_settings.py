"""
Global difficulty setting.

Translation of ``GameSettings.java``. Java's static class becomes module
state behind plain functions, which is the idiomatic Python shape for a
single global setting.
"""

from enum import Enum, auto


class Difficulty(Enum):
    """
    The three difficulty levels.
    """

    EASY = auto()
    NORMAL = auto()
    HARD = auto()


_difficulty = Difficulty.NORMAL


def get_difficulty():
    """
    The current difficulty.
    """
    return _difficulty


def set_difficulty(difficulty):
    """
    Set the current difficulty.
    """
    global _difficulty
    _difficulty = difficulty


def cycle_difficulty():
    """
    Advance EASY to NORMAL to HARD and wrap back to EASY.
    """
    global _difficulty
    _difficulty = {
        Difficulty.EASY: Difficulty.NORMAL,
        Difficulty.NORMAL: Difficulty.HARD,
        Difficulty.HARD: Difficulty.EASY,
    }[_difficulty]


def difficulty_label():
    """
    The display label of the current difficulty.
    """
    return _difficulty.name

