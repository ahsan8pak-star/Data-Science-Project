"""
Door selection: five mystery doors, reveal art and minigame handoff.

Translation of ``DoorSelectionScreen.java``. Selection wraps over the
five doors; opening plays the per-type sounds, applies the door effect
and shows the matching ASCII reveal art. A minigame door arms the
pending handoff instead of dealing at once. The art tables are the Java
originals with trailing whitespace stripped.
"""

import tkinter as tk

import sound_manager
from base_screen import (
    ARC_DIM,
    ARC_GLOW,
    ARC_LIME,
    ARC_NEON,
    ARC_TEXT,
    BaseGameScreen,
    HINT_FONT,
)
from door_factory import DoorFactory
from minigame_door import MinigameDoor
from nothing_door import NothingDoor
from penalty_door import PenaltyDoor
from reward_door import RewardDoor


DOOR_COUNT = 5
DOOR_ROWS = 12

CHEST_ART = (
    "*******************************************************************************",
    "          |                   |                  |                     |",
    " _________|________________.=\"\"_;=.______________|_____________________|_______",
    "|                   |  ,-\"_,=\"\"     `\"=.|                  |",
    "|___________________|__\"=._o`\"-._        `\"=.______________|___________________",
    "          |                `\"=._o`\"=._      _`\"=._                     |",
    " _________|_____________________:=._o \"=._.\"|.-=\"'\"=.__________________|_______",
    "|                   |    __.--\" , ; `\"=._o.\" ,-\"\"\"-._ \".   |",
    "|___________________|_._\"  ,. .` ` `` ,  `\"-._\"-._   \". '__|___________________",
    "          |           |o`\"=._` , \"` `; .\". ,  \"-._\"-._; ;              |",
    " _________|___________| ;`-.o`\"=._; .\" ` '`.\"|` . \"-._ /_______________|_______",
    "|                   | |o;    `\"-.o`\"=._``  '` \" ,__.--o;   |",
    "|___________________|_| ;     (#) `-.o `\"=.`_.--\"_o.-; ;___|___________________",
    "____/______/______/___|o;._    '      `.o|o_.--'    ;o;____/______/______/____",
    "/______/______/______/_\"=._o--._        ; | ;        ; ;/______/______/______/_",
    "____/______/______/______/__\"=._o--._   ;o|o;     _._;o;____/______/______/____",
    "/______/______/______/______/____\"=._o._; | ;_.--\"o.--\"_/______/______/______/_",
    "____/______/______/______/______/_____\"=.o|o_.--\"\"___/______/______/______/____",
    "/______/______/______/______/______/______/______/______/______/______/______/_",
    "*******************************************************************************",
)

POISON_ART = (
    "                                       ______",
    "                                       |____|",
    "                                    __/      \\__",
    "                                   /            \\",
    "---------------------------------- |            | ----------------------------------",
    "|                                  |            |                                  |",
    "|                                  |            |                                  |",
    "|                                  \\____________/                                  |",
    "|                                                                                  |",
    "|                            __----------------------__                            |",
    "|                          ..'                        '..                          |",
    "|                        ./                              \\.                        |",
    "|                       ./                                \\.                       |",
    "|                      ./                                  \\.                      |",
    "|                      /                                    \\                      |",
    "|                     | \\                                  / |                     |",
    "|                     |  \\                                /  |                     |",
    "|                     |   \\                              /   |                     |",
    "|                  #######  ########  ##  #####  ########  ###  ##                 |",
    "|                  ##   ##  ##    ##  ##  ##     ##    ##  ## # ##                 |",
    "|                  #######  ##    ##  ##  #####  ##    ##  ## # ##                 |",
    "|               __ ##       ##    ##  ##     ##  ##    ##  ##  ### __              |",
    "|              (   ##       ########  ##  #####  ########  ##   ##   )             |",
    "|              )    \\_    /      ...    /   \\    ...      \\    _/    (             |",
    "|             (     _ '.  \\            /     \\            /  .' _     )            |",
    "|              '---' '. '. \\          (       )          / .' .' '---'             |",
    "|                      '. '.\\          '-'''-'          /.' .'                     |",
    "|                        '.  \\__                     __/  .'                         |",
    "|                          '. \\|'\\...-_--_-_-_--.../'|/ .'                         |",
    "|                           .' |  ||||_||_|_|_|||||  |  '.                         |",
    "|                         .'  .|  '\\.|||\\_|_/|||./'  |'.  '.                       |",
    "|                       .'  .' |                     |  '.  '.                     |",
    "|                _____.'  .'   '\\.   ..       ..   ./'    '.  '._____              |",
    "|              (       _.'       '-_             _-'        '_        )            |",
    "|               |     /             '._________.'             \\      |             |",
    "|                \\___/                                         \\____/              |",
    "|                                                                                  |",
    "------------------------------------------------------------------------------------",
)

