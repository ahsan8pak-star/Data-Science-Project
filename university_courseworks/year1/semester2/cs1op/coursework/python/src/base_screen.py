"""
Shared arcade styling for every game screen.

Translation of ``BaseGameScreen.java``. The six greens and the black
background become hex strings, and the Graphics2D helpers become canvas
helpers with the same geometry: bordered rectangles, centred text and
plain positioned text in the Monospaced family.
"""

import tkinter as tk
import tkinter.font as tkfont

import crt_settings


ARC_NEON = "#00ff41"
ARC_LIME = "#64ff3c"
ARC_TEXT = "#00d700"
ARC_DIM = "#009100"
ARC_PANEL = "#002d00"
ARC_GLOW = "#00c800"
ARC_BG = "#000000"

ACCENT_GREEN = ARC_NEON
BG_BLACK = ARC_BG
DARK_GREEN = ARC_PANEL

TITLE_FONT = ("Monospaced", 56, "bold")
SUBTITLE_FONT = ("Monospaced", 32, "bold")
OPTION_FONT = ("Monospaced", 28, "bold")
BODY_FONT = ("Monospaced", 18, "normal")
SMALL_FONT = ("Monospaced", 14, "normal")
HINT_FONT = ("Monospaced", 13, "normal")
TINY_FONT = ("Monospaced", 11, "normal")


class BaseGameScreen(tk.Frame):
    """
    A black arcade-styled frame holding a gui and controller reference.
    """

    def __init__(self, gui, controller):
        super().__init__(gui, bg=ARC_BG)
        self.gui = gui
        self.controller = controller

    def canvas(self):
        """
        A black canvas filling this screen for custom drawing.
        """
        widget = tk.Canvas(self, bg=ARC_BG, highlightthickness=0)
        widget.pack(fill=tk.BOTH, expand=True)
        return widget

    @staticmethod
    def draw_border(canvas, x, y, width, height, thickness=3):
        """
        A neon rectangle border of the given thickness.
        """
        canvas.create_rectangle(x, y, x + width, y + height, outline=ARC_NEON, width=thickness)

    @staticmethod
    def centred_x(canvas, text, centre_x, font):
        """
        The x origin that centres text of the given font on centre_x.
        """
        measure = tkfont.Font(font=font).measure(text)
        return centre_x - measure // 2

    @staticmethod
    def draw_centred_text(canvas, text, centre_x, y, font, fill=ARC_NEON):
        """
        Draw text centred horizontally on centre_x.
        """
        canvas.create_text(centre_x, y, text=text, font=font, fill=fill)

    @staticmethod
    def draw_text(canvas, text, x, y, font, fill=ARC_NEON):
        """
        Draw text at an exact position.
        """
        canvas.create_text(x, y, text=text, font=font, fill=fill, anchor="nw")

    @staticmethod
    def draw_crt_overlay(canvas, width, height):
        """
        Scanline pass of the CRT overlay when enabled.

        The Java gradient vignette and flicker have no canvas equivalent
        without per-pixel alpha, so only the scanline layer translates;
        thresholds and intensity still follow ``crt_settings``.
        """
        if not crt_settings.is_enabled() or crt_settings.get_intensity() <= 0:
            return
        for y in range(0, height, 2):
            canvas.create_line(0, y, width, y, fill="#000000")

