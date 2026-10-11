"""
Captain dialogue: branching state machine plus the helmet view.

Translation of ``DialogueScreen.java``. The five-state machine
(INTRODUCTION, DICE_PROMPT, DICE_RESULT, DICE_DECLINED, REJECTION) and
every transition are preserved: ENTER advances lines, the last line of
a decision state arms the Y/N prompt, YES on the dice prompt rolls for
starting HP, and finishing DICE_RESULT or DICE_DECLINED writes the HP
into EXP and deals doors. The helmet art is the Java original with
trailing whitespace stripped.
"""

import tkinter as tk
from enum import Enum, auto

import sound_manager
from base_screen import (
    ARC_DIM,
    ARC_LIME,
    ARC_NEON,
    ARC_TEXT,
    BaseGameScreen,
    HINT_FONT,
)
from dice_system import DiceSystem


INTRO_LINES = (
    "WELCOME, <USER>!",
    "You look a bit confused.",
    "Don't worry. I'll explain everything.",
    "Basically, you were sent on a mission.",
    "A SPACE MISSION!",
    "Seems obvious but all you got to do is to get enough EXP to go back home.",
    "If you want to know why you're here and everything else.",
    "Beats me, not my problem...",
    "BUT!",
    "At least I'll help you go back.",
    "Deal?",
)

DICE_LINES = (
    "Hey...",
    "I got something to show you...",
    "A lucky dice. A space dice to be exact.",
    "Looks a bit weird... so shiny...",
    "Wanna have a roll?",
)

DICE_DECLINED_LINES = (
    "Alright then...",
    "We'll manage without it.",
)

REJECTION_LINES = (
    "Suit yourself...",
    "You drift off into space, contemplating if you agreed to whatever it said to you.",
    "Before you even get to deepen everything about this and whatever comes to your mind.",
    "You simply passed out.",
    "That quick.",
    "Too bad.",
)

HELMET = (
    "                             ##################",
    "                         #####                #####",
    "                      ####                        #####",
    "                   ####                               ####",
    "                 ###           ##############           ###",
    "               ###        #####              #####        ###",
    "             ###    ######                        #######   ###",
    "            ##    ##           ##############           ##   ###",
    "           ##  ###        ########################        ##   ##",
    "          ### ##       ########         #####   #####       ##  ##",
    "         ##  ##    #########            ###       ######     ##  ##",
    "        ##  ##    #######        ##########       ########    ##  ##",
    "        ## ##   #####         ###############   ############   ## ##",
    "        ## ## #####       ####################################  ## ##",
    "        ## ## ####   #########################################   ## ##",
    "  ###### ##  ####    ##########################################  ## ######",
    " ##   ## ##  ####    ##########################################  ## ##   ##",
    " ##   ## ##  ##################################################  ## ##   ##",
    " ##   ## ##  #####   ##########################################  ## ##   ##",
    " ##   ## ##  #####   ##########################################  ## ##   ##",
    " ##   ## ##  ##################################################  ## ##   ##",
    " ##   ## ##  ##########################################   #####  ## ##   ##",
    " ##   ## ##  ########################################       ###  ## ##   ##",
    "  ###### ##  ########################################       ###  ## ######",
    "      ##   ## #########################################   ### #     ##",
    "      ##     ## ################################   ######## ###     ##",
    "        ##    ##  ##############################   ######  ###    ##",
    "        #####   ###  ##################################  ####  #####",
    "        ## ###     ####  ###########################  ####   #### ##",
    "        ## #######     #####                    #####     ####### ##",
    "         ###      ###       ####################       ####     ###",
    "           ####      ####                          ####      ####",
    "              ##        ######                ######        ##",
    "                ####         ##################         ####",
    "                   ####                              ####",
    "                       #######                #######",
    "                              ################",
    "",
    "",
    "",
)


class DialoguePhase(Enum):
    """
    The five dialogue states.
    """

    INTRODUCTION = auto()
    DICE_PROMPT = auto()
    DICE_RESULT = auto()
    DICE_DECLINED = auto()
    REJECTION = auto()


