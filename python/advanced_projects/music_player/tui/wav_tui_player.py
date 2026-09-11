import os
import random
import sys
import time

# Suppress Pygame support prompt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

try:
    import pygame
except (ImportError, ModuleNotFoundError):
    print("Error: 'pygame' module is not installed. Please run 'pip install pygame-ce'.")
    sys.exit(1)

TOTAL_WIDTH = 60


def display_tui_banner(title):
    """Renders a structured ASCII box banner with heading text centred across 60 characters."""
    print("=" * TOTAL_WIDTH)
    print(title.center(TOTAL_WIDTH))
    print("=" * TOTAL_WIDTH)


def display_info_box(lines, prepend_newline=False):
    """Renders a dynamically bordered panel fitted to the longest string in the lines list."""
    max_len = max(len(line) for line in lines)
    border = "-" * (max_len + 4)

    if prepend_newline:
        print(f"\n{border}")
    else:
        print(border)

    for line in lines:
        print(f"| {line.ljust(max_len)} |")

    print(border)


class WAVAudioPlayer:
    """Handles Pygame mixer audio operations, stream tracking, and playback states."""

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.current_song = None
        self.current_track_num = None
        self.is_paused = False
        self.status = "Stopped"
        self.loop_track = False
        self.loop_playlist = False
        self.shuffle = False

        try:
            pygame.mixer.init()
        except pygame.error as e:
            display_info_box([f"[X] Audio engine initialisation failed: {e}"], prepend_newline=True)

    def get_wav_files(self):
        """Retrieves a list of .wav files from the target directory."""
        if not os.path.isdir(self.folder_path):
            return []

        return [f for f in os.listdir(self.folder_path) if f.endswith(".wav")]

    def show_status(self):
        """Displays the updated track status info box."""
        if self.current_song and self.current_track_num is not None:
            track_loop_str = "ON" if self.loop_track else "OFF"
            playlist_loop_str = "ON" if self.loop_playlist else "OFF"
            shuffle_str = "ON" if self.shuffle else "OFF"

            display_info_box([
                f"Track Number  : {self.current_track_num}",
                f"Now Playing   : {self.current_song}",
                f"Status        : {self.status}",
                f"Loop Track    : {track_loop_str}",
                f"Loop Playlist : {playlist_loop_str}",
                f"Shuffle       : {shuffle_str}"
            ])

    def play(self, song_name, track_num=None):
        """Starts or plays the specified audio track."""
        file_path = os.path.join(self.folder_path, song_name)

        if not os.path.exists(file_path):
            display_info_box([f"[X] FileExistsError: Track '{song_name}' not found!"], prepend_newline=True)
            return False

        try:
            loops = -1 if self.loop_track else 0
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play(loops=loops)
            self.current_song = song_name
            self.current_track_num = track_num
            self.is_paused = False
            self.status = "Active Playing"

            display_info_box(["[P] Playing Music WAV Player"], prepend_newline=True)
            self.show_status()
            return True

        except pygame.error as e:
            display_info_box([f"[X] Playback Exception: {e}"], prepend_newline=True)
            return False

    def pause(self):
        """Pauses active audio playback."""
        if pygame.mixer.music.get_busy() and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.status = "Paused"
            display_info_box(["[||] Playback paused"], prepend_newline=True)
            self.show_status()
        else:
            display_info_box(["[!] Track is not actively playing or already paused."], prepend_newline=True)

    def resume(self):
        """Resumes / Continues playback from a paused state."""
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.status = "Active Playing"
            display_info_box(["[>] Playing Resumed"], prepend_newline=True)
            self.show_status()
        else:
            display_info_box(["[!] Track is not currently paused."], prepend_newline=True)

    def forward(self, wav_files, current_idx):
        """Skips forward by increasing playlist position index by +1 or picking a random track if shuffle is ON."""
        if not wav_files:
            display_info_box(["[!] Playlist is empty."], prepend_newline=True)
            return current_idx

        if self.shuffle and len(wav_files) > 1:
            available_indices = [i for i in range(len(wav_files)) if i != current_idx]
            next_idx = random.choice(available_indices)
        else:
            if current_idx + 1 >= len(wav_files) and not self.loop_playlist:
                display_info_box(["[!] End of playlist reached (Loop Playlist is OFF)."], prepend_newline=True)
                return current_idx
            next_idx = (current_idx + 1) % len(wav_files)

        display_info_box([f"[>>] Forward (-> Track {next_idx + 1})"], prepend_newline=True)
        self.play(wav_files[next_idx], track_num=next_idx + 1)
        return next_idx

    def backward(self, wav_files, current_idx):
        """Skips backward by decreasing playlist position index by -1 or picking a random track if shuffle is ON."""
        if not wav_files:
            display_info_box(["[!] Playlist is empty."], prepend_newline=True)
            return current_idx

        if self.shuffle and len(wav_files) > 1:
            available_indices = [i for i in range(len(wav_files)) if i != current_idx]
            prev_idx = random.choice(available_indices)
        else:
            if current_idx - 1 < 0 and not self.loop_playlist:
                display_info_box(["[!] Beginning of playlist reached (Loop Playlist is OFF)."], prepend_newline=True)
                return current_idx
            prev_idx = (current_idx - 1) % len(wav_files)

        display_info_box([f"[<<] Backward (-> Track {prev_idx + 1})"], prepend_newline=True)
        self.play(wav_files[prev_idx], track_num=prev_idx + 1)
        return prev_idx

    def restart(self):
        """Restarts / Starts the current track from the beginning."""
        if self.current_song:
            display_info_box(["[R] Restarting current track"], prepend_newline=True)
            self.play(self.current_song, track_num=self.current_track_num)
        else:
            display_info_box(["[!] No track selected to restart."], prepend_newline=True)

    def toggle_loop_track(self):
        """Toggles looping for the current single audio track."""
        self.loop_track = not self.loop_track
        state_str = "ENABLED" if self.loop_track else "DISABLED"
        display_info_box([f"[->-] Loop Single Track : {state_str}"], prepend_newline=True)
        if self.current_song and pygame.mixer.music.get_busy():
            loops = -1 if self.loop_track else 0
            pos = pygame.mixer.music.get_pos() / 1000.0
            pygame.mixer.music.play(loops=loops, start=max(0.0, pos))
        self.show_status()

    def toggle_loop_playlist(self):
        """Toggles continuous looping for the entire playlist."""
        self.loop_playlist = not self.loop_playlist
        state_str = "ENABLED" if self.loop_playlist else "DISABLED"
        display_info_box([f"[<=>] Loop Entire Playlist : {state_str}"], prepend_newline=True)
        self.show_status()

    def toggle_shuffle(self):
        """Toggles shuffle mode for random track selection."""
        self.shuffle = not self.shuffle
        state_str = "ENABLED" if self.shuffle else "DISABLED"
        display_info_box([f"[~?~] Shuffle Playback : {state_str}"], prepend_newline=True)
        self.show_status()

    def stop_music_file(self):
        """Stops active music file playback without shutting down the audio engine."""
        pygame.mixer.music.stop()
        self.is_paused = False
        self.status = "Stopped Playing"
        display_info_box(["[ STOP ] Stopped music file playback"], prepend_newline=True)
        self.show_status()

    def stop_music_player(self):
        """Shuts down the Pygame mixer engine entirely."""
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        display_info_box(["[X] Audio engine player shut down"], prepend_newline=True)


