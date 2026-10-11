"""
Main menu: selection state plus the arcade title view.

Translation of ``MainMenuScreen.java``. Navigation wraps around the four
options; mouse hover follows the Java hit boxes (rows from y=330 spaced
85 apart, 25 pixels either side). Sounds fire on move, hover change and
confirm exactly as the Java does.
"""

import tkinter as tk

import sound_manager
from base_screen import (
    ARC_DIM,
    ARC_GLOW,
    ARC_LIME,
    ARC_NEON,
    ARC_TEXT,
    BaseGameScreen,
    HINT_FONT,
    OPTION_FONT,
    SMALL_FONT,
    TITLE_FONT,
)


OPTIONS = ("START GAME", "SOUND", "OPTIONS", "QUIT")
FIRST_ROW_Y = 330
ROW_SPACING = 85
ROW_HALF_HEIGHT = 25


class MainMenuState:
    """
    The selected and hovered option, without any widgets.
    """

    def __init__(self):
        self.selected = 0
        self.hovered = -1

    def move_up(self):
        """
        Wrap one option upwards with a navigate sound.
        """
        self.selected = (self.selected - 1) % len(OPTIONS)
        sound_manager.play_once(sound_manager.MENU_NAVIGATE)

    def move_down(self):
        """
        Wrap one option downwards with a navigate sound.
        """
        self.selected = (self.selected + 1) % len(OPTIONS)
        sound_manager.play_once(sound_manager.MENU_NAVIGATE)

    def hover_at(self, mouse_y):
        """
        Update the hovered row from a mouse y position.

        Returns True when the hover changed onto a real option.
        """
        previous = self.hovered
        self.hovered = -1
        row_y = FIRST_ROW_Y
        for i in range(len(OPTIONS)):
            if row_y - ROW_HALF_HEIGHT <= mouse_y <= row_y + ROW_HALF_HEIGHT:
                self.hovered = i
                break
            row_y += ROW_SPACING
        if self.hovered != previous and self.hovered >= 0:
            sound_manager.play_once(sound_manager.MENU_NAVIGATE)
            return True
        return False

    def confirm(self, controller):
        """
        Run the selected option: start, sound, options, or quit.
        """
        sound_manager.play_once(sound_manager.MENU_SELECT)
        if self.selected == 0:
            controller.start_game()
        elif self.selected == 1:
            controller.show_sound_screen()
        elif self.selected == 2:
            controller.show_options()
        else:
            sound_manager.stop_all()
            raise SystemExit(0)


class MainMenuScreen(BaseGameScreen):
    """
    The SPACE MISSION title screen with keyboard and mouse navigation.
    """

    def __init__(self, gui, controller):
        super().__init__(gui, controller)
        self.state = MainMenuState()
        self.canvas_widget = self.canvas()
        self.bind("<KeyPress>", self._on_key)
        self.canvas_widget.bind("<Motion>", self._on_motion)
        self.canvas_widget.bind("<Button-1>", self._on_click)
        self.bind("<Configure>", lambda _e: self.redraw())

    def _on_key(self, event):
        if event.keysym in ("Up", "w", "W"):
            self.state.move_up()
            self.redraw()
        elif event.keysym in ("Down", "s", "S"):
            self.state.move_down()
            self.redraw()
        elif event.keysym == "Return":
            self.state.confirm(self.controller)

    def _on_motion(self, event):
        self.state.hover_at(event.y)
        self.redraw()

    def _on_click(self, _event):
        if self.state.hovered >= 0:
            self.state.selected = self.state.hovered
            self.state.confirm(self.controller)

    def redraw(self):
        """
        Paint the title, subtitle and the four options.
        """
        canvas = self.canvas_widget
        canvas.delete("all")
        width = max(canvas.winfo_width(), 900)
        height = max(canvas.winfo_height(), 650)
        canvas.create_rectangle(50, 50, width - 50, height - 50, outline=ARC_NEON, width=3)
        self.draw_centred_text(canvas, "SPACE MISSION", width // 2, 150, TITLE_FONT, ARC_LIME)
        self.draw_centred_text(canvas, "INSERT COIN TO CONTINUE", width // 2, 185, SMALL_FONT, ARC_DIM)
        row_y = FIRST_ROW_Y
        for i, option in enumerate(OPTIONS):
            if i == self.state.selected or i == self.state.hovered:
                canvas.create_rectangle(width // 2 - 190, row_y - 26, width // 2 + 190, row_y + 26,
                                        fill=ARC_GLOW, outline=ARC_NEON)
                self.draw_centred_text(canvas, option, width // 2, row_y, OPTION_FONT, ARC_LIME)
            else:
                self.draw_centred_text(canvas, option, width // 2, row_y, OPTION_FONT, ARC_TEXT)
            row_y += ROW_SPACING
        self.draw_text(canvas, "Up/Down  WASD  Mouse to Navigate   |   ENTER or Click to Select",
                       60, height - 60, HINT_FONT, ARC_DIM)

