"""
Menu, name, options, sound-tab, dialogue, door and status states.

All state classes run without widgets: controllers are fakes recording
navigation, sounds stay silent, and dice and factories take seeded or
scripted doubles.
"""

import random

import pytest

import crt_settings
import sound_settings
from crt_screen import CrtState
from dialogue_screen import DICE_DECLINED_LINES, DICE_LINES, INTRO_LINES, DialogueState
from door_selection_screen import DoorSelectionState, art_for_door, door_line
from door_factory import DoorFactory
from game import Game, WIN_EXP
from game_play_screen import GameplayState, GameplayStatus, status_of
from main_menu_screen import OPTIONS, MainMenuState
from minigame_door import MinigameDoor
from name_entry_screen import MAX_NAME_LENGTH, NameBuffer, is_valid_character
from nothing_door import NothingDoor
from options_screen import OptionsState
from penalty_door import PenaltyDoor
from player import Player
from reward_door import RewardDoor
from sound_screen import CATEGORIES, SoundScreenState


class FakeController:
    def __init__(self, player=None):
        self.player = player
        self.shown = []
        self.minigames = []
        self.door_selections = 0
        self.menu_visits = 0
        self.options_visits = 0

    def get_current_player(self):
        return self.player

    def show_screen(self, name):
        self.shown.append(name)

    def start_door_selection(self):
        self.door_selections += 1

    def start_minigame(self, game_type):
        self.minigames.append(game_type)

    def go_back_to_main_menu(self):
        self.menu_visits += 1

    def show_options(self):
        self.options_visits += 1

    def show_sound_screen(self):
        self.shown.append("SOUND_SCREEN")


@pytest.fixture()
def controller():
    Game.reset()
    return FakeController(Player("Pilot", 100, Game.get_instance()))


def test_menu_options_listed():
    assert OPTIONS == ("START GAME", "SOUND", "OPTIONS", "QUIT")


def test_menu_wraps_both_directions():
    state = MainMenuState()
    state.move_up()
    assert state.selected == 3
    state.move_down()
    assert state.selected == 0


def test_menu_hover_rows_and_change_only():
    state = MainMenuState()
    assert state.hover_at(330) is True
    assert state.hovered == 0
    assert state.hover_at(330) is False
    assert state.hover_at(10) is False
    assert state.hovered == -1


def test_menu_confirm_routes():
    controller = FakeController()
    state = MainMenuState()
    state.selected = 1
    state.confirm(controller)
    assert controller.shown == ["SOUND_SCREEN"]
    state.selected = 2
    state.confirm(controller)
    assert controller.options_visits == 1


def test_menu_quit_raises_system_exit():
    state = MainMenuState()
    state.selected = 3
    with pytest.raises(SystemExit) as exc:
        state.confirm(FakeController())
    assert exc.value.code == 0


def test_name_buffer_accepts_printable_ascii_to_fifteen():
    buffer = NameBuffer()
    assert is_valid_character("A")
    assert is_valid_character(" ")
    assert not is_valid_character("\t")
    assert buffer.type_character("A")
    assert not buffer.type_character("\t")
    for _ in range(MAX_NAME_LENGTH - 1):
        assert buffer.type_character("x")
    assert len(buffer.text) == MAX_NAME_LENGTH
    assert not buffer.type_character("y")
    assert buffer.backspace()
    assert len(buffer.text) == MAX_NAME_LENGTH - 1
    buffer.text = ""
    assert not buffer.backspace()


def test_options_texts_follow_settings(controller):
    state = OptionsState()
    texts = state.option_texts()
    assert texts[0] == "DIFFICULTY: NORMAL"
    assert texts[1] == "SOUND: ON"
    assert texts[2] == "VOLUME: 50"
    assert texts[3] == "BACK TO MAIN MENU"


def test_options_left_cycles_difficulty_backwards():
    state = OptionsState()
    state.adjust_left()
    assert state.option_texts()[0] == "DIFFICULTY: EASY"
    state.adjust_right()
    assert state.option_texts()[0] == "DIFFICULTY: NORMAL"


def test_options_sound_toggle_and_volume_clamp():
    state = OptionsState()
    state.selected = 1
    state.adjust_right()
    assert state.option_texts()[1] == "SOUND: OFF"
    state.selected = 2
    state.volume = 0
    state.adjust_left()
    assert state.volume == 0
    state.volume = 100
    state.adjust_right()
    assert state.volume == 100
    state.selected = 3
    state.adjust_left()
    state.adjust_right()


def test_options_confirm_back_navigates(controller):
    state = OptionsState()
    state.selected = 3
    state.confirm(controller)
    assert controller.menu_visits == 1