NOTHING_ART = (
    " ___________________________",
    "|\\ ________________________/|",
    "| |        |               ||",
    "| |        |   /' .        ||",
    "| |        |   |    ' .    ||",
    "| |        |   |       \\   ||",
    "| |        |   |       |   ||",
    "| |        |   \\       |   ||",
    "| |        |    ' .    |   ||",
    "| |        |        ' ./   ||",
    "| |        ()              ||",
    "| |        |               ||",
    "| |        |   /' .        ||",
    "| |        |   |    ' .    ||",
    "| |        |   |       \\   ||",
    "| |        |   |       |   ||",
    "| |        |   \\       |   ||",
    "| |        |    ' .    |   ||",
    "| |        |        ' ./   ||",
    "| |        '  .            ||",
    "| |              '  .      ||",
    "|/_____________________'  .\\|",
)

PONG_ART = (
    "",
    "                                        ..-+##+-..",
    "                                       .++......-#.",
    "                                      .+-.........+.",
    "            ...-+#######+-...         .#..........#.           ....-----....",
    "         ..-#################+..       +-........-+.       ..-##++----++++###-..",
    "       .-#######################+.     .++--.----+.     ..+#+--+++++++++++++++##-..",
    "      .###########################+.     .-+##+-.     ..++-++++++++++++++++++++++#+.",
    "    .-##############################+.               .++-++++++-------+++++++++++++#..",
    "   .+################################+.            ..#-++++++-------++++++++++++++++#-.",
    "   -#+#################################.           .#+++++++-----++++++++++++++++++++#-",
    "  .#+####+++###########################+          .#++++++++++++++++++++++++++++++++++#.",
    " .-#+###++++############################.        .++++++++++++++++++++++++++++++++++++#-.",
    " .+#+###++++#############################.       -#+++++++++++++++++++++++++++++++++++++.",
    " .+#+###++++#############################.      .+#++++++++++++++++++++++++++++++++++++#.",
    " .+#+###+++++############################.      .#++++++++++++++++++++++++++++++++++++++.",
    " .-#+####################################.      .##+++++++++++++++++++++++++++++++++++#+.",
    "  .++################################+-++.      .+++##++++++++++++++++++++++++++++++++#.",
    "   -##############################+----#.        .+---+##++++++++++++++++++++++++++++#+.",
    "   .-##########################+------++          ++...--+##+++++++++++++++++++++++++#.",
    "    .-######################---------++.          .#---------##+++++++++++++++++++++#.",
    "      .#################+--##++#+---++.            .#+----+###--##++++++++++++++++#+.",
    "       .-############+----++----+#--+.              .#---#----++---+##+++++++++++#-.",
    "         .-#######+-..-----#-..---##-                -#+#-..--+#------+##++++++#-.",
    "           ..-##+---.------+#-..---#+                -#+-..--+#----------+###+..",
    "               ..--+#######+##-.----++.             .#+------#--+++++++##+-..",
    "                          ..-#+------++.           .#-------##-.........",
    "                             .++-------#.         -#-------#..",
    "                              .++-------#.      .++-------#..",
    "                               .+--------#-    .++-------#-",
    "                                .++----+#-.    -#+------#-.",
    "                                 .#++#-.        ..-#+--+-.",
    "                                  ...              ..-#-.",
)

