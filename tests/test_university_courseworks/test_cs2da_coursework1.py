"""Tests for the CS2DA coursework 1 helpers (Tasks 1-3)."""

import math
from pathlib import Path

import pytest

from tests.test_university_courseworks.conftest import PROJECT_ROOT, load_module


def _load(relative):
    path = PROJECT_ROOT / "university_courseworks" / "year2" / "semester1" / "cs2da" / relative
    return load_module(path)


def test_generate_dfa_personalised_table():
    gd = _load("coursework/python/generate_dfa.py")
    delta, accepting, initial = gd.generate(34001219)
    assert initial == 0
    assert delta == [
        [1, -1, -1],
        [2, 1, 0],
        [-1, 0, 0],
    ]
    assert accepting == [False, False, True]


def test_generate_dfa_print_table(capsys):
    gd = _load("coursework/python/generate_dfa.py")
    delta, accepting, _ = gd.generate(34001219)
    gd.print_table(delta, accepting)
    out = capsys.readouterr().out
    assert " q0 | q1 | -- | --" in out
    assert "Accepting states:  q2" in out


def test_draw_dfa_dot():
    dd = _load("coursework/python/draw_dfa.py")
    delta = [[1, -1, -1], [2, 1, 0], [-1, 0, 0]]
    accepting = [False, False, True]
    text = dd.generate_dot(delta, accepting)
    assert "start -> q0;" in text
    assert "q2 [shape=doublecircle];" in text
    assert 'q0 -> q1 [label="a"];' in text
    assert 'q2 -> q0 [label="b"];' in text
    assert 'q2 -> q0 [label="c"];' in text


def test_draw_dfa_symbol_count_mismatch():
    dd = _load("coursework/python/draw_dfa.py")
    with pytest.raises(ValueError):
        dd.generate_dot([[0]], [True], symbols="ab")


def test_generate_network_matches_brief_example_matrix():
    gn = _load("coursework/python/generate_network.py")
    matrix = gn.generate(1234567890)
    assert matrix[0][0] == 0
    assert math.isnan(matrix[0][1])
    assert matrix[0][2] == 7
    assert math.isnan(matrix[0][3])
    assert matrix[0][4] == 37
    assert matrix[0][5] == 58
    assert math.isnan(matrix[1][0])
    assert matrix[1][2] == 47
    assert matrix[1][3] == 3
    assert matrix[2][0] == 7
    assert math.isnan(matrix[2][3])
    assert matrix[3][0] == 1
    assert math.isnan(matrix[3][1])
    assert math.isnan(matrix[3][2])
    assert matrix[3][4] == 34
    assert math.isnan(matrix[4][0])
    assert math.isnan(matrix[4][1])
    assert matrix[4][2] == 17
    assert matrix[5][0] == 58
    assert matrix[5][1] == 70
    assert math.isnan(matrix[5][2])
    assert math.isnan(matrix[5][3])


def test_generate_network_personalised_matrix_for_34001219():
    gn = _load("coursework/python/generate_network.py")
    matrix = gn.generate(34001219)
    assert len(matrix) == 6
    assert all(len(row) == 6 for row in matrix)
    expected = [
        [0.0, 15.0, float("nan"), 9.0, 42.0, 10.0],
        [15.0, 0.0, 46.0, 37.0, float("nan"), float("nan")],
        [26.0, float("nan"), 0.0, 24.0, float("nan"), 32.0],
        [9.0, 37.0, float("nan"), 0.0, 38.0, 84.0],
        [42.0, float("nan"), 28.0, 38.0, 0.0, float("nan")],
        [10.0, float("nan"), float("nan"), 84.0, 26.0, 0.0],
    ]
    for row, expected_row in zip(matrix, expected):
        for value, expected_value in zip(row, expected_row):
            if math.isnan(expected_value):
                assert math.isnan(value)
            else:
                assert value == expected_value


def test_travel_time_follows_the_coursework_speeds():
    gn = _load("coursework/python/generate_network.py")
    assert gn.travel_time(0) == 0
    assert gn.travel_time(3) == pytest.approx(3 / 5)     # under 5 miles -> 5 mph
    assert gn.travel_time(5) == pytest.approx(5 / 20)    # from 5 up to 10 miles -> 20 mph
    assert gn.travel_time(10) == pytest.approx(10 / 20)  # up to and including 10 miles -> 20 mph
    assert gn.travel_time(11) == pytest.approx(11 / 30)  # above 10 miles -> 30 mph
    assert math.isnan(gn.travel_time(float("nan")))


def test_to_travel_times_converts_the_distances_matrix():
    gn = _load("coursework/python/generate_network.py")
    times = gn.to_travel_times([[0, 7], [float("nan"), 0]])
    assert times[0][1] == pytest.approx(7 / 20)
    assert math.isnan(times[1][0])


def test_generate_network_dot_uses_only_defined_roads():
    gn = _load("coursework/python/generate_network.py")
    dn = _load("coursework/python/draw_network.py")
    dot = dn.generate_dot([[0, 7], [float("nan"), 0]])
    assert 'A -> B [label = "7"];' in dot
    assert "B -> A" not in dot
    assert "rankdir = TB;" in dot

    personalised = dn.generate_dot(gn.generate(34001219))
    assert 'A -> B [label = "15"];' in personalised
    assert 'A -> C' not in personalised

