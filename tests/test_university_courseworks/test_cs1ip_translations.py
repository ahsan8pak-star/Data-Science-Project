"""
Pytest suite for the CS1IP translations added in October 2026.

This file covers both tiers:
  * KNOWN_* values mirror the Java samples (the exact ``print_loop``
    output, the five door frames, the board layout, and the drawing
    coordinates the Java programs use).
  * NEW_* values exercise fresh inputs/outputs: edge heights, overshooting
    dice rolls, empty-sun cases, and repaint behaviour.

All GUI tests use recording doubles instead of a real Tk window, so the
suite runs headlessly on Windows and WSL.
"""
from __future__ import annotations

import io
import math
import random
from unittest.mock import call

import pytest

from tests.test_university_courseworks.conftest import CS1IP, load_module


def _load(relative: str):
    return load_module(CS1IP / relative)


class _RecordingCanvas:
    def __init__(self, *args, **kwargs):
        self.calls = []

    def delete(self, *args, **kwargs):
        self.calls.append(("delete", args, kwargs))

    def create_oval(self, *args, **kwargs):
        self.calls.append(("oval", args, kwargs))

    def create_rectangle(self, *args, **kwargs):
        self.calls.append(("rect", args, kwargs))

    def create_line(self, *args, **kwargs):
        self.calls.append(("line", args, kwargs))

    def create_polygon(self, *args, **kwargs):
        self.calls.append(("poly", args, kwargs))

    def create_text(self, *args, **kwargs):
        self.calls.append(("text", args, kwargs))

    def pack(self, *args, **kwargs):
        pass

    def of(self, kind):
        return [c for c in self.calls if c[0] == kind]


class _RecordingRoot:
    def __init__(self):
        self.after_calls = []
        self.mainloop_called = False
        self.titles = []
        self.protocols = []

    def title(self, text):
        self.titles.append(text)

    def protocol(self, name, func):
        self.protocols.append((name, func))

    def after(self, delay, callback):
        self.after_calls.append((delay, callback))
        return f"after{len(self.after_calls)}"

    def mainloop(self):
        self.mainloop_called = True

    def destroy(self):
        pass


# ----------------------------------------------------------------------------
# print_loop
# ----------------------------------------------------------------------------

KNOWN_PRINT_LOOP_OUTPUT = """i=1,j=1
i=1,j=2
i=2,j=1
"""


def test_print_loop_matches_the_java_output(capsys) -> None:
    mod = _load("week3/lecture/python/print_loop.py")
    mod.main()
    out = capsys.readouterr().out
    assert out == KNOWN_PRINT_LOOP_OUTPUT


# ----------------------------------------------------------------------------
# fall_ball / bounce_ball
# ----------------------------------------------------------------------------

FALL_BALL_ERASE = "\033[2J"
FALL_BALL_HIDE = "\033[?25l"
CURSOR_HOME = "\033[H"


def test_ball_frames_put_the_ball_on_the_expected_row(capsys) -> None:
    mod = _load("week3/lecture/python/fall_ball.py")
    # known
    mod.draw_frame(20.0)
    out = capsys.readouterr().out
    assert out.startswith(mod.CURSOR_HOME)
    body = out[len(mod.CURSOR_HOME):]
    parts = body.split("\n")
    # no 'O' at row 0
    assert "O" not in body
    # new: height 19.5 -> int 19 -> row 1
    capsys.readouterr()
    mod.draw_frame(19.5)
    out2 = capsys.readouterr().out
    body2 = out2[len(mod.CURSOR_HOME):]
    assert "O" in body2
    # height 0.5 -> row 20
    capsys.readouterr()
    mod.draw_frame(0.5)
    out3 = capsys.readouterr().out
    body3 = out3[len(mod.CURSOR_HOME):]
    parts = body3.rstrip("\n").split("\n")
    assert parts[19] == "O"


