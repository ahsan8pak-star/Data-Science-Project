"""
Shared test utilities for exercising the scripts under `Python/`.

Most files in this project are procedural "coursework" scripts: they call
input()/print() directly at module level instead of being wrapped in a
single clean function, and several now guard that body behind
`if __name__ == "__main__":` so they can also be safely imported by
sibling scripts (e.g. area_volume_calculator.py importing area/volume,
triangle_calculator.py importing cosine_rule/sine_rule).

This conftest provides `run_script()`, which:

  1. Executes a given .py file via runpy.run_path(..., run_name="__main__"),
     the same mechanism Python itself uses for `python -m` - so __name__
     really is "__main__" for the duration of the run (making
     if-__name__-main guards fire correctly) and the script's own
     directory is temporarily added to sys.path (so sibling imports like
     `from area import area` resolve, exactly as they would for a real
     `python some_script.py` run).
  2. Feeds it a scripted sequence of answers for any input() calls it makes.
  3. Silences time.sleep() so countdown-style scripts run instantly.
  4. Captures everything the script prints to stdout.
  5. Returns both a lightweight module-like wrapper around the script's
     resulting globals (so top-level functions/variables can be inspected
     or called directly in further assertions) and the captured output
     (so printed behaviour can be asserted on too).
"""

import contextlib
import io
import os
import runpy
import sys
import types

from pathlib import Path
from unittest.mock import patch

TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
PYTHON_DIR = PROJECT_ROOT / "Python"

# Force the terminal execution to automatically see your code directories
sys.path.insert(0, str(PYTHON_DIR))


def run_script(relative_path, inputs=None, patches=None, cwd=None):

    """
    Execute ``Python/<relative_path>`` as if it had been run directly via
    ``python <relative_path>``.

    relative_path : path relative to the Python/ folder, e.g.
                    "algorithmic_data_converters/weight_converter.py"
    inputs        : list of strings returned in order for each input() call
                    the script makes. If the script asks for more input than
                    was provided, an EOFError is raised (mirrors real stdin
                    EOF behaviour) instead of hanging.
    patches       : optional list of already-built unittest.mock.patch(...)
                    context managers (e.g. patch("random.choice", ...)) to
                    apply for the duration of the run, on top of the
                    input()/time.sleep() patches already applied.
    cwd           : optional directory to run the script from (useful for
                    scripts that read/write local files, e.g. file_writer.py).

    Returns (module, printed_output).

    Uses runpy.run_path(..., run_name="__main__") rather than a hand-rolled
    importlib spec. This matters for two real behaviours some scripts rely
    on: (1) several scripts guard their executable body behind
    `if __name__ == "__main__":` so they're safe to import as plain modules
    from sibling scripts - runpy correctly sets __name__ to "__main__" for
    the duration of the run (and restores sys.modules["__main__"]
    afterwards) so those guards fire exactly as they would for a real user;
    (2) some scripts do plain sibling imports (`from area import area`,
    `import cosine_rule`) that only resolve because a directly-run script's
    own directory is temporarily added to the front of sys.path - runpy
    does this automatically too.
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
                    pass  # a script deliberately calling exit()/quit() is fine
            
                except Exception as exc:

                    """
                    A handful of the coursework scripts have genuine bugs
                    that make them crash partway through (e.g. calling
                    .clear() and then .pop() on the same list back to
                    back). Rather than hide that, attach whatever was
                    printed *before* the crash to the exception so tests
                    can still assert on it, then let the real exception
                    propagate.
                    """

                    setattr(exc, "partial_output", buf.getvalue())
                    raise
    finally:
       
        # Clean up the sys.path addition regardless of success/failure
        # Prevent leaks into unrelated tests or shadow same-named modules.
       
        try:
            sys.path.remove(script_dir)
       
        except ValueError:
            pass

    """
    Wrap the returned globals dict in a lightweight module-like object so
    existing assertions like `mod.some_function(...)` / `mod.some_var`
    keep working exactly as they did against a real imported module.
    """
    
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

