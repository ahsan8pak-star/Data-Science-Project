"""
Pytest suite for the music player in `python/advanced_projects/music_player/`.

There are two families here:

  * TUI players (`tui/mp3_tui_player.py`, `tui/wav_tui_player.py`) - the
    core audio-engine classes (MP3AudioPlayer / WAVAudioPlayer) plus pure
    rendering helpers (display_tui_banner / display_info_box). Their only
    third-party dependency is pygame, which is mocked below so the classes
    can be unit-tested without an audio device.

  * GUI players (`gui/*_gui_player.py`) - thin wrappers that instantiate
    tkinter widgets and delegate to the TUI classes. tkinter is also mocked,
    so the widget tree and delegation logic can be verified headlessly.

No real audio or display is touched.
"""

import importlib.util
import sys

import pytest

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from tests.test_advanced_projects.conftest import BASE_DIR, load_module

MP3_TUI = "music_player/tui/mp3_tui_player.py"
WAV_TUI = "music_player/tui/wav_tui_player.py"
MP3_GUI_PATH = BASE_DIR / "music_player" / "gui" / "mp3_gui_player.py"
WAV_GUI_PATH = BASE_DIR / "music_player" / "gui" / "wav_gui_player.py"


def _build_audio_context():
    """
    Stand-in modules for pygame (and one tkinter stub) to drop into
    sys.modules. Every attribute is a MagicMock, so the player classes behave
    as if a real audio backend were responding.
    """
    music = MagicMock(name="music")
    mixer = MagicMock(name="mixer")
    mixer.music = music

    pygame_stub = SimpleNamespace(
        mixer=mixer,
        music=music,
        error=RuntimeError,  # stands in for pygame.error
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


# ---------------------------------------------------------------------------
# Pure rendering helpers (no pygame state touched)
# ---------------------------------------------------------------------------
@pytest.fixture()
def tui_modules(audio_ctx):
    """Both TUI modules loaded once the pygame stub is in place."""
    return {
        "mp3": load_module(MP3_TUI),
        "wav": load_module(WAV_TUI),
    }


class TestBannerAndInfoBox:
    """Pure ASCII rendering used by both TUI players."""

    def test_banner_centres_title_across_60_chars(self, tui_modules, capsys):
        tui_modules["mp3"].display_tui_banner("MP3 PLAYER")
        out = capsys.readouterr().out.splitlines()

        assert out[0] == "=" * 60
        assert out[2] == "=" * 60
        assert out[1] == "MP3 PLAYER".center(60)

    def test_info_box_border_fits_longest_line(self, tui_modules, capsys):
        lines = ["Track Number  : 1", "Now Playing   : some-long-name.mp3"]
        tui_modules["mp3"].display_info_box(lines)

        out = capsys.readouterr().out.splitlines()
        longest = max(len(line) for line in lines)
        assert out[0] == "-" * (longest + 4)
        assert out[-1] == "-" * (longest + 4)

    def test_info_box_pads_each_line_to_same_width(self, tui_modules, capsys):
        lines = ["a", "longer line here"]
        tui_modules["mp3"].display_info_box(lines)

        out = capsys.readouterr().out.splitlines()
        inner = out[1:-1]
        assert {len(line) for line in inner} == {len(max(inner, key=len))}

    def test_banner_and_info_box_mirrored_in_wav_player(self, tui_modules, capsys):
        tui_modules["wav"].display_tui_banner("WAV PLAYER")
        tui_modules["wav"].display_info_box(["hello"])

        out = capsys.readouterr().out
        assert "WAV PLAYER" in out
        assert "| hello |" in out


# ---------------------------------------------------------------------------
# MP3AudioPlayer / WAVAudioPlayer - structurally identical logic
# ---------------------------------------------------------------------------
class TestAudioPlayers:
    """Shared behaviour across the MP3 and WAV engine classes.

    Both player classes are nearly identical, so each test drives both of
    them; `players` is a {format: fresh_instance} mapping.
    """

    @pytest.fixture()
    def players(self, audio_ctx, tmp_path):
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

    def test_init_sets_default_state(self, players):
        for player in players.values():
            assert player.loop_track is False
            assert player.loop_playlist is False
            assert player.shuffle is False
            assert player.status == "Stopped"
            assert player.current_song is None

    def test_get_files_filters_by_extension(self, players):
        methods = {"mp3": "get_mp3_files", "wav": "get_wav_files"}
        expected = {
            "mp3": ["alpha.mp3", "beta.mp3"],
            "wav": ["alpha.wav", "beta.wav"],
        }
        for extension, player in players.items():
            assert getattr(player, methods[extension])() == expected[extension]

    def test_get_files_stays_empty_for_nonexistent_folder(self, players, tmp_path):
        methods = {"mp3": "get_mp3_files", "wav": "get_wav_files"}
        for extension, player in players.items():
            player.folder_path = str(tmp_path / "does-not-exist")
            assert getattr(player, methods[extension])() == []

    def test_play_missing_file_returns_false(self, players, capsys):
        for player in players.values():
            assert player.play("missing.mp3") is False

        assert "not found" in capsys.readouterr().out.lower()

    def test_play_sets_state_and_returns_true(self, players):
        for extension, player in players.items():
            song = f"alpha.{extension}"
            assert player.play(song, track_num=1) is True
            assert player.current_song == song
            assert player.current_track_num == 1
            assert player.status == "Active Playing"
            assert player.is_paused is False

    def test_pause_when_playing_marks_paused(self, players):
        for extension, player in players.items():
            player.play(f"alpha.{extension}", track_num=1)
            player.pause()
            assert player.is_paused is True
            assert player.status == "Paused"

    def test_resume_after_pause_clears_state(self, players):
        for extension, player in players.items():
            player.play(f"alpha.{extension}", track_num=1)
            player.pause()
            player.resume()
            assert player.is_paused is False
            assert player.status == "Active Playing"

    def test_forward_increments_index(self, players):
        for extension, player in players.items():
            files = [f"alpha.{extension}", f"beta.{extension}"]
            assert player.forward(files, 0) == 1

    def test_backward_decrements_index(self, players):
        for extension, player in players.items():
            files = [f"alpha.{extension}", f"beta.{extension}"]
            assert player.backward(files, 1) == 0

    def test_forward_empty_playlist_stays_put(self, players):
        for player in players.values():
            assert player.forward([], 0) == 0
            assert player.backward([], 0) == 0

    def test_forward_past_end_respects_loop_playlist_off(self, players, capsys):
        for extension, player in players.items():
            files = [f"alpha.{extension}"]
            assert player.forward(files, 0) == 0

        assert "End of playlist reached" in capsys.readouterr().out

    def test_forward_past_end_wraps_when_loop_playlist_on(self, players):
        for extension, player in players.items():
            files = [f"alpha.{extension}", f"beta.{extension}"]
            player.loop_playlist = True
            assert player.forward(files, 1) == 0

    def test_toggles_flip_attributes(self, players):
        for player in players.values():
            player.toggle_loop_track()
            assert player.loop_track is True
            player.toggle_loop_track()
            assert player.loop_track is False

            player.toggle_loop_playlist()
            assert player.loop_playlist is True

            player.toggle_shuffle()
            assert player.shuffle is True

    def test_stop_music_file_marks_stopped(self, players):
        for extension, player in players.items():
            player.play(f"alpha.{extension}", track_num=1)
            player.stop_music_file()
            assert player.status == "Stopped Playing"

    def test_play_runs_pygame_mixer_music(self, players, audio_ctx):
        for extension, player in players.items():
            player.play(f"alpha.{extension}", track_num=1)

        calls = []
        for ext in ("mp3", "wav"):
            calls.append((f"alpha.{ext}", 0))
        music = audio_ctx["pygame"].mixer.music
        assert music.play.call_count == len(calls)


# ---------------------------------------------------------------------------
# TUI entry points (banner + empty-folder guard)
# ---------------------------------------------------------------------------
class TestTuiEntryPoints:

    @pytest.fixture(autouse=True)
    def _load(self, audio_ctx):
        self.mp3 = load_module(MP3_TUI)
        self.wav = load_module(WAV_TUI)

    def test_mp3_player_empty_folder_reports_error(self, capsys):
        with patch.object(self.mp3.MP3AudioPlayer, "get_mp3_files", return_value=[]):
            self.mp3.mp3_player()
        assert "No .mp3 files found" in capsys.readouterr().out

    def test_wav_player_empty_folder_reports_error(self, capsys):
        with patch.object(self.wav.WAVAudioPlayer, "get_wav_files", return_value=[]):
            self.wav.wav_player()
        assert "No .wav files found" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# GUI wrappers (tkinter mocked; delegation to the TUI engine verified)
# ---------------------------------------------------------------------------
def _load_gui_module(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestMP3GUI:

    @pytest.fixture(autouse=True)
    def _build(self, audio_ctx):
        self.gui_mod = _load_gui_module(MP3_GUI_PATH, "mp3_gui_player")
        self.root = MagicMock(name="root")
        self.gui = self.gui_mod.MP3GUIPlayer(self.root)

    def test_window_configuration(self):
        self.root.title.assert_called_once_with("MP3 GUI Player")
        self.root.geometry.assert_called_once_with("500x450")

    def test_player_starts_uninitialised(self):
        assert self.gui.player is None
        assert self.gui.mp3_files == []
        assert self.gui.current_idx == 0

    def test_select_folder_reporting_error_for_empty_folder(self, audio_ctx):
        get_dir = self.gui_mod.filedialog.askdirectory
        get_dir.return_value = "/empty/songs"

        with patch.object(
            self.gui_mod.MP3AudioPlayer, "get_mp3_files", return_value=[]
        ):
            self.gui_mod.messagebox.showerror = MagicMock()
            self.gui._select_folder()

        assert self.gui_mod.messagebox.showerror.call_count == 1


class TestWAVGUI:

    @pytest.fixture(autouse=True)
    def _build(self, audio_ctx):
        self.gui_mod = _load_gui_module(WAV_GUI_PATH, "wav_gui_player")
        self.root = MagicMock(name="root")
        self.gui = self.gui_mod.WAVGUIPlayer(self.root)

    def test_window_configuration(self):
        self.root.title.assert_called_once_with("WAV GUI Player")
        self.root.geometry.assert_called_once_with("500x450")

    def test_select_folder_returns_early_without_choice(self):
        self.gui_mod.filedialog.askdirectory.return_value = ""
        self.gui._select_folder()
        assert self.gui.player is None