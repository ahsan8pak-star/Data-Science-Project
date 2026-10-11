"""
Space Invaders view: canvas rendering and input over InvadersState.

Translation of the presentation half of ``SpaceInvadersMinigame.java``.
The frame loop runs on a tkinter timer instead of the Java thread;
ENTER starts each wave, SPACE shoots, P pauses, ESC opens the pause
menu, and ENTER on the end overlay reports back to the controller
(100 EXP for the win, a lost life otherwise). Enemy shapes follow the
Java geometry: green UFO, blue spacecraft, red alien, two frames each.
"""

import time
import tkinter as tk

import crt_settings
import sound_manager
import sound_settings
from base_screen import (
    ARC_DIM,
    ARC_LIME,
    ARC_NEON,
    ARC_PANEL,
    ARC_TEXT,
    BaseGameScreen,
)
from game_settings import difficulty_label
from space_invaders import (
    EBH,
    EBW,
    ES,
    GH,
    GW,
    PBH,
    PBW,
    PH,
    PLAYER_Y,
    PW,
    SI_WIN_EXP,
    EnemyType,
    InvadersState,
)


class SpaceInvadersView(BaseGameScreen):
    """
    The playable invasion with wave messages and pause menu.
    """

    def __init__(self, gui, controller):
        super().__init__(gui, controller)
        player = controller.get_current_player() if controller is not None else None
        self.state = InvadersState(player.get_exp() if player is not None else 0)
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
        self.canvas_widget.bind("<ButtonRelease-1>", lambda _e: setattr(self, "_dragging", None))
        self.bind("<Configure>", lambda _e: self.redraw())
        self._last_ms = self._clock_ms()
        self._schedule_tick()

    @staticmethod
    def _clock_ms():
        return int(time.monotonic() * 1000)

    def _schedule_tick(self):
        self.after(16, self._tick)

    def _tick(self):
        if self.state.game_active:
            now = self._clock_ms()
            self.state.advance_clock(max(0, now - self._last_ms))
            self._last_ms = now
            if (not self.state.game_paused and not self.state.game_ended
                    and not self.state.show_msg and not self.paused_menu):
                self.state.tick()
            self.redraw()
            self._schedule_tick()

    def _on_key_press(self, event):
        key = event.keysym
        if self.state.game_ended:
            if key == "Return" and self.controller is not None:
                sound_manager.stop_sound(sound_manager.SI_LOSE)
                sound_manager.stop_all()
                if self.state.player_won:
                    self.controller.on_minigame_won("SPACE_INVADERS", SI_WIN_EXP)
                else:
                    self.controller.on_minigame_lost()
            return
        if self.paused_menu:
            if key == "Escape":
                self.paused_menu = False
                self.redraw()
            return
        if self.state.show_msg:
            if key == "Return":
                self.state.start_wave_loop()
                self.redraw()
            return
        if key == "Left":
            self.state.move_left = True
        elif key == "Right":
            self.state.move_right = True
        elif key == "space":
            self.state.do_shoot = True
        elif key in ("p", "P"):
            self.state.game_paused = not self.state.game_paused
        elif key == "Escape":
            self.paused_menu = True
            self.pause_tab = "MAIN"
            self.redraw()

    def _on_key_release(self, event):
        key = event.keysym
        if key == "Left":
            self.state.move_left = False
        elif key == "Right":
            self.state.move_right = False
        elif key == "space":
            self.state.do_shoot = False

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
            self.state.game_active = False
            self.state.stop_all_enemy_loops()
            sound_manager.stop_sound(sound_manager.SI_LOSE)
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
        Halt the loop and release the saucer loops, used on teardown.
        """
        self.state.game_active = False
        self.state.stop_all_enemy_loops()
        sound_manager.stop_sound(sound_manager.SI_LOSE)

    def redraw(self):
        """
        Paint the ship, saucers, shots, HUD and overlays.
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

        if self.state.show_msg and not self.state.game_ended:
            lines = self.state.msg_text.split("\n")
            row_h = int(32 * min(sx, sy))
            top = ph // 2 - len(lines) * row_h // 2
            for i, line in enumerate(lines):
                canvas.create_text(pw // 2, top + i * row_h, text=line,
                                   font=("Monospaced", int(22 * min(sx, sy)), "bold"), fill="#00ff00")
            self.draw_crt_overlay(canvas, pw, ph)
            return
        px, py = located(self.state.player_x), tall(PLAYER_Y)
        psw, psh = located(PW), tall(PH)
        canvas.create_polygon(px + psw // 2, py, px, py + psh, px + psw, py + psh, fill="#00ff00", outline="")
        for enemy in self.state.enemies:
            self._draw_enemy(canvas, enemy, located(enemy.x), tall(enemy.y),
                             located(ES), tall(ES), self.state.anim_frame, sx, sy)
        for bullet in self.state.player_bullets:
            canvas.create_rectangle(located(bullet.x), tall(bullet.y),
                                    located(bullet.x) + located(PBW), tall(bullet.y) + tall(PBH),
                                    fill="#ffff00", outline="")
        for bullet in self.state.enemy_bullets:
            canvas.create_rectangle(located(bullet.x), tall(bullet.y),
                                    located(bullet.x) + located(EBW), tall(bullet.y) + tall(EBH),
                                    fill="#ff5050", outline="")
        scale = min(sx, sy)
        canvas.create_text(located(10), tall(24),
                           text=("WAVE: " + str(self.state.current_wave) + "/" + str(self.state.total_waves)
                                 + "   Speed: " + ("%.1f" % self.state.current_speed)
                                 + "   Mini-lives: " + str(self.state.mini_lives)
                                 + "   [" + difficulty_label() + "]"),
                           font=("Monospaced", int(14 * scale), "bold"), fill="#00ff00", anchor="w")
        bar_w, bar_h, bar_x, bar_y = located(200), tall(9), located(10), tall(30)
        canvas.create_rectangle(bar_x, bar_y, bar_x + bar_w, bar_y + bar_h, fill="#282828", outline="")
        canvas.create_rectangle(bar_x, bar_y,
                                bar_x + (self.state.current_wave - 1) * bar_w // self.state.total_waves,
                                bar_y + bar_h, fill="#00c800", outline="")
        if self.state.hit_timer > 0:
            canvas.create_text(pw // 2, ph // 2 - tall(55), text=self.state.hit_msg,
                               font=("Monospaced", int(17 * scale), "bold"), fill="#ffdc00")
        canvas.create_text(located(10), ph - tall(8), text="LEFT/RIGHT: Move   SPACE: Shoot   P: Pause   ESC: Menu",
                           font=("Monospaced", int(11 * scale), "normal"), fill="#007800", anchor="w")
        self.draw_crt_overlay(canvas, pw, ph)
        if self.state.game_ended:
            canvas.create_rectangle(0, 0, pw, ph, fill="black", stipple="gray50", outline="")
            end_fill = "#00ff00" if self.state.player_won else "#ff0000"
            self.draw_centred_text(canvas, self.state.end_msg, pw // 2, ph // 2,
                                   ("Monospaced", int(36 * scale), "bold"), end_fill)
            self.draw_centred_text(canvas, "Press ENTER to continue", pw // 2, ph // 2 + tall(55),
                                   ("Monospaced", int(18 * scale), "normal"), "#00ff00")
        elif self.paused_menu:
            self._draw_pause_menu(canvas, pw, ph)

    def _draw_enemy(self, canvas, enemy, ex, ey, ew, eh, frame):
        if enemy.kind == EnemyType.UFO:
            self._draw_ufo(canvas, ex, ey, ew, eh, frame)
        elif enemy.kind == EnemyType.SPACECRAFT:
            self._draw_spacecraft(canvas, ex, ey, ew, eh, frame)
        else:
            self._draw_alien(canvas, ex, ey, ew, eh, frame)

    @staticmethod
    def _draw_ufo(canvas, ex, ey, ew, eh, frame):
        body = "#00ff00"
        unit = max(1, ew // 12)
        canvas.create_oval(ex + ew * 3 // 8, ey, ex + ew * 3 // 8 + ew // 4, ey + eh // 4, fill=body, outline="")
        canvas.create_oval(ex + unit, ey + eh // 6, ex + unit + ew - 2 * unit, ey + eh // 6 + eh * 2 // 5,
                           fill=body, outline="")
        canvas.create_rectangle(ex, ey + eh * 2 // 5, ex + ew, ey + eh * 2 // 5 + eh // 3, fill=body, outline="")
        left_r, light_y, count = unit + 1, ey + eh * 2 // 5 + unit, 5
        for i in range(count):
            lx = ex + unit + i * (ew - 2 * unit) // (count - 1) - left_r
            canvas.create_oval(lx, light_y, lx + left_r * 2, light_y + left_r * 2,
                               fill="#ffffff" if i % 2 == frame else body, outline="")
        canvas.create_rectangle(ex + ew // 6, ey + eh * 2 // 3, ex + ew // 6 + ew * 2 // 3,
                                ey + eh * 2 // 3 + unit, fill=body, outline="")

    @staticmethod
    def _draw_spacecraft(canvas, ex, ey, ew, eh, frame):
        body = "#0000ff"
        unit = max(1, ew // 10)
        fw, fx = ew * 2 // 5, ex + (ew - ew * 2 // 5) // 2
        canvas.create_rectangle(fx, ey, fx + fw, ey + eh * 3 // 4, fill=body, outline="")
        canvas.create_rectangle(fx + fw // 4, ey - unit * 2, fx + fw // 4 + fw // 2, ey, fill=body, outline="")
        canvas.create_rectangle(ex, ey + eh // 2, ex + ew, ey + eh // 2 + eh // 5, fill=body, outline="")
        canvas.create_rectangle(fx + fw // 4, ey + eh * 3 // 4, fx + fw // 4 + fw // 2,
                                ey + eh * 3 // 4 + unit * 2, fill=body, outline="")
        cockpit = "#000000" if frame == 0 else "#ffffff"
        canvas.create_rectangle(fx + fw // 4, ey + eh // 5, fx + fw // 4 + fw // 2,
                                ey + eh // 5 + eh // 7, fill=cockpit, outline="")
        canvas.create_rectangle(fx + fw // 4, ey + eh // 5 + eh // 7 + unit,
                                fx + fw // 4 + fw // 2, ey + eh // 5 + eh // 7 + unit + eh // 7,
                                fill=cockpit, outline="")

    @staticmethod
    def _draw_alien(canvas, ex, ey, ew, eh, frame):
        body = "#ff0000"
        unit = max(1, ew // 11)

        def block(col, row, cols=1, rows=1):
            canvas.create_rectangle(ex + col * unit, ey + row * unit,
                                    ex + (col + cols) * unit, ey + (row + rows) * unit,
                                    fill=body, outline="")

        def eye(col):
            canvas.create_rectangle(ex + col * unit, ey + 2 * unit + unit // 2,
                                    ex + (col + 2) * unit, ey + 2 * unit + unit // 2 + 2 * unit,
                                    fill="#ffffff", outline="")

        if frame == 0:
            block(2, 0, 1, 2)
            block(8, 0, 1, 2)
        else:
            block(1, 0, 1, 2)
            block(9, 0, 1, 2)
        block(2, 2, 7, 3)
        eye(3)
        eye(6)
        block(0, 5, 11, 3)
        block(3, 8, 5, 2)
        block(0, 5, 2, 2)
        block(9, 5, 2, 2)
        if frame == 0:
            block(2, 10, 2, 2)
            block(7, 10, 2, 2)
        else:
            block(0, 10, 2, 2)
            block(9, 10, 2, 2)

    def _draw_pause_menu(self, canvas, pw, ph):
        canvas.create_rectangle(0, 0, pw, ph, fill="black", stipple="gray75", outline="")
        box_w, box_h = min(620, pw - 60), ph - 80
        box_x, box_y = (pw - box_w) // 2, 40
        canvas.create_rectangle(box_x, box_y, box_x + box_w, box_y + box_h, outline="#00ff00", width=3)
        self.draw_centred_text(canvas, "PAUSED", box_x + box_w // 2, box_y + 38,
                               ("Monospaced", 28, "bold"), "#00ff00")
        tab_y, tab_w, tab_h = box_y + 56, box_w // 2 - 20, 30
        self.rects["main_tab"] = (box_x + 10, tab_y, tab_w, tab_h)
        self.rects["sound_tab"] = (box_x + box_w // 2 + 10, tab_y, tab_w, tab_h)
        self._draw_tab(canvas, "CRT / DISPLAY", self.rects["main_tab"], self.pause_tab == "MAIN")
        self._draw_tab(canvas, "SOUND VOLUMES", self.rects["sound_tab"], self.pause_tab == "SOUND")
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
        canvas.create_rectangle(rx, ry, rx + rw, ry + rh, fill="#00c800", outline="#00ff00", width=2)
        canvas.create_text(rx + rw // 2, ry + 17, text="RESUME", font=("Monospaced", 16, "bold"), fill="#ffffff")
        qx, qy, qw, qh = self.rects["quit"]
        canvas.create_rectangle(qx, qy, qx + qw, qy + qh, fill="#b40000", outline="#00ff00", width=2)
        canvas.create_text(qx + qw // 2, qy + 17, text="QUIT", font=("Monospaced", 16, "bold"), fill="#ffffff")

    def _draw_tab(self, canvas, label, rect, active):
        x, y, w, h = rect
        canvas.create_rectangle(x, y, x + w, y + h, fill="#00c800" if active else "#003c00", outline="#00ff00")
        canvas.create_text(x + w // 2, y + 15, text=label, font=("Monospaced", 13, "bold"),
                           fill="#000000" if active else "#00c800")

    def _draw_crt_panel(self, canvas, x, y, w, _h):
        self.rects = {k: v for k, v in self.rects.items() if not k.startswith("CRT")}
        cy = y + 14
        canvas.create_text(x, cy + 14, text="CRT Effect:", font=("Monospaced", 15, "bold"),
                           fill="#00ff00", anchor="w")
        tog_x = x + 130
        on_r = (tog_x, cy, 56, 26)
        off_r = (tog_x + 64, cy, 56, 26)
        enabled = crt_settings.is_enabled()
        canvas.create_rectangle(on_r[0], on_r[1], on_r[0] + 56, on_r[1] + 26,
                                fill="#00c800" if enabled else "#003200", outline="#00ff00")
        canvas.create_text(on_r[0] + 28, on_r[1] + 13, text="ON", font=("Monospaced", 12, "bold"),
                           fill="#000000" if enabled else "#00c800")
        canvas.create_rectangle(off_r[0], off_r[1], off_r[0] + 56, off_r[1] + 26,
                                fill="#960000" if not enabled else "#1e0000", outline="#00ff00")
        canvas.create_text(off_r[0] + 28, off_r[1] + 13, text="OFF", font=("Monospaced", 12, "bold"),
                           fill="#ffffff" if not enabled else "#b40000")
        self.rects["CRT_ON"] = on_r
        self.rects["CRT_OFF"] = off_r
        cy += 44
        canvas.create_text(x, cy + 14, text="Intensity:", font=("Monospaced", 15, "bold"),
                           fill="#00ff00" if enabled else "#005000", anchor="w")
        sx, sw = x + 130, w - 170
        self.crt_slider = (sx, cy, sw, 16)
        fill = crt_settings.get_intensity() / 100.0
        canvas.create_rectangle(sx, cy, sx + sw, cy + 16, fill="#002800", outline="")
        canvas.create_rectangle(sx, cy, sx + int(sw * fill), cy + 16,
                                fill="#00c800" if enabled else "#003c00", outline="")
        canvas.create_rectangle(sx, cy, sx + sw, cy + 16, outline="#00ff00")
        canvas.create_rectangle(sx + int(sw * fill) - 4, cy - 3, sx + int(sw * fill) + 4, cy + 19,
                                fill="#00c800", outline="")
        canvas.create_text(sx + sw + 8, cy + 13, text=str(crt_settings.get_intensity()) + "%",
                           font=("Monospaced", 13, "bold"), fill="#00ff00", anchor="w")
        canvas.create_text(x, cy + 50, text="0-33: Scanlines only   34-66: + Vignette   67-100: + Flicker",
                           font=("Monospaced", 12, "normal"), fill="#00a000", anchor="w")
        canvas.create_text(x, cy + 80, text="Reference: perchance.org/text-adventure-template",
                           font=("Monospaced", 11, "normal"), fill="#007800", anchor="w")

    def _draw_sound_panel(self, canvas, x, y, w, h):
        si_sounds = sound_settings.get_sound_files_for_category("Invaders")
        general_sounds = sound_settings.get_general_sound_files()
        cy, label_w = y, 200
        sx, sw, row_h = x + label_w, w - label_w - 60, 26
        canvas.create_text(x, cy + 13, text="SPACE INVADERS SOUNDS", font=("Monospaced", 13, "bold"),
                           fill="#00c800", anchor="w")
        cy += 20
        for sound_file in si_sounds:
            self._draw_sound_row(canvas, sound_file, x, cy, sx, sw, row_h)
            cy += row_h
        cy += 8
        canvas.create_text(x, cy + 13, text="GENERAL SOUNDS", font=("Monospaced", 13, "bold"),
                           fill="#00c800", anchor="w")
        cy += 20
        max_rows = (h - (cy - y)) // row_h
        for sound_file in general_sounds[:max_rows]:
            self._draw_sound_row(canvas, sound_file, x, cy, sx, sw, row_h)
            cy += row_h

    def _draw_sound_row(self, canvas, sound_file, x, cy, sx, sw, row_h):
        name = sound_settings.get_display_name(sound_file)
        vol = sound_settings.get_volume(sound_file)
        short = name[:21] + "." if len(name) > 22 else name
        canvas.create_text(x, cy + row_h - 8, text=short, font=("Monospaced", 12, "bold"),
                           fill="#00dc00", anchor="w")
        rect = (sx, cy + 4, sw, row_h - 10)
        self.rects[sound_file] = rect
        canvas.create_rectangle(sx, cy + 4, sx + sw, cy + row_h - 6, fill="#002800", outline="")
        canvas.create_rectangle(sx, cy + 4, sx + int(sw * vol / 100.0), cy + row_h - 6, fill="#00b400", outline="")
        canvas.create_rectangle(sx, cy + 4, sx + sw, cy + row_h - 6, outline="#00ff00")
        thumb = sx + int(sw * vol / 100.0) - 3
        canvas.create_rectangle(thumb, cy + 2, thumb + 6, cy + row_h - 2, fill="#00b400", outline="")
        canvas.create_text(sx + sw + 6, cy + row_h - 7, text=str(vol) + "%",
                           font=("Monospaced", 11, "normal"), fill="#00c800", anchor="w")

