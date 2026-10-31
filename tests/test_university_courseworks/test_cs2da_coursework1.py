"""Tests for the CS2DA coursework 1 helpers (Tasks 1-2)."""

from pathlib import Path

import pytest

from tests.test_university_courseworks.conftest import PROJECT_ROOT, load_module


def _load(relative):
    path = PROJECT_ROOT / "university_courseworks" / "year2" / "semester1" / "cs2da" / relative
    return load_module(path)


def test_generate_dfa_personalised_table():
    gd = _load("coursework1/python/generate_dfa.py")
    delta, accepting, initial = gd.generate(34001219)
    assert initial == 0
    assert delta == [
        [1, -1, -1],
        [2, 1, 0],
        [-1, 0, 0],
    ]
    assert accepting == [False, False, True]


def test_generate_dfa_print_table(capsys):
    gd = _load("coursework1/python/generate_dfa.py")
    delta, accepting, _ = gd.generate(34001219)
    gd.print_table(delta, accepting)
    out = capsys.readouterr().out
    assert " q0 | q1 | -- | --" in out
    assert "Accepting states:  q2" in out


def test_draw_dfa_dot():
    dd = _load("coursework1/python/draw_dfa.py")
    delta = [[1, -1, -1], [2, 1, 0], [-1, 0, 0]]
    accepting = [False, False, True]
    text = dd.generate_dot(delta, accepting)
    assert "start -> q0;" in text
    assert "q2 [shape=doublecircle];" in text
    assert 'q0 -> q1 [label="a"];' in text
    assert 'q2 -> q0 [label="b"];' in text
    assert 'q2 -> q0 [label="c"];' in text


def test_draw_dfa_symbol_count_mismatch():
    dd = _load("coursework1/python/draw_dfa.py")
    with pytest.raises(ValueError):
        dd.generate_dot([[0]], [True], symbols="ab")

