"""
Box geometry and input prompting of the text interface.
"""

import text_ui


def test_box_exact_layout(capsys):
    text_ui.box("Hi", ["ab"])
    out = capsys.readouterr().out.split("\n")
    assert out[0] == "-" * 6
    assert out[1] == "| Hi |"
    assert out[2] == "-" * 6
    assert out[3] == "| ab |"
    assert out[4] == "-" * 6


def test_box_width_follows_longest_line(capsys):
    text_ui.box("T", ["a longer line"])
    out = capsys.readouterr().out.split("\n")
    assert out[0] == "-" * 17
    assert out[1] == "|       T       |"


def test_box_accepts_varargs(capsys):
    text_ui.box("Title", "one", "two")
    out = capsys.readouterr().out
    assert "| one" in out
    assert "| two" in out


def test_box_accepts_mixed_list_and_varargs(capsys):
    text_ui.box("Title", ["one"], "two")
    out = capsys.readouterr().out
    assert "| one" in out
    assert "| two" in out


def test_prompt_strips_input(capsys):
    assert text_ui.prompt("Choose:", input_fn=lambda: "  1  ") == "1"
    assert capsys.readouterr().out == "Choose: "