class DialogueState:
    """
    The branching dialogue machine, without any widgets.
    """

    def __init__(self, controller, dice=None):
        self.controller = controller
        self.dice = dice if dice is not None else DiceSystem()
        self.reset()

    def reset(self):
        """
        Restart the dialogue for a new game, stopping rejection music.
        """
        sound_manager.stop_sound(sound_manager.HORROR_LOOP)
        self.phase = DialoguePhase.INTRODUCTION
        self.awaiting_yn = False
        self.starting_hp = 100
        self.load_lines(INTRO_LINES)

    def player_tag(self):
        """
        The upper-cased player name, or CAPTAIN before naming.
        """
        player = self.controller.get_current_player()
        if player is None:
            return "CAPTAIN"
        return player.get_name().upper()

    def load_lines(self, src):
        """
        Fill the line buffer, substituting the player tag for <USER>.
        """
        tag = self.player_tag()
        self.lines = [line.replace("<USER>", tag) for line in src]
        self.line_idx = 0
        self.awaiting_yn = False

    def is_decision_state(self):
        """
        True while a Y/N answer can close the current scene.
        """
        return self.phase in (DialoguePhase.INTRODUCTION, DialoguePhase.DICE_PROMPT)

    def current_line(self):
        """
        The line on display.
        """
        if 0 <= self.line_idx < len(self.lines):
            return self.lines[self.line_idx]
        return ""

    def handle_escape(self):
        """
        Leave the rejection scene for the main menu.

        Returns True when the key was consumed.
        """
        if self.phase == DialoguePhase.REJECTION:
            sound_manager.stop_sound(sound_manager.HORROR_LOOP)
            self.controller.show_screen("MAIN_MENU")
            return True
        return False

    def advance(self):
        """
        Move ENTER forward: next line, arming Y/N on the last one.
        """
        if self.awaiting_yn:
            return
        sound_manager.play_once(sound_manager.MENU_NAVIGATE)
        if self.line_idx < len(self.lines) - 1:
            self.line_idx += 1
            if self.line_idx == len(self.lines) - 1 and self.is_decision_state():
                self.awaiting_yn = True
        else:
            self.end_of_lines()

    def answer_yes(self):
        """
        Accept the deal or the dice roll.
        """
        self.awaiting_yn = False
        sound_manager.play_once(sound_manager.DIALOGUE_YES)
        if self.phase == DialoguePhase.INTRODUCTION:
            self.phase = DialoguePhase.DICE_PROMPT
            self.load_lines(DICE_LINES)
        elif self.phase == DialoguePhase.DICE_PROMPT:
            self.dice.roll()
            self.starting_hp = self.dice.get_hp_from_roll(self.dice.get_last_roll())
            self.phase = DialoguePhase.DICE_RESULT
            self.lines = [
                "Alright!",
                "You rolled a " + str(self.dice.get_last_roll()) + "!  Starting EXP: " + str(self.starting_hp) + ".",
                "Let's get started!",
            ]
            self.line_idx = 0

    def answer_no(self):
        """
        Refuse the deal or decline the dice.
        """
        self.awaiting_yn = False
        sound_manager.play_once(sound_manager.DIALOGUE_NO)
        if self.phase == DialoguePhase.INTRODUCTION:
            self.phase = DialoguePhase.REJECTION
            self.load_lines(REJECTION_LINES)
            sound_manager.play_loop(sound_manager.HORROR_LOOP)
        elif self.phase == DialoguePhase.DICE_PROMPT:
            self.phase = DialoguePhase.DICE_DECLINED
            self.load_lines(DICE_DECLINED_LINES)

    def end_of_lines(self):
        """
        Leave a finished scene: doors deal, or menu on rejection.
        """
        if self.phase in (DialoguePhase.DICE_RESULT, DialoguePhase.DICE_DECLINED):
            player = self.controller.get_current_player()
            if player is not None:
                player.set_exp(self.starting_hp)
            self.controller.start_door_selection()
        elif self.phase == DialoguePhase.REJECTION:
            sound_manager.stop_sound(sound_manager.HORROR_LOOP)
            self.controller.show_screen("MAIN_MENU")