SPACE_INVADERS_ART = (
    " /\\/\\/\\                            /  \\",
    "| \\  / |                         /      \\",
    "|  \\/  |                       /          \\",
    "|  /\\  |----------------------|     /\\     |",
    "| /  \\ |                      |    /  \\    |",
    "|/    \\|                      |   /    \\   |",
    "|\\    /|                      |  | (  ) |  |",
    "| \\  / |                      |  | (  ) |  |",
    "|  \\/  |                 /\\   |  |      |  |   /\\",
    "|  /\\  |                /  \\  |  |      |  |  /  \\",
    "| /  \\ |               |----| |  |      |  | |----|",
    "|/    \\|---------------|    | | /|  ..  |\\ | |    |",
    "|\\    /|               |    | /  |  ..  |  \\ |    |",
    "| \\  / |               |    /    |  ..  |    \\    |",
    "|  \\/  |               |  /      |  ..  |      \\  |",
    "|  /\\  |---------------|/        |  ..  |        \\|",
    "| /  \\ |              /          |  ..  |          \\",
    "|/    \\|              (          |      |           )",
    "|/\\/\\/\\|               |    | |--|      |--| |    |",
    "------------------------/  \\-----/  \\/  \\-----/  \\--------",
    "                        \\\\//     \\\\//\\\\//     \\\\//",
    "                         \\/       \\/  \\/       \\/",
)


def door_line(door_num, row):
    """
    One row of the numbered mystery-door box, twelve rows per door.
    """
    return {
        0: "╔═══════════╗",
        1: "║ ╔══════╗ ║",
        2: "║ ║  " + str(door_num) + "  ║ ║",
        3: "║ ║     ║ ║",
        4: "║ ║     ║ ║",
        5: "║ ╚══════╝ ║",
        6: "()═════════║",
        7: "║ ╔══════╗ ║",
        8: "║ ║     ║ ║",
        9: "║ ║     ║ ║",
        10: "║ ╚══════╝ ║",
        11: "╚═══════════╝",
    }.get(row, "")


def art_for_door(door):
    """
    The reveal art matching a door's type.
    """
    if isinstance(door, RewardDoor):
        return CHEST_ART
    if isinstance(door, PenaltyDoor):
        return POISON_ART
    if isinstance(door, NothingDoor):
        return NOTHING_ART
    if isinstance(door, MinigameDoor):
        if door.get_game_type() == "PONG":
            return PONG_ART
        return SPACE_INVADERS_ART
    return NOTHING_ART


class DoorSelectionState:
    """
    The five doors, selection cursor and reveal flow, widget-free.
    """

    def __init__(self, controller, factory=None):
        self.controller = controller
        self.factory = factory if factory is not None else DoorFactory()
        self.reset_doors()

    def reset_doors(self):
        """
        Deal five fresh doors and clear the reveal state.
        """
        self.doors = [self.factory.create_random_door(i) for i in range(1, DOOR_COUNT + 1)]
        self.selected = 0
        self.revealed = False
        self.result_message = ""
        self.minigame_pending = False
        self.pending_minigame_type = ""

    def move_selection(self, delta):
        """
        Wrap the cursor over the five doors with a navigate sound.
        """
        self.selected = (self.selected + delta) % DOOR_COUNT
        sound_manager.play_once(sound_manager.DOOR_NAVIGATE)

    def open_selected(self):
        """
        Open the cursor door: apply its effect, sound it, reveal the art.

        Returns the result message shown on the reveal panel.
        """
        if not 0 <= self.selected < len(self.doors):
            return ""
        door = self.doors[self.selected]
        player = self.controller.get_current_player()
        if player is None:
            return ""
        sound_manager.play_once(sound_manager.DOOR_OPEN)
        door.interact(player)
        if isinstance(door, RewardDoor):
            sound_manager.play_once(sound_manager.CHEST_SHINE)
            sound_manager.play_once(sound_manager.REWARD_POINTS)
            self.result_message = "You Found a Shiny Chest!  +" + str(door.get_exp_value()) + " EXP!"
        elif isinstance(door, PenaltyDoor):
            sound_manager.play_once(sound_manager.POISON_SMOKE)
            sound_manager.play_once(sound_manager.PENALTY_POINTS)
            self.result_message = "Toxic Fumes!  " + str(abs(door.get_exp_value())) + " EXP Lost!"
        elif isinstance(door, NothingDoor):
            sound_manager.play_once(sound_manager.DOOR_CLOSE)
            self.result_message = "The Door Reveals Nothing but an Empty Void..."
        elif isinstance(door, MinigameDoor):
            sound_manager.play_once(sound_manager.MENU_SELECT)
            self.minigame_pending = True
            self.pending_minigame_type = door.get_game_type()
            game_name = "PONG" if door.get_game_type() == "PONG" else "SPACE INVADERS"
            self.result_message = "A Challenge Awaits!  Press ENTER to Play " + game_name + "!"
        self.revealed = True
        return self.result_message

    def confirm_revealed(self):
        """
        Leave the reveal panel: minigame handoff, win/loss routing, or redeal.

        Returns the action taken: ``minigame``, ``gameplay`` or ``redeal``.
        """
        from game import WIN_EXP
        if self.minigame_pending:
            self.controller.start_minigame(self.pending_minigame_type)
            return "minigame"
        player = self.controller.get_current_player()
        if player is not None and (player.get_exp() >= WIN_EXP
                                   or player.get_lives() <= 0 or player.get_exp() < 0):
            self.controller.show_screen("GAMEPLAY")
            return "gameplay"
        self.reset_doors()
        return "redeal"


