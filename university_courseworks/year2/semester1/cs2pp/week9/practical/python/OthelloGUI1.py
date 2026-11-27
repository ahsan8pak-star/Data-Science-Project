"""
Othello GUI, task 1 of 3: main window scaffold.

Builds the Othello main window that will host the board, transport controls
and grid cells introduced in the later tasks.
"""

from PyQt5.QtWidgets import QApplication, QMainWindow

import sys  # Standard library: provides sys.argv and the Qt event-loop exit


class OthelloGUI1(QMainWindow):
    """Main window for the Othello GUI; task-1 scaffold."""

    def __init__(self):
        """Initialise the Othello main window and apply task-1 window settings."""
        super().__init__()
        self.setWindowTitle("Othello")  # Sets the window title
        self.setMinimumSize(800, 800)  # Sets the minimum window size


if __name__ == "__main__":  # Standard Python guard: runs the Othello GUI main window when executed directly
    app = QApplication(sys.argv)
    window = OthelloGUI1()
    window.show()

    sys.exit(app.exec_())

