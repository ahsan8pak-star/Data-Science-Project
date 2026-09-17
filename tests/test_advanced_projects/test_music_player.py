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
MP3_TUI_PATH = BASE_DIR / "music_player" / "tui" / "mp3_tui_player.py"
WAV_TUI_PATH = BASE_DIR / "music_player" / "tui" / "wav_tui_player.py"
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

    def test_pause_when_idle_reports_not_playing(self, players, audio_ctx, capsys):

        # A fresh player has no active playback; force get_busy() falsy so
        # pause() skips the pause branch and falls into the else arm.
        audio_ctx["pygame"].mixer.music.get_busy.return_value = False
        for player in players.values():
            player.pause()
        assert "Track is not actively playing or already paused." in capsys.readouterr().out

    def test_resume_without_a_pause_reports_not_paused(self, players, capsys):

        # is_paused starts False, so resume() goes straight to its else arm.
        for player in players.values():
            player.resume()
        assert "Track is not currently paused." in capsys.readouterr().out

    def test_backward_at_start_respects_loop_playlist_off(self, players, capsys):

        # backward() from index 0 with Loop Playlist OFF is unreachable via
        # the forward-only menu cycle - drive it straight against the method.
        for extension, player in players.items():
            files = [f"alpha.{extension}"]
            assert player.backward(files, 0) == 0
        assert "Beginning of playlist reached" in capsys.readouterr().out

    def test_restart_with_no_selected_track_reports(self, players, capsys):

        # The full-menu cycle always restarts a track that is already
        # playing, so the no-song else branch is hit directly here.
        for player in players.values():
            assert player.current_song is None
            player.restart()
        assert "No track selected to restart." in capsys.readouterr().out

    @pytest.mark.parametrize(
        "path,player_cls",
        [(MP3_TUI, "MP3AudioPlayer"), (WAV_TUI, "WAVAudioPlayer")],
    )
    def test_init_reporting_audio_engine_failure(self, audio_ctx, capsys, path, player_cls):

        # mixer.init() raising pygame.error (RuntimeError in the stub)
        # must be caught and reported, not crash the constructor.
        audio_ctx["pygame"].mixer.init.side_effect = RuntimeError("no sound device")
        mod = load_module(path)
        getattr(mod, player_cls)("C:/missing")
        assert "[X] Audio engine initialisation failed: no sound device" in capsys.readouterr().out

    @pytest.mark.parametrize(
        "path,player_cls",
        [(MP3_TUI, "MP3AudioPlayer"), (WAV_TUI, "WAVAudioPlayer")],
    )
    def test_play_reporting_playback_exception(self, audio_ctx, tmp_path, capsys, path, player_cls):

        # music.play() raising pygame.error falls into the play() except
        # branch: the method returns False and prints the error box.
        audio_ctx["pygame"].mixer.music.play.side_effect = RuntimeError("decode failed")
        song = tmp_path / "alpha.mp3"
        song.write_bytes(b"")
        mod = load_module(path)
        player = getattr(mod, player_cls)(str(tmp_path))
        assert player.play(song.name) is False
        assert "[X] Playback Exception: decode failed" in capsys.readouterr().out


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

    @pytest.mark.parametrize("path", [MP3_TUI_PATH, WAV_TUI_PATH])
    def test_import_fallback_when_pygame_is_missing(self, path, capsys):

        """
        Forces `import pygame` to fail regardless of the stubbed
        sys.modules entry, confirming lines 11-13 print the install hint
        and exit(1) immediately for a machine without pygame. runpy runs
        the file as `__main__`, exactly like `python file.py`, which is
        the only way to fire that top-level import guard - a plain module
        import would skip it.
        """

        import builtins
        import runpy

        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name in {"pygame", "pygame.mixer"}:
                raise ModuleNotFoundError("No module named 'pygame'")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=fake_import):
            with pytest.raises(SystemExit):
                runpy.run_path(str(path), run_name="__main__")
        assert "Error: 'pygame' module is not installed." in capsys.readouterr().out


