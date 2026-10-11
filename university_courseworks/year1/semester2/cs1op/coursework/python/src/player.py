"""
The player: name, experience points, lives and inventory.

Translation of ``Player.java``. Every EXP or life change notifies the
game's listeners, preserving the Observer wiring exactly: ``set_exp``,
``add_exp``, ``subtract_exp`` and ``change_exp`` all emit ``EXP_CHANGED``,
``lose_life`` emits ``LIFE_LOST``, and ``add_item`` emits
``ITEM_COLLECTED`` with the item as payload.
"""

from game_event import EventType, GameEvent


class Player:
    """
    Mutable player state bound to a game for event notification.
    """

    def __init__(self, name, starting_exp=0, game=None):
        self.name = name
        self.exp = starting_exp
        self.lives = 3
        self.inventory = []
        self.game = game

    def set_game(self, game):
        """
        Inject the game reference this player notifies.
        """
        self.game = game

    def _game(self):
        if self.game is None:
            from game import Game
            self.game = Game.get_instance()
        return self.game

    def set_exp(self, exp):
        """
        Set EXP to a specific value and notify listeners.
        """
        self.exp = exp
        self._game().notify_listeners(GameEvent(EventType.EXP_CHANGED, self))

    def add_exp(self, amount):
        """
        Add EXP to the current total and notify listeners.
        """
        self.exp += amount
        self._game().notify_listeners(GameEvent(EventType.EXP_CHANGED, self))

    def subtract_exp(self, amount):
        """
        Subtract EXP from the current total and notify listeners.
        """
        self.exp -= amount
        self._game().notify_listeners(GameEvent(EventType.EXP_CHANGED, self))

    def change_exp(self, delta):
        """
        Change EXP by a signed delta and notify listeners.
        """
        self.exp += delta
        self._game().notify_listeners(GameEvent(EventType.EXP_CHANGED, self))

    def get_name(self):
        """
        The player's name.
        """
        return self.name

    def get_exp(self):
        """
        The player's current EXP.
        """
        return self.exp

    def get_lives(self):
        """
        The player's remaining lives.
        """
        return self.lives

    def lose_life(self):
        """
        Lose one life, never dropping below zero, and notify listeners.
        """
        self.lives = max(0, self.lives - 1)
        self._game().notify_listeners(GameEvent(EventType.LIFE_LOST, self))

    def is_game_over(self):
        """
        True when the run has ended: no lives left or negative EXP.
        """
        return self.lives <= 0 or self.exp < 0

    def is_bankrupt(self):
        """
        True when EXP has fallen below zero.
        """
        return self.exp < 0

    def add_item(self, item):
        """
        Collect an item into the inventory and notify listeners.
        """
        self.inventory.append(item)
        self._game().notify_listeners(GameEvent(EventType.ITEM_COLLECTED, item))

    def has_item(self, item_name):
        """
        True when the inventory holds an item of that name, any case.
        """
        return any(i.get_name().lower() == item_name.lower() for i in self.inventory)

    def get_inventory(self):
        """
        The live inventory list.
        """
        return self.inventory

