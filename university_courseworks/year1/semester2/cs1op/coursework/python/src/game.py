"""
Singleton game state with the text-mode adventure loop.

Translation of ``Game.java``. The Singleton becomes class-level instance
management with ``get_instance`` and ``reset``; the Observer fan-out is a
plain listener list. The small ``o``-style dice art in the starting-EXP
roll is the Java original, distinct from the ``DiceSystem`` box art.
"""

import random

import text_ui
from door_factory import DoorFactory
from game_event import EventType, GameEvent
from minigame_door import MinigameDoor
from player import Player


WIN_EXP = 500
MAX_NAME_LENGTH = 15

DICE_ART = {
    1: "+-----+\n|     |\n|  o  |\n|     |\n+-----+",
    2: "+-----+\n|o    |\n|     |\n|    o|\n+-----+",
    3: "+-----+\n|o    |\n|  o  |\n|    o|\n+-----+",
    4: "+-----+\n|o   o|\n|     |\n|o   o|\n+-----+",
    5: "+-----+\n|o   o|\n|  o  |\n|o   o|\n+-----+",
    6: "+-----+\n|o   o|\n|o   o|\n|o   o|\n+-----+",
}

STARTING_EXP = {1: 50, 2: 50, 3: 100, 4: 100, 5: 200, 6: 200}


