"""
Singleton lifecycle, menus and the text adventure loop.

Ports the ``Game`` cases of the Java suites and pins the text flows
the suites never drove: name validation, menu choices, victory,
defeat, quitting, invalid input and the life-loss dice.
"""

import random

import pytest

import text_ui
from door_factory import DoorFactory
from game import WIN_EXP, Game
from game_event import EventType
from minigame_door import MinigameDoor
from nothing_door import NothingDoor
from player import Player
from reward_door import RewardDoor


def make_inputs(*answers):
    iterator = iter(answers)
    return lambda: next(iterator)


@pytest.fixture()
def game():
    Game.reset()
    return Game.get_instance()


def test_singleton_returns_same_instance(game):
    assert Game.get_instance() is game


def test_reset_replaces_singleton(game):
    Game.reset()
    assert Game.get_instance() is not game
    assert Game.get_instance().get_player() is None


def test_initialize_player_rolls_starting_exp(game):
    game.rng = random.Random(4)
    game.initialize_player("TestPlayer")
    player = game.get_player()
    assert player.get_name() == "TestPlayer"
    assert player.get_exp() in (50, 100, 200)
    assert player.get_lives() == 3


def test_win_exp_threshold_is_500():
    assert WIN_EXP == 500


def test_get_valid_name_accepts_first_answer(game):
    assert game.get_valid_name(make_inputs("A.I.M")) == "A.I.M"


def test_get_valid_name_rejects_empty_then_long(game, capsys):
    name = game.get_valid_name(make_inputs("", "x" * 16, "Pilot"))
    assert name == "Pilot"
    assert "Invalid" in capsys.readouterr().out


def test_main_menu_quit(game, capsys):
    game.main_menu(make_inputs("3"))
    assert "Thanks for playing!" in capsys.readouterr().out


def test_main_menu_q_quits(game, capsys):
    game.main_menu(make_inputs("q"))
    assert "Thanks for playing!" in capsys.readouterr().out


def test_main_menu_toggle_then_quit(game, capsys):
    assert game.sound_on
    game.main_menu(make_inputs("2", "3"))
    assert not game.sound_on
    assert "Sound is now Off" in capsys.readouterr().out


def test_main_menu_invalid_then_quit(game, capsys):
    game.main_menu(make_inputs("9", "3"))
    assert "Please choose 1, 2, or 3." in capsys.readouterr().out


def test_play_loop_victory(game, capsys):
    game.player = Player("Pilot", 500)
    game.doors = [NothingDoor("Empty", "Void")]
    game.play_loop(make_inputs())
    assert "VICTORY" in capsys.readouterr().out


def test_play_loop_defeat_on_no_lives(game, capsys):
    game.player = Player("Pilot", 10)
    game.player.lose_life()
    game.player.lose_life()
    game.player.lose_life()
    game.play_loop(make_inputs())
    assert "DEFEAT" in capsys.readouterr().out


def test_play_loop_quit(game, capsys):
    game.player = Player("Pilot", 10)
    game.doors = [NothingDoor("Empty", "Void")]
    game.play_loop(make_inputs("quit"))
    assert "Thanks for playing!" in capsys.readouterr().out


def test_play_loop_invalid_then_out_of_range_then_quit(game, capsys):
    game.player = Player("Pilot", 10)
    game.doors = [NothingDoor("Empty", "Void")]
    game.play_loop(make_inputs("abc", "7", "quit"))
    out = capsys.readouterr().out
    assert "Please enter a number between 1 and 1." in out
    assert "No such door." in out


def test_play_loop_reward_then_victory(game, capsys, monkeypatch):
    game.player = Player("Pilot", 490)
    game.doors = [RewardDoor("Safe", "Harmless.", 25)]
    monkeypatch.setattr(DoorFactory, "create_random_door", lambda self, i: NothingDoor("E", "V"))
    game.play_loop(make_inputs("1"))
    out = capsys.readouterr().out
    assert "You gained 25 EXP!" in out
    assert "VICTORY" in out


def test_play_loop_bankrupt_breaks(game, capsys):
    from penalty_door import PenaltyDoor
    game.player = Player("Pilot", 10)
    game.doors = [PenaltyDoor("Trap", "Dark.", 25)]
    game.play_loop(make_inputs("1"))
    assert "Bankrupt" in capsys.readouterr().out


def test_play_loop_minigame_costs_life_and_redeals(game, monkeypatch):
    game.player = Player("Pilot", 100)
    game.doors = [MinigameDoor("Hatch", "Craft.", "PONG")]
    monkeypatch.setattr(Game, "setup_doors", lambda self: setattr(self, "doors", []))
    game.play_loop(make_inputs("1", "quit"))
    assert game.player.get_lives() == 2


def test_door_chosen_and_minigame_events_fire(game):
    seen = []
    game.add_listener(seen.append)
    game.player = Player("Pilot", 100)
    game.doors = [MinigameDoor("Hatch", "Craft.", "PONG")]
    game.play_loop(make_inputs("1", "quit"))
    kinds = [e.get_type() for e in seen]
    assert EventType.DOOR_CHOSEN in kinds
    assert EventType.MINIGAME_STARTED in kinds


def _seed_with_first_roll(predicate):
    for seed in range(200):
        if predicate(random.Random(seed).randint(1, 6)):
            return seed
    raise AssertionError("no seed found")


def test_handle_life_loss_wipes_on_low_roll(game, capsys):
    game.rng = random.Random(_seed_with_first_roll(lambda r: r <= 4))
    game.player = Player("Pilot", 120, game)
    game.handle_life_loss()
    out = capsys.readouterr().out
    assert game.player.get_exp() == 0
    assert "EXP Lost" in out


def test_handle_life_loss_spares_on_high_roll(game, capsys):
    game.rng = random.Random(_seed_with_first_roll(lambda r: r >= 5))
    game.player = Player("Pilot", 120, game)
    game.handle_life_loss()
    assert game.player.get_exp() == 120
    assert "EXP Saved" in capsys.readouterr().out


def test_start_full_text_run_to_quit(game, capsys, monkeypatch):
    game.rng = random.Random(2)
    monkeypatch.setattr(DoorFactory, "create_random_door", lambda self, i: NothingDoor("E", "V"))
    game.start(make_inputs("Pilot", "1", "quit"))
    out = capsys.readouterr().out
    assert "SPACE DOOR ADVENTURE" in out
    assert "Starting EXP" in out
    assert "Thanks for playing!" in out