# ---------------------------------------------------------------------------
# TUI menu loops (input()-driven song selection + in-track control menu)
# ---------------------------------------------------------------------------
class TestTuiMenuLoops:

    @pytest.fixture(autouse=True)
    def _load(self, audio_ctx):
        self.mp3 = load_module(MP3_TUI)
        self.wav = load_module(WAV_TUI)

    @pytest.fixture()
    def songs(self):
        return ["alpha.mp3", "beta.mp3"]

    @pytest.fixture()
    def menu_path(self, songs):
        """
        Drive the outer track-selection menu and every in-track control
        option once: play, pause, resume, forward, restart, loop track,
        loop playlist, shuffle, stop file, back to track list, then quit.
        """
        return ["1", "1", "2", "3", "4", "6", "7", "8", "9", "10", "11", "Q"]

    def test_mp3_full_menu_cycle(self, menu_path, songs, audio_ctx, capsys):
        # Walk every menu option once with a real player object; pygame is a
        # shared mock so the tape position and playback flags can be asserted.
        audio_ctx["pygame"].mixer.music.get_pos.return_value = 3000
        with patch.object(self.mp3.MP3AudioPlayer, "get_mp3_files", return_value=songs), \
                patch("os.path.exists", return_value=True), \
                patch("builtins.input", side_effect=iter(menu_path)):
            self.mp3.mp3_player()

        out = capsys.readouterr().out
        assert "Playing Music MP3 Player" in out
        assert "Playback paused" in out
        assert "Playing Resumed" in out
        assert "Forward (-> Track 2)" in out
        assert "Restarting current track" in out
        assert "Loop Single Track : ENABLED" in out
        assert "Loop Entire Playlist : ENABLED" in out
        assert "Shuffle Playback : ENABLED" in out
        assert "Stopped music file playback" in out
        assert "Shutting down MP3 Player interface..." in out

    def test_wav_full_menu_cycle(self, menu_path, songs, audio_ctx, capsys):
        # WAV variant of the full-cycle walk; terminates via menu option "1"
        # (Quit Player) instead of the MP3 "Q", so "0"-only output stays absent.
        audio_ctx["pygame"].mixer.music.get_pos.return_value = 3000
        with patch.object(self.wav.WAVAudioPlayer, "get_wav_files", return_value=songs), \
                patch("os.path.exists", return_value=True), \
                patch("builtins.input", side_effect=iter(menu_path)):
            self.wav.wav_player()

        out = capsys.readouterr().out
        assert "Playing Music WAV Player" in out
        assert "Playback paused" in out
        assert "Forward (-> Track 2)" in out
        assert "Loop Single Track : ENABLED" in out
        assert "Shutdown WAV Player interface..." not in out  # quit via '0', not 'Q'
        assert "Shutting down WAV Player interface..." in out

    def test_mp3_error_paths_and_shuffle(self, songs, capsys):
        """
        Non-digit input, out-of-range track, shuffle-driven forward/
        backward, an invalid in-track option, and hard quit via '0'.
        """
        with patch.object(self.mp3.MP3AudioPlayer, "get_mp3_files", return_value=songs), \
                patch("os.path.exists", return_value=True), \
                patch("random.choice", side_effect=lambda seq: seq[0]), \
                patch("builtins.input", side_effect=iter(
                    ["abc", "99", "2", "9", "4", "5", "12", "0"]
                )):
            self.mp3.mp3_player()

        out = capsys.readouterr().out
        assert "Please enter a valid numerical index." in out
        assert "Selected track index out of range." in out
        assert "Shuffle Playback : ENABLED" in out
        assert "Forward (-> Track 1)" in out  # shuffle picks the other index
        assert "Backward (-> Track 2)" in out
        assert "Invalid choice" in out
        assert "Audio engine player shut down" in out

    def test_wav_error_paths_and_shuffle(self, songs, capsys):
        # Mirror case: WAV error branches, with a deterministic shuffle picking
        # the other (index-0) track for the forward/backward labels.
        with patch.object(self.wav.WAVAudioPlayer, "get_wav_files", return_value=songs), \
                patch("os.path.exists", return_value=True), \
                patch("random.choice", side_effect=lambda seq: seq[0]), \
                patch("builtins.input", side_effect=iter(
                    ["abc", "99", "2", "9", "4", "5", "12", "0"]
                )):
            self.wav.wav_player()

        out = capsys.readouterr().out
        assert "Please enter a valid numerical index." in out
        assert "Shuffle Playback : ENABLED" in out
        assert "Invalid choice" in out

    def test_mp3_main_guard_catches_keyboard_interrupt(self, audio_ctx, capsys):
        # Running the real file as __main__; the guard's Ctrl+C handler prints
        # the goodbye banner instead of dumping a traceback.
        import runpy

        with patch("os.path.isdir", return_value=True), \
                patch("os.listdir", return_value=["alpha.mp3", "beta.mp3"]), \
                patch("builtins.input", side_effect=KeyboardInterrupt()):
            runpy.run_path(str(MP3_TUI_PATH), run_name="__main__")

        out = capsys.readouterr().out
        assert "MP3 player session terminated by user." in out

    def test_wav_main_guard_catches_keyboard_interrupt(self, audio_ctx, capsys):
        # Same KeyboardInterrupt capture for the WAV CLI's __main__ guard.
        import runpy

        with patch("os.path.isdir", return_value=True), \
                patch("os.listdir", return_value=["alpha.wav", "beta.wav"]), \
                patch("builtins.input", side_effect=KeyboardInterrupt()):
            runpy.run_path(str(WAV_TUI_PATH), run_name="__main__")

        out = capsys.readouterr().out
        assert "WAV player session terminated by user." in out


