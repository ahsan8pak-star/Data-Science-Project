"""
Shared test utilities for exercising the Python coursework programs stored
under the top-level `university_courseworks/` directory.

Unlike the per-paradigm suites under tests/, these programs are not Python
"projects" but individual module files sitting next to their .java twins in
a course folder (e.g. the 60-credit spiralling Practical / "goblet" brief).
Each module is imported WITHOUT running its `if __name__ == "__main__":`
guard via `load_module()` below, so functions can be unit-tested directly
while any interactive input()/print() flow is driven by the test itself.
"""

import importlib.util
import sys
import types

"""
Provide a tkinter stub so modules that import tkinter (e.g. cs1op's
options_screen.py, base_screen.py) can be imported on platforms where
python3-tk is not installed (WSL/Linux). The tests in this suite only
exercise OptionsState, which does not reference any tkinter widget, so a
stub is sufficient.
"""
if "tkinter" not in sys.modules:
    _tkinter_stub = types.ModuleType("tkinter")
    _tkinter_stub.__path__ = []
    _tkinter_stub.Tk = type("Tk", (), {})
    _tkinter_stub.Frame = type("Frame", (), {})
    _tkinter_stub.Canvas = type("Canvas", (), {})
    _tkinter_stub.Button = type("Button", (), {})
    _tkinter_stub.Label = type("Label", (), {})
    _tkinter_stub.Entry = type("Entry", (), {})
    _tkinter_stub.StringVar = type("StringVar", (), {})
    _tkinter_stub.IntVar = type("IntVar", (), {})
    _tkinter_stub.BooleanVar = type("BooleanVar", (), {})
    _tkinter_stub.NORMAL = "normal"
    _tkinter_stub.DISABLED = "disabled"
    _tkinter_stub.BOTH = "both"
    _tkinter_stub.TOP = "top"
    _tkinter_stub.BOTTOM = "bottom"
    _tkinter_stub.LEFT = "left"
    _tkinter_stub.RIGHT = "right"
    _tkinter_stub.CENTER = "center"
    _tkinter_stub.X = "x"
    _tkinter_stub.Y = "y"
    _tkinter_stub.END = "end"
    _tkinter_stub.INSERT = "insert"
    _tkinter_stub.NW = "nw"
    _tkinter_stub.NE = "ne"
    _tkinter_stub.SW = "sw"
    _tkinter_stub.SE = "se"
    _tkinter_stub.W = "w"
    _tkinter_stub.E = "e"
    _tkinter_stub.S = "s"
    _tkinter_stub.N = "n"
    _tkinter_stub.ORDINAL = "ordinal"
    # tkinter.font submodule (imported by base_screen.py)
    _tkinter_font_stub = types.ModuleType("tkinter.font")
    _tkinter_stub.font = _tkinter_font_stub
    sys.modules["tkinter"] = _tkinter_stub
    sys.modules["tkinter.font"] = _tkinter_font_stub

from pathlib import Path

# Walk up until the repository root (named 'Data-Science-Project') is found.
PROJECT_ROOT = Path(__file__).resolve()
while PROJECT_ROOT.name != 'Data-Science-Project':
    PROJECT_ROOT = PROJECT_ROOT.parent

CS1IP = PROJECT_ROOT / 'university_courseworks' / 'year1' / 'semester1' / 'cs1ip'
COURSEWORK1 = CS1IP / 'coursework1'
COURSEWORK2 = CS1IP / 'coursework2'

CS1OP = PROJECT_ROOT / 'university_courseworks' / 'year1' / 'semester2' / 'cs1op'
CS1OP_COURSEWORK = CS1OP / 'coursework'
CS1OP_PYTHON_SRC = CS1OP_COURSEWORK / 'python' / 'src'
CS1OP_JAVA_SRC = CS1OP_COURSEWORK / 'java' / 'src'
CS1OP_RESOURCES = CS1OP_COURSEWORK / 'java' / 'resources'

# Each coursework folder splits its artefacts by language or role, so tests
# address files through these constants: a re-layout is a change here, not one edit per assertion.
COURSEWORK1_PYTHON = COURSEWORK1 / 'python'
COURSEWORK1_JAVA = COURSEWORK1 / 'java'
COURSEWORK2_PYTHON = COURSEWORK2 / 'python'
COURSEWORK2_JAVA = COURSEWORK2 / 'java'
COURSEWORK2_DATA = COURSEWORK2 / 'data'


def load_module(filepath, module_name=None):
    """
    Import a coursework .py file as a plain module WITHOUT executing its
    `if __name__ == "__main__":` block. Returns the live module so tests can
    call its functions/classes directly or read its constants.
    """
    filepath = Path(filepath)
    assert filepath.exists(), f"Script not found: {filepath}"

    if module_name is None:
        module_name = filepath.stem

    spec = importlib.util.spec_from_file_location(module_name, str(filepath))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

