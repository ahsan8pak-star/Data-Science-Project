"""
Othello GUI, task 4 of 4: board frame scaffold.

Hosts the grid of GridCell instances for the Othello GUI, completing the
scaffold sequence started in task 3.
"""

from PyQt5.QtWidgets import QWidget


class OthelloGUI4(QWidget):
    """Board container for the Othello GUI (task 4 scaffold)."""

    def __init__(self, parent=None):
        """Initialise the board container."""
        super().__init__(parent)

