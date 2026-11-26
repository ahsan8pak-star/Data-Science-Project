# -*- coding: utf-8 -*-
"""
Created on Tue May  6 09:23:10 2025

@author: Martin Lester
"""

from copy import deepcopy
import random

# This class encapsulates the game logic.
class Othello:

    # Constants for the content of a board grid cell.
    # Maybe these should be Python Enums, but it seems like too much hassle.
    WHITE = 1
    BLACK = -1
    EMPTY = 0
    OOB = 2  # Out Of Bounds

    # Width and height of a new board.
    # These are only used when creating a new board,
    # so if you want to adapt the game to a different board size,
    # you just need to pass the constructor an initial board of the size you want.
    WIDTH = 8
    HEIGHT = 8

    # Constructor.
    # Optionally takes existing board (defaults to new board) and current player (defaults to Black).
    def __init__(self, b=None, p=-1):
        if b is None:
            # Make a standard starting board.
            self.board = [
                [0 for y in range(Othello.HEIGHT)] for x in range(Othello.WIDTH)
            ]
            self.board[3][3] = Othello.WHITE
            self.board[4][4] = Othello.WHITE
            self.board[3][4] = Othello.BLACK
            self.board[4][3] = Othello.BLACK
        
        else:
            # Copy the existing board.
            # Must use deepcopy() to avoid aliasing.
            self.board = deepcopy(b)

        self.player = p

    # Return a new Othello game object with no shared state.
    def clone(self):
        return Othello(self.board, self.player)

    # Change whose turn it is. Used mainly after making a move.
    # For convenience, returns self, so other methods can be chained afterwards.
    def flip_player(self):
        self.player = self.opponent()
        return self

    # Return the opponent (who is not currently due to play).
    def opponent(self):
        return self.player * -1

    # Return the string "Black" or "White", indicating the current player's colour.
    def player_name(self, p=None):
        if p is None:
            p = self.player
        
        if p == Othello.BLACK:
            return "Black"
        
        else:
            return "White"

    # Is (x,y) a legal move?
    def legal_move(self, x, y):
        return self.clone().move(x, y)

    # Attempt to place a disc on (x,y) and flip discs as appropriate.
    # Returns True if move was legal and successful.
    # Returns False if move was illegal, in which case board is unchanged.
    # This never changes the current player.
    def move(self, x, y):
        flipped = False  # Was the move successful?

        # Check if the target cell is empty; if not, move fails.
        if self.get_cell(x, y) != Othello.EMPTY:
            return False
        # But don't set the target cell yet.
        # Avoid making any changes to the board until we are sure the move is legal.

        # Iterate over all 8 possible directions (horizontal, vertical, diagonal).
        # A direction is defined by a step change in x-ordinate and y-ordinate...
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # ...of which at least one must be non-zero.
                if dx == 0 and dy == 0:
                    continue

                # Look at the first cell in the direction.
                (tryx, tryy) = (x + dx, y + dy)
                # If it isn't an opponent disc, move onto the next direction.
                if self.get_cell(tryx, tryy) != self.opponent():
                    continue

                # Keep going in that direction until the first non-opponent disc.
                # (Could be current player's disc, empty, or out of bounds).
                while self.get_cell(tryx, tryy) == self.opponent():
                    (tryx, tryy) = (tryx + dx, tryy + dy)

                # If the line doesn't end with a current player disc, there are no flips.
                # So move onto the next direction.
                if self.get_cell(tryx, tryy) != self.player:
                    continue

                # At this point, we know that a flip will occur.
                flipped = True
                # Step backwards to the last opponent disc.
                (tryx, tryy) = (tryx - dx, tryy - dy)

                # Keep going backwards, flipping discs as we go,
                # until we get back to the starting point (which will be empty).
                while self.get_cell(tryx, tryy) == self.opponent():
                    self.set_cell(tryx, tryy, self.player)
                    (tryx, tryy) = (tryx - dx, tryy - dy)

        # Now we have looked at all directions.
        # If at least one counter was flipped, the move was legal.
        # So finally we can fill the target grid cell.
        # (This is subtly different from the algorithm you might derive directly from
        # the rules, where you would place the disc in the target cell before flipping.)
        if flipped:
            self.set_cell(x, y, self.player)
        # Note that this method does not flip the player.

        # Return whether the move was legal.
        return flipped

    # Can the current player move anywhere?
    def can_move(self):
        for x in range(0, self.width()):
            for y in range(0, self.height()):
        
                if self.legal_move(x, y):
                    return True
        return False

    # Is the game over (meaning that neither player has a legal move)?
    def game_over(self):
        return (
            self.can_move() == False and self.clone().flip_player().can_move() == False
        )

    # Count scores and return the winner of the game (Othello.BLACK or Othello.WHITE),
    # or Othello.EMPTY in the rare case of a tie.
    def winner(self):
        net = self.net_score(self.player)
        if net > 0:
            return self.player
        
        if net < 0:
            return self.opponent()
        return Othello.EMPTY

    # Count the current score of the specified player.
    def score(self, p):
        return sum(map(lambda row: row.count(p), self.board))

    # Count the net score of the specified player.
    def net_score(self, p):
        return sum(map(lambda row: sum(row), self.board)) * p

    def heuristic_moves(self):
        # Algorithm adapted from a program by Graham Charlton via Tim Hartnell.
        current_score = self.score(self.opponent())
        for x in range(0, self.width()):
            for y in range(0, self.height()):
                o = self.clone()
                
                if not o.move(x, y):
                    continue

                # Count pieces flipped.
                gain = current_score - o.score(self.opponent())

                # If move is on row/column next to an edge, halve score gain.
                # (Rationale: This space is likely to be flipped by an edge move,
                # after which it will be difficult to flip back.)
                if x == 1 or y == 1 or x == self.width() - 2 or y == self.height() - 2:
                    gain = gain / 2
                
                # Otherwise, if move is on row/column on an edge, double score gain.
                # (Rationale: This space is unlikely to be flipped.)
                elif (
                    x == 0 or y == 0 or x == self.width() - 1 or y == self.height() - 1
                ):
                    gain = gain * 2

                yield (gain, (x, y))

    def heuristic_hint(self):
        all_scores = list(self.heuristic_moves())
        if not all_scores:
            return None
    
        max_score = max(all_scores, key=lambda m: m[0])[0]
        max_scores = [m for m in all_scores if m[0] == max_score]
    
        return random.choice(max_scores)[1]

    # Primitive accessor method to set contents of board cell (x,y) to player p.
    def set_cell(self, x, y, p):
        self.board[x][y] = p

    # Primitive accessor method to get contents of board cell (x,y).
    # Returns Othello.OOB if the co-ordinates were out of bounds (off the board).
    def get_cell(self, x, y):
        if x < 0 or y < 0:
            return Othello.OOB
    
        if x >= self.width() or y >= self.height():
            return Othello.OOB
        return self.board[x][y]

    # Returns the width of the board.
    def width(self):
        return len(self.board)

    # Returns the height of the board.
    def height(self):
        return len(self.board[0])