# ---------------------------------------------------------------------------
# GUI wrappers (tkinter mocked; delegation to the TUI engine verified)
# ---------------------------------------------------------------------------
def _load_gui_module(path, module_name):
    # Straight importlib exec - tkinter was already replaced with Mockables by
    # the audio_ctx fixture, and the GUI file has no __main__ side effects,
    # so a plain import yields a patchable, real module.
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
        # Constructor produces the root window with the fixed MP3 geometry.
        self.root.title.assert_called_once_with("MP3 GUI Player")
        self.root.geometry.assert_called_once_with("500x450")

    def test_player_starts_uninitialised(self):
        # No song selected before a folder is picked: no player, no tracks.
        assert self.gui.player is None
        assert self.gui.mp3_files == []
        assert self.gui.current_idx == 0

    def test_select_folder_returns_early_without_choice(self):
        # Mirror of the WAV test: cancelling the folder dialog (empty string)
        # leaves the player unbuilt instead of crashing.
        self.gui_mod.filedialog.askdirectory.return_value = ""
        self.gui._select_folder()
        assert self.gui.player is None

    def test_select_folder_reporting_error_for_empty_folder(self, audio_ctx):
        # Choosing a folder with zero .mp3 files pops a messagebox error
        # instead of constructing a player.
        get_dir = self.gui_mod.filedialog.askdirectory
        get_dir.return_value = "/empty/songs"

        with patch.object(
            self.gui_mod.MP3AudioPlayer, "get_mp3_files", return_value=[]
        ):
            self.gui_mod.messagebox.showerror = MagicMock()
            self.gui._select_folder()

        assert self.gui_mod.messagebox.showerror.call_count == 1

    def test_select_folder_populates_track_list(self, audio_ctx):
        # A folder with files builds an MP3AudioPlayer and inserts one listbox
        # entry per track.
        self.gui_mod.filedialog.askdirectory.return_value = "/songs"
        with patch.object(
            self.gui_mod.MP3AudioPlayer, "get_mp3_files", return_value=["alpha.mp3", "beta.mp3"]
        ):
            self.gui._select_folder()

        assert self.gui.player is not None
        assert self.gui.folder_label.config.call_args_list
        assert self.gui.track_listbox.insert.call_count == 2
        self.gui.status_label.config.assert_called()

    def test_playback_controls_guard_without_player(self):
        # With no player the control buttons must no-op rather than crash.
        self.gui.player = None
        self.gui.mp3_files = []
        self.gui._play()
        self.gui._forward()
        self.gui._backward()

    def test_transport_controls_delegate_to_player(self, audio_ctx):
        # Buttons forward straight into the real player methods, whose
        # playback side effects are all handled by the pygame mock.
        player = MagicMock(name="mp3_player", current_song="alpha.mp3", status="Active")
        self.gui.player = player
        self.gui.mp3_files = ["alpha.mp3", "beta.mp3"]
        self.gui.current_idx = 0

        self.gui._play(); player.play.assert_called()
        self.gui._pause(); player.pause.assert_called()
        self.gui._resume(); player.resume.assert_called()
        self.gui._stop(); player.stop_music_file.assert_called()

    def test_track_skip_updates_current_index(self, audio_ctx):
        # forward()/backward() are mocked to return the next index, and the
        # listbox selection follows it via selection_set.
        player = MagicMock(name="mp3_player", current_song="alpha.mp3", status="Active")
        player.forward.return_value = 1
        player.backward.return_value = 0
        self.gui.player = player
        self.gui.mp3_files = ["alpha.mp3", "beta.mp3"]

        self.gui._forward()
        assert self.gui.current_idx == 1
        self.gui.track_listbox.selection_clear.assert_called()
        self.gui.track_listbox.selection_set.assert_called_with(1)

        self.gui._backward()
        assert self.gui.current_idx == 0

    def test_toggle_callbacks_sync_checkbox_var(self, audio_ctx):
        # side_effect (not a fixed return) drives each toggle with a distinct
        # checked/unchecked state so the loop/shuffle flags mirror it.
        player = MagicMock(name="mp3_player", current_song="alpha.mp3", status="Active")
        self.gui.player = player
        self.gui.loop_track_var.get.side_effect = [True, False, True]

        self.gui._toggle_loop_track()
        assert player.loop_track is True
        self.gui._toggle_loop_playlist()
        assert player.loop_playlist is False
        self.gui._toggle_shuffle()
        assert player.shuffle is True

    def test_update_status_displays_now_playing(self, audio_ctx):
        # The status label text is rewritten with the current track name.
        player = MagicMock(name="mp3_player", current_song="alpha.mp3", status="Active")
        self.gui.player = player
        self.gui._update_status()
        text = self.gui.status_label.config.call_args[1].get("text", "")
        assert "alpha.mp3" in text

    def test_update_status_noop_without_song(self, audio_ctx):
        # No current song -> the label is left untouched (no config write).
        player = MagicMock(name="mp3_player", current_song=None)
        self.gui.player = player
        self.gui._update_status()
        self.gui.status_label.config.assert_not_called()

    def test_on_track_select_sets_index(self):
        # Clicking a listbox entry stores that entry's index as the current.
        self.gui.track_listbox.curselection.return_value = (3,)
        self.gui._on_track_select(None)
        assert self.gui.current_idx == 3

    def test_on_track_select_ignores_empty_selection(self):
        # A deselection event (empty tuple) keeps the existing index.
        self.gui.track_listbox.curselection.return_value = ()
        self.gui._on_track_select(None)
        assert self.gui.current_idx == 0

    def test_main_entry_point(self, audio_ctx):
        # main() builds a Tk root and hands control to mainloop().
        self.gui_mod.main()
        self.gui_mod.tk.Tk.return_value.mainloop.assert_called_once()

    def test_main_guard_executes(self, audio_ctx):
        # The bottom `if __name__ == "__main__"` reaches main() without error.
        import runpy
        runpy.run_path(str(MP3_GUI_PATH), run_name="__main__")


class TestWAVGUI:

    @pytest.fixture(autouse=True)
    def _build(self, audio_ctx):
        self.gui_mod = _load_gui_module(WAV_GUI_PATH, "wav_gui_player")
        self.root = MagicMock(name="root")
        self.gui = self.gui_mod.WAVGUIPlayer(self.root)

    def test_window_configuration(self):
        # Mirror of the MP3 window check: fixed WAV title and geometry.
        self.root.title.assert_called_once_with("WAV GUI Player")
        self.root.geometry.assert_called_once_with("500x450")

    def test_select_folder_returns_early_without_choice(self):
        # Cancelling the folder dialog (empty string) leaves the player None.
        self.gui_mod.filedialog.askdirectory.return_value = ""
        self.gui._select_folder()
        assert self.gui.player is None

    def test_select_folder_populates_track_list(self, audio_ctx):
        # Folder with files -> WAVAudioPlayer built, one listbox row per track.
        self.gui_mod.filedialog.askdirectory.return_value = "/songs"
        with patch.object(
            self.gui_mod.WAVAudioPlayer, "get_wav_files", return_value=["alpha.wav", "beta.wav"]
        ):
            self.gui._select_folder()

        assert self.gui.player is not None
        assert self.gui.track_listbox.insert.call_count == 2
        self.gui.status_label.config.assert_called()

    def test_select_folder_reporting_error_for_empty_folder(self, audio_ctx):
        # Mirror of the MP3 test: an empty .wav folder pops a messagebox
        # error via the showerror branch instead of building a player.
        self.gui_mod.filedialog.askdirectory.return_value = "/empty/songs"
        with patch.object(
            self.gui_mod.WAVAudioPlayer, "get_wav_files", return_value=[]
        ):
            self.gui_mod.messagebox.showerror = MagicMock()
            self.gui._select_folder()

        assert self.gui_mod.messagebox.showerror.call_count == 1

    def test_playback_controls_guard_without_player(self):
        # Same no-player guard as the MP3 UI: buttons are safe to click.
        self.gui.player = None
        self.gui.wav_files = []
        self.gui._play()
        self.gui._forward()
        self.gui._backward()

    def test_transport_controls_delegate_to_player(self, audio_ctx):
        # Buttons delegate into the real player methods via the pygame mock.
        player = MagicMock(name="wav_player", current_song="alpha.wav", status="Active")
        self.gui.player = player
        self.gui.wav_files = ["alpha.wav", "beta.wav"]
        self.gui.current_idx = 0

        self.gui._play(); player.play.assert_called()
        self.gui._pause(); player.pause.assert_called()
        self.gui._resume(); player.resume.assert_called()
        self.gui._stop(); player.stop_music_file.assert_called()

    def test_track_skip_updates_current_index(self, audio_ctx):
        # forward()/backward() return the target index and the listbox
        # selection tracks it.
        player = MagicMock(name="wav_player", current_song="alpha.wav", status="Active")
        player.forward.return_value = 1
        player.backward.return_value = 0
        self.gui.player = player
        self.gui.wav_files = ["alpha.wav", "beta.wav"]

        self.gui._forward()
        assert self.gui.current_idx == 1
        self.gui.track_listbox.selection_set.assert_called_with(1)

        self.gui._backward()
        assert self.gui.current_idx == 0

    def test_toggle_callbacks_sync_checkbox_var(self, audio_ctx):
        # WAV UI has only loop/shuffle toggles; each reads its BooleanVar's
        # fixed return and pushes it into the player attributes.
        player = MagicMock(name="wav_player", current_song="alpha.wav", status="Active")
        self.gui.player = player
        self.gui.loop_track_var.get.return_value = True
        self.gui.shuffle_var.get.return_value = True

        self.gui._toggle_loop_track()
        assert player.loop_track is True
        self.gui._toggle_shuffle()
        assert player.shuffle is True

    def test_toggle_loop_playlist_syncs_checkbox_var(self, audio_ctx):
        # The Loop Playlist toggle existed but was never exercised; under the
        # BooleanVar mock any var object drives it, so read loop_playlist_var
        # and confirm the player flag follows.
        player = MagicMock(name="wav_player", current_song="alpha.wav", status="Active")
        self.gui.player = player
        self.gui.loop_playlist_var.get.return_value = True

        self.gui._toggle_loop_playlist()
        assert player.loop_playlist is True

    def test_update_status_displays_now_playing(self, audio_ctx):
        # Status label shows the current track name, same as the MP3 UI.
        player = MagicMock(name="wav_player", current_song="alpha.wav", status="Active")
        self.gui.player = player
        self.gui._update_status()
        text = self.gui.status_label.config.call_args[1].get("text", "")
        assert "alpha.wav" in text

    def test_on_track_select_sets_index(self):
        # Mirror of the MP3 test: clicking a listbox entry stores the index.
        self.gui.track_listbox.curselection.return_value = (3,)
        self.gui._on_track_select(None)
        assert self.gui.current_idx == 3

    def test_on_track_select_ignores_empty_selection(self):
        # A deselection event (empty tuple) keeps the existing index.
        self.gui.track_listbox.curselection.return_value = ()
        self.gui._on_track_select(None)
        assert self.gui.current_idx == 0

    def test_main_entry_point(self, audio_ctx):
        # main() starts the Tk event loop.
        self.gui_mod.main()
        self.gui_mod.tk.Tk.return_value.mainloop.assert_called_once()

    def test_main_guard_executes(self, audio_ctx):
        # The __main__ guard reaches main() without error.
        import runpy
        runpy.run_path(str(WAV_GUI_PATH), run_name="__main__")

