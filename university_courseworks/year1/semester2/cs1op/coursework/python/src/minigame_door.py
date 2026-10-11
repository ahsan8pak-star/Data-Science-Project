"""
A door that leads to a minigame.

Translation of ``MinigameDoor.java``. Opening itself changes nothing;
the controller launches the named minigame from the door's game type.
"""

from door import Door


class MinigameDoor(Door):
    """
    Opening names the minigame to launch: ``PONG`` or ``SPACE_INVADERS``.
    """

    def __init__(self, name, description, game_type):
        super().__init__(name, description)
        self.game_type = game_type

    def get_game_type(self):
        """
        The minigame identifier this door leads to.
        """
        return self.game_type

    def interact(self, player):
        return "You enter the spaceship!"

