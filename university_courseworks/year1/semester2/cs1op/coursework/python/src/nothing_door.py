"""
A door that reveals nothing and changes nothing.

Translation of ``NothingDoor.java``.
"""

from door import Door


class NothingDoor(Door):
    """
    Opening returns the empty-space message and leaves EXP untouched.
    """

    def interact(self, player):
        return "The door reveals nothing. Just empty space."

