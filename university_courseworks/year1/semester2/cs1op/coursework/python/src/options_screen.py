"""
Options: difficulty, sound toggle and volume state plus its view.

Translation of ``OptionsScreen.java``. Moving left on difficulty cycles
twice forward, which is one step back over the three states; volume
moves one unit per press clamped to 0-100; ENTER toggles difficulty and
sound but leaves volume to the arrow keys. Hover follows the Java rows
from y=230 spaced 95 apart, 28 pixels either side.
"""

import tkinter as tk

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
OPT_SOUND = 1
OPT_VOLUME = 2
OPT_BACK = 3

FIRST_ROW_Y = 230
ROW_SPACING = 95
ROW_HALF_HEIGHT = 28


class OptionsState:
    """
    The selected option, sound flag and volume, without any widgets.
    """

    def __init__(self):
        self.selected = 0
        self.hovered = -1
        self.sound_enabled = True
        self.volume = 50

    def option_texts(self):
        """
        The four labelled rows for the current settings.
        """
        return (
            "DIFFICULTY: " + game_settings.difficulty_label(),
            "SOUND: " + ("ON" if self.sound_enabled else "OFF"),
            "VOLUME: " + str(self.volume),
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
        Step the selected setting down: difficulty back, sound off, -1 vol.
        """
        if self.selected == OPT_DIFFICULTY:
            game_settings.cycle_difficulty()
            game_settings.cycle_difficulty()
        elif self.selected == OPT_SOUND:
            self.sound_enabled = not self.sound_enabled
        elif self.selected == OPT_VOLUME:
            self.volume = max(0, self.volume - 1)

    def adjust_right(self):
        """
        Step the selected setting up: difficulty on, sound on, +1 vol.
        """
        if self.selected == OPT_DIFFICULTY:
            game_settings.cycle_difficulty()
        elif self.selected == OPT_SOUND:
            self.sound_enabled = not self.sound_enabled
        elif self.selected == OPT_VOLUME:
            self.volume = min(100, self.volume + 1)

    def confirm(self, controller):
        """
        Activate the selected row: cycle, toggle, or go back.
        """
        if self.selected == OPT_DIFFICULTY:
            game_settings.cycle_difficulty()
        elif self.selected == OPT_SOUND:
            self.sound_enabled = not self.sound_enabled
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
        Paint the title, the four rows and the volume slider.
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
            if i == OPT_VOLUME:
                bar_w, bar_h = 300, 12
                bar_x, bar_y = width // 2 - bar_w // 2, row_y + 22
                canvas.create_rectangle(bar_x, bar_y, bar_x + bar_w, bar_y + bar_h, fill="#1e1e1e", outline="")
                canvas.create_rectangle(bar_x, bar_y, bar_x + int(self.state.volume / 100.0 * bar_w),
                                        bar_y + bar_h, fill=ARC_NEON, outline="")
                canvas.create_rectangle(bar_x, bar_y, bar_x + bar_w, bar_y + bar_h, outline="#00ff00")
            row_y += ROW_SPACING
        self.draw_centred_text(canvas, "Use Up/Down or WASD to move, Left/Right or A/D to adjust volume (1 unit)",
                               width // 2, height - 120, HINT_FONT, ARC_TEXT)
        self.draw_centred_text(canvas, "ENTER to toggle SOUND, ESC to go back, Mouse click to select",
                               width // 2, height - 92, HINT_FONT, ARC_TEXT)
        self.draw_centred_text(canvas, "Difficulty affects Pong AI and Space Invaders speed / shooting",
                               width // 2, height - 64, HINT_FONT, ARC_TEXT)

