"""
Factory that builds doors from ``doors.txt`` or from fallback rules.

Translation of ``DoorFactory.java``. The template format is preserved
exactly: ``Type | Description | ASCII_KEY | Value | Dice #``, where only
lines whose type is one of reward, penalty, nothing, pong minigame,
space invaders minigame or minigame are read. Note the Java quirk kept
here: ``minigame`` is a recognised template type but has no branch in the
creation switch, so it falls through to the fallback door.
"""

import random
from pathlib import Path

from minigame_door import MinigameDoor
from nothing_door import NothingDoor
from penalty_door import PenaltyDoor
from reward_door import RewardDoor


RECOGNISED_TYPES = frozenset({
    "reward",
    "penalty",
    "nothing",
    "pong minigame",
    "space invaders minigame",
    "minigame",
})

DEFAULT_RESOURCES = Path(__file__).resolve().parent.parent / "resources"


class DoorFactory:
    """
    Creates doors from templates, falling back to dice rules without a file.
    """

    def __init__(self, resources_dir=None, rng=None):
        self.rng = rng if rng is not None else random.Random()
        self.templates = []
        self.resources_dir = Path(resources_dir) if resources_dir else DEFAULT_RESOURCES
        self.load_templates()

    def load_templates(self):
        """
        Read recognised template lines from ``doors.txt``, if it exists.
        """
        doors_file = self.resources_dir / "doors.txt"
        if not doors_file.exists():
            return
        for raw in doors_file.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) < 2:
                continue
            if parts[0].strip().lower() in RECOGNISED_TYPES:
                self.templates.append(parts)

    def create_random_door(self, index):
        """
        Build a door from a random template, or the fallback rules.
        """
        if self.templates:
            parts = self.templates[self.rng.randrange(len(self.templates))]
            door_type = parts[0].strip().lower()
            desc = parts[1].strip() if len(parts) > 1 else ""
            if door_type == "reward":
                return RewardDoor("Door " + str(index), desc, self._value(parts, 50))
            if door_type == "penalty":
                return PenaltyDoor("Door " + str(index), desc, self._value(parts, 25, absolute=True))
            if door_type == "pong minigame":
                return MinigameDoor("Door " + str(index), desc, "PONG")
            if door_type == "space invaders minigame":
                return MinigameDoor("Door " + str(index), desc, "SPACE_INVADERS")
            if door_type == "nothing":
                return NothingDoor("Door " + str(index), desc)
        return self.create_fallback_door(index)

    @staticmethod
    def _value(parts, default, absolute=False):
        try:
            value = int(parts[3].strip())
        except (IndexError, ValueError):
            return default
        return abs(value) if absolute else value

    def create_fallback_door(self, index):
        """
        Dice fallback used when no template applies: minigames on 0-1,
        penalty on 2-4, nothing on 5, reward otherwise.
        """
        roll = self.rng.randrange(12)
        if roll == 0:
            return MinigameDoor("Mysterious Hatch", "A hatch to a strange craft.", "PONG")
        if roll == 1:
            return MinigameDoor("Strange Spacecraft", "A hatch into the unknown.", "SPACE_INVADERS")
        if roll <= 4:
            return PenaltyDoor("Trap Door", "A dark trap that drains energy.", 25 + self.rng.randrange(25))
        if roll == 5:
            return NothingDoor("Empty Door", "A door with nothing behind it.")
        return RewardDoor("Safe Door", "A door that seems harmless.", 25 + self.rng.randrange(25))

