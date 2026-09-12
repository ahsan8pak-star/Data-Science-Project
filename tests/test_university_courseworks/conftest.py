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

from pathlib import Path

# Walk up until we find the repository root (named 'Data-Science-Project').
PROJECT_ROOT = Path(__file__).resolve()
while PROJECT_ROOT.name != 'Data-Science-Project':
    PROJECT_ROOT = PROJECT_ROOT.parent

CS1IP = PROJECT_ROOT / 'university_courseworks' / 'year1' / 'cs1ip'
COURSEWORK1 = CS1IP / 'coursework1'
COURSEWORK2 = CS1IP / 'coursework2'


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