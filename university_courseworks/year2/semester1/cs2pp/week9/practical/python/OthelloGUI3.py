"""
Othello GUI, task 3 of 3: grid cell.

A single grid cell rendered as a pushable button, labelled by column letter
and row number; bounds-checked for the 8x8 board.
"""


class GridCell(QPushButton):
    """A single Othello grid cell as a pushable button."""

    def __init__(self, x, y):
        """Initialise the grid cell at coordinates (x, y)."""
        super().__init__()
        self.x = x  # Column index for the cell
        self.y = y  # Row index for the cell
        if 0 <= x < 8 and 0 <= y < 8:
            self.setText(f"{chr(65 + x)}{y + 1}")  # Label the cell as column letter + row number