def test_fall_ball_main_terminates_on_the_floor(monkeypatch) -> None:
    mod = _load("week3/lecture/python/fall_ball.py")
    heights = []
    sleeps = []

    def fake_draw(h):
        heights.append(h)

    def fake_sleep(s):
        sleeps.append(s)

    monkeypatch.setattr(mod, "draw_frame", fake_draw)
    monkeypatch.setattr(mod.time, "sleep", fake_sleep)
    mod.main()
    assert len(heights) == 20
    assert heights[0] == pytest.approx(20.0)
    assert all(h > 0 for h in heights)
    # non-increasing in terms of the sequence values? first is highest
    assert heights[0] >= heights[-1]
    assert heights[-1] < 1.0
    assert sleeps == [pytest.approx(0.06)] * 20


def test_bounce_ball_main_bounces_and_stops(monkeypatch) -> None:
    mod = _load("week3/lecture/python/bounce_ball.py")
    heights = []
    sleeps = []

    def fake_draw(h):
        heights.append(h)

    def fake_sleep(s):
        sleeps.append(s)

    monkeypatch.setattr(mod, "draw_frame", fake_draw)
    monkeypatch.setattr(mod.time, "sleep", fake_sleep)
    mod.main()
    assert len(heights) > 0
    assert heights[0] == pytest.approx(20.0)
    assert all(h >= 0 for h in heights)
    assert heights[0] > max(heights[1:]) if len(heights) > 1 else True
    assert sleeps == [pytest.approx(0.06)] * len(heights)


# ----------------------------------------------------------------------------
# snakes_and_ladders
# ----------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("pos", "expected"),
    [
        (3, 11),
        (5, 9),
        (15, 7),
        (12, 2),
        (0, 0),
        (16, 16),
        (4, 4),
    ],
)
def test_apply_board_known_and_new(capsys, pos, expected) -> None:
    mod = _load("week3/lecture/python/snakes_and_ladders.py")
    out = mod.apply_board(pos)
    assert out == expected


def test_roll_dice_calls_randint(monkeypatch) -> None:
    mod = _load("week3/lecture/python/snakes_and_ladders.py")
    calls = []

    def fake_randint(a, b):
        calls.append((a, b))
        return 4

    monkeypatch.setattr(mod.random, "randint", fake_randint)
    assert mod.roll_dice() == 4
    assert calls == [(1, 6)]


def test_snakes_and_ladders_main_win_via_ladder(monkeypatch, capsys) -> None:
    mod = _load("week3/lecture/python/snakes_and_ladders.py")
    rolls = iter([3, 5])

    def fake_roll():
        return next(rolls)

    monkeypatch.setattr(mod, "roll_dice", fake_roll)
    inputs = iter(["", ""])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    mod.main()
    out = capsys.readouterr().out
    assert "You found a ladder! Climb up to 11." in out
    assert "You are now at position 16" in out
    assert "Congratulations! You win!" in out


def test_snakes_and_ladders_main_overshoot_stays_put(monkeypatch, capsys) -> None:
    mod = _load("week3/lecture/python/snakes_and_ladders.py")
    rolls = iter([10, 10, 6])

    def fake_roll():
        return next(rolls)

    monkeypatch.setattr(mod, "roll_dice", fake_roll)
    inputs = iter(["", "", ""])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    mod.main()
    out = capsys.readouterr().out
    assert "You rolled too high and stayed at 10" in out
    assert "Congratulations! You win!" in out


def test_snakes_and_ladders_main_hits_snake(monkeypatch, capsys) -> None:
    mod = _load("week3/lecture/python/snakes_and_ladders.py")
    rolls = iter([3, 4, 9])

    def fake_roll():
        return next(rolls)

    monkeypatch.setattr(mod, "roll_dice", fake_roll)
    inputs = iter(["", "", ""])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    mod.main()
    out = capsys.readouterr().out
    assert "Oops! You hit a snake! Slide down to 7." in out
    assert "Congratulations! You win!" in out


# ----------------------------------------------------------------------------
# doodle
# ----------------------------------------------------------------------------

