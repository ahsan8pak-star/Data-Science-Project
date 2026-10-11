"""
Links the GUI shell to the game logic and owns screen transitions.

Translation of ``GameController.java``. Results handling is preserved:
a minigame win grants EXP, a loss costs a life, and every major
transition stops all sounds first. One defect in the Java is repaired
here rather than reproduced: ``show_crt_screen`` built a ``CRTScreen``
class that does not exist in the Java sources, so the Python names the
real ``CrtScreen`` implemented beside the other screens.
"""

import sound_manager
from game import Game, WIN_EXP


class GameController:
    """
    Mediates between screens and the singleton game state.
    """

    def __init__(self, gui):
        self.gui = gui
        self.current_player = None
        self.game_instance = None

    def start_game(self):
        """
        Begin a session by navigating to name entry.
        """
        sound_manager.stop_all()
        self.gui.show_screen("NAME_ENTRY")

    def show_options(self):
        """
        Open a fresh options screen.
        """
        from options_screen import OptionsScreen
        self.gui.add_screen(OptionsScreen(self.gui, self), "OPTIONS")
        self.gui.show_screen("OPTIONS")

    def show_crt_screen(self):
        """
        Open the full-screen CRT display settings page.
        """
        from crt_screen import CrtScreen
        self.gui.add_screen(CrtScreen(self.gui, self), "CRT_SCREEN")
        self.gui.show_screen("CRT_SCREEN")

    def show_sound_screen(self):
        """
        Open the per-sound volume settings screen.
        """
        from sound_screen import SoundScreen
        self.gui.add_screen(SoundScreen(self.gui, self), "SOUND_SCREEN")
        self.gui.show_screen("SOUND_SCREEN")

    def go_back_to_main_menu(self):
        """
        Return to the main menu, stopping all sounds.
        """
        sound_manager.stop_all()
        self.gui.show_screen("MAIN_MENU")

    def show_screen(self, name):
        """
        Navigate to a registered screen by name.
        """
        self.gui.show_screen(name)

    def start_door_selection(self):
        """
        Open a fresh five-door selection screen.
        """
        from door_selection_screen import DoorSelectionScreenView
        self.gui.add_screen(DoorSelectionScreenView(self.gui, self), "DOOR_SELECTION")
        self.gui.show_screen("DOOR_SELECTION")

    def set_player_name(self, name):
        """
        Create the player and move on to the dialogue.
        """
        self.game_instance = Game.get_instance()
        self.game_instance.initialize_player(name)
        self.current_player = self.game_instance.get_player()
        self.gui.show_screen("DIALOGUE")

    def start_minigame(self, game_name):
        """
        Launch the named minigame, or fall back to gameplay when spent.
        """
        if self.current_player is None or self.current_player.get_lives() <= 0:
            self.gui.show_screen("GAMEPLAY")
            return
        sound_manager.stop_all()
        if game_name == "PONG":
            from pong_view import PongMinigameView
            self.gui.add_screen(PongMinigameView(self.gui, self), "MINIGAME_PONG")
            self.gui.show_screen("MINIGAME_PONG")
        elif game_name == "SPACE_INVADERS":
            from space_invaders_view import SpaceInvadersView
            self.gui.add_screen(SpaceInvadersView(self.gui, self), "MINIGAME_SPACE_INVADERS")
            self.gui.show_screen("MINIGAME_SPACE_INVADERS")

    def on_minigame_won(self, game_type, exp_gained):
        """
        Grant the winnings and continue, win or lose, from gameplay.
        """
        sound_manager.stop_all()
        self.gui.remove_screen("MINIGAME_PONG")
        self.gui.remove_screen("MINIGAME_SPACE_INVADERS")
        if self.current_player is not None:
            self.current_player.add_exp(exp_gained)
        self.check_win_loss_or_continue()

    def on_minigame_lost(self):
        """
        Cost a life for the lost minigame and continue from gameplay.
        """
        sound_manager.stop_all()
        self.gui.remove_screen("MINIGAME_PONG")
        self.gui.remove_screen("MINIGAME_SPACE_INVADERS")
        if self.current_player is not None:
            sound_manager.play_once(sound_manager.LIFE_LOST)
            self.current_player.lose_life()
        self.check_win_loss_or_continue()

    def check_win_loss_or_continue(self):
        """
        Route to gameplay on a decided run, else deal fresh doors.
        """
        if self.current_player is None:
            self.gui.show_screen("MAIN_MENU")
            return
        if (self.current_player.get_exp() >= WIN_EXP
                or self.current_player.get_lives() <= 0
                or self.current_player.get_exp() < 0):
            self.gui.show_screen("GAMEPLAY")
        else:
            self.start_door_selection()

    def game_over(self):
        """
        End the game and return to the main menu.
        """
        sound_manager.stop_all()
        self.gui.show_screen("MAIN_MENU")

    def get_current_player(self):
        """
        The currently active player, if one has been named.
        """
        return self.current_player