class DoorSelectionScreenView(BaseGameScreen):
    """
    The five-door grid and the ASCII reveal panel.
    """

    def __init__(self, gui, controller):
        super().__init__(gui, controller)
        self.state = DoorSelectionState(controller)
        self.canvas_widget = self.canvas()
        self.bind("<KeyPress>", self._on_key)
        self.bind("<Configure>", lambda _e: self.redraw())

    def _on_key(self, event):
        key = event.keysym
        if self.state.revealed:
            if key == "Return":
                self.state.confirm_revealed()
                self.redraw()
            return
        if key in ("Left", "a", "A"):
            self.state.move_selection(-1)
            self.redraw()
        elif key in ("Right", "d", "D"):
            self.state.move_selection(1)
            self.redraw()
        elif key == "Return":
            self.state.open_selected()
            self.redraw()
        elif key == "Escape":
            self.controller.show_screen("GAMEPLAY")

    def redraw(self):
        """
        Paint the status bar with either the grid or the reveal panel.
        """
        canvas = self.canvas_widget
        canvas.delete("all")
        width = max(canvas.winfo_width(), 900)
        height = max(canvas.winfo_height(), 650)
        canvas.create_rectangle(20, 20, width - 20, height - 20, outline=ARC_NEON, width=2)
        player = self.controller.get_current_player()
        if player is not None:
            canvas.create_text(30, 45, text="EXP: " + str(player.get_exp()) + " / 500",
                               font=("Monospaced", 14, "normal"), fill=ARC_TEXT, anchor="w")
            canvas.create_text(30, 65, text="Lives: " + str(player.get_lives()),
                               font=("Monospaced", 14, "normal"), fill=ARC_TEXT, anchor="w")
        if self.state.revealed:
            self._draw_reveal(canvas, width, height)
        else:
            self._draw_grid(canvas, width, height)

    def _draw_grid(self, canvas, width, height):
        self.draw_centred_text(canvas, "CHOOSE  A  DOOR", width // 2, 100, ("Monospaced", 24, "bold"), ARC_LIME)
        font = ("Monospaced", 13, "normal")
        sample = max((door_line(5, row) for row in range(DOOR_ROWS)), key=len)
        col_w = len(sample)
        gap = 8
        start_x = 60
        start_y = 120
        for i in range(DOOR_COUNT):
            x = start_x + i * (col_w + gap)
            selected = i == self.state.selected
            for row in range(DOOR_ROWS):
                canvas.create_text(x, start_y + row * 16, text=door_line(i + 1, row), font=font,
                                   fill=ARC_LIME if selected else ARC_TEXT, anchor="nw")
        self.draw_centred_text(canvas, "DOOR " + str(self.state.selected + 1) + "  selected",
                               width // 2, start_y + DOOR_ROWS * 16 + 28, ("Monospaced", 14, "bold"))
        self.draw_centred_text(canvas, "[ ← ] [ → ] Select     [ ENTER ] Open Door     [ ESC ] Back",
                               width // 2, height - 30, HINT_FONT, ARC_DIM)

    def _draw_reveal(self, canvas, width, height):
        message = self.state.result_message
        canvas.create_rectangle(width // 2 - len(message) * 5 - 25, 75,
                                width // 2 + len(message) * 5 + 25, 111, outline=ARC_NEON, width=2)
        self.draw_centred_text(canvas, message, width // 2, 99, ("Monospaced", 16, "bold"))
        door = self.state.doors[self.state.selected]
        art = art_for_door(door)
        canvas.create_text(width // 2, 130, text="\n".join(art), font=("Monospaced", 6, "normal"),
                           fill=ARC_TEXT, anchor="n")
        hint = "[ ENTER ] Play Minigame" if self.state.minigame_pending else "[ ENTER ] Continue"
        self.draw_centred_text(canvas, hint, width // 2, height - 25, HINT_FONT, ARC_DIM)