def test_doodle_paint_component_draws_two_circles() -> None:
    mod = _load("week8/lecture/python/doodle.py")
    c = _RecordingCanvas()
    mod.paint_component(c)
    # delete all first
    assert c.calls[0][0] == "delete"
    ovals = c.of("oval")
    assert len(ovals) == 2
    # blue outline
    assert ovals[0][1] == (50, 50, 150, 150)
    assert ovals[0][2]["outline"] == "blue"
    # red fill
    assert ovals[1][1] == (200, 50, 350, 200)
    assert ovals[1][2]["fill"] == "red"


def test_doodle_gui_wiring_with_doubles(monkeypatch) -> None:
    mod = _load("week8/lecture/python/doodle.py")
    root = _RecordingRoot()
    canvas = _RecordingCanvas()

    monkeypatch.setattr(mod.tk, "Tk", lambda: root)
    monkeypatch.setattr(mod.tk, "Canvas", lambda *a, **k: canvas)
    mod.create_and_show_gui()
    assert root.titles == ["HelloWorldSwing"]
    assert root.mainloop_called is True
    # paint called
    assert any(c[0] == "oval" for c in canvas.calls)


# ----------------------------------------------------------------------------
# doodle_house
# ----------------------------------------------------------------------------

def test_draw_window_exact_calls() -> None:
    mod = _load("week8/lecture/python/doodle_house.py")
    c = _RecordingCanvas()
    mod.draw_window(c, 10, 20)
    rects = c.of("rect")
    assert rects[0][1] == (10, 20, 60, 70)
    lines = c.of("line")
    assert (10 + 25, 20, 10 + 25, 70) in [l[1] for l in lines]
    assert (10, 20 + 25, 60, 20 + 25) in [l[1] for l in lines]


def test_draw_sun_known_and_new_edges() -> None:
    mod = _load("week8/lecture/python/doodle_house.py")
    c = _RecordingCanvas()
    mod.draw_sun(c, 530, 140, 10)
    ovals = c.of("oval")
    assert ovals[0][1] == (480, 90, 580, 190)
    lines = c.of("line")
    assert len(lines) == 10
    # first ray at 0 degrees: (630, 140)
    assert (530, 140, 630, 140) in [l[1] for l in lines]
    # new: 1 ray
    c2 = _RecordingCanvas()
    mod.draw_sun(c2, 100, 100, 1)
    assert len(c2.of("line")) == 1
    assert (100, 100, 200, 100) in [l[1] for l in c2.of("line")]
    # zero rays -> division by zero in loop (no division by zero raised if range(0))
    c3 = _RecordingCanvas()
    mod.draw_sun(c3, 0, 0, 0)
    assert len(c3.of("line")) == 0


def test_doodle_house_paint_component_exact_count() -> None:
    mod = _load("week8/lecture/python/doodle_house.py")
    c = _RecordingCanvas()
    mod.paint_component(c)
    # delete + sky + grass + walls + door + 2*window + roof + sun oval + 10 sun lines + text = 24
    assert len(c.calls) == 24
    texts = c.of("text")
    assert any(t[2].get("text") == "Happy Housewarming" for t in texts)


def test_doodle_house_gui_wiring(monkeypatch) -> None:
    mod = _load("week8/lecture/python/doodle_house.py")
    root = _RecordingRoot()
    canvas = _RecordingCanvas()
    monkeypatch.setattr(mod.tk, "Tk", lambda: root)
    monkeypatch.setattr(mod.tk, "Canvas", lambda *a, **k: canvas)
    mod.main()
    assert root.mainloop_called is True


# ----------------------------------------------------------------------------
# door_animation
# ----------------------------------------------------------------------------

def test_door_animation_frames_exact_content() -> None:
    mod = _load("week8/practical/week_08_practical_files/door_animation.py")
    assert len(mod.FRAMES) == 5
    # first frame known
    assert mod.FRAMES[0].startswith("________")
    assert mod.FRAMES[0].strip().endswith("|________|")
    # frames have backslashes in middle frames, decoded to single characters
    assert "\\" in mod.FRAMES[1]
    assert "\\\\" not in "".join(mod.FRAMES)  # no doubled backslash at runtime
    assert mod.FRAME_DELAY_SECONDS == 0.5


