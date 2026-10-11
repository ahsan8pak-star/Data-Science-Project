"""
Main application window with named-screen switching.

Translation of ``GameGUI.java``. The Swing ``CardLayout`` becomes a dict
of frames with exactly one packed at a time; the startup permission
dialog becomes a tkinter message box. Importing this module is safe
headless — no window exists until ``GameGUI`` is constructed.
"""

import tkinter as tk
from tkinter import messagebox

import sound_manager


class GameGUI(tk.Tk):
    """
    The Space Mission window, owning the controller and the screens.
    """

    def __init__(self):
        super().__init__()
        self.title("Space Mission")
        self.minsize(900, 650)
        self.geometry("1100x750")
        self.configure(bg="black")
        self.resizable(True, True)

        from game_controller import GameController
        self.controller = GameController(self)
        self.screens = {}
        self._current = None

        from main_menu_screen import MainMenuScreen
        from name_entry_screen import NameEntryScreen
        from dialogue_screen import DialogueScreenView
        from game_play_screen import GamePlayScreen
        from door_selection_screen import DoorSelectionScreenView
        self.add_screen(MainMenuScreen(self, self.controller), "MAIN_MENU")
        self.add_screen(NameEntryScreen(self, self.controller), "NAME_ENTRY")
        self.add_screen(DialogueScreenView(self, self.controller), "DIALOGUE")
        self.add_screen(GamePlayScreen(self, self.controller), "GAMEPLAY")
        self.add_screen(DoorSelectionScreenView(self, self.controller), "DOOR_SELECTION")

        if not self.ask_permission():
            sound_manager.stop_all()
            self.destroy()
            return
        self.show_screen("MAIN_MENU")

    def ask_permission(self):
        """
        Confirm the game may run, mirroring the startup prompt.
        """
        try:
            return messagebox.askyesno("Permission Request", "Allow Space Mission to run?")
        except tk.TclError:
            return False

    def show_screen(self, name):
        """
        Raise the named screen, stopping sounds for the main menu.
        """
        if name == "MAIN_MENU":
            sound_manager.stop_all()
        if self._current is not None:
            self._current.pack_forget()
        screen = self.screens.get(name)
        if screen is not None:
            screen.pack(fill=tk.BOTH, expand=True)
            self._current = screen
            try:
                screen.focus_set()
            except tk.TclError:
                pass

    def add_screen(self, screen, name):
        """
        Register a screen under a name, replacing any previous one.
        """
        old = self.screens.get(name)
        if old is not None and old is not screen:
            old.pack_forget()
            old.destroy()
        self.screens[name] = screen

    def remove_screen(self, name):
        """
        Drop the named screen from the registry.
        """
        screen = self.screens.pop(name, None)
        if screen is not None:
            if screen is self._current:
                screen.pack_forget()
                self._current = None
            screen.destroy()

    def run(self):
        """
        Enter the tkinter main loop.
        """
        self.mainloop()

