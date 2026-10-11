"""
Gameplay status: win/lose routing and the status view.

Translation of ``GamePlayScreen.java``. The four player states (WIN,
DEAD, BANKRUPT, NORMAL) drive both the entry sounds — victory plays
once, defeat loops until ESC — and the key handling: ENTER continues
from victory, ESC leaves from anywhere, any other key deals doors.
"""

import tkinter as tk

import sound_manager
from base_screen import (
    ARC_DIM,
    ARC_LIME,
    ARC_NEON,
    ARC_TEXT,
    BaseGameScreen,
)
from game import WIN_EXP


class GameplayStatus:
    """
    The four status states of the gameplay screen.
    """

    WIN = "WIN"
    DEAD = "DEAD"
    BANKRUPT = "BANKRUPT"
    NORMAL = "NORMAL"


def status_of(player):
    """
    Classify a player into WIN, DEAD, BANKRUPT or NORMAL.
    """
    if player is None:
        return GameplayStatus.NORMAL
    if player.get_exp() >= WIN_EXP:
        return GameplayStatus.WIN
    if player.get_lives() <= 0:
        return GameplayStatus.DEAD
    if player.get_exp() < 0:
        return GameplayStatus.BANKRUPT
    return GameplayStatus.NORMAL


class GameplayState:
    """
    Entry-sound tracking and key routing, without any widgets.
    """

    def __init__(self, controller):
        self.controller = controller
        self.last_sound_state = "NONE"

    def on_shown(self):
        """
        Play the entry sound once per state entry.
        """
        status = status_of(self.controller.get_current_player())
        if status == GameplayStatus.NORMAL:
            self.last_sound_state = "NONE"
            return
        if status != self.last_sound_state:
            self.last_sound_state = status
            sound_manager.stop_all()
            if status == GameplayStatus.WIN:
                sound_manager.play_once(sound_manager.GAME_WIN_SOUND)
            else:
                sound_manager.play_loop(sound_manager.GAME_OVER_SOUND)

    def handle_key(self, keysym):
        """
        Route a key press for the current status.

        Returns the action taken: ``dialogue``, ``menu``, ``doors`` or
        ``none``.
        """
        player = self.controller.get_current_player()
        if player is None:
            return "none"
        status = status_of(player)
        if status == GameplayStatus.WIN:
            if keysym == "Return":
                sound_manager.stop_all()
                self.controller.show_screen("DIALOGUE")
                return "dialogue"
            if keysym == "Escape":
                sound_manager.stop_all()
                self.controller.go_back_to_main_menu()
                return "menu"
            return "none"
        if status in (GameplayStatus.DEAD, GameplayStatus.BANKRUPT):
            if keysym == "Escape":
                sound_manager.stop_sound(sound_manager.GAME_OVER_SOUND)
                sound_manager.stop_all()
                self.controller.go_back_to_main_menu()
                return "menu"
            return "none"
        if keysym == "Escape":
            sound_manager.stop_all()
            self.controller.go_back_to_main_menu()
            return "menu"
        self.last_sound_state = "NONE"
        self.controller.show_screen("DOOR_SELECTION")
        return "doors"