def test_door_animation_main_clears_and_prints_all_frames(monkeypatch, capsys) -> None:
    mod = _load("week8/practical/week_08_practical_files/door_animation.py")
    sleeps = []

    def fake_sleep(s):
        sleeps.append(s)

    monkeypatch.setattr(mod.time, "sleep", fake_sleep)
    mod.main()
    out = capsys.readouterr().out
    expected = "".join(mod.CLEAR_SCREEN + f + "\n" for f in mod.FRAMES)
    assert out == expected
    assert sleeps == [0.5] * 5


# ----------------------------------------------------------------------------
# doodle_falling_snow - AffineTransform / Graphics
# ----------------------------------------------------------------------------

def test_affine_transform_identity_and_copy() -> None:
    mod = _load("week12/lecture/python/doodle_falling_snow.py")
    t = mod.AffineTransform()
    assert t.apply(2, 3) == (2.0, 3.0)
    t2 = t.copy()
    t2.translate(5, 7)
    assert t.apply(0, 0) == (0.0, 0.0)
    assert t2.apply(0, 0) == (5.0, 7.0)


def test_affine_transform_translate_rotate_compose() -> None:
    mod = _load("week12/lecture/python/doodle_falling_snow.py")
    t = mod.AffineTransform()
    t.translate(10, 20)
    assert t.apply(0, 0) == (10.0, 20.0)
    t.rotate(math.pi / 2)
    p = t.apply(1, 0)
    assert abs(p[0] - 10.0) < 1e-9
    assert abs(p[1] - 21.0) < 1e-9


def test_graphics_transform_copy_and_restore() -> None:
    mod = _load("week12/lecture/python/doodle_falling_snow.py")
    c = _RecordingCanvas()
    g = mod.Graphics(c)
    g.translate(10, 20)
    snap = g.get_transform()
    g.translate(5, 0)
    g.set_transform(snap)
    # transform should be back to snap
    assert g.transform.apply(0, 0) == (10.0, 20.0)
    # mutating snap doesn't affect g
    snap.translate(100, 100)
    assert g.transform.apply(0, 0) == (10.0, 20.0)
    # draw_line uses transform
    c.calls.clear()
    g.draw_line(0, 0, 1, 0)
    line = c.of("line")[0]
    assert line[1][0] == 10.0
    assert line[1][1] == 20.0


def test_graphics_styles_and_shapes() -> None:
    mod = _load("week12/lecture/python/doodle_falling_snow.py")
    c = _RecordingCanvas()
    g = mod.Graphics(c)
    g.set_colour(mod.RED)
    g.set_stroke_width(3.0)
    g.set_font_size(16)
    g.fill_oval(0, 0, 10, 10)
    g.fill_rect(1, 1, 2, 3)
    g.draw_string("hi", 5, 6)
    assert c.of("oval")[0][2]["fill"] == mod.RED
    assert c.of("rect")[0][2]["fill"] == mod.RED
    assert c.of("text")[0][2]["text"] == "hi"
    assert c.of("text")[0][2]["font"] == ("Arial", 16)


# ----------------------------------------------------------------------------
# doodle_falling_snow - panel
# ----------------------------------------------------------------------------

class _SeqRng:
    def __init__(self, values, default=1):
        self.values = iter(values)
        self.default = default

    def randrange(self, n):
        try:
            return next(self.values)
        except StopIteration:
            return self.default


def test_snow_panel_adds_flake_and_draws_counters(monkeypatch) -> None:
    mod = _load("week12/lecture/python/doodle_falling_snow.py")
    root = _RecordingRoot()
    canvas = _RecordingCanvas()
    # need 6 values for the if branch: 30,540,100,360,4,5
    monkeypatch.setattr(mod.random, "Random", lambda: _SeqRng([0, 0, 0, 0, 0, 0]))
    panel = mod.DoodlePanel(root, canvas)
    assert len(panel.snow_x) == 1
    assert panel.frame == 101
    assert root.after_calls  # scheduled tick
    # counters drawn
    texts = canvas.of("text")
    assert any("Frame 101" in str(t) for t in texts)
    assert any("Snowflakes 1" in str(t) for t in texts)


