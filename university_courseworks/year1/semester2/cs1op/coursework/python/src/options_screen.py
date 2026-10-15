"""
Options: difficulty, display settings and sound settings.

Translation of ``OptionsScreen.java``. Moving left on difficulty cycles
twice forward, which is one step back over the three states; ENTER cycles
difficulty and navigates to the two dedicated settings pages. Hover
follows the Java rows from y=230 spaced 95 apart, 28 pixels either side.

Two rows here are navigation, not inline settings. DISPLAY opens the
full-screen CRT page, and SOUND opens the per-sound volume page - both
already exist and are reachable from the main menu as well. An earlier
version of this screen carried inline SOUND and VOLUME rows whose values
lived only in ``OptionsState`` and were read by nothing: the sound state
lives in ``sound_settings`` and the volumes live beside it, so the rows
reported a setting the game never consulted. They are replaced by links to
the pages that hold the real state.
"""

import tkinter as tk

import crt_settings
import game_settings
import sound_manager
from base_screen import (
    ARC_DIM,
    ARC_NEON,
    ARC_TEXT,
    BaseGameScreen,
    DARK_GREEN,
    HINT_FONT,
)


OPT_DIFFICULTY = 0
OPT_DISPLAY = 1
OPT_SOUND = 2
OPT_BACK = 3

FIRST_ROW_Y = 230
ROW_SPACING = 95
ROW_HALF_HEIGHT = 28


class OptionsState:
    """
    The selected option, without any widgets.
    """

    def __init__(self):
        self.selected = 0
        self.hovered = -1

    def option_texts(self):
        """
        The four labelled rows for the current settings.

        The CRT row echoes the live overlay state so the setting can be
        checked before starting, without opening the display page.
        """
        return (
            "DIFFICULTY: " + game_settings.difficulty_label(),
            "DISPLAY (CRT: " + ("ON" if crt_settings.is_enabled() else "OFF") + ")",
            "SOUND SETTINGS",
            "BACK TO MAIN MENU",
        )

    def move_selection(self, delta):
        """
        Wrap the selection by delta with a navigate sound.
        """
        self.selected = (self.selected + delta) % 4
        sound_manager.play_once(sound_manager.MENU_NAVIGATE)

    def hover_at(self, mouse_y):
        """
        Update the hovered row, sounding only on a changed option.
        """
        previous = self.hovered
        self.hovered = -1
        row_y = FIRST_ROW_Y
        for i in range(4):
            if row_y - ROW_HALF_HEIGHT <= mouse_y <= row_y + ROW_HALF_HEIGHT:
                self.hovered = i
                break
            row_y += ROW_SPACING
        if self.hovered != previous and self.hovered >= 0:
            sound_manager.play_once(sound_manager.MENU_NAVIGATE)

    def adjust_left(self):
        """
        Step the selected setting down: difficulty back one of three.
        """
        if self.selected == OPT_DIFFICULTY:
            game_settings.cycle_difficulty()
            game_settings.cycle_difficulty()

    def adjust_right(self):
        """
        Step the selected setting up: difficulty on one of three.
        """
        if self.selected == OPT_DIFFICULTY:
            game_settings.cycle_difficulty()

    def confirm(self, controller):
        """
        Activate the selected row: cycle, navigate, or go back.
        """
        if self.selected == OPT_DIFFICULTY:
            game_settings.cycle_difficulty()
        elif self.selected == OPT_DISPLAY:
            controller.show_crt_screen()
        elif self.selected == OPT_SOUND:
            controller.show_sound_screen()
        elif self.selected == OPT_BACK:
            controller.go_back_to_main_menu()


class OptionsScreen(BaseGameScreen):
    """
    The OPTIONS page with its volume slider and hints.
    """

    def __init__(self, gui, controller):
        super().__init__(gui, controller)
        self.state = OptionsState()
        self.canvas_widget = self.canvas()
        self.bind("<KeyPress>", self._on_key)
        self.canvas_widget.bind("<Motion>", self._on_motion)
        self.canvas_widget.bind("<Button-1>", self._on_click)
        self.bind("<Configure>", lambda _e: self.redraw())

    def _on_key(self, event):
        key = event.keysym
        if key in ("Up", "w", "W"):
            self.state.move_selection(-1)
        elif key in ("Down", "s", "S"):
            self.state.move_selection(1)
        elif key in ("Left", "a", "A"):
            self.state.adjust_left()
            sound_manager.play_once(sound_manager.MENU_NAVIGATE)
        elif key in ("Right", "d", "D"):
            self.state.adjust_right()
            sound_manager.play_once(sound_manager.MENU_NAVIGATE)
        elif key == "Return":
            sound_manager.play_once(sound_manager.MENU_SELECT)
            self.state.confirm(self.controller)
        elif key == "Escape":
            sound_manager.play_once(sound_manager.MENU_NAVIGATE)
            self.controller.go_back_to_main_menu()
        else:
            return
        self.redraw()

    def _on_motion(self, event):
        self.state.hover_at(event.y)
        self.redraw()

    def _on_click(self, _event):
        if self.state.hovered >= 0:
            self.state.selected = self.state.hovered
            sound_manager.play_once(sound_manager.MENU_SELECT)
            self.state.confirm(self.controller)
            self.redraw()

    def redraw(self):
        """
        Paint the title and the four setting rows.
        """
        canvas = self.canvas_widget
        canvas.delete("all")
        width = max(canvas.winfo_width(), 900)
        height = max(canvas.winfo_height(), 650)
        canvas.create_rectangle(50, 50, width - 100, height - 100, outline=ARC_NEON, width=3)
        self.draw_centred_text(canvas, "OPTIONS", width // 2, 130, ("Monospaced", 46, "bold"))
        texts = self.state.option_texts()
        row_y = FIRST_ROW_Y
        for i, text in enumerate(texts):
            if i == self.state.selected or i == self.state.hovered:
                canvas.create_rectangle(width // 2 - 220, row_y - 28, width // 2 + 220, row_y + 28,
                                        fill=DARK_GREEN, outline="")
            fill = ARC_NEON
            self.draw_centred_text(canvas, text, width // 2, row_y, ("Monospaced", 22, "bold"), fill)
            row_y += ROW_SPACING
        self.draw_centred_text(canvas, "Use Up/Down or WASD to move, Left/Right or A/D to change difficulty",
                               width // 2, height - 120, HINT_FONT, ARC_TEXT)
        self.draw_centred_text(canvas, "ENTER opens DISPLAY or SOUND, ESC returns to the main menu",
                               width // 2, height - 92, HINT_FONT, ARC_TEXT)
        self.draw_centred_text(canvas, "Difficulty affects Pong AI and Space Invaders speed / shooting",
                               width // 2, height - 64, HINT_FONT, ARC_TEXT)