def wav_player():
    music_folder = r"C:\Users\A.I.M\C.S\WAV"
    player = WAVAudioPlayer(music_folder)

    display_tui_banner("WAV PLAYER")

    wav_files = player.get_wav_files()

    if not wav_files:
        display_info_box([f"[X] Error: No .wav files found in folder:\n{music_folder}"], prepend_newline=True)
        return

    display_info_box([
        f"Directory    : {music_folder}",
        f"Tracks Found : {len(wav_files)}"
    ])

    while True:
        print("\nAvailable Song List:")
        for idx, song in enumerate(wav_files, start=1):
            print(f"[{idx}] {song}")

        choice_input = input("\nEnter track number to play (or 'Q' to quit): ").strip()

        if choice_input.upper() == "Q":
            player.stop_music_player()
            display_info_box(["Shutting down WAV Player interface..."], prepend_newline=True)
            break

        if not choice_input.isdigit():
            display_info_box(["[X] Error: Please enter a valid numerical index."], prepend_newline=True)
            continue

        choice_idx = int(choice_input) - 1

        if not (0 <= choice_idx < len(wav_files)):
            display_info_box(["[X] Error: Selected track index out of range."], prepend_newline=True)
            continue

        player.play(wav_files[choice_idx], track_num=choice_idx + 1)

        # In-track control loop
        in_track_menu = True
        while in_track_menu:
            loop_track_status = "ON" if player.loop_track else "OFF"
            loop_playlist_status = "ON" if player.loop_playlist else "OFF"
            shuffle_status = "ON" if player.shuffle else "OFF"

            print(f"\nSelect Music Control Action (Track #{choice_idx + 1}):")
            print("[1] Play / Start")
            print("[2] Pause")
            print("[3] Resume / Continue")
            print("[4] Forward (+1 Song / Next Track)")
            print("[5] Backward (-1 Song / Previous Track)")
            print("[6] Restart / Start")
            print(f"[7] Toggle Loop Track (Currently: {loop_track_status})")
            print(f"[8] Toggle Loop Playlist (Currently: {loop_playlist_status})")
            print(f"[9] Toggle Shuffle (Currently: {shuffle_status})")
            print("[10] Stop Music File")
            print("[11] Return to Track Selection Menu")
            print("[0] Quit Player")

            cmd = input("\nEnter choice (0-11): ").strip()

            match cmd:
                case "1":
                    player.play(wav_files[choice_idx], track_num=choice_idx + 1)

                case "2":
                    player.pause()

                case "3":
                    player.resume()

                case "4":
                    choice_idx = player.forward(wav_files, choice_idx)

                case "5":
                    choice_idx = player.backward(wav_files, choice_idx)

                case "6":
                    player.restart()

                case "7":
                    player.toggle_loop_track()

                case "8":
                    player.toggle_loop_playlist()

                case "9":
                    player.toggle_shuffle()

                case "10":
                    player.stop_music_file()

                case "11":
                    player.stop_music_file()
                    in_track_menu = False

                case "0":
                    player.stop_music_player()
                    display_info_box(["Shutting down WAV Player interface..."], prepend_newline=True)
                    return

                case _:
                    display_info_box(["[X] Invalid choice! Please enter an option from 0 to 11."], prepend_newline=True)


if __name__ == "__main__":
    try:
        wav_player()
    except KeyboardInterrupt:
        print(f"\n\n{'=' * TOTAL_WIDTH}")
        print("[!] WAV player session terminated by user.".center(TOTAL_WIDTH))
        print("Have a great day!".center(TOTAL_WIDTH))
        print("=" * TOTAL_WIDTH)