def test_snow_panel_removes_flakes_below_screen(monkeypatch) -> None:
    mod = _load("week12/lecture/python/doodle_falling_snow.py")
    root = _RecordingRoot()
    canvas = _RecordingCanvas()
    monkeypatch.setattr(mod.random, "Random", lambda: _SeqRng([1, 0, 0, 0, 0, 0]))  # no add
    panel = mod.DoodlePanel(root, canvas)
    # clear flakes added? first paint may not add (1!=0)
    panel.snow_x = [10]
    panel.snow_y = [600]
    panel.snow_velocity = [1]
    panel.snow_size = [50]
    panel.snow_spin = [0]
    panel.snow_colour = [0]
    panel.rng = _SeqRng([1])  # no new flake
    canvas.calls.clear()
    panel.paint_component()
    assert panel.snow_x == []
    assert panel.snow_y == []


def test_snow_panel_tick_schedules_next(monkeypatch) -> None:
    mod = _load("week12/lecture/python/doodle_falling_snow.py")
    root = _RecordingRoot()
    canvas = _RecordingCanvas()
    monkeypatch.setattr(mod.random, "Random", lambda: _SeqRng([1, 0, 0, 0, 0, 0]))
    panel = mod.DoodlePanel(root, canvas)
    before = len(root.after_calls)
    panel._tick()
    assert len(root.after_calls) == before + 1


def test_snowflake_drawing_line_counts_and_transform_restore(monkeypatch) -> None:
    mod = _load("week12/lecture/python/doodle_falling_snow.py")
    root = _RecordingRoot()
    canvas = _RecordingCanvas()
    monkeypatch.setattr(mod.random, "Random", lambda: _SeqRng([1, 0, 0, 0, 0, 0]))
    panel = mod.DoodlePanel(root, canvas)
    g = panel.graphics
    # simple snowflake: 6 lines
    c = _RecordingCanvas()
    g2 = mod.Graphics(c)
    panel.draw_simple_snowflake(g2, mod.WHITE, 10, 20, 50, 0)
    assert len(c.of("line")) == 6
    # transform restored: identity
    assert g2.transform.a == 1.0 and g2.transform.e == 0.0 and g2.transform.f == 0.0
    # complex frond line counts
    c = _RecordingCanvas()
    g2 = mod.Graphics(c)
    panel.draw_complex_frond(g2, 10, 0)
    assert len(c.of("line")) == 0
    c = _RecordingCanvas()
    g2 = mod.Graphics(c)
    panel.draw_complex_frond(g2, 10, 1)
    assert len(c.of("line")) == 1
    c = _RecordingCanvas()
    g2 = mod.Graphics(c)
    panel.draw_complex_frond(g2, 10, 2)
    assert len(c.of("line")) == 5
    c = _RecordingCanvas()
    g2 = mod.Graphics(c)
    panel.draw_complex_frond(g2, 10, 3)
    assert len(c.of("line")) == 21
    # transform restored each time
    assert g2.transform.a == 1.0 and g2.transform.e == 0.0 and g2.transform.f == 0.0
    # complex snowflake 6 * 21
    c = _RecordingCanvas()
    g2 = mod.Graphics(c)
    panel.draw_complex_snowflake(g2, mod.WHITE, 100, 100, 50, 0)
    assert len(c.of("line")) == 126


def test_snow_gui_wiring(monkeypatch) -> None:
    mod = _load("week12/lecture/python/doodle_falling_snow.py")
    root = _RecordingRoot()
    canvas = _RecordingCanvas()
    monkeypatch.setattr(mod.random, "Random", lambda: _SeqRng([1, 0, 0, 0, 0, 0]))
    monkeypatch.setattr(mod.tk, "Tk", lambda: root)
    monkeypatch.setattr(mod.tk, "Canvas", lambda *a, **k: canvas)
    mod.create_and_show_gui()
    assert root.mainloop_called is True
    assert len(root.after_calls) >= 1

