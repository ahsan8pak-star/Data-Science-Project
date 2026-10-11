"""
Dice rolls, lookup tables and ASCII faces.

Ports the ``DiceSystem`` cases of ``GameTestSuite`` and
``TestGameLogic``, with the face-art content pinned beyond the
non-empty check the Java suite asserts.
"""

import random

import pytest

from dice_system import DiceSystem


@pytest.fixture()
def dice():
    return DiceSystem(random.Random(42))


def test_roll_stays_in_range(dice):
    for _ in range(100):
        assert 1 <= dice.roll() <= 6


def test_roll_averages_mid_table():
    dice = DiceSystem(random.Random(7))
    total = sum(dice.roll() for _ in range(100))
    assert 200 < total < 500


def test_last_roll_tracks(dice):
    assert dice.get_last_roll() == 0
    roll = dice.roll()
    assert dice.get_last_roll() == roll


def test_hp_table():
    dice = DiceSystem()
    assert [dice.get_hp_from_roll(v) for v in (1, 2, 3, 4, 5, 6)] == [50, 50, 100, 100, 200, 200]


def test_door_bonus_table():
    dice = DiceSystem()
    assert dice.get_door_bonus_from_roll(1, 50) == 50
    assert dice.get_door_bonus_from_roll(2, 50) == 50
    assert dice.get_door_bonus_from_roll(3, 50) == 100
    assert dice.get_door_bonus_from_roll(4, 50) == 100
    assert dice.get_door_bonus_from_roll(5, 50) == 200
    assert dice.get_door_bonus_from_roll(6, 50) == 200


def test_face_arrays_hold_seven_lines_with_pips():
    dice = DiceSystem()
    for face in range(1, 7):
        lines = dice.get_dice_face_array(face)
        assert len(lines) == 7
        assert sum(line.count("\u25cf") for line in lines) == face
    blank = dice.get_dice_face_array(0)
    assert len(blank) == 7
    assert all("\u25cf" not in line for line in blank)


def test_current_face_follows_last_roll(dice):
    dice.roll()
    assert dice.get_current_dice_array() == dice.get_dice_face_array(dice.get_last_roll())


def test_face_ascii_is_non_empty_joined_lines(dice):
    for _ in range(6):
        dice.roll()
        ascii_art = dice.get_dice_face_ascii()
        assert ascii_art
        assert len(ascii_art.strip().split("\n")) == 7


def test_face_one_carries_a_single_centre_pip():
    lines = DiceSystem().get_dice_face_array(1)
    pip_rows = [i for i, line in enumerate(lines) if "\u25cf" in line]
    assert pip_rows == [3]
    middle = lines[3][2:]
    assert middle.index("\u25cf") == len(middle) - middle.index("\u25cf") - 2

