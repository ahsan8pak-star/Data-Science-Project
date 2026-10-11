"""
Event object and listener protocol for the Observer pattern.

Translation of ``GameEvent.java`` and ``GameEventListener.java``. The Java
interface becomes a ``typing.Protocol``: any object with an ``on_event``
method can listen, with no inheritance required.
"""

from enum import Enum, auto
from typing import Any, Protocol


class EventType(Enum):
    """
    The kinds of game event listeners can receive.
    """

    EXP_CHANGED = auto()
    LIFE_LOST = auto()
    ITEM_COLLECTED = auto()
    DOOR_CHOSEN = auto()
    MINIGAME_STARTED = auto()


class GameEvent:
    """
    A typed event carrying a payload object.
    """

    def __init__(self, type, payload):
        self.type = type
        self.payload = payload

    def get_type(self):
        """
        The event's type.
        """
        return self.type

    def get_payload(self):
        """
        The event's payload object.
        """
        return self.payload


class GameEventListener(Protocol):
    """
    Receives game events. Implementations define ``on_event``.
    """

    def on_event(self, event: GameEvent) -> Any:
        """
        Called when a game event occurs.
        """
        ...

