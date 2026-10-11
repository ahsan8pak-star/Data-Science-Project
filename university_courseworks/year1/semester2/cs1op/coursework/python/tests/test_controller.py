"""
Controller routing with a fake GUI shell.

View construction needs a display, so screen-creating paths swap the
tkinter views for recording fakes at call time; everything else runs
against the real controller and singleton.
"""

import pytest

import sound_manager
from game import Game
from game_controller import GameController
from player import Player


class FakeGui:
    def __init__(self):
        self.shown = []
        self.added = {}
        self.removed = []

    def show_screen(self, name):
        self.shown.append(name)

    def add_screen(self, screen, name):
        self.added[name] = screen

    def remove_screen(self, name):
        self.removed.append(name)


class FakeScreen:
    def __init__(self, gui, controller):
        self.gui = gui
        self.controller = controller


@pytest.fixture()
def setup():
    Game.reset()
    gui = FakeGui()
    controller = GameController(gui)
    return gui, controller


def test_start_game_navigates_to_name_entry(setup):
    gui, controller = setup
    controller.start_game()
    assert gui.shown == ["NAME_ENTRY"]


def test_go_back_to_main_menu(setup):
    gui, controller = setup
    controller.go_back_to_main_menu()
    assert gui.shown == ["MAIN_MENU"]


def test_game_over_returns_to_menu(setup):
    gui, controller = setup
    controller.game_over()
    assert gui.shown == ["MAIN_MENU"]


def test_set_player_name_creates_player_and_dialogue(setup):
    gui, controller = setup
    controller.set_player_name("Pilot")
    assert controller.get_current_player().get_name() == "Pilot"
    assert controller.get_current_player().get_exp() in (50, 100, 200)
    assert gui.shown == ["DIALOGUE"]


def test_start_minigame_without_player_falls_back(setup):
    gui, controller = setup
    controller.start_minigame("PONG")
    assert gui.shown == ["GAMEPLAY"]
    assert gui.added == {}


def test_start_minigame_without_lives_falls_back(setup):
    gui, controller = setup
    controller.current_player = Player("Pilot", 100, Game.get_instance())
    controller.current_player.lose_life()
    controller.current_player.lose_life()
    controller.current_player.lose_life()
    controller.start_minigame("PONG")
    assert gui.shown == ["GAMEPLAY"]


def test_start_minigame_builds_views(setup, monkeypatch):
    import game_controller
    monkeypatch.setattr("pong_view.PongMinigameView", FakeScreen)
    monkeypatch.setattr("space_invaders_view.SpaceInvadersView", FakeScreen)
    gui, controller = setup
    controller.current_player = Player("Pilot", 100, Game.get_instance())
    controller.start_minigame("PONG")
    assert isinstance(gui.added["MINIGAME_PONG"], FakeScreen)
    assert gui.shown[-1] == "MINIGAME_PONG"
    controller.start_minigame("SPACE_INVADERS")
    assert isinstance(gui.added["MINIGAME_SPACE_INVADERS"], FakeScreen)
    assert gui.shown[-1] == "MINIGAME_SPACE_INVADERS"
    controller.start_minigame("UNKNOWN")
    assert "UNKNOWN" not in gui.added


def test_show_options_sound_and_crt_build_views(setup, monkeypatch):
    monkeypatch.setattr("options_screen.OptionsScreen", FakeScreen)
    monkeypatch.setattr("sound_screen.SoundScreen", FakeScreen)
    monkeypatch.setattr("crt_screen.CrtScreen", FakeScreen)
    gui, controller = setup
    controller.show_options()
    assert isinstance(gui.added["OPTIONS"], FakeScreen)
    controller.show_sound_screen()
    assert isinstance(gui.added["SOUND_SCREEN"], FakeScreen)
    controller.show_crt_screen()
    assert isinstance(gui.added["CRT_SCREEN"], FakeScreen)
    assert gui.shown == ["OPTIONS", "SOUND_SCREEN", "CRT_SCREEN"]


def test_start_door_selection_builds_view(setup, monkeypatch):
    monkeypatch.setattr("door_selection_screen.DoorSelectionScreenView", FakeScreen)
    gui, controller = setup
    controller.start_door_selection()
    assert isinstance(gui.added["DOOR_SELECTION"], FakeScreen)
    assert gui.shown == ["DOOR_SELECTION"]


def test_minigame_won_grants_exp_and_continues(setup, monkeypatch):
    monkeypatch.setattr("door_selection_screen.DoorSelectionScreenView", FakeScreen)
    gui, controller = setup
    controller.current_player = Player("Pilot", 100, Game.get_instance())
    controller.on_minigame_won("PONG", 50)
    assert controller.current_player.get_exp() == 150
    assert gui.removed == ["MINIGAME_PONG", "MINIGAME_SPACE_INVADERS"]
    assert gui.shown == ["DOOR_SELECTION"]


def test_minigame_won_at_threshold_routes_to_gameplay(setup):
    gui, controller = setup
    controller.current_player = Player("Pilot", 490, Game.get_instance())
    controller.on_minigame_won("SPACE_INVADERS", 100)
    assert controller.current_player.get_exp() == 590
    assert gui.shown == ["GAMEPLAY"]


def test_minigame_lost_costs_life_and_continues(setup, monkeypatch):
    monkeypatch.setattr("door_selection_screen.DoorSelectionScreenView", FakeScreen)
    gui, controller = setup
    controller.current_player = Player("Pilot", 100, Game.get_instance())
    controller.on_minigame_lost()
    assert controller.current_player.get_lives() == 2
    assert gui.removed == ["MINIGAME_PONG", "MINIGAME_SPACE_INVADERS"]
    assert gui.shown == ["DOOR_SELECTION"]


def test_minigame_lost_on_last_life_routes_to_gameplay(setup):
    gui, controller = setup
    controller.current_player = Player("Pilot", 100, Game.get_instance())
    controller.current_player.lose_life()
    controller.current_player.lose_life()
    controller.on_minigame_lost()
    assert controller.current_player.get_lives() == 0
    assert gui.shown == ["GAMEPLAY"]


def test_minigame_callbacks_without_player_stay_safe(setup, monkeypatch):
    monkeypatch.setattr("door_selection_screen.DoorSelectionScreenView", FakeScreen)
    gui, controller = setup
    controller.on_minigame_won("PONG", 50)
    controller.on_minigame_lost()
    assert gui.shown == ["MAIN_MENU", "MAIN_MENU"]

