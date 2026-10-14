"""
Tests for the GUI music players (gui/mp3_gui_player.py, gui/wav_gui_player.py).

Covers:
  * Window configuration and initial state
  * Folder selection (populates track list, empty-folder error, cancel)
  * Guarded playback controls (safe without active player)
  * Transport delegation to the TUI audio engine
  * Track skipping and listbox selection sync
  * Checkbox toggle syncing (loop track, loop playlist, shuffle)
  * Status label updates
  * Track selection via listbox
  * Main entry point and __main__ guard
"""


from unittest.mock import MagicMock, patch

import pytest

from tests.test_advanced_projects.music_player.conftest import (
    MP3_GUI_PATH,
    WAV_GUI_PATH,
    load_gui_module,
)


class TestMP3GUI:
    """
    The MP3 pygame GUI - window setup, folder selection, guarded playback and
    transport controls, track skipping, loop/playlist checkbox syncing,
    status updates and the main guard.
    """

    @pytest.fixture(autouse=True)
    def _build(self, audio_ctx):
        self.gui_mod = load_gui_module(MP3_GUI_PATH, "mp3_gui_player")
        self.root = MagicMock(name="root")
        self.gui = self.gui_mod.MP3GUIPlayer(self.root)

    def test_window_configuration(self):
        self.root.title.assert_called_once_with("MP3 GUI Player")
        self.root.geometry.assert_called_once_with("500x450")

    def test_player_starts_uninitialised(self):
        assert self.gui.player is None
        assert self.gui.mp3_files == []
        assert self.gui.current_idx == 0

    def test_transport_and_toggle_handlers_are_safe_with_no_active_player(self):
        """
        All six `if self.player:` guards in the transport and checkbox-sync
        handlers short-circuit into a harmless no-op when no folder is chosen.
        """
        assert self.gui.player is None

        self.gui._pause()
        self.gui._resume()
        self.gui._stop()
        self.gui._toggle_loop_track()
        self.gui._toggle_loop_playlist()
        self.gui._toggle_shuffle()

        assert self.gui.player is None

    def test_select_folder_returns_early_without_choice(self):
        self.gui_mod.filedialog.askdirectory.return_value = ""
        self.gui._select_folder()
        assert self.gui.player is None

    def test_select_folder_reporting_error_for_empty_folder(self, audio_ctx):
        get_dir = self.gui_mod.filedialog.askdirectory
        get_dir.return_value = "/empty/songs"

        with patch.object(
            self.gui_mod.MP3AudioPlayer, "get_mp3_files", return_value=[]
        ):
            self.gui_mod.messagebox.showerror = MagicMock()
            self.gui._select_folder()

        assert self.gui_mod.messagebox.showerror.call_count == 1

    def test_select_folder_populates_track_list(self, audio_ctx):
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
        self.gui.player = None
        self.gui.mp3_files = []
        self.gui._play()
        self.gui._forward()
        self.gui._backward()

    def test_transport_controls_delegate_to_player(self, audio_ctx):
        player = MagicMock(name="mp3_player", current_song="alpha.mp3", status="Active")
        self.gui.player = player
        self.gui.mp3_files = ["alpha.mp3", "beta.mp3"]
        self.gui.current_idx = 0

        self.gui._play(); player.play.assert_called()
        self.gui._pause(); player.pause.assert_called()
        self.gui._resume(); player.resume.assert_called()
        self.gui._stop(); player.stop_music_file.assert_called()

    def test_track_skip_updates_current_index(self, audio_ctx):
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
        player = MagicMock(name="mp3_player", current_song="alpha.mp3", status="Active")
        self.gui.player = player
        self.gui._update_status()
        text = self.gui.status_label.config.call_args[1].get("text", "")
        assert "alpha.mp3" in text

    def test_update_status_noop_without_song(self, audio_ctx):
        player = MagicMock(name="mp3_player", current_song=None)
        self.gui.player = player
        self.gui._update_status()
        self.gui.status_label.config.assert_not_called()

    def test_on_track_select_sets_index(self):
        self.gui.track_listbox.curselection.return_value = (3,)
        self.gui._on_track_select(None)
        assert self.gui.current_idx == 3

    def test_on_track_select_ignores_empty_selection(self):
        self.gui.track_listbox.curselection.return_value = ()
        self.gui._on_track_select(None)
        assert self.gui.current_idx == 0

    def test_window_is_not_resizable(self):
        self.root.resizable.assert_called_once_with(False, False)

    def test_play_passes_the_selected_track_and_its_number(self, audio_ctx):
        player = MagicMock(name="mp3_player", current_song="alpha.mp3", status="Active")
        self.gui.player = player
        self.gui.mp3_files = ["alpha.mp3", "beta.mp3"]
        self.gui.current_idx = 0

        self.gui._play()

        player.play.assert_called_once_with("alpha.mp3", track_num=1)

    def test_play_targets_the_track_chosen_in_the_listbox(self, audio_ctx):
        """
        _on_track_select changes which track _play() plays, so the two must
        be pinned together rather than only the index in isolation.
        """
        player = MagicMock(name="mp3_player", current_song="beta.mp3", status="Active")
        self.gui.player = player
        self.gui.mp3_files = ["alpha.mp3", "beta.mp3"]
        self.gui.track_listbox.curselection.return_value = (1,)
        self.gui._on_track_select(None)

        self.gui._play()

        player.play.assert_called_once_with("beta.mp3", track_num=2)

    def test_pause_refreshes_the_status_label(self, audio_ctx):
        player = MagicMock(name="mp3_player", current_song="alpha.mp3", status="Active")
        self.gui.player = player

        self.gui._pause()

        player.pause.assert_called_once_with()
        self.gui.status_label.config.assert_called()

    def test_stop_refreshes_the_status_label(self, audio_ctx):
        player = MagicMock(name="mp3_player", current_song="alpha.mp3", status="Active")
        self.gui.player = player

        self.gui._stop()

        player.stop_music_file.assert_called_once_with()
        self.gui.status_label.config.assert_called()

    def test_select_folder_numbers_the_track_rows(self, audio_ctx):
        """
        The listbox rows are numbered from 1, not 0, so the row text is the
        only place an off-by-one in the enumerate start would show.
        """
        self.gui_mod.filedialog.askdirectory.return_value = "/songs"
        with patch.object(
            self.gui_mod.MP3AudioPlayer, "get_mp3_files",
            return_value=["alpha.mp3", "beta.mp3"],
        ):
            self.gui._select_folder()

        rows = [call.args[1] for call in self.gui.track_listbox.insert.call_args_list]
        assert rows == ["[1] alpha.mp3", "[2] beta.mp3"]

    def test_main_entry_point(self, audio_ctx):
        self.gui_mod.launch_mp3_player()
        self.gui_mod.tk.Tk.return_value.mainloop.assert_called_once()

    def test_main_guard_executes(self, audio_ctx):
        import runpy
        runpy.run_path(str(MP3_GUI_PATH), run_name="__main__")


