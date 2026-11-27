
# Based on code from https://www.pythonguis.com/

# Import necessary libraries.
# Qt6 is current, but Qt5 is in Anaconda and mostly API-compatible.
from PyQt5.QtWidgets import QMainWindow, QLabel

# Qt provides QMainWindow to represent the main window of your application.
# Subclass it to create your own application.
class MainWindow(QMainWindow):
    # The constructor gets run when the class is instantiated.
    def __init__(self):
        super().__init__()

        # Set the window title.
        self.setWindowTitle("Hello")

        # Create a label widget.
        x = QLabel("World")

# Instantiate the main window.
window = MainWindow()
window.show()

