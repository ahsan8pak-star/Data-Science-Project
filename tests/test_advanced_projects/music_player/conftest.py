"""
Shared fixtures for the music player test package.

Mirrors the cs1op coursework test package structure: a self-contained
conftest providing audio-engine stubs, fresh player instances, and
module-loading helpers so each test file focuses on behaviour.

Two player families are covered:

  * TUI players (tui/mp3_tui_player.py, tui/wav_tui_player.py) - the
    core audio-engine classes plus pure rendering helpers. Their only
    third-party dependency is pygame, mocked here.

  * GUI players (gui/mp3_gui_player.py, gui/wav_gui_player.py) - thin
    tkinter wrappers delegating to the TUI classes. tkinter is mocked
    so the widget tree and delegation logic run headlessly.

No real audio or display is touched.
"""

import importlib.util
import sys

import pytest

from types import SimpleNamespace
from unittest.mock import MagicMock

from tests.test_advanced_projects.conftest import BASE_DIR, load_module

MP3_TUI = "music_player/tui/mp3_tui_player.py"
WAV_TUI = "music_player/tui/wav_tui_player.py"
MP3_TUI_PATH = BASE_DIR / "music_player" / "tui" / "mp3_tui_player.py"
WAV_TUI_PATH = BASE_DIR / "music_player" / "tui" / "wav_tui_player.py"
MP3_GUI_PATH = BASE_DIR / "music_player" / "gui" / "mp3_gui_player.py"
WAV_GUI_PATH = BASE_DIR / "music_player" / "gui" / "wav_gui_player.py"


def _build_audio_context():
    """
    Stand-in modules for pygame (and one tkinter stub) to drop into
    sys.modules. Every attribute is a MagicMock, so the player classes
    behave as if a real audio backend were responding.
    """
    music = MagicMock(name="music")
    mixer = MagicMock(name="mixer")
    mixer.music = music

    pygame_stub = SimpleNamespace(
        mixer=mixer,
        music=music,
        error=RuntimeError,
    )
    tkinter_stub = MagicMock(name="tkinter")

    return {"pygame": pygame_stub, "tkinter": tkinter_stub}


@pytest.fixture()
def audio_ctx(monkeypatch):
    """Install stand-in pygame/tkinter modules in sys.modules per test."""
    context = _build_audio_context()
    for name, stub in context.items():
        monkeypatch.setitem(sys.modules, name, stub)
    return context


@pytest.fixture()
def tui_modules(audio_ctx):
    """Both TUI modules loaded once the pygame stub is in place."""
    return {
        "mp3": load_module(MP3_TUI),
        "wav": load_module(WAV_TUI),
    }


@pytest.fixture()
def players(audio_ctx, tmp_path):
    """
    Fresh MP3AudioPlayer and WAVAudioPlayer instances pointing at a
    temporary folder with two .mp3 and two .wav files.
    """
    mp3_mod = load_module(MP3_TUI)
    wav_mod = load_module(WAV_TUI)

    songs = tmp_path / "songs"
    songs.mkdir()
    (songs / "alpha.mp3").write_bytes(b"")
    (songs / "beta.mp3").write_bytes(b"")
    (songs / "alpha.wav").write_bytes(b"")
    (songs / "beta.wav").write_bytes(b"")
    (songs / "notes.txt").write_text("ignore me")

    return {
        "mp3": mp3_mod.MP3AudioPlayer(str(songs)),
        "wav": wav_mod.WAVAudioPlayer(str(songs)),
    }


def load_gui_module(path, module_name):
    """
    Import a GUI module via importlib exec. tkinter was already replaced
    with a MagicMock by the audio_ctx fixture, and the GUI file has no
    __main__ side effects, so a plain import yields a patchable module.
    """
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

