"""
Player state, progression and observer wiring.

Ports ``GameTest.testPlayerInitializationWithExp``, ``testPlayerAddExp``
and ``testPlayerAddItem``, the player cases of ``GameTestSuite`` and the
player cases of ``TestGameLogic``, plus event-payload checks the Java
suite never asserted.
"""

import pytest

from game import Game
from game_event import EventType
from item import Item
from player import Player


@pytest.fixture()
def player():
    Game.reset()
    return Player("TestPlayer")


def test_initialization_defaults(player):
    assert player.get_name() == "TestPlayer"
    assert player.get_exp() == 0
    assert player.get_lives() == 3
    assert player.get_inventory() == []


def test_initialization_with_starting_exp():
    assert Player("Tester", 100).get_exp() == 100


def test_add_exp():
    player = Player("Tester", 100)
    player.add_exp(25)
    assert player.get_exp() == 125


def test_exp_gain_accumulates(player):
    player.add_exp(50)
    assert player.get_exp() == 50
    player.add_exp(75)
    assert player.get_exp() == 125


def test_exp_penalty(player):
    player.add_exp(100)
    player.subtract_exp(30)
    assert player.get_exp() == 70


def test_set_exp(player):
    player.set_exp(200)
    assert player.get_exp() == 200


def test_exp_edge_cases(player):
    player.set_exp(0)
    assert player.get_exp() == 0
    player.set_exp(500)
    assert player.get_exp() == 500
    player.add_exp(1000)
    assert player.get_exp() == 1500


def test_maximum_exp(player):
    player.add_exp(10000)
    assert player.get_exp() == 10000


def test_lose_life(player):
    initial = player.get_lives()
    player.lose_life()
    assert player.get_lives() == initial - 1


def test_lives_never_go_below_zero(player):
    for _ in range(5):
        player.lose_life()
    assert player.get_lives() == 0


def test_game_over_when_lives_zero(player):
    player.lose_life()
    player.lose_life()
    player.lose_life()
    assert player.get_lives() == 0
    assert player.is_game_over()


def test_game_over_when_bankrupt(player):
    player.subtract_exp(1)
    assert player.is_bankrupt()
    assert player.is_game_over()


def test_alive_by_default(player):
    assert not player.is_game_over()
    assert not player.is_bankrupt()


def test_exp_persists_across_life_loss(player):
    player.set_exp(250)
    player.lose_life()
    assert player.get_exp() == 250


def test_name_preserved_by_play(player):
    player.add_exp(100)
    player.lose_life()
    assert player.get_name() == "TestPlayer"


def test_single_character_name():
    assert Player("A").get_name() == "A"


def test_add_item_and_has_item_case_insensitive(player):
    coin = Item("Coin", "A shiny gold coin")
    player.add_item(coin)
    assert player.has_item("Coin")
    assert player.has_item("coin")
    assert player.has_item("COIN")
    assert not player.has_item("Crown")
    assert player.get_inventory() == [coin]


def test_item_string_representation():
    assert str(Item("Coin", "A shiny gold coin")) == "Coin: A shiny gold coin"


def test_exp_change_notifies_with_player_payload(player):
    seen = []
    Game.get_instance().add_listener(seen.append)
    player.set_exp(10)
    player.add_exp(5)
    player.subtract_exp(2)
    player.change_exp(1)
    assert [e.get_type() for e in seen] == [EventType.EXP_CHANGED] * 4
    assert all(e.get_payload() is player for e in seen)


def test_lose_life_notifies_with_player_payload(player):
    seen = []
    Game.get_instance().add_listener(seen.append)
    player.lose_life()
    assert len(seen) == 1
    assert seen[0].get_type() == EventType.LIFE_LOST
    assert seen[0].get_payload() is player


def test_add_item_notifies_with_item_payload(player):
    seen = []
    Game.get_instance().add_listener(seen.append)
    coin = Item("Coin", "A shiny gold coin")
    player.add_item(coin)
    assert len(seen) == 1
    assert seen[0].get_type() == EventType.ITEM_COLLECTED
    assert seen[0].get_payload() is coin


def test_injected_game_reference_receives_events():
    custom = Game(rng=None)
    custom.listeners.clear()
    seen = []
    custom.add_listener(seen.append)
    player = Player("Tester", 0, custom)
    player.add_exp(10)
    player.lose_life()
    assert [e.get_type() for e in seen] == [EventType.EXP_CHANGED, EventType.LIFE_LOST]

