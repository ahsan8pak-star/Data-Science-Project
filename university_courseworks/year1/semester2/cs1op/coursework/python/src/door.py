"""
Abstract base class for every door type.

Translation of ``Door.java``. Python's ``abc`` module carries the abstract
``interact`` method that Java declares abstract, so a door that cannot be
opened cannot be instantiated.
"""

from abc import ABC, abstractmethod


class Door(ABC):
    """
    A named, described door the player can open.

    Subclasses decide what opening does by implementing ``interact``.
    """

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def get_name(self):
        """
        The door's display name.
        """
        return self.name

    def get_description(self):
        """
        The door's display description.
        """
        return self.description

    @abstractmethod
    def interact(self, player):
        """
        Open the door for the given player.

        Returns the result message shown to the player.
        """