def test_sound_state_tabs_clamp_and_files():
    state = SoundScreenState()
    assert CATEGORIES[0] == "Navigation"
    assert len(state.files()) == 3
    state.previous_category()
    assert state.selected_category == 0
    for _ in range(10):
        state.next_category()
    assert state.selected_category == len(CATEGORIES) - 1
    assert len(state.files()) == 12


def test_sound_volume_from_mouse_geometry():
    state = SoundScreenState()
    assert state.volume_from_mouse("f", (100, 0, 200, 10), 200) == 50
    assert state.volume_from_mouse("f", (100, 0, 200, 10), 100) == 0


def test_dialogue_greets_player_by_tag(controller):
    state = DialogueState(controller)
    assert state.lines[0] == "WELCOME, PILOT!"
    assert state.current_line() == "WELCOME, PILOT!"


def test_dialogue_greets_captain_without_player():
    state = DialogueState(FakeController())
    assert state.lines[0] == "WELCOME, CAPTAIN!"


def _run_to_prompt(state):
    while not state.awaiting_yn:
        state.advance()


def test_dialogue_yes_path_rolls_and_deals(controller):
    import dice_system
    dice = dice_system.DiceSystem(random.Random(9))
    state = DialogueState(controller, dice)
    _run_to_prompt(state)
    state.answer_yes()
    assert state.phase.name == "DICE_PROMPT"
    _run_to_prompt(state)
    state.answer_yes()
    assert state.phase.name == "DICE_RESULT"
    while state.phase.name == "DICE_RESULT" and not controller.door_selections:
        state.advance()
    assert controller.door_selections == 1
    assert controller.player.get_exp() == state.starting_hp
    assert controller.player.get_exp() in (50, 100, 200)


def test_dialogue_dice_decline_keeps_default_hp(controller):
    state = DialogueState(controller)
    _run_to_prompt(state)
    state.answer_yes()
    _run_to_prompt(state)
    state.answer_no()
    assert state.phase.name == "DICE_DECLINED"
    assert state.lines == list(DICE_DECLINED_LINES)
    while state.phase.name == "DICE_DECLINED" and not controller.door_selections:
        state.advance()
    assert controller.door_selections == 1
    assert controller.player.get_exp() == 100


def test_dialogue_rejection_returns_to_menu():
    controller = FakeController(Player("Pilot", 100, Game.get_instance()))
    state = DialogueState(controller)
    _run_to_prompt(state)
    state.answer_no()
    assert state.phase.name == "REJECTION"
    assert state.handle_escape()
    assert controller.shown == ["MAIN_MENU"]
    assert state.handle_escape()
    assert controller.shown == ["MAIN_MENU", "MAIN_MENU"]


def test_dialogue_advance_ignores_keys_while_awaiting(controller):
    state = DialogueState(controller)
    _run_to_prompt(state)
    before = state.line_idx
    state.advance()
    assert state.line_idx == before


def test_dialogue_reset_restores_introduction(controller):
    state = DialogueState(controller)
    _run_to_prompt(state)
    state.answer_yes()
    state.reset()
    assert state.phase.name == "INTRODUCTION"
    assert state.lines[0] == "WELCOME, PILOT!"


def test_door_lines_are_twelve_box_rows():
    assert door_line(1, 0) == "╔═══════════╗"
    assert door_line(3, 2) == "║ ║  3  ║ ║"
    assert door_line(5, 11) == "╚═══════════╝"
    assert door_line(1, 12) == ""
    assert door_line(1, -1) == ""


def test_art_matches_door_type():
    assert art_for_door(RewardDoor("R", "d", 1))[0].startswith("***")
    assert art_for_door(PenaltyDoor("P", "d", 1))[1].strip() == "|____|"
    assert art_for_door(NothingDoor("N", "d"))[0].strip() == "___________________________"
    assert art_for_door(MinigameDoor("M", "d", "PONG"))[1].strip().startswith("..-+##+-..")
    assert art_for_door(MinigameDoor("M", "d", "SPACE_INVADERS"))[0].startswith(" /\\/\\/\\")


def test_door_selection_deals_five_and_wraps(controller, tmp_path):
    doors_file = tmp_path / "doors.txt"
    doors_file.write_text("Reward | Chest | art | 10\n", encoding="utf-8")
    state = DoorSelectionState(controller, DoorFactory(tmp_path, random.Random(0)))
    assert len(state.doors) == 5
    state.move_selection(-1)
    assert state.selected == 4
    state.move_selection(1)
    assert state.selected == 0


