"""
Shared test utilities for exercising the scripts under
`python/advanced_projects/` (machine learning, music players, transactions).

Mechanism mirrors tests/test_functional_programming/conftest.py - see that
file's docstring for the full rationale. Reproduced here so each test package
under tests/ stays self-contained.

Two entry points are provided:

  * run_script(relative_path, ...) - executes a script as if it had been run
    directly via `python <relative_path>` (runpy.run_path with run_name
    "__main__"), feeding mocked input and capturing stdout.

  * load_module(relative_path) - imports a script as a plain module WITHOUT
    executing its `if __name__ == "__main__":` guard. This is required for
    the music player scripts, whose __main__ blocks launch interactive
    pygame/tkinter loops that must never run under pytest.
"""

import contextlib
import importlib.util
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

BASE_DIR = PROJECT_ROOT / 'python' / 'advanced_projects'

# Force the terminal execution to automatically see your code directories
sys.path.insert(0, str(BASE_DIR))


def run_script(relative_path, inputs=None, patches=None, cwd=None):

    """
    Execute ``python/advanced_projects/<relative_path>`` as if it had been
    run directly via ``python <relative_path>``.

    Returns (module, printed_output). See the functional/imperative conftest
    docstrings for the full parameter documentation - behaviour is identical.
    """

    filepath = BASE_DIR / relative_path
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


def load_module(relative_path):

    """
    Import the module at ``python/advanced_projects/<relative_path>`` WITHOUT
    running its ``if __name__ == "__main__":`` block.

    Returns the live module so tests can call its functions/classes directly.
    """

    filepath = BASE_DIR / relative_path
    assert filepath.exists(), f"Script not found: {filepath}"

    script_dir = str(filepath.parent)
    sys.path.insert(0, script_dir)

    try:
        spec = importlib.util.spec_from_file_location(filepath.stem, str(filepath))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    finally:
        try:
            sys.path.remove(script_dir)

        except ValueError:
            pass

    return module


@contextlib.contextmanager
def _chdir(path):
    old = os.getcwd()
    os.chdir(path)

    try:
        yield

    finally:
        os.chdir(old)