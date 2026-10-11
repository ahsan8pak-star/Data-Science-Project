"""
A door that takes experience points from the player.

Translation of ``PenaltyDoor.java``. The stored value is the positive
drain; ``get_exp_value`` reports it negated, exactly as the Java does.
"""

from door import Door


class PenaltyDoor(Door):
    """
    Opening drains the stored EXP value from the player.
    """

    def __init__(self, name, description, exp):
        super().__init__(name, description)
        self.exp = exp

    def get_exp_value(self):
        """
        The EXP change on opening, negative because it is a penalty.
        """
        return -self.exp

    def interact(self, player):
        player.change_exp(-self.exp)
        return "You lost " + str(self.exp) + " EXP."

