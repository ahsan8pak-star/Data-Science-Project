import os  # Standard library: file path operations and directory resolution
import sys  # Standard library: modifies sys.path to locate tui modules
import tkinter as tk  # Standard library: GUI toolkit for building the player window
from tkinter import filedialog, messagebox  # Standard library: file browser dialog and popup alerts

# Builds the absolute path to the sibling tui/ folder so Python can locate it at runtime
_tui_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tui"))
sys.path.insert(0, _tui_dir)

# import tui/mp3_tui_player.py: provides MP3AudioPlayer class with play(), pause(), resume(),
# forward(), backward(), restart(), stop_music_file(), stop_music_player(),
# toggle_loop_track(), toggle_loop_playlist(), toggle_shuffle(), get_mp3_files(), show_status()

from mp3_tui_player import MP3AudioPlayer  # import tui/mp3_tui_player.py: the core audio engine class


class MP3GUIPlayer:
    """(AI) Main GUI window wrapping the TUI MP3AudioPlayer in a tkinter interface."""

    def __init__(self, root):
        """(AI) Initialises the main window and instance state."""
        self.root = root
        self.root.title("MP3 GUI Player")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        self.player = None          # (AI) Holds the MP3AudioPlayer instance once a folder is selected
        self.mp3_files = []         # (AI) List of .mp3 filenames loaded from the chosen directory
        self.current_idx = 0        # (AI) Index of the currently selected/playing track

        self._build_ui()            # (AI) Delegates all widget creation to the layout method below

    def _build_ui(self):
        """(AI) Constructs and packs all GUI widgets into the root window."""

        # Folder selection area: a frame containing a label and a button to open the directory picker
        folder_frame = tk.Frame(self.root, pady=10)
        folder_frame.pack(fill=tk.X)

        self.folder_label = tk.Label(folder_frame, text="No folder selected", wraplength=460)  # Displays the currently selected folder path
        self.folder_label.pack()

        tk.Button(folder_frame, text="Select MP3 Folder", command=self._select_folder).pack()  # Button that triggers _select_folder()

        # Track listbox area: a scrollable list showing all discovered .mp3 files
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        self.track_listbox = tk.Listbox(list_frame, height=10)  # Scrollable listbox showing all discovered .mp3 files
        self.track_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame, command=self.track_listbox.yview)  # Vertical scrollbar paired with the listbox
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.track_listbox.config(yscrollcommand=scrollbar.set)
        self.track_listbox.bind("<<ListboxSelect>>", self._on_track_select)  # Binds selection event to _on_track_select()

        self.status_label = tk.Label(self.root, text="", pady=5)  # Status label showing now-playing info
        self.status_label.pack()

        # Transport control buttons: each calls a method that delegates to the corresponding TUI player function
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack()

        tk.Button(control_frame, text="<<", width=5, command=self._backward).grid(row=0, column=0, padx=2)    # calls player.backward()
        tk.Button(control_frame, text="Play", width=5, command=self._play).grid(row=0, column=1, padx=2)      # calls player.play()
        tk.Button(control_frame, text="Pause", width=5, command=self._pause).grid(row=0, column=2, padx=2)    # calls player.pause()
        tk.Button(control_frame, text="Resume", width=5, command=self._resume).grid(row=0, column=3, padx=2)  # calls player.resume()
        tk.Button(control_frame, text=">>", width=5, command=self._forward).grid(row=0, column=4, padx=2)     # calls player.forward()
        tk.Button(control_frame, text="Stop", width=5, command=self._stop).grid(row=0, column=5, padx=2)      # calls player.stop_music_file()

        # Toggle checkboxes for loop and shuffle: BooleanVar instances sync checkbox state with player attributes
        toggle_frame = tk.Frame(self.root, pady=5)
        toggle_frame.pack()

        self.loop_track_var = tk.BooleanVar()       # Boolean variable bound to Loop Track checkbox
        self.loop_playlist_var = tk.BooleanVar()    # Boolean variable bound to Loop Playlist checkbox
        self.shuffle_var = tk.BooleanVar()          # Boolean variable bound to Shuffle checkbox

        tk.Checkbutton(toggle_frame, text="Loop Track", variable=self.loop_track_var, command=self._toggle_loop_track).grid(row=0, column=0, padx=5)        # toggles player.loop_track
        tk.Checkbutton(toggle_frame, text="Loop Playlist", variable=self.loop_playlist_var, command=self._toggle_loop_playlist).grid(row=0, column=1, padx=5)  # toggles player.loop_playlist
        tk.Checkbutton(toggle_frame, text="Shuffle", variable=self.shuffle_var, command=self._toggle_shuffle).grid(row=0, column=2, padx=5)                    # toggles player.shuffle

    def _select_folder(self):
        """(AI) Opens a directory chooser and populates the track list."""

        folder = filedialog.askdirectory(title="Select MP3 Folder")  # Opens native directory picker dialog
        if not folder:
            return

        self.player = MP3AudioPlayer(folder)          # import tui/mp3_tui_player.py: creates a new player instance for the chosen folder
        self.mp3_files = self.player.get_mp3_files()  # import tui/mp3_tui_player.py: returns a list of .mp3 filenames in the folder

        self.folder_label.config(text=folder)         # Updates the label to show the selected folder path
        self.track_listbox.delete(0, tk.END)          # Clears the listbox before repopulating

        if not self.mp3_files:                        # Shows an error popup if no .mp3 files are found
            messagebox.showerror("Error", f"No .mp3 files found in:\n{folder}")
            return

        for idx, song in enumerate(self.mp3_files, start=1):  # Populates the listbox with numbered track names
            self.track_listbox.insert(tk.END, f"[{idx}] {song}")

        self.status_label.config(text=f"Tracks found: {len(self.mp3_files)}")  # Updates the status label with track count

    def _on_track_select(self, event):
        """(AI) Callback fired when a listbox item is clicked."""
        selection = self.track_listbox.curselection()  # Returns the tuple of selected item indices
        if selection:
            self.current_idx = selection[0]  # Sets current_idx to the selected track index

    def _play(self):
        """(AI) Plays the currently selected track."""

        if not self.player or not self.mp3_files:
            return

        self.player.play(self.mp3_files[self.current_idx], track_num=self.current_idx + 1)  # import tui/mp3_tui_player.py: loads and plays the .mp3 file via pygame.mixer
        self._update_status()  # Refreshes the status label after playback starts

    def _pause(self):
        """(AI) Pauses the active track."""

        if self.player:
            self.player.pause()  # import tui/mp3_tui_player.py: pauses playback via pygame.mixer.music.pause()
            self._update_status()

    def _resume(self):
        """(AI) Resumes a paused track."""

        if self.player:
            self.player.resume()  # import tui/mp3_tui_player.py: unpauses playback via pygame.mixer.music.unpause()
            self._update_status()

    def _forward(self):
        """(AI) Skips to the next track (or random if shuffle is ON)."""

        if not self.player or not self.mp3_files:
            return

        self.current_idx = self.player.forward(self.mp3_files, self.current_idx)  # import tui/mp3_tui_player.py: increments index (+1) or picks random if shuffle
        self.track_listbox.selection_clear(0, tk.END)   # Clears the current listbox highlight
        self.track_listbox.selection_set(self.current_idx)  # Highlights the newly selected track
        self._update_status()

    def _backward(self):
        """(AI) Skips to the previous track (or random if shuffle is ON)."""

        if not self.player or not self.mp3_files:
            return

        self.current_idx = self.player.backward(self.mp3_files, self.current_idx)  # import tui/mp3_tui_player.py: decrements index (-1) or picks random if shuffle
        self.track_listbox.selection_clear(0, tk.END)   # Clears the current listbox highlight
        self.track_listbox.selection_set(self.current_idx)  # Highlights the newly selected track
        self._update_status()

    def _stop(self):
        """(AI) Stops the current track playback."""

        if self.player:
            self.player.stop_music_file()  # import tui/mp3_tui_player.py: stops playback via pygame.mixer.music.stop()
            self._update_status()

    def _toggle_loop_track(self):
        """(AI) Syncs the Loop Track checkbox state to the player."""

        if self.player:
            self.player.loop_track = self.loop_track_var.get()  # Sets player.loop_track from the checkbox BooleanVar
            self._update_status()

    def _toggle_loop_playlist(self):
        """(AI) Syncs the Loop Playlist checkbox state to the player."""

        if self.player:
            self.player.loop_playlist = self.loop_playlist_var.get()  # Sets player.loop_playlist from the checkbox BooleanVar
            self._update_status()

    def _toggle_shuffle(self):
        """(AI) Syncs the Shuffle checkbox state to the player."""

        if self.player:
            self.player.shuffle = self.shuffle_var.get()  # Sets player.shuffle from the checkbox BooleanVar
            self._update_status()

    def _update_status(self):
        """(AI) Refreshes the status label to display current song and playback state."""

        if self.player and self.player.current_song:
            status_text = (
                f"Now Playing: {self.player.current_song} | "
                f"Status: {self.player.status}"
            )
            self.status_label.config(text=status_text)  # Updates the label widget text


def main():
    """(AI) Entry point: creates the tkinter root window and launches MP3GUIPlayer."""
    root = tk.Tk()
    MP3GUIPlayer(root)
    root.mainloop()


if __name__ == "__main__":  # Standard Python guard: runs main() only when executed directly
    main()