class GamePlayScreen(BaseGameScreen):
    """
    The pilot status page with victory and defeat variants.
    """

    def __init__(self, gui, controller):
        super().__init__(gui, controller)
        self.state = GameplayState(controller)
        self.canvas_widget = self.canvas()
        self.bind("<KeyPress>", self._on_key)
        self.bind("<Configure>", lambda _e: self.redraw())
        self.bind("<Map>", lambda _e: (self.state.on_shown(), self.redraw()))

    def _on_key(self, event):
        self.state.handle_key(event.keysym)
        self.redraw()

    def show(self):
        """
        Refresh entry sounds and repaint, called by the shell on display.
        """
        self.state.on_shown()
        self.redraw()

    def redraw(self):
        """
        Paint the status, victory, defeat or bankrupt panel.
        """
        canvas = self.canvas_widget
        canvas.delete("all")
        width = max(canvas.winfo_width(), 900)
        height = max(canvas.winfo_height(), 650)
        canvas.create_rectangle(50, 50, width - 50, height - 50, outline=ARC_NEON, width=2)
        self.draw_centred_text(canvas, "SPACE MISSION", width // 2, 100, ("Monospaced", 32, "bold"), ARC_LIME)
        player = self.controller.get_current_player()
        if player is None:
            return
        status = status_of(player)
        canvas.create_text(80, 160, text="Pilot: " + player.get_name(),
                           font=("Monospaced", 18, "normal"), fill=ARC_TEXT, anchor="w")
        canvas.create_text(80, 200, text="EXP Collected: " + str(player.get_exp()) + " / 500",
                           font=("Monospaced", 18, "normal"), fill=ARC_TEXT, anchor="w")
        canvas.create_text(80, 240, text="Lives Remaining: " + str(player.get_lives()),
                           font=("Monospaced", 18, "normal"), fill=ARC_TEXT, anchor="w")
        if status == GameplayStatus.WIN:
            self.draw_centred_text(canvas, "MISSION ACCOMPLISHED!", width // 2, 320,
                                   ("Monospaced", 36, "bold"), ARC_LIME)
            canvas.create_text(80, 370, text="You Have Gathered Enough EXP to Return Home!",
                               font=("Monospaced", 20, "normal"), fill=ARC_TEXT, anchor="w")
            canvas.create_text(80, 400, text="Congratulations, " + player.get_name() + "!",
                               font=("Monospaced", 20, "normal"), fill=ARC_TEXT, anchor="w")
            self.draw_centred_text(canvas, "Press ENTER to Continue or ESC to Quit", width // 2, 460,
                                   ("Monospaced", 14, "normal"), ARC_DIM)
        elif status == GameplayStatus.DEAD:
            self.draw_centred_text(canvas, "YOU DIED", width // 2, 300, ("Monospaced", 36, "bold"), ARC_TEXT)
            canvas.create_text(80, 350, text="Your Journey Has Ended...",
                               font=("Monospaced", 20, "normal"), fill=ARC_TEXT, anchor="w")
            canvas.create_text(80, 385, text="Final EXP: " + str(player.get_exp()),
                               font=("Monospaced", 20, "normal"), fill=ARC_TEXT, anchor="w")
            self.draw_centred_text(canvas, "Press ESC to Return to Menu", width // 2, 450,
                                   ("Monospaced", 18, "bold"), ARC_DIM)
        elif status == GameplayStatus.BANKRUPT:
            self.draw_centred_text(canvas, "GAME OVER", width // 2, 300, ("Monospaced", 36, "bold"), ARC_TEXT)
            canvas.create_text(80, 350, text="Your EXP Was Completely Depleted!",
                               font=("Monospaced", 20, "normal"), fill=ARC_TEXT, anchor="w")
            canvas.create_text(80, 385, text="Final EXP: " + str(player.get_exp()),
                               font=("Monospaced", 20, "normal"), fill=ARC_TEXT, anchor="w")
            canvas.create_text(80, 420, text="The Void Has Claimed You...",
                               font=("Monospaced", 20, "normal"), fill=ARC_TEXT, anchor="w")
            self.draw_centred_text(canvas, "Press ESC to Return to Menu", width // 2, 470,
                                   ("Monospaced", 18, "bold"), ARC_DIM)
        else:
            canvas.create_text(80, 360, text="Navigate Doors to Gain Experience and Complete Your Mission!",
                               font=("Monospaced", 14, "normal"), fill=ARC_DIM, anchor="w")
            canvas.create_text(80, 400, text="Reward Doors Provide EXP, Penalty Doors Drain EXP,",
                               font=("Monospaced", 14, "normal"), fill=ARC_DIM, anchor="w")
            canvas.create_text(80, 430, text="and Minigame Doors Offer Challenging Opportunities.",
                               font=("Monospaced", 14, "normal"), fill=ARC_DIM, anchor="w")
            self.draw_centred_text(canvas, "Press Any Key to Enter the Next Round   |   ESC to Go Back to Menu",
                                   width // 2, 500, ("Monospaced", 16, "normal"), ARC_NEON)

