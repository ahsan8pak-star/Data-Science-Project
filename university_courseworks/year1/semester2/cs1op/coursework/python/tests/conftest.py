"""
Test package for the CS1OP Python translation.

Puts ``../src`` on the import path so the test modules can import the game
package by its plain module names, mirroring how the Java sources sit
together in one ``src/`` folder.
"""

import sys
from pathlib import Path


SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pytest

import crt_settings
import game
import game_settings
import sound_manager
import sound_settings
from game_settings import Difficulty


@pytest.fixture(autouse=True)
def isolated_game_state():
    """
    Fresh singleton, silent backend and default settings per test.

    The game notifies a global singleton and the settings live in
    modules, so every test starts from the same clean state.
    """
    game.Game.reset()
    sound_manager.set_backend(sound_manager.SilentBackend())
    volumes = dict(sound_settings._volumes)
    game_settings.set_difficulty(Difficulty.NORMAL)
    crt_settings.set_enabled(False)
    crt_settings.set_intensity(40)
    crt_settings.reset_flicker()
    yield
    game.Game.reset()
    sound_manager.set_backend(sound_manager.SilentBackend())
    sound_settings._volumes.clear()
    sound_settings._volumes.update(volumes)
    game_settings.set_difficulty(Difficulty.NORMAL)
    crt_settings.set_enabled(False)
    crt_settings.set_intensity(40)
    crt_settings.reset_flicker()

