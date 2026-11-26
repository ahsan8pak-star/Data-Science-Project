import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dice, Dice, Baby!")

        # Create a button widget.
        self.b = QPushButton("Let's Roll!")
        self.b.setFixedSize(200,100)
        self.setCentralWidget(self.b)
        
app = QApplication(sys.argv)

window = MainWindow()
window.show()

window.setMinimumSize(640,480)

app.exec()

