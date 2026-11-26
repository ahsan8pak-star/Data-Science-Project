"""
Othello GUI, task 2 of 3: central widget with push button.

Hosts the push button for the Othello GUI; the grid cells from task 3 will
be added around it.
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout


class OthelloGUI2(QWidget):
    """Central widget hosting the Othello push button (task 2)."""

    def __init__(self, parent=None):
        """Build the central widget and wire the push button."""
        super().__init__(parent)
        self.setLayout(QVBoxLayout())  # Layout holding the push button
        self.pushButton = QPushButton("Othello")  # Push button for the Othello GUI
        self.pushButton.clicked.connect(self.push_button)  # Connect the button click to the handler

    def push_button(self):
        """Handle the push button click (task 2 scaffold)."""
        pass