class Game:
    """
    The single shared game state, door deck and event bus.
    """

    _instance = None

    def __init__(self, rng=None):
        self.player = None
        self.listeners = []
        self.doors = []
        self.sound_on = True
        self.rng = rng if rng is not None else random.Random()

    @classmethod
    def get_instance(cls):
        """
        The singleton instance, created on first use.
        """
        if cls._instance is None:
            cls._instance = Game()
        return cls._instance

    @classmethod
    def reset(cls):
        """
        Replace the singleton with a fresh game, used for replay.
        """
        cls._instance = Game()

    def initialize_player(self, name):
        """
        Create the player for GUI mode with a dice-rolled starting EXP.
        """
        self.player = Player(name, self.roll_starting_exp())

    def get_player(self):
        """
        The current player, if one has been created.
        """
        return self.player

    def add_listener(self, listener):
        """
        Register an event listener or plain callable.
        """
        self.listeners.append(listener)

    def notify_listeners(self, event):
        """
        Fan an event out to every listener in registration order.
        """
        for listener in self.listeners:
            if callable(getattr(listener, "on_event", None)):
                listener.on_event(event)
            else:
                listener(event)

    def start(self, input_fn=None):
        """
        Run the text-based game: name entry, menu, then the door loop.
        """
        text_ui.box("SPACE DOOR ADVENTURE", "A small text-based sci-fi roguelike.", "Navigate doors to earn EXP.")
        name = self.get_valid_name(input_fn)
        start_exp = self.roll_starting_exp()
        self.player = Player(name, start_exp)
        text_ui.box("Starting EXP", "You rolled the dice and start with " + str(start_exp) + " EXP.")
        self.add_listener(self._text_listener)
        self.main_menu(input_fn)

    def _text_listener(self, event):
        event_type = event.get_type()
        if event_type == EventType.EXP_CHANGED:
            if self.sound_on:
                print("[SFX] EXP updated.")
            print("[DEBUG] EXP now " + str(event.get_payload().get_exp()))
        elif event_type == EventType.LIFE_LOST:
            if self.sound_on:
                print("[SFX] Life lost!")
            print("[DEBUG] Lives left " + str(event.get_payload().get_lives()))
            self.handle_life_loss()
        elif event_type == EventType.DOOR_CHOSEN:
            if self.sound_on:
                print("[SFX] Door opening...")
            print("[DEBUG] Door chosen: " + event.get_payload().get_name())
        elif event_type == EventType.MINIGAME_STARTED:
            if self.sound_on:
                print("[SFX] Launching minigame...")
            print("[DEBUG] Minigame starting...")

    def get_valid_name(self, input_fn=None):
        """
        Read a player name of 1 to 15 characters, reprompting on invalid.
        """
        while True:
            print("Enter your name (1-" + str(MAX_NAME_LENGTH) + " chars): ", end="", flush=True)
            reader = input_fn if input_fn is not None else input
            name = reader().strip()
            if not name:
                text_ui.box("Invalid", "Name cannot be empty.")
            elif len(name) > MAX_NAME_LENGTH:
                text_ui.box("Invalid", "Name too long. Maximum " + str(MAX_NAME_LENGTH) + " characters.")
            else:
                return name

    def main_menu(self, input_fn=None):
        """
        The text main menu: play, toggle sound, or quit.
        """
        while True:
            text_ui.box("MAIN MENU", "1) Play", "2) Toggle sound (" + ("On" if self.sound_on else "Off") + ")", "3) Quit")
            choice = text_ui.prompt("Choose an option:", input_fn)
            if choice == "1":
                self.setup_doors()
                self.play_loop(input_fn)
                break
            if choice == "2":
                self.sound_on = not self.sound_on
                text_ui.box("Sound", "Sound is now " + ("On" if self.sound_on else "Off"))
            elif choice == "3" or choice.lower() == "q":
                text_ui.box("Exit", "Thanks for playing!")
                break
            else:
                text_ui.box("Invalid", "Please choose 1, 2, or 3.")

    def setup_doors(self):
        """
        Deal five fresh random doors for the round.
        """
        factory = DoorFactory()
        self.doors = [factory.create_random_door(i) for i in range(1, 6)]

    def roll_starting_exp(self):
        """
        Roll for starting EXP and show the small dice art, returning EXP.
        """
        roll = self.rng.randint(1, 6)
        return self.show_dice_roll(roll, DICE_ART.get(roll, DICE_ART[6]), STARTING_EXP[roll])

    def show_dice_roll(self, roll, art, exp):
        """
        Display the roll announcement box and return the EXP value.
        """
        text_ui.box("Dice Roll", ["You rolled a " + str(roll) + "!"] + art.split("\n"))
        return exp

    def play_loop(self, input_fn=None):
        """
        The main door loop: victory at 500 EXP, defeat at ruin.
        """
        while True:
            if self.player.get_exp() >= WIN_EXP:
                text_ui.box("VICTORY", "You have reached " + str(self.player.get_exp()) + " EXP!", "You win!")
                break
            if self.player.is_bankrupt() or self.player.get_lives() <= 0:
                text_ui.box("DEFEAT", "You have run out of EXP or lives.", "Game over.")
                break
            text_ui.box("STATUS", "Player: " + self.player.get_name(), "EXP: " + str(self.player.get_exp()),
                         "Lives: " + str(self.player.get_lives()))
            text_ui.box("DOOR SELECTION", "Choose a door to open (1-" + str(len(self.doors)) + ") or type QUIT:",
                         "Each door is randomized.")
            for i, door in enumerate(self.doors):
                text_ui.box("Door " + str(i + 1), "[??] " + door.get_description())
            choice = text_ui.prompt("Your choice:", input_fn)
            if choice.lower() == "quit":
                text_ui.box("Exit", "Thanks for playing!")
                break
            try:
                sel = int(choice) - 1
            except ValueError:
                text_ui.box("Invalid", "Please enter a number between 1 and " + str(len(self.doors)) + ".")
                continue
            if sel < 0 or sel >= len(self.doors):
                text_ui.box("Invalid", "No such door.")
                continue
            selected = self.doors[sel]
            self.notify_listeners(GameEvent(EventType.DOOR_CHOSEN, selected))
            text_ui.box("Door Opened", "You open door " + str(sel + 1) + ": " + selected.get_description())
            if isinstance(selected, MinigameDoor):
                self.notify_listeners(GameEvent(EventType.MINIGAME_STARTED, selected))
                text_ui.box("Minigame", "Starting " + selected.get_game_type() + "! (Play in GUI version)")
                self.player.lose_life()
                self.setup_doors()
            else:
                result = selected.interact(self.player)
                text_ui.box("Result", result)
                if self.player.is_bankrupt():
                    text_ui.box("Bankrupt", "Your EXP fell below 0.")
                    break
                self.doors[sel] = DoorFactory().create_random_door(sel + 1)

    def handle_life_loss(self):
        """
        Roll the life-loss dice: 1-4 wipes EXP to zero, 5-6 spares it.
        """
        roll = self.rng.randint(1, 6)
        text_ui.box("Life Lost", ["You rolled a " + str(roll) + "!"] + DICE_ART.get(roll, DICE_ART[6]).split("\n"))
        if roll <= 4:
            self.player.set_exp(0)
            text_ui.box("EXP Lost", "Unlucky! Your EXP has been wiped out.", "Current EXP: " + str(self.player.get_exp()))
        else:
            text_ui.box("EXP Saved", "Lucky! You keep your EXP.", "Current EXP: " + str(self.player.get_exp()))

    def get_dice_art(self, roll):
        """
        The small dice art for a roll, defaulting to the six face.
        """
        return DICE_ART.get(roll, DICE_ART[6])

