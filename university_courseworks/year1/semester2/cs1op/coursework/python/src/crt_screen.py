"""
Full-screen CRT display settings page.

This screen has no Java counterpart file: ``GameController`` builds a
``CRTScreen`` that does not exist in the Java sources, so the Java tree
does not compile as committed. The Python translation implements the
clearly intended screen instead of reproducing the break, reusing the
pause-menu CRT semantics: an on/off toggle and a 0-100 intensity slider
with the 0-33 / 34-66 / 67-100 band legend. ESC returns to options.
"""

import tkinter as tk

import crt_settings
import sound_manager
from base_screen import (
    ARC_DIM,
    ARC_LIME,
    ARC_NEON,
    ARC_PANEL,
    ARC_TEXT,
    BaseGameScreen,
    HINT_FONT,
)


class CrtState:
    """
    The CRT toggle and intensity choice, without any widgets.
    """

    def __init__(self):
        self.focus_intensity = False

    def toggle_on(self):
        """
        Switch the overlay on with a navigate sound.
        """
        crt_settings.set_enabled(True)
        sound_manager.play_once(sound_manager.MENU_NAVIGATE)

    def toggle_off(self):
        """
        Switch the overlay off with a navigate sound.
        """
        crt_settings.set_enabled(False)
        sound_manager.play_once(sound_manager.MENU_NAVIGATE)

    def set_intensity_from_mouse(self, slider_rect, mouse_x):
        """
        The 0-100 intensity for a slider drag at mouse_x.
        """
        x, _y, width, _h = slider_rect
        crt_settings.set_intensity(int(100.0 * (mouse_x - x) / width))

    def confirm(self, controller):
        """
        Leave the page: ENTER on the toggle flips it, else back.
        """
        if self.focus_intensity:
            if crt_settings.is_enabled():
                self.toggle_off()
            else:
                self.toggle_on()
        else:
            sound_manager.play_once(sound_manager.MENU_SELECT)
            controller.show_options()


class CrtScreen(BaseGameScreen):
    """
    The CRT_SCREEN page the controller navigates to from options.
    """

    def __init__(self, gui, controller):
        super().__init__(gui, controller)
        self.state = CrtState()
        self.on_rect = None
        self.off_rect = None
        self.slider_rect = None
        self.canvas_widget = self.canvas()
        self.bind("<KeyPress>", self._on_key)
        self.canvas_widget.bind("<ButtonPress-1>", self._on_press)
        self.canvas_widget.bind("<B1-Motion>", self._on_drag)
        self.bind("<Configure>", lambda _e: self.redraw())

    def _on_key(self, event):
        key = event.keysym
        if key == "Escape":
            sound_manager.play_once(sound_manager.MENU_NAVIGATE)
            self.controller.show_options()
        elif key in ("Up", "w", "W", "Down", "s", "S"):
            self.state.focus_intensity = not self.state.focus_intensity
            sound_manager.play_once(sound_manager.MENU_NAVIGATE)
            self.redraw()
        elif key in ("Left", "a", "A"):
            if self.state.focus_intensity:
                crt_settings.set_intensity(crt_settings.get_intensity() - 1)
            else:
                self.state.toggle_off()
            self.redraw()
        elif key in ("Right", "d", "D"):
            if self.state.focus_intensity:
                crt_settings.set_intensity(crt_settings.get_intensity() + 1)
            else:
                self.state.toggle_on()
            self.redraw()
        elif key == "Return":
            self.state.confirm(self.controller)
            self.redraw()

    def _on_press(self, event):
        if self.on_rect and self._inside(event, self.on_rect):
            self.state.toggle_on()
            self.redraw()
        elif self.off_rect and self._inside(event, self.off_rect):
            self.state.toggle_off()
            self.redraw()
        elif self.slider_rect and self._inside(event, self.slider_rect):
            self.state.set_intensity_from_mouse(self.slider_rect, event.x)
            self.redraw()

    def _on_drag(self, event):
        if self.slider_rect is not None:
            self.state.set_intensity_from_mouse(self.slider_rect, event.x)
            self.redraw()

    @staticmethod
    def _inside(event, rect):
        x, y, w, h = rect
        return x <= event.x <= x + w and y <= event.y <= y + h

    def redraw(self):
        """
        Paint the toggle, the intensity slider and the band legend.
        """
        canvas = self.canvas_widget
        canvas.delete("all")
        width = max(canvas.winfo_width(), 900)
        height = max(canvas.winfo_height(), 650)
        self.draw_border(canvas, 50, 50, width - 100, height - 100, 3)
        self.draw_centred_text(canvas, "CRT DISPLAY", width // 2, 130, ("Monospaced", 46, "bold"), ARC_LIME)
        enabled = crt_settings.is_enabled()
        x, y = width // 2 - 120, 220
        self.on_rect = (x, y, 100, 40)
        self.off_rect = (x + 130, y, 100, 40)
        canvas.create_text(x - 20, y + 20, text="Effect:", font=("Monospaced", 18, "bold"),
                           fill=ARC_TEXT, anchor="e")
        canvas.create_rectangle(x, y, x + 100, y + 40,
                                fill=ARC_TEXT if enabled else ARC_PANEL, outline=ARC_NEON)
        canvas.create_text(x + 50, y + 20, text="ON", font=("Monospaced", 14, "bold"),
                           fill="#000000" if enabled else ARC_DIM)
        canvas.create_rectangle(x + 130, y, x + 230, y + 40,
                                fill=ARC_PANEL if enabled else ARC_TEXT, outline=ARC_NEON)
        canvas.create_text(x + 180, y + 20, text="OFF", font=("Monospaced", 14, "bold"),
                           fill=ARC_DIM if enabled else ARC_LIME)
        bar_x, bar_y, bar_w, bar_h = width // 2 - 150, 300, 300, 16
        self.slider_rect = (bar_x, bar_y, bar_w, bar_h)
        fill = crt_settings.get_intensity() / 100.0
        canvas.create_text(bar_x - 20, bar_y + 8, text="Intensity:", font=("Monospaced", 18, "bold"),
                           fill=ARC_TEXT if enabled else ARC_DIM, anchor="e")
        canvas.create_rectangle(bar_x, bar_y, bar_x + bar_w, bar_y + bar_h, fill=ARC_PANEL, outline=ARC_NEON)
        canvas.create_rectangle(bar_x, bar_y, bar_x + int(bar_w * fill), bar_y + bar_h,
                                fill=ARC_TEXT if enabled else ARC_PANEL, outline="")
        canvas.create_text(bar_x + bar_w + 12, bar_y + 8, text=str(crt_settings.get_intensity()) + "%",
                           font=("Monospaced", 13, "bold"), fill=ARC_NEON, anchor="w")
        self.draw_centred_text(canvas, "0-33: Scanlines Only   34-66: Plus Vignette   67-100: Plus Flicker",
                               width // 2, 360, HINT_FONT, ARC_DIM)
        self.draw_centred_text(canvas, "Up/Down to move   Left/Right to adjust   ENTER to confirm   ESC for Options",
                               width // 2, height - 80, HINT_FONT, ARC_DIM)

