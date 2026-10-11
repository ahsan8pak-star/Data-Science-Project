"""
Pong view: canvas rendering and input over the PongState match.

Translation of the presentation half of ``PongMinigame.java``. The
frame loop runs on a tkinter timer instead of the Java thread, and the
serve pause resumes through the same timer. The pause overlay carries
the CRT/display and sound-volume tabs with the Java geometry.
"""

import tkinter as tk

import crt_settings
import sound_manager
import sound_settings
from base_screen import (
    ARC_DIM,
    ARC_GLOW,
    ARC_LIME,
    ARC_NEON,
    ARC_PANEL,
    ARC_TEXT,
    BaseGameScreen,
)
from game_settings import difficulty_label
from pong_game import (
    BS,
    GH,
    GW,
    LEFT_X,
    PH,
    PONG_WIN_EXP,
    PW,
    RIGHT_X,
    PongState,
)


class PongMinigameView(BaseGameScreen):
    """
    The playable Pong table with pause menu and end overlay.
    """

    def __init__(self, gui, controller):
        super().__init__(gui, controller)
        player = controller.get_current_player() if controller is not None else None
        if player is not None:
            self.state = PongState(player.get_name(), player.get_exp())
        else:
            self.state = PongState()
        self.paused_menu = False
        self.pause_tab = "MAIN"
        self.rects = {}
        self.crt_slider = None
        self._dragging = None
        self.canvas_widget = self.canvas()
        self.bind("<KeyPress>", self._on_key_press)
        self.bind("<KeyRelease>", self._on_key_release)
        self.canvas_widget.bind("<ButtonPress-1>", self._on_press)
        self.canvas_widget.bind("<B1-Motion>", self._on_drag)
        self.canvas_widget.bind("<ButtonRelease-1>", lambda _e: self._clear_drag())
        self.bind("<Configure>", lambda _e: self.redraw())
        self._schedule_tick()

    def _clear_drag(self):
        self._dragging = None

    def _schedule_tick(self):
        self.after(16, self._tick)

    def _tick(self):
        if self.state.active:
            if not self._is_paused() and not self.state.game_ended and not self.paused_menu:
                self.state.tick()
                if self.state.resume_due:
                    self.state.resume_due = False
                    self.after(750, self.state.unpause)
            self.redraw()
            self._schedule_tick()

    def _is_paused(self):
        return self.state.paused

    def toggle_pause(self):
        """
        Flip the match pause flag.
        """
        self.state.paused = not self.state.paused

    def _on_key_press(self, event):
        key = event.keysym
        if key in ("Up", "w", "W"):
            self.state.keys.add("up")
        elif key in ("Down", "s", "S"):
            self.state.keys.add("down")
        elif key in ("i", "I"):
            self.state.keys.add("i")
        elif key in ("k", "K"):
            self.state.keys.add("k")
        if self.state.game_ended:
            if key == "Return" and self.controller is not None:
                sound_manager.stop_sound(sound_manager.PONG_LOSE)
                sound_manager.stop_all()
                if self.state.player_won:
                    self.controller.on_minigame_won("PONG", PONG_WIN_EXP)
                else:
                    self.controller.on_minigame_lost()
            return
        if self.paused_menu:
            if key == "Escape":
                self.paused_menu = False
                self.redraw()
            return
        if key in ("p", "P"):
            self.toggle_pause()
        elif key == "Escape":
            self.paused_menu = True
            self.pause_tab = "MAIN"
            self.redraw()

    def _on_key_release(self, event):
        key = event.keysym
        if key in ("Up", "w", "W"):
            self.state.keys.discard("up")
        elif key in ("Down", "s", "S"):
            self.state.keys.discard("down")
        elif key in ("i", "I"):
            self.state.keys.discard("i")
        elif key in ("k", "K"):
            self.state.keys.discard("k")

    def _on_press(self, event):
        if not self.paused_menu:
            return
        point = (event.x, event.y)
        if self._hit("main_tab", point):
            self.pause_tab = "MAIN"
            self.redraw()
            return
        if self._hit("sound_tab", point):
            self.pause_tab = "SOUND"
            self.redraw()
            return
        if self._hit("resume", point):
            self.paused_menu = False
            self.redraw()
            return
        if self._hit("quit", point):
            self.state.active = False
            sound_manager.stop_sound(sound_manager.PONG_LOSE)
            if self.controller is not None:
                self.controller.show_screen("DOOR_SELECTION")
            return
        if self.pause_tab == "MAIN":
            if self._hit("crt_on", point):
                crt_settings.set_enabled(True)
                self.redraw()
                return
            if self._hit("crt_off", point):
                crt_settings.set_enabled(False)
                self.redraw()
                return
            if self.crt_slider and self._inside(point, self.crt_slider):
                self._dragging = "CRT"
                crt_settings.set_intensity(int(100.0 * (event.x - self.crt_slider[0]) / self.crt_slider[2]))
                self.redraw()
        else:
            for name, rect in self.rects.items():
                if name.startswith("CRT"):
                    continue
                if self._inside(point, rect):
                    self._dragging = name
                    sound_settings.set_volume(name, int(100.0 * (event.x - rect[0]) / rect[2]))
                    self.redraw()
                    break

    def _on_drag(self, event):
        if not self.paused_menu or self._dragging is None:
            return
        if self._dragging == "CRT" and self.crt_slider is not None:
            crt_settings.set_intensity(int(100.0 * (event.x - self.crt_slider[0]) / self.crt_slider[2]))
            self.redraw()
        else:
            rect = self.rects.get(self._dragging)
            if rect is not None:
                sound_settings.set_volume(self._dragging, int(100.0 * (event.x - rect[0]) / rect[2]))
                self.redraw()

    def _hit(self, name, point):
        rect = self.rects.get(name)
        return rect is not None and self._inside(point, rect)

    @staticmethod
    def _inside(point, rect):
        x, y, w, h = rect
        return x <= point[0] <= x + w and y <= point[1] <= y + h

    def stop_game(self):
        """
        Halt the loop and release the defeat loop, used on teardown.
        """
        self.state.active = False
        sound_manager.stop_sound(sound_manager.PONG_LOSE)

    def redraw(self):
        """
        Paint the table, scores, overlays and pause menu.
        """
        canvas = self.canvas_widget
        canvas.delete("all")
        pw = max(canvas.winfo_width(), 800)
        ph = max(canvas.winfo_height(), 600)
        sx, sy = pw / GW, ph / GH

        def located(v):
            return int(round(v * sx))

        def tall(v):
            return int(round(v * sy))

        canvas.create_line(pw // 2, 0, pw // 2, ph, fill=ARC_DIM, width=2, dash=(int(10 * sy), int(10 * sy)))
        canvas.create_rectangle(located(LEFT_X), tall(self.state.left_y),
                                located(LEFT_X + PW), tall(self.state.left_y + PH), fill=ARC_NEON, outline="")
        canvas.create_rectangle(located(RIGHT_X), tall(self.state.right_y),
                                located(RIGHT_X + PW), tall(self.state.right_y + PH), fill=ARC_NEON, outline="")
        canvas.create_oval(located(int(self.state.ball_x)), tall(int(self.state.ball_y)),
                           located(int(self.state.ball_x) + BS), tall(int(self.state.ball_y) + BS),
                           fill=ARC_NEON, outline="")
        scale = min(sx, sy)
        canvas.create_text(int(pw * 0.25), int(50 * sy), text=str(self.state.left_score),
                           font=("Monospaced", int(36 * scale), "bold"), fill=ARC_LIME)
        canvas.create_text(int(pw * 0.72), int(50 * sy), text=str(self.state.right_score),
                           font=("Monospaced", int(36 * scale), "bold"), fill=ARC_LIME)
        canvas.create_text(int(pw * 0.07), int(50 * sy), text=self.state.player_name.upper(),
                           font=("Monospaced", int(14 * scale), "normal"), fill=ARC_TEXT, anchor="w")
        canvas.create_text(int(pw * 0.60), int(50 * sy), text="CPU [" + difficulty_label() + "]",
                           font=("Monospaced", int(14 * scale), "normal"), fill=ARC_TEXT, anchor="w")
        target = "First to " + str(self.state.win_score)
        canvas.create_text(pw // 2, int(30 * sy), text=target,
                           font=("Monospaced", int(14 * scale), "normal"), fill=ARC_DIM)
        canvas.create_text(int(16 * sx), ph - int(10 * sy),
                           text="W / Up  S / Down: Paddle   I / K: Override CPU   P: Pause   ESC: Menu",
                           font=("Monospaced", max(8, int(11 * scale)), "normal"),
                           fill="#005000", anchor="w")
        self.draw_crt_overlay(canvas, pw, ph)
        if self.state.game_ended:
            canvas.create_rectangle(0, 0, pw, ph, fill="black", stipple="gray50", outline="")
            self.draw_centred_text(canvas, self.state.end_msg, pw // 2, ph // 2,
                                   ("Monospaced", int(50 * scale), "bold"),
                                   ARC_LIME if self.state.player_won else ARC_TEXT)
            self.draw_centred_text(canvas, "Press ENTER to Continue", pw // 2, ph // 2 + int(65 * sy),
                                   ("Monospaced", int(20 * scale), "normal"))
        elif self.paused_menu:
            self._draw_pause_menu(canvas, pw, ph)

    def _draw_pause_menu(self, canvas, pw, ph):
        canvas.create_rectangle(0, 0, pw, ph, fill="black", stipple="gray75", outline="")
        box_w, box_h = min(620, pw - 80), ph - 80
        box_x, box_y = (pw - box_w) // 2, 40
        canvas.create_rectangle(box_x, box_y, box_x + box_w, box_y + box_h, outline=ARC_NEON, width=3)
        self.draw_centred_text(canvas, "PAUSED", box_x + box_w // 2, box_y + 38,
                               ("Monospaced", 28, "bold"), ARC_LIME)
        tab_y, tab_w, tab_h = box_y + 56, box_w // 2 - 20, 30
        self.rects["main_tab"] = (box_x + 10, tab_y, tab_w, tab_h)
        self.rects["sound_tab"] = (box_x + box_w // 2 + 10, tab_y, tab_w, tab_h)
        self._draw_pause_tab(canvas, "CRT / DISPLAY", self.rects["main_tab"], self.pause_tab == "MAIN")
        self._draw_pause_tab(canvas, "SOUND VOLUMES", self.rects["sound_tab"], self.pause_tab == "SOUND")
        content_y = tab_y + tab_h + 16
        content_h = box_h - (content_y - box_y) - 60
        if self.pause_tab == "MAIN":
            self._draw_crt_panel(canvas, box_x + 10, content_y, box_w - 20, content_h)
        else:
            self._draw_sound_panel(canvas, box_x + 10, content_y, box_w - 20, content_h)
        btn_y, btn_w = box_y + box_h - 48, box_w // 2 - 20
        self.rects["resume"] = (box_x + 10, btn_y, btn_w, 36)
        self.rects["quit"] = (box_x + box_w // 2 + 10, btn_y, btn_w, 36)
        rx, ry, rw, rh = self.rects["resume"]
        canvas.create_rectangle(rx, ry, rx + rw, ry + rh, fill=ARC_TEXT, outline=ARC_NEON, width=2)
        canvas.create_text(rx + rw // 2, ry + 17, text="RESUME", font=("Monospaced", 16, "bold"), fill="#000000")
        qx, qy, qw, qh = self.rects["quit"]
        canvas.create_rectangle(qx, qy, qx + qw, qy + qh, fill=ARC_PANEL, outline=ARC_DIM, width=2)
        canvas.create_text(qx + qw // 2, qy + 17, text="QUIT", font=("Monospaced", 16, "bold"), fill=ARC_TEXT)

    def _draw_pause_tab(self, canvas, label, rect, active):
        x, y, w, h = rect
        canvas.create_rectangle(x, y, x + w, y + h, fill=ARC_TEXT if active else ARC_PANEL, outline=ARC_NEON)
        canvas.create_text(x + w // 2, y + 15, text=label, font=("Monospaced", 13, "bold"),
                           fill="#000000" if active else ARC_DIM)

    def _draw_crt_panel(self, canvas, x, y, w, _h):
        self.rects = {k: v for k, v in self.rects.items() if not k.startswith("CRT")}
        cy = y + 14
        canvas.create_text(x, cy + 14, text="CRT Effect:", font=("Monospaced", 15, "bold"),
                           fill=ARC_TEXT, anchor="w")
        tog_x = x + 120
        self.rects["CRT_ON"] = (tog_x, cy, 56, 26)
        self.rects["CRT_OFF"] = (tog_x + 64, cy, 56, 26)
        enabled = crt_settings.is_enabled()
        ox, oy, ow, oh = self.rects["CRT_ON"]
        canvas.create_rectangle(ox, oy, ox + ow, oy + oh, fill=ARC_TEXT if enabled else ARC_PANEL, outline=ARC_NEON)
        canvas.create_text(ox + 28, oy + 13, text="ON", font=("Monospaced", 12, "bold"),
                           fill="#000000" if enabled else ARC_DIM)
        fx, fy, fw, fh = self.rects["CRT_OFF"]
        canvas.create_rectangle(fx, fy, fx + fw, fy + fh, fill=ARC_PANEL if enabled else "#001900",
                                outline=ARC_NEON if enabled else ARC_DIM)
        canvas.create_text(fx + 28, fy + 13, text="OFF", font=("Monospaced", 12, "bold"),
                           fill=ARC_DIM if enabled else ARC_LIME)
        cy += 44
        canvas.create_text(x, cy + 14, text="Intensity:", font=("Monospaced", 15, "bold"),
                           fill=ARC_TEXT if enabled else ARC_DIM, anchor="w")
        sx, sw, sh = x + 120, w - 160, 16
        self.crt_slider = (sx, cy, sw, sh)
        fill = crt_settings.get_intensity() / 100.0
        canvas.create_rectangle(sx, cy, sx + sw, cy + sh, fill=ARC_PANEL, outline="")
        canvas.create_rectangle(sx, cy, sx + int(sw * fill), cy + sh,
                                fill=ARC_TEXT if enabled else "#002800", outline="")
        canvas.create_rectangle(sx, cy, sx + sw, cy + sh, outline=ARC_NEON if enabled else ARC_DIM)
        canvas.create_rectangle(sx + int(sw * fill) - 4, cy - 3, sx + int(sw * fill) + 4, cy + sh + 3,
                                fill=ARC_LIME, outline="")
        canvas.create_text(sx + sw + 8, cy + 13, text=str(crt_settings.get_intensity()) + "%",
                           font=("Monospaced", 13, "bold"), fill=ARC_NEON, anchor="w")
        canvas.create_text(x, cy + 50, text="0-33: Scanlines Only   34-66: Plus Vignette   67-100: Plus Flicker",
                           font=("Monospaced", 12, "normal"), fill=ARC_DIM, anchor="w")

    def _draw_sound_panel(self, canvas, x, y, w, h):
        pong_sounds = sound_settings.get_sound_files_for_category("Pong")
        general_sounds = sound_settings.get_general_sound_files()
        cy, label_w = y, 180
        sx, sw, row_h = x + label_w, w - label_w - 60, 26
        canvas.create_text(x, cy + 13, text="PONG SOUNDS", font=("Monospaced", 13, "bold"),
                           fill=ARC_TEXT, anchor="w")
        cy += 20
        for sound_file in pong_sounds:
            self._draw_sound_row(canvas, sound_file, x, cy, sx, sw, row_h)
            cy += row_h
        cy += 8
        canvas.create_text(x, cy + 13, text="GENERAL SOUNDS", font=("Monospaced", 13, "bold"),
                           fill=ARC_TEXT, anchor="w")
        cy += 20
        max_rows = (h - (cy - y)) // row_h
        for sound_file in general_sounds[:max_rows]:
            self._draw_sound_row(canvas, sound_file, x, cy, sx, sw, row_h)
            cy += row_h

    def _draw_sound_row(self, canvas, sound_file, x, cy, sx, sw, row_h):
        name = sound_settings.get_display_name(sound_file)
        vol = sound_settings.get_volume(sound_file)
        short = name[:19] + "." if len(name) > 20 else name
        canvas.create_text(x, cy + row_h - 8, text=short, font=("Monospaced", 12, "bold"),
                           fill=ARC_TEXT, anchor="w")
        rect = (sx, cy + 4, sw, row_h - 10)
        self.rects[sound_file] = rect
        canvas.create_rectangle(sx, cy + 4, sx + sw, cy + row_h - 6, fill=ARC_PANEL, outline="")
        canvas.create_rectangle(sx, cy + 4, sx + int(sw * vol / 100.0), cy + row_h - 6, fill=ARC_TEXT, outline="")
        canvas.create_rectangle(sx, cy + 4, sx + sw, cy + row_h - 6, outline=ARC_NEON)
        thumb = sx + int(sw * vol / 100.0) - 3
        canvas.create_rectangle(thumb, cy + 2, thumb + 6, cy + row_h - 2, fill=ARC_LIME, outline="")
        canvas.create_text(sx + sw + 6, cy + row_h - 7, text=str(vol) + "%",
                           font=("Monospaced", 11, "normal"), fill=ARC_DIM, anchor="w")

