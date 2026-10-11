"""
Name entry: printable-ASCII buffer plus the input box view.

Translation of ``NameEntryScreen.java``. Names hold 1 to 15 printable
ASCII characters (space to tilde); every accepted keystroke and every
backspace plays the typewriter sound, ENTER confirms a non-empty name
and ESC returns to the main menu.
"""

import tkinter as tk

import sound_manager
from base_screen import (
    ARC_DIM,
    ARC_LIME,
    ARC_NEON,
    ARC_TEXT,
    BaseGameScreen,
    SMALL_FONT,
    SUBTITLE_FONT,
    TITLE_FONT,
)


MAX_NAME_LENGTH = 15


def is_valid_character(char):
    """
    True for printable ASCII from space to tilde, as the Java checks.
    """
    return " " <= char <= "~"


class NameBuffer:
    """
    The name being typed, without any widgets.
    """

    def __init__(self):
        self.text = ""

    def type_character(self, char):
        """
        Append a valid character, sounding the typewriter key.

        Returns True when the character was accepted.
        """
        if is_valid_character(char) and len(self.text) < MAX_NAME_LENGTH:
            self.text += char
            sound_manager.play_once(sound_manager.TYPEWRITER)
            return True
        return False

    def backspace(self):
        """
        Drop the last character with a typewriter sound, if any.
        """
        if not self.text:
            return False
        self.text = self.text[:-1]
        sound_manager.play_once(sound_manager.TYPEWRITER)
        return True


class NameEntryScreen(BaseGameScreen):
    """
    The ENTER YOUR NAME box with a blinking-underscore cursor.
    """

    def __init__(self, gui, controller):
        super().__init__(gui, controller)
        self.buffer = NameBuffer()
        self.canvas_widget = self.canvas()
        self.bind("<KeyPress>", self._on_key_press)
        self.bind("<Key>", self._on_key_type)
        self.bind("<Configure>", lambda _e: self.redraw())

    def _on_key_press(self, event):
        if event.keysym == "Escape":
            sound_manager.play_once(sound_manager.MENU_NAVIGATE)
            self.controller.go_back_to_main_menu()
        elif event.keysym == "BackSpace":
            if self.buffer.backspace():
                self.redraw()
        elif event.keysym == "Return" and self.buffer.text:
            sound_manager.play_once(sound_manager.MENU_SELECT)
            self.controller.set_player_name(self.buffer.text)

    def _on_key_type(self, event):
        if event.char and self.buffer.type_character(event.char):
            self.redraw()

    def redraw(self):
        """
        Paint the title, prompt and the current input box.
        """
        canvas = self.canvas_widget
        canvas.delete("all")
        width = max(canvas.winfo_width(), 900)
        height = max(canvas.winfo_height(), 650)
        self.draw_centred_text(canvas, "SPACE MISSION", width // 2, 120, TITLE_FONT, ARC_LIME)
        self.draw_centred_text(canvas, "ENTER YOUR NAME", width // 2, 250, SUBTITLE_FONT, ARC_NEON)
        box_x, box_y, box_w, box_h = 150, 280, width - 300, 120
        self.draw_border(canvas, box_x, box_y, box_w, box_h, 3)
        canvas.create_text(box_x + 40, box_y + 75, text=self.buffer.text + "_",
                           font=("Monospaced", 28, "normal"), fill=ARC_TEXT, anchor="w")
        self.draw_text(canvas, "Max " + str(MAX_NAME_LENGTH) + " Characters   |   ENTER to Confirm",
                       60, height - 100, SMALL_FONT, ARC_DIM)
        self.draw_text(canvas, "Press ESC to Return to the Main Menu", 60, height - 70, SMALL_FONT, ARC_DIM)

