"""
Doors, the factory template rules and the fallback dice.

Ports the door cases of ``GameTest``, ``GameTestSuite`` and
``TestGameLogic``, including the shipped ``doors.txt`` format and the
``minigame``-type fallthrough the Java switch carries.
"""

import random
from pathlib import Path

import pytest

from door import Door
from door_factory import DoorFactory
from game import Game
from minigame_door import MinigameDoor
from nothing_door import NothingDoor
from penalty_door import PenaltyDoor
from player import Player
from reward_door import RewardDoor


RESOURCES = Path(__file__).resolve().parent.parent / "resources"


@pytest.fixture()
def player():
    Game.reset()
    return Player("TestPlayer")


def test_door_is_abstract():
    with pytest.raises(TypeError):
        Door("Door", "A door")


def test_reward_door_grants_exp(player):
    door = RewardDoor("Reward Door", "A shiny chest", 50)
    result = door.interact(player)
    assert result
    assert player.get_exp() == 50
    assert door.get_exp_value() == 50


def test_penalty_door_drains_exp(player):
    player.set_exp(100)
    door = PenaltyDoor("Penalty Door", "A poison bottle", 25)
    result = door.interact(player)
    assert result
    assert player.get_exp() == 75
    assert door.get_exp_value() == -25


def test_minigame_door_changes_nothing(player):
    door = MinigameDoor("Pong Door", "Table tennis court", "PONG")
    assert door.get_game_type() == "PONG"
    assert door.get_name() == "Pong Door"
    assert door.interact(player) == "You enter the spaceship!"
    assert player.get_exp() == 0
    assert player.get_lives() == 3


def test_nothing_door_changes_nothing(player):
    door = NothingDoor("Empty Door", "A door with nothing behind it.")
    assert door.interact(player) == "The door reveals nothing. Just empty space."
    assert player.get_exp() == 0


def test_door_name_and_description():
    door = RewardDoor("Test Door", "Test Description", 100)
    assert door.get_name() == "Test Door"
    assert door.get_description() == "Test Description"


def test_shipped_doors_txt_exists_with_content():
    doors_file = RESOURCES / "doors.txt"
    assert doors_file.exists()
    assert doors_file.stat().st_size > 0


def test_factory_reads_shipped_templates():
    factory = DoorFactory(RESOURCES, random.Random(3))
    assert factory.templates
    doors = {factory.create_random_door(i) for i in range(1, 60)}
    assert doors


def test_factory_template_types_map_to_doors(tmp_path):
    doors_file = tmp_path / "doors.txt"
    doors_file.write_text(
        "# comment\n\nReward | Chest | art | 60\n"
        "Penalty | Trap | art | 30\n"
        "Nothing | Void | art | 0\n"
        "Pong Minigame | Court | art | 0\n"
        "Space Invaders Minigame | Hatch | art | 0\n"
        "Unknown | Skip me | art | 0\n"
        "Broken line without separator\n",
        encoding="utf-8",
    )
    factory = DoorFactory(tmp_path, random.Random(1))
    assert len(factory.templates) == 5
    seen = {type(factory.create_random_door(i)).__name__ for i in range(1, 40)}
    assert seen <= {"RewardDoor", "PenaltyDoor", "NothingDoor", "MinigameDoor"}


def test_factory_template_values_parsed(tmp_path):
    doors_file = tmp_path / "doors.txt"
    doors_file.write_text("Reward | Chest | art | 60\nPenalty | Trap | art | 30\n", encoding="utf-8")
    factory = DoorFactory(tmp_path, random.Random(0))
    values = set()
    for i in range(1, 30):
        door = factory.create_random_door(i)
        if isinstance(door, RewardDoor):
            values.add(door.get_exp_value())
        if isinstance(door, PenaltyDoor):
            values.add(door.get_exp_value())
    assert 60 in values
    assert -30 in values


def test_factory_minigame_type_falls_through_to_fallback(tmp_path, monkeypatch):
    doors_file = tmp_path / "doors.txt"
    doors_file.write_text("Minigame | Mystery | art | 0\n", encoding="utf-8")
    factory = DoorFactory(tmp_path, random.Random(0))
    rolls = iter([7, 7, 7])
    monkeypatch.setattr(factory.rng, "randrange", lambda n: next(rolls) if n == 12 else 0)
    door = factory.create_random_door(1)
    assert isinstance(door, RewardDoor)


def test_factory_missing_file_uses_fallback(tmp_path):
    factory = DoorFactory(tmp_path / "absent", random.Random(11))
    assert factory.templates == []
    door = factory.create_random_door(1)
    assert isinstance(door, Door)


def test_factory_fallback_covers_every_branch():
    factory = DoorFactory("nowhere", random.Random(0))
    kinds = set()
    for roll in range(12):
        factory.rng = _scripted_rng([roll, 7])
        kinds.add(type(factory.create_fallback_door(1)).__name__)
    assert kinds == {"MinigameDoor", "PenaltyDoor", "NothingDoor", "RewardDoor"}


def _scripted_rng(values):
    iterator = iter(values)

    class Scripted:
        def randrange(self, n):
            return next(iterator) % n

    return Scripted()


def test_factory_fallback_pong_and_invader_names():
    factory = DoorFactory("nowhere", random.Random(0))
    factory.rng = _scripted_rng([0])
    pong = factory.create_fallback_door(1)
    factory.rng = _scripted_rng([1])
    invaders = factory.create_fallback_door(1)
    assert isinstance(pong, MinigameDoor) and pong.get_game_type() == "PONG"
    assert pong.get_name() == "Mysterious Hatch"
    assert isinstance(invaders, MinigameDoor) and invaders.get_game_type() == "SPACE_INVADERS"
    assert invaders.get_name() == "Strange Spacecraft"

