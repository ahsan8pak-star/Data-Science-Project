"""
A door that grants experience points.

Translation of ``RewardDoor.java``.
"""

from door import Door


class RewardDoor(Door):
    """
    Opening grants the stored EXP value to the player.
    """

    def __init__(self, name, description, exp):
        super().__init__(name, description)
        self.exp = exp

    def get_exp_value(self):
        """
        The EXP granted on opening.
        """
        return self.exp

    def interact(self, player):
        player.change_exp(self.exp)
        return "You gained " + str(self.exp) + " EXP!"