class DialogueScreenView(BaseGameScreen):
    """
    The helmet-and-speech-bubble dialogue view.
    """

    def __init__(self, gui, controller):
        super().__init__(gui, controller)
        self.state = DialogueState(controller)
        self.canvas_widget = self.canvas()
        self.bind("<KeyPress>", self._on_key)
        self.bind("<Configure>", lambda _e: self.redraw())

    def _on_key(self, event):
        if event.keysym == "Escape":
            if self.state.handle_escape():
                self.redraw()
            return
        if self.state.awaiting_yn:
            char = event.char.upper() if event.char else ""
            if char == "Y":
                self.state.answer_yes()
                self.redraw()
            elif char == "N":
                self.state.answer_no()
                self.redraw()
            return
        if event.keysym == "Return":
            self.state.advance()
            self.redraw()

    def redraw(self):
        """
        Paint the speech bubble, name box and helmet or dice art.
        """
        canvas = self.canvas_widget
        canvas.delete("all")
        width = max(canvas.winfo_width(), 900)
        height = max(canvas.winfo_height(), 650)
        if self.state.phase == DialoguePhase.REJECTION:
            self._draw_rejection(canvas, width, height)
        else:
            self._draw_scene(canvas, width, height)

    def _draw_scene(self, canvas, width, height):
        bubble_h = max(125, height // 6)
        canvas.create_rectangle(10, 8, width - 10, 8 + bubble_h, outline=ARC_NEON, width=3)
        canvas.create_rectangle(14, 12, width - 14, bubble_h + 4, fill="#000000", outline="")
        canvas.create_text(30, 53, text=self.state.current_line(), font=("Monospaced", 18, "bold"),
                           fill=ARC_TEXT, anchor="w", width=width - 80)
        if self.state.awaiting_yn:
            self.draw_centred_text(canvas, "[ Y ] Yes                         [ N ] No",
                                   width // 2, bubble_h - 6, ("Monospaced", 16, "bold"), ARC_LIME)
        elif self.state.line_idx < len(self.state.lines) - 1:
            canvas.create_text(width - 40, bubble_h - 2, text="[ENTER \u25ba]",
                               font=("Monospaced", 12, "normal"), fill=ARC_DIM, anchor="e")
        tag = self.state.player_tag()[:15]
        name_font = ("Monospaced", 22 if len(tag) <= 8 else (17 if len(tag) <= 12 else 14), "bold")
        box_y = 8 + bubble_h + 10
        canvas.create_text(width // 2, box_y + 22, text=tag, font=name_font, fill=ARC_NEON)
        art_top = box_y + 50
        if self.state.phase == DialoguePhase.DICE_RESULT:
            face = self.state.dice.get_dice_face_array(max(1, min(6, self.state.dice.get_last_roll())))
            art = list(face) + ["", "Rolled: " + str(self.state.dice.get_last_roll())
                                + "   |   Starting EXP: " + str(self.state.starting_hp)]
        else:
            art = list(HELMET)
        canvas.create_text(width // 2, art_top, text="\n".join(art), font=("Monospaced", 7, "normal"),
                           fill=ARC_TEXT, anchor="n")

    def _draw_rejection(self, canvas, width, height):
        box = (30, 50, width - 60, height - 100)
        canvas.create_rectangle(box[0], box[1], box[0] + box[2], box[1] + box[3], outline=ARC_NEON, width=3)
        canvas.create_text(box[0] + 30, box[1] + 60, text=self.state.current_line(),
                           font=("Monospaced", 22, "normal"), fill=ARC_TEXT, anchor="nw", width=box[2] - 60)
        canvas.create_text(box[0] + 10, box[1] + box[3] - 10, text="[ ESC ] Return to Menu",
                           font=("Monospaced", 11, "normal"), fill=ARC_DIM, anchor="sw")

