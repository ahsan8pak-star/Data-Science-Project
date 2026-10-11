"""
A collectible item held in the player's inventory.

Translation of ``Item.java``.
"""

class Item:
    """
    A named item with a description.
    """

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def get_name(self):
        """
        The item's name.
        """
        return self.name

    def get_description(self):
        """
        The item's description.
        """
        return self.description

    def __str__(self):
        return self.name + ": " + self.description