if __name__ == "__main__":
    o = Othello()

    while True:

        print(" ", end="")
        for x in range(0, o.width()):
            print(chr(ord("A") + x), end="")
        print()
    
        for y in range(0, o.height()):
            print(y + 1, end="")
    
            for x in range(0, o.width()):
                c = o.get_cell(x, y)
    
                if c == o.WHITE:
                    print("@", end="")
    
                elif c == o.BLACK:
                    print("O", end="")
    
                else:
                    print(" ", end="")
            print()

        if o.game_over():
            break

        print()
        print("Current scores:")
        print("Black:", o.score(Othello.BLACK))
        print("White:", o.score(Othello.WHITE))
        print()

        print(o.player_name(), "to move:")

        if not o.can_move():
            input("No legal move. Press return to pass.")
            o.flip_player()
            continue

        while True:
            trymove = input("Enter your move. ").rstrip()
    
            if len(trymove) != 2:
                print("Enter a letter followed by a number.")
                continue
    
            x = ord(trymove[0:1].upper()) - ord("A")
    
            if x < 0 or x >= o.width():
                print("Invalid column.")
                continue
    
            y = ord(trymove[1:2]) - ord("1")
    
            if y < 0 or y >= o.height():
                print("Invalid row.")
                continue
    
            if not o.legal_move(x, y):
                print("Illegal move.")
                continue
    
            o.move(x, y)
            o.flip_player()
            break

    print()
    print("Final scores:")
    print("Black:", o.score(Othello.BLACK))
    print("White:", o.score(Othello.WHITE))
    print()

    winner = o.winner()
    
    if winner == Othello.BLACK:
        print("Black wins.")
    
    elif winner == Othello.WHITE:
        print("White wins.")
    
    else:
        print("It is a tie!")
