"""
Sound settings: category tabs and per-sound sliders plus its view.

Translation of ``SoundScreen.java``. Category order and membership match
the Java exactly: Navigation (3), Dialogue (3), Doors (7), Player (3),
Pong (6), Invaders (12). Mouse geometry follows the Java hit boxes:
tabs at y=80 height 36 from x=20, sliders in rows below.
"""

import tkinter as tk

import sound_manager
import sound_settings
from base_screen import (
    ARC_DIM,
    ARC_NEON,
    ARC_TEXT,
    BaseGameScreen,
    HINT_FONT,
)


GREEN_BRIGHT = "#00ff00"
GREEN_MID = "#00c800"
GREEN_DIM = "#008000"
GREEN_DARK = "#002800"

CATEGORIES = ("Navigation", "Dialogue", "Doors", "Player", "Pong", "Invaders")

CATEGORY_FILES = (
    (sound_manager.MENU_NAVIGATE, sound_manager.MENU_SELECT, sound_manager.TYPEWRITER),
    (sound_manager.DIALOGUE_YES, sound_manager.DIALOGUE_NO, sound_manager.HORROR_LOOP),
    (sound_manager.DOOR_NAVIGATE, sound_manager.DOOR_OPEN, sound_manager.DOOR_CLOSE,
     sound_manager.CHEST_SHINE, sound_manager.REWARD_POINTS, sound_manager.POISON_SMOKE,
     sound_manager.PENALTY_POINTS),
    (sound_manager.LIFE_LOST, sound_manager.GAME_OVER_SOUND, sound_manager.GAME_WIN_SOUND),
    (sound_manager.PONG_PLAYER_HIT, sound_manager.PONG_CPU_HIT, sound_manager.PONG_PLAYER_POINT,
     sound_manager.PONG_CPU_POINT, sound_manager.PONG_WIN, sound_manager.PONG_LOSE),
    (sound_manager.SI_PLAYER_SHOOT, sound_manager.SI_MINI_LIFE_LOST, sound_manager.SI_UFO_FLY,
     sound_manager.SI_UFO_SHOOT, sound_manager.SI_UFO_DIE, sound_manager.SI_SPACECRAFT_SHOOT,
     sound_manager.SI_SPACECRAFT_DIE, sound_manager.SI_ALIEN_SHOOT, sound_manager.SI_ALIEN_DIE,
     sound_manager.SI_NEXT_WAVE, sound_manager.SI_WIN, sound_manager.SI_LOSE),
)

TAB_Y = 80
TAB_H = 36
TAB_X0 = 20


class SoundScreenState:
    """
    The active category tab and the slider being dragged, widget-free.
    """

    def __init__(self):
        self.selected_category = 0
        self.dragging_slider = None
        self.slider_rects = {}

    def previous_category(self):
        """
        Move one tab left, floored at the first.
        """
        self.selected_category = max(0, self.selected_category - 1)
        sound_manager.play_once(sound_manager.MENU_NAVIGATE)

    def next_category(self):
        """
        Move one tab right, capped at the last.
        """
        self.selected_category = min(len(CATEGORIES) - 1, self.selected_category + 1)
        sound_manager.play_once(sound_manager.MENU_NAVIGATE)

    def files(self):
        """
        The sound files of the active category.
        """
        return CATEGORY_FILES[self.selected_category]

    def tab_at(self, x, width):
        """
        The tab index under mouse x, or -1 when between tabs.
        """
        tab_w = (width - 40) // len(CATEGORIES)
        for i in range(len(CATEGORIES)):
            if TAB_X0 + i * tab_w <= x <= TAB_X0 + (i + 1) * tab_w:
                return i
        return -1

    def volume_from_mouse(self, sound_file, rect, mouse_x):
        """
        The 0-100 volume for a slider drag at mouse_x.
        """
        x, _y, width, _h = rect
        return int(100.0 * (mouse_x - x) / width)