class TestWAVGUI:
    """
    The WAV pygame GUI - the same window, folder, playback, transport, track
    and status behaviour as the MP3 player, with its own checkbox syncing.
    """

    @pytest.fixture(autouse=True)
    def _build(self, audio_ctx):
        self.gui_mod = load_gui_module(WAV_GUI_PATH, "wav_gui_player")
        self.root = MagicMock(name="root")
        self.gui = self.gui_mod.WAVGUIPlayer(self.root)

    def test_window_configuration(self):
        self.root.title.assert_called_once_with("WAV GUI Player")
        self.root.geometry.assert_called_once_with("500x450")

    def test_select_folder_returns_early_without_choice(self):
        self.gui_mod.filedialog.askdirectory.return_value = ""
        self.gui._select_folder()
        assert self.gui.player is None

    def test_select_folder_populates_track_list(self, audio_ctx):
        self.gui_mod.filedialog.askdirectory.return_value = "/songs"
        with patch.object(
            self.gui_mod.WAVAudioPlayer, "get_wav_files", return_value=["alpha.wav", "beta.wav"]
        ):
            self.gui._select_folder()

        assert self.gui.player is not None
        assert self.gui.track_listbox.insert.call_count == 2
        self.gui.status_label.config.assert_called()

    def test_select_folder_reporting_error_for_empty_folder(self, audio_ctx):
        self.gui_mod.filedialog.askdirectory.return_value = "/empty/songs"
        with patch.object(
            self.gui_mod.WAVAudioPlayer, "get_wav_files", return_value=[]
        ):
            self.gui_mod.messagebox.showerror = MagicMock()
            self.gui._select_folder()

        assert self.gui_mod.messagebox.showerror.call_count == 1

    def test_playback_controls_guard_without_player(self):
        self.gui.player = None
        self.gui.wav_files = []
        self.gui._play()
        self.gui._forward()
        self.gui._backward()

    def test_transport_and_toggle_handlers_are_safe_with_no_active_player(self):
        """
        The six `if self.player:` guards in the transport and checkbox-sync
        handlers and _update_status()'s `if self.player and
        self.player.current_song:` all stay silent no-ops without a player.
        """
        self.gui.player = None
        self.gui.wav_files = []

        self.gui._pause()
        self.gui._resume()
        self.gui._stop()
        self.gui._toggle_loop_track()
        self.gui._toggle_loop_playlist()
        self.gui._toggle_shuffle()
        self.gui._update_status()

        assert self.gui.player is None

    def test_transport_controls_delegate_to_player(self, audio_ctx):
        player = MagicMock(name="wav_player", current_song="alpha.wav", status="Active")
        self.gui.player = player
        self.gui.wav_files = ["alpha.wav", "beta.wav"]
        self.gui.current_idx = 0

        self.gui._play(); player.play.assert_called()
        self.gui._pause(); player.pause.assert_called()
        self.gui._resume(); player.resume.assert_called()
        self.gui._stop(); player.stop_music_file.assert_called()

    def test_track_skip_updates_current_index(self, audio_ctx):
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
        player = MagicMock(name="wav_player", current_song="alpha.wav", status="Active")
        self.gui.player = player
        self.gui.loop_track_var.get.return_value = True
        self.gui.shuffle_var.get.return_value = True

        self.gui._toggle_loop_track()
        assert player.loop_track is True
        self.gui._toggle_shuffle()
        assert player.shuffle is True

    def test_toggle_loop_playlist_syncs_checkbox_var(self, audio_ctx):
        """
        The Loop Playlist toggle reads its BooleanVar and pushes the value
        into the player's loop_playlist flag.
        """
        player = MagicMock(name="wav_player", current_song="alpha.wav", status="Active")
        self.gui.player = player
        self.gui.loop_playlist_var.get.return_value = True

        self.gui._toggle_loop_playlist()
        assert player.loop_playlist is True

    def test_update_status_displays_now_playing(self, audio_ctx):
        player = MagicMock(name="wav_player", current_song="alpha.wav", status="Active")
        self.gui.player = player
        self.gui._update_status()
        text = self.gui.status_label.config.call_args[1].get("text", "")
        assert "alpha.wav" in text

    def test_on_track_select_sets_index(self):
        self.gui.track_listbox.curselection.return_value = (3,)
        self.gui._on_track_select(None)
        assert self.gui.current_idx == 3

    def test_on_track_select_ignores_empty_selection(self):
        self.gui.track_listbox.curselection.return_value = ()
        self.gui._on_track_select(None)
        assert self.gui.current_idx == 0

    def test_window_is_not_resizable(self):
        self.root.resizable.assert_called_once_with(False, False)

    def test_play_passes_the_selected_track_and_its_number(self, audio_ctx):
        player = MagicMock(name="wav_player", current_song="alpha.wav", status="Active")
        self.gui.player = player
        self.gui.wav_files = ["alpha.wav", "beta.wav"]
        self.gui.current_idx = 0

        self.gui._play()

        player.play.assert_called_once_with("alpha.wav", track_num=1)

    def test_play_targets_the_track_chosen_in_the_listbox(self, audio_ctx):
        """
        _on_track_select changes which track _play() plays, so the two must
        be pinned together rather than only the index in isolation.
        """
        player = MagicMock(name="wav_player", current_song="beta.wav", status="Active")
        self.gui.player = player
        self.gui.wav_files = ["alpha.wav", "beta.wav"]
        self.gui.track_listbox.curselection.return_value = (1,)
        self.gui._on_track_select(None)

        self.gui._play()

        player.play.assert_called_once_with("beta.wav", track_num=2)

    def test_pause_refreshes_the_status_label(self, audio_ctx):
        player = MagicMock(name="wav_player", current_song="alpha.wav", status="Active")
        self.gui.player = player

        self.gui._pause()

        player.pause.assert_called_once_with()
        self.gui.status_label.config.assert_called()

    def test_stop_refreshes_the_status_label(self, audio_ctx):
        player = MagicMock(name="wav_player", current_song="alpha.wav", status="Active")
        self.gui.player = player

        self.gui._stop()

        player.stop_music_file.assert_called_once_with()
        self.gui.status_label.config.assert_called()

    def test_select_folder_numbers_the_track_rows(self, audio_ctx):
        """
        The listbox rows are numbered from 1, not 0, so the row text is the
        only place an off-by-one in the enumerate start would show.
        """
        self.gui_mod.filedialog.askdirectory.return_value = "/songs"
        with patch.object(
            self.gui_mod.WAVAudioPlayer, "get_wav_files",
            return_value=["alpha.wav", "beta.wav"],
        ):
            self.gui._select_folder()

        rows = [call.args[1] for call in self.gui.track_listbox.insert.call_args_list]
        assert rows == ["[1] alpha.wav", "[2] beta.wav"]

    def test_main_entry_point(self, audio_ctx):
        self.gui_mod.launch_wav_player()
        self.gui_mod.tk.Tk.return_value.mainloop.assert_called_once()

    def test_main_guard_executes(self, audio_ctx):
        import runpy
        runpy.run_path(str(WAV_GUI_PATH), run_name="__main__")

