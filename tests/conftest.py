"""
Shared test utilities for exercising the scripts under `Python/`.

Most files in this project are procedural "coursework" scripts: they call
input()/print() directly at module level instead of being wrapped in a
single clean function. The old placeholder tests in this folder worked
around that by re-implementing toy versions of the logic (e.g. their own
local `is_prime`) directly inside the test file, which meant they never
actually touched the real source files at all.

This conftest instead provides `run_script()`, which:

  1. Loads a given .py file as its own fresh module via importlib, so files
     with special characters in their names/paths (e.g. "Algorithms&Data
     Converters") can still be tested without needing to be valid import
     statements.
  2. Feeds it a scripted sequence of answers for any input() calls it makes.
  3. Silences time.sleep() so countdown-style scripts run instantly.
  4. Captures everything the script prints to stdout.
  5. Returns both the executed module (so top-level functions/variables can
     be inspected or reused directly in further assertions) and the
     captured output (so printed behaviour can be asserted on too).
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import uuid
from pathlib import Path
from unittest.mock import patch

import pytest

TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
PYTHON_DIR = PROJECT_ROOT / "Python"


def run_script(relative_path, inputs=None, patches=None, cwd=None):
    """
    Execute ``Python/<relative_path>`` as an isolated module.

    relative_path : path relative to the Python/ folder, e.g.
                    "Algorithms&DataConverters/WeightConverter.py"
    inputs        : list of strings returned in order for each input() call
                    the script makes. If the script asks for more input than
                    was provided, an EOFError is raised (mirrors real stdin
                    EOF behaviour) instead of hanging.
    patches       : optional list of already-built unittest.mock.patch(...)
                    context managers (e.g. patch("random.choice", ...)) to
                    apply for the duration of the run, on top of the
                    input()/time.sleep() patches already applied.
    cwd           : optional directory to run the script from (useful for
                    scripts that read/write local files, e.g. FileWriter.py).

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

    # A unique module name per call avoids clashes in sys.modules between
    # unrelated scripts that happen to share a stem, and avoids re-using a
    # stale cached module.
    module_name = f"_script_under_test_{uuid.uuid4().hex}"
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)

    buf = io.StringIO()

    with contextlib.ExitStack() as stack:
        stack.enter_context(patch("builtins.input", side_effect=fake_input))
        stack.enter_context(patch("time.sleep", return_value=None))
        for p in (patches or []):
            stack.enter_context(p)
        if cwd is not None:
            stack.enter_context(_chdir(cwd))
        with contextlib.redirect_stdout(buf):
            try:
                spec.loader.exec_module(module)
            except SystemExit:
                pass  # a script deliberately calling exit()/quit() is fine
            except Exception as exc:
                # A handful of the coursework scripts have genuine bugs that
                # make them crash partway through (e.g. calling .clear() and
                # then .pop() on the same list back to back). Rather than
                # hide that, attach whatever was printed *before* the crash
                # to the exception so tests can still assert on it, then
                # let the real exception propagate.
                exc.partial_output = buf.getvalue()
                raise

    return module, buf.getvalue()


@contextlib.contextmanager
def _chdir(path):
    import os

    old = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


@pytest.fixture
def script(tmp_path):
    """Fixture wrapper around run_script(), defaulting cwd to a scratch tmp_path
    so any scripts that write local files (e.g. FileWriter.py) don't pollute
    the real repository."""

    def _runner(relative_path, inputs=None, patches=None, cwd=tmp_path):
        return run_script(relative_path, inputs=inputs, patches=patches, cwd=cwd)

    return _runner