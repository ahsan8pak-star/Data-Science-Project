"""
Tests for the TUI music players (tui/mp3_tui_player.py, tui/wav_tui_player.py).

Covers:
  * Pure rendering helpers (display_tui_banner, display_info_box)
  * MP3AudioPlayer / WAVAudioPlayer engine behaviour
  * Console entry points (empty-folder guard, pygame import fallback)
  * Interactive menu loops (full cycle, error paths, KeyboardInterrupt)
"""

from unittest.mock import patch

import pytest

from tests.test_advanced_projects.music_player.conftest import (
    MP3_TUI,
    MP3_TUI_PATH,
    WAV_TUI,
    WAV_TUI_PATH,
)


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


class TestAudioPlayers:
    """
    Shared behaviour across the MP3 and WAV engine classes.
    """

    def test_init_sets_default_state(self, players):
        for player in players.values():
            assert player.loop_track is False
            assert player.loop_playlist is False
            assert player.shuffle is False
            assert player.status == "Stopped"
            assert player.current_song is None

    def test_get_files_filters_by_extension(self, players):
        """
        [AI] Compares sorted, not raw order. `get_mp3_files()` returns
        `os.listdir()` filtered, and listdir order is a filesystem artefact,
        not a contract: NTFS returns alpha before beta, ext4 returns beta
        before alpha. Asserting the raw list made this case pass on Windows
        and fail on Linux for a reason that has nothing to do with the
        filtering it is supposed to check.
        """
        methods = {"mp3": "get_mp3_files", "wav": "get_wav_files"}
        expected = {
            "mp3": ["alpha.mp3", "beta.mp3"],
            "wav": ["alpha.wav", "beta.wav"],
        }
        for extension, player in players.items():
            found = getattr(player, methods[extension])()
            assert sorted(found) == expected[extension]

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

        music = audio_ctx["pygame"].mixer.music
        assert music.play.call_count == 2

    def test_pause_when_idle_reports_not_playing(self, players, audio_ctx, capsys):
        audio_ctx["pygame"].mixer.music.get_busy.return_value = False
        for player in players.values():
            player.pause()
        assert "Track is not actively playing or already paused." in capsys.readouterr().out

    def test_resume_without_a_pause_reports_not_paused(self, players, capsys):
        for player in players.values():
            player.resume()
        assert "Track is not currently paused." in capsys.readouterr().out

    def test_backward_at_start_respects_loop_playlist_off(self, players, capsys):
        for extension, player in players.items():
            files = [f"alpha.{extension}"]
            assert player.backward(files, 0) == 0
        assert "Beginning of playlist reached" in capsys.readouterr().out

    def test_restart_with_no_selected_track_reports(self, players, capsys):
        for player in players.values():
            assert player.current_song is None
            player.restart()
        assert "No track selected to restart." in capsys.readouterr().out

    @pytest.mark.parametrize(
        "path,player_cls",
        [(MP3_TUI, "MP3AudioPlayer"), (WAV_TUI, "WAVAudioPlayer")],
    )
    def test_init_reporting_audio_engine_failure(self, audio_ctx, capsys, path, player_cls):
        audio_ctx["pygame"].mixer.init.side_effect = RuntimeError("no sound device")
        from tests.test_advanced_projects.conftest import load_module
        mod = load_module(path)
        getattr(mod, player_cls)("C:/missing")
        assert "[X] Audio engine initialisation failed: no sound device" in capsys.readouterr().out

    @pytest.mark.parametrize(
        "path,player_cls",
        [(MP3_TUI, "MP3AudioPlayer"), (WAV_TUI, "WAVAudioPlayer")],
    )
    def test_play_reporting_playback_exception(self, audio_ctx, tmp_path, capsys, path, player_cls):
        audio_ctx["pygame"].mixer.music.play.side_effect = RuntimeError("decode failed")
        song = tmp_path / "alpha.mp3"
        song.write_bytes(b"")
        from tests.test_advanced_projects.conftest import load_module
        mod = load_module(path)
        player = getattr(mod, player_cls)(str(tmp_path))
        assert player.play(song.name) is False
        assert "[X] Playback Exception: decode failed" in capsys.readouterr().out


class TestTuiEntryPoints:
    """
    Console entry points for both players - the empty-folder error
    report and the import fallback taken when pygame is absent.
    """

    @pytest.fixture(autouse=True)
    def _load(self, audio_ctx, tui_modules):
        self.mp3 = tui_modules["mp3"]
        self.wav = tui_modules["wav"]

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


class TestTuiMenuLoops:
    """
    The interactive menu loop of each console player - a full cycle, the
    error and shuffle paths, and KeyboardInterrupt caught by the main guard.
    """

    @pytest.fixture(autouse=True)
    def _load(self, audio_ctx, tui_modules):
        self.mp3 = tui_modules["mp3"]
        self.wav = tui_modules["wav"]

    @pytest.fixture()
    def songs(self):
        return ["alpha.mp3", "beta.mp3"]

    @pytest.fixture()
    def menu_path(self, songs):
        return ["1", "1", "2", "3", "4", "6", "7", "8", "9", "10", "11", "Q"]

    def test_mp3_full_menu_cycle(self, menu_path, songs, audio_ctx, capsys):
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
        assert "Shutdown WAV Player interface..." not in out
        assert "Shutting down WAV Player interface..." in out

    def test_mp3_error_paths_and_shuffle(self, songs, capsys):
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
        assert "Forward (-> Track 1)" in out
        assert "Backward (-> Track 2)" in out
        assert "Invalid choice" in out
        assert "Audio engine player shut down" in out

    def test_wav_error_paths_and_shuffle(self, songs, capsys):
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
        import runpy

        with patch("os.path.isdir", return_value=True), \
                patch("os.listdir", return_value=["alpha.mp3", "beta.mp3"]), \
                patch("builtins.input", side_effect=KeyboardInterrupt()):
            runpy.run_path(str(MP3_TUI_PATH), run_name="__main__")

        out = capsys.readouterr().out
        assert "MP3 player session terminated by user." in out

    def test_wav_main_guard_catches_keyboard_interrupt(self, audio_ctx, capsys):
        import runpy

        with patch("os.path.isdir", return_value=True), \
                patch("os.listdir", return_value=["alpha.wav", "beta.wav"]), \
                patch("builtins.input", side_effect=KeyboardInterrupt()):
            runpy.run_path(str(WAV_TUI_PATH), run_name="__main__")

        out = capsys.readouterr().out
        assert "WAV player session terminated by user." in out

