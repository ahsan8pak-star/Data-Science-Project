"""
Line-by-line Python translation of ``week_03_lecture_code/SnakesAndLadders.java``.

The Java program is a one-player board game on a 4x4 grid. The player
presses Enter to roll a six-sided die, moves forward, and may then climb a
ladder or slide down a snake. Rolling past the winning square is not
allowed: the player stays put.

Java to Python mapping used here:

  ``final int WINNING_POSITION = 16`` -> a module constant
  ``new Scanner(System.in)``          -> ``input()``
  ``scanner.nextLine()``              -> ``input()`` (discard the result)
  ``new Random()``                    -> the ``random`` module
  ``dice.nextInt(6) + 1``             -> ``random.randint(1, 6)``
  ``scanner.close()``                 -> no equivalent (Python has no handle)

``random.randint(1, 6)`` is inclusive at both ends. Java's ``nextInt(6)``
returns 0 to 5, so the ``+ 1`` is what makes it a real die. Writing
``random.randint(1, 7)`` instead would allow a 7, and ``random.randrange(1,
6)`` would never roll a 6 - both are common off-by-one mistakes.
"""

import random

# 4x4 board: the highest reachable square is 16.
WINNING_POSITION = 16

# Ladders and snakes as "old square -> new square". Dictionaries replace
# the Java if/else chains and keep movement logic separate from the board.
LADDERS = {3: 11, 5: 9}
SNAKES = {15: 7, 12: 2}


def roll_dice() -> int:
    """
    Return a value from 1 to 6, mirroring ``dice.nextInt(6) + 1``.

    ``randint`` is inclusive, so the range is written exactly as the die
    faces. Using ``randrange`` would need an exclusive upper bound of 7.
    """
    return random.randint(1, 6)


def apply_board(position: int) -> int:
    """
    Apply a ladder or a snake at ``position`` and return the new square.

    Java checks ladders first, then snakes, with separate ``if`` chains.
    The two dictionaries preserve that order. The checks are independent
    because a ladder and a snake never share a square on this board.
    """
    if position in LADDERS:
        print(f"You found a ladder! Climb up to {LADDERS[position]}.")
        return LADDERS[position]
    if position in SNAKES:
        print(f"Oops! You hit a snake! Slide down to {SNAKES[position]}.")
        return SNAKES[position]
    return position


def main() -> None:
    """
    Mirror of ``SnakesAndLadders.main``.

    Java's ``while (!gameOver)`` becomes ``while not game_over``. The game
    is only won by landing exactly on square 16; a roll that would take the
    player past it is ignored and the position stays unchanged.
    """
    player_position = 0
    game_over = False

    while not game_over:
        print("Your turn.")
        print("Press Enter to roll the dice...", end="")
        # Java reads and discards one line from the Scanner. Python's
        # input() does the same; assigning nowhere discards the value.
        input()

        dice_roll = roll_dice()
        print(f"You rolled a {dice_roll}")

        new_position = player_position + dice_roll
        if new_position > WINNING_POSITION:
            # Overshooting is a no-move turn, not a bounce-back.
            print(f"You rolled too high and stayed at {player_position}")
        else:
            player_position = new_position
            player_position = apply_board(player_position)
            print(f"You are now at position {player_position}")

            if player_position == WINNING_POSITION:
                print("Congratulations! You win!")
                game_over = True

    # Java calls scanner.close() here. Python's input() owns no resource that
    # the program can close, so there is deliberately no equivalent line.


if __name__ == "__main__":
    main()

