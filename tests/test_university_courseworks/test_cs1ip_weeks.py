"""
Pytest suite for the cs1ip week Python programs under university_courseworks/.

Exercises the 34 week scripts that previously had no test at all: the 18 files
under week*/lecture/python/ and the 16 under week*/practical/ (the fourteen
week1 taskN.py scripts, the week7 system-log generator, and the week8 map
generator). Most of these files are top-level scripts rather than importable
modules - they carry no `if __name__ == "__main__"` guard and no callable API -
so "exercise" here means run the module body once through ``load_module`` and
confirm it reaches the end. Running them is also what gives these files their
first line coverage.

Two files are known to fail when executed, and are asserted to fail for that
exact reason, so the exception list stays load-bearing rather than becoming a
filter that hides new breakage:

  - week1/practical/python/task10.py formats the name with ``%d``, raising
    ``TypeError: %d format: a real number is required, not str``;
  - week2/lecture/python/input.py calls ``input()`` at module level, raising
    ``EOFError`` because the test session supplies no stdin.

If either file is repaired this suite fails ("DID NOT RAISE") and the entry is
removed; if any other file starts failing to execute, the suite fails too.
"""

from __future__ import annotations

import io

import pytest

from tests.test_university_courseworks.conftest import CS1IP, load_module


WEEK_LECTURE_RELATIVE = [
    "week1/lecture/python/variables.py",
    "week2/lecture/python/input.py",
    "week2/lecture/python/selection.py",
    "week3/lecture/python/do_while.py",
    "week3/lecture/python/for_loop.py",
    "week3/lecture/python/loop_control.py",
    "week3/lecture/python/while_loop.py",
    "week4/lecture/python/function_overload.py",
    "week4/lecture/python/recursion.py",
    "week4/lecture/python/return.py",
    "week4/lecture/python/testing.py",
    "week4/lecture/python/variable_scope.py",
    "week5/lecture/python/array.py",
    "week5/lecture/python/matrix.py",
    "week7/lecture/python/file_io_and_data_handling.py",
    "week10/lecture/python/bubble_sort.py",
    "week11/lecture/python/lamda_filter_map.py",
    "week12/lecture/python/defensive_programming.py",
]

WEEK_PRACTICAL_RELATIVE = [
    "week1/practical/python/task1.py",
    "week1/practical/python/task2.py",
    "week1/practical/python/task3.py",
    "week1/practical/python/task4.py",
    "week1/practical/python/task5.py",
    "week1/practical/python/task6.py",
    "week1/practical/python/task7.py",
    "week1/practical/python/task8.py",
    "week1/practical/python/task9.py",
    "week1/practical/python/task10.py",
    "week1/practical/python/task11.py",
    "week1/practical/python/task12.py",
    "week1/practical/python/task13.py",
    "week1/practical/python/task14.py",
    "week7/practical/week_07_practical_files/task8_gen_system_logs.py",
    "week8/practical/week_08_practical_files/map_generator.py",
]

# file -> the exception its known defect raises on execution.
KNOWN_EXECUTION_FAILURES = {
    "week1/practical/python/task10.py": TypeError,
    "week2/lecture/python/input.py": EOFError,
}

ALL_WEEK_RELATIVE = WEEK_LECTURE_RELATIVE + WEEK_PRACTICAL_RELATIVE


@pytest.fixture(autouse=True)
def _empty_stdin(monkeypatch):
    """
    Give every script an empty stdin.

    A module-level ``input()`` then raises ``EOFError`` deterministically,
    instead of ``OSError`` under pytest's capture or blocking on a real
    terminal - the failure mode must not depend on how the suite is invoked.
    """
    monkeypatch.setattr("sys.stdin", io.StringIO(""))


@pytest.mark.parametrize("rel_path", ALL_WEEK_RELATIVE)
def test_week_program_executes(rel_path: str) -> None:
    """
    The script runs to completion, or fails only in its known, asserted way.

    A file already in KNOWN_EXECUTION_FAILURES is expected to raise and is
    asserted to raise that exact type, so a repaired file fails here and the
    list is revisited. Every other file must execute cleanly; a new import or
    runtime error surfaces as a normal test failure.
    """
    filepath = CS1IP / rel_path
    assert filepath.is_file(), f"{rel_path} is missing from the cs1ip weeks"
    expected = KNOWN_EXECUTION_FAILURES.get(rel_path)
    if expected is not None:
        with pytest.raises(expected):
            load_module(filepath)
        return
    assert load_module(filepath) is not None