class SoundScreen(BaseGameScreen):
    """
    The SOUND SETTINGS page with tabs and draggable volume sliders.
    """

    def __init__(self, gui, controller):
        super().__init__(gui, controller)
        self.state = SoundScreenState()
        self.canvas_widget = self.canvas()
        self.bind("<KeyPress>", self._on_key)
        self.canvas_widget.bind("<ButtonPress-1>", self._on_press)
        self.canvas_widget.bind("<B1-Motion>", self._on_drag)
        self.canvas_widget.bind("<ButtonRelease-1>", lambda _e: setattr(self.state, "dragging_slider", None))
        self.bind("<Configure>", lambda _e: self.redraw())

    def _on_key(self, event):
        key = event.keysym
        if key == "Escape":
            sound_manager.play_once(sound_manager.MENU_NAVIGATE)
            self.controller.go_back_to_main_menu()
        elif key in ("Left", "a", "A"):
            self.state.previous_category()
            self.redraw()
        elif key in ("Right", "d", "D"):
            self.state.next_category()
            self.redraw()

    def _on_press(self, event):
        width = max(self.canvas_widget.winfo_width(), 900)
        tab = self.state.tab_at(event.x, width)
        if tab >= 0:
            self.state.selected_category = tab
            sound_manager.play_once(sound_manager.MENU_NAVIGATE)
            self.redraw()
            return
        for sound_file, rect in self.state.slider_rects.items():
            x, y, w, h = rect
            if x <= event.x <= x + w and y <= event.y <= y + h:
                self.state.dragging_slider = sound_file
                sound_settings.set_volume(sound_file, self.state.volume_from_mouse(sound_file, rect, event.x))
                self.redraw()
                return

    def _on_drag(self, event):
        dragging = self.state.dragging_slider
        if dragging is None:
            return
        rect = self.state.slider_rects.get(dragging)
        if rect is None:
            return
        sound_settings.set_volume(dragging, self.state.volume_from_mouse(dragging, rect, event.x))
        self.redraw()

    def redraw(self):
        """
        Paint the tabs and the active category's sliders.
        """
        canvas = self.canvas_widget
        canvas.delete("all")
        width = max(canvas.winfo_width(), 900)
        height = max(canvas.winfo_height(), 650)
        self.draw_border(canvas, 20, 20, width - 40, height - 40, 2)
        self.draw_centred_text(canvas, "SOUND SETTINGS", width // 2, 65, ("Monospaced", 32, "bold"), GREEN_BRIGHT)
        tab_w = (width - 40) // len(CATEGORIES)
        for i, label in enumerate(CATEGORIES):
            tx = TAB_X0 + i * tab_w
            selected = i == self.state.selected_category
            canvas.create_rectangle(tx, TAB_Y, tx + tab_w, TAB_Y + TAB_H,
                                    fill=GREEN_DIM if selected else GREEN_DARK, outline=GREEN_BRIGHT)
            fill = GREEN_BRIGHT if selected else GREEN_MID
            canvas.create_text(tx + tab_w // 2, TAB_Y + 23, text=label,
                               font=("Monospaced", 13, "bold"), fill=fill)
        self.state.slider_rects = {}
        files = self.state.files()
        label_x = 35
        slider_x = width // 3
        slider_w = int(width * 0.45)
        vol_x = slider_x + slider_w + 12
        row_h = min(42, (height - 160) // max(1, len(files)))
        y = 135
        for sound_file in files:
            name = sound_settings.get_display_name(sound_file)
            vol = sound_settings.get_volume(sound_file)
            canvas.create_text(label_x, y + row_h // 2 + 5, text=name,
                               font=("Monospaced", 14, "bold"), fill=GREEN_BRIGHT, anchor="w")
            rect = (slider_x, y + row_h // 2 - 9, slider_w, 18)
            self.state.slider_rects[sound_file] = rect
            canvas.create_rectangle(slider_x, rect[1], slider_x + slider_w, rect[1] + 18,
                                    fill="#001400", outline="")
            canvas.create_rectangle(slider_x, rect[1], slider_x + int(slider_w * vol / 100.0),
                                    rect[1] + 18, fill=GREEN_MID, outline="")
            canvas.create_rectangle(slider_x, rect[1], slider_x + slider_w, rect[1] + 18, outline=GREEN_BRIGHT)
            thumb_x = slider_x + int(slider_w * vol / 100.0) - 4
            canvas.create_rectangle(thumb_x, rect[1] - 3, thumb_x + 8, rect[1] + 21, fill=GREEN_BRIGHT, outline="")
            canvas.create_text(vol_x, y + row_h // 2 + 5, text=str(vol) + "%",
                               font=("Monospaced", 13, "normal"), fill=GREEN_MID, anchor="w")
            y += row_h
        self.draw_centred_text(canvas, "A / D or Left / Right to Switch Tab   |   Drag Sliders to Adjust Volume   |   ESC to Go Back",
                               width // 2, height - 28, HINT_FONT, GREEN_DIM)