def test_open_reward_reveals_chest_message(controller):
    controller.player.set_exp(0)
    state = DoorSelectionState(controller)
    state.doors = [RewardDoor("Safe", "Harmless.", 25)]
    message = state.open_selected()
    assert message == "You Found a Shiny Chest!  +25 EXP!"
    assert controller.player.get_exp() == 25
    assert state.revealed


def test_open_penalty_reveals_toxic_message(controller):
    state = DoorSelectionState(controller)
    state.doors = [PenaltyDoor("Trap", "Dark.", 25)]
    assert state.open_selected() == "Toxic Fumes!  25 EXP Lost!"
    assert controller.player.get_exp() == 75


def test_open_nothing_reveals_void_message(controller):
    state = DoorSelectionState(controller)
    state.doors = [NothingDoor("Empty", "Void.")]
    assert state.open_selected() == "The Door Reveals Nothing but an Empty Void..."
    assert controller.player.get_exp() == 100


def test_open_minigame_arms_pending_handoff(controller):
    state = DoorSelectionState(controller)
    state.doors = [MinigameDoor("Hatch", "Craft.", "PONG")]
    assert state.open_selected().endswith("Press ENTER to Play PONG!")
    assert state.minigame_pending
    assert state.pending_minigame_type == "PONG"
    assert state.confirm_revealed() == "minigame"
    assert controller.minigames == ["PONG"]


def test_confirm_revealed_routes_decided_runs_to_gameplay(controller):
    state = DoorSelectionState(controller)
    state.doors = [NothingDoor("Empty", "Void.")]
    state.open_selected()
    controller.player.set_exp(WIN_EXP)
    assert state.confirm_revealed() == "gameplay"
    assert controller.shown == ["GAMEPLAY"]


def test_confirm_revealed_redeals_live_runs(controller, tmp_path):
    doors_file = tmp_path / "doors.txt"
    doors_file.write_text("Reward | Chest | art | 10\n", encoding="utf-8")
    state = DoorSelectionState(controller, DoorFactory(tmp_path, random.Random(0)))
    state.doors = [NothingDoor("Empty", "Void.")]
    state.open_selected()
    assert state.confirm_revealed() == "redeal"
    assert not state.revealed
    assert len(state.doors) == 5


def test_gameplay_status_classification():
    assert status_of(None) == GameplayStatus.NORMAL
    assert status_of(Player("W", 500)) == GameplayStatus.WIN
    dead = Player("D", 10)
    dead.lose_life()
    dead.lose_life()
    dead.lose_life()
    assert status_of(dead) == GameplayStatus.DEAD
    assert status_of(Player("B", -5)) == GameplayStatus.BANKRUPT
    assert status_of(Player("N", 10)) == GameplayStatus.NORMAL


def test_gameplay_win_keys(controller):
    controller.player.set_exp(WIN_EXP)
    state = GameplayState(controller)
    state.on_shown()
    assert state.last_sound_state == "WIN"
    assert state.handle_key("Return") == "dialogue"
    assert controller.shown == ["DIALOGUE"]
    assert state.handle_key("Escape") == "menu"
    assert state.handle_key("x") == "none"


def test_gameplay_dead_key_only_escapes(controller):
    controller.player.lose_life()
    controller.player.lose_life()
    controller.player.lose_life()
    state = GameplayState(controller)
    state.on_shown()
    assert state.last_sound_state == "DEAD"
    assert state.handle_key("Return") == "none"
    assert state.handle_key("Escape") == "menu"


def test_gameplay_normal_key_deals_doors(controller):
    state = GameplayState(controller)
    state.on_shown()
    assert state.last_sound_state == "NONE"
    assert state.handle_key("space") == "doors"
    assert controller.shown == ["DOOR_SELECTION"]


def test_gameplay_no_player_is_inert():
    state = GameplayState(FakeController())
    state.on_shown()
    assert state.handle_key("Return") == "none"


def test_crt_toggle_and_intensity_geometry():
    state = CrtState()
    assert not crt_settings.is_enabled()
    state.toggle_on()
    assert crt_settings.is_enabled()
    state.toggle_off()
    assert not crt_settings.is_enabled()
    state.set_intensity_from_mouse((100, 0, 200, 10), 200)
    assert crt_settings.get_intensity() == 50
    state.set_intensity_from_mouse((100, 0, 200, 10), 400)
    assert crt_settings.get_intensity() == 100


def test_crt_confirm_leaves_or_flips():
    controller = FakeController()
    state = CrtState()
    state.focus_intensity = False
    state.confirm(controller)
    assert controller.options_visits == 1
    state.focus_intensity = True
    state.confirm(controller)
    assert crt_settings.is_enabled()
    state.confirm(controller)
    assert not crt_settings.is_enabled()

