"""
Re-export of the shared run_script harness in tests/conftest.py.

The imperative, functional and object-oriented packages used byte-identical
copies of this harness. It now lives in one place so the three cannot drift.
tests/test_advanced_projects/conftest.py stays separate: it binds a different
base directory and adds load_module().
"""
from tests.conftest import (
    PROJECT_ROOT,
    PYTHON_DIR,
    PYTHON_SOURCE_DIR,
    TESTS_DIR,
    run_script,
    _chdir,
)

__all__ = [
    "PROJECT_ROOT",
    "PYTHON_DIR",
    "PYTHON_SOURCE_DIR",
    "TESTS_DIR",
    "run_script",
    "_chdir",
]

