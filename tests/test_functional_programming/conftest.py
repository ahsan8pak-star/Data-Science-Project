"""
Shared test utilities for exercising the scripts under `python/functional_programming/`.

Identical mechanism to tests/test_imperative_programming/conftest.py and
tests/test_object_oriented_programming/conftest.py - see those files'
docstrings for the full rationale. Reproduced here so each test package
under tests/ stays self-contained.

None of the scripts under functional_programming/fundamental_topics/ call
input(), so run_script() here is mainly used for its module-capture and
stdout-capture behaviour rather than its input-feeding behaviour.
"""

import contextlib
import io
import os
import runpy
import sys
import types

from unittest.mock import patch
from pathlib import Path

# This finds the root by looking for the directory containing the projects
# Replace 'Data-Science-Project' with the exact name of the root folder if it differs
PROJECT_ROOT = Path(__file__).resolve()
while PROJECT_ROOT.name != 'Data-Science-Project':
    PROJECT_ROOT = PROJECT_ROOT.parent

PYTHON_SOURCE_DIR = PROJECT_ROOT / 'python'

TESTS_DIR = Path(__file__).resolve().parent
PYTHON_DIR = PROJECT_ROOT / "python"

# Force the terminal execution to automatically see your code directories
sys.path.insert(0, str(PYTHON_DIR))


def run_script(relative_path, inputs=None, patches=None, cwd=None):

    """
    Execute ``python/<relative_path>`` as if it had been run directly via
    ``python <relative_path>``.

    relative_path : path relative to the python/ folder, e.g.
                    "functional_programming/fundamental_topics/filter.py"
    inputs        : list of strings returned in order for each input() call
                    the script makes (unused by the current functional
                    programming scripts, but kept for parity with the
                    other two conftest.py files).
    patches       : optional list of already-built unittest.mock.patch(...)
                    context managers to apply for the duration of the run.
    cwd           : optional directory to run the script from.

    Returns (module, printed_output).
    """

    filepath = PYTHON_DIR / relative_path
    assert filepath.exists(), f"Script not found: {filepath}"

    inputs = list(inputs or [])
    input_iter = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(input_iter)

        except StopIteration:
            raise EOFError("run_script(): no more mocked input available")

    buf = io.StringIO()
    namespace = {}

    script_dir = str(filepath.parent)
    sys.path.insert(0, script_dir)

    try:
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch("builtins.input", side_effect=fake_input))
            stack.enter_context(patch("time.sleep", return_value=None))

            for p in (patches or []):
                stack.enter_context(p)

            if cwd is not None:
                stack.enter_context(_chdir(cwd))

            with contextlib.redirect_stdout(buf):
                try:
                    namespace = runpy.run_path(str(filepath), run_name="__main__")

                except SystemExit:
                    pass

                except Exception as exc:
                    setattr(exc, "partial_output", buf.getvalue())
                    raise
    finally:
        try:
            sys.path.remove(script_dir)

        except ValueError:
            pass

    module = types.ModuleType(filepath.stem)
    module.__dict__.update(namespace)

    return module, buf.getvalue()


@contextlib.contextmanager
def _chdir(path):
    old = os.getcwd()
    os.chdir(path)

    try:
        yield

    finally:
        os.chdir(old)

