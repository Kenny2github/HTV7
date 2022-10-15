import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget
)

from .main_widget import MainWidget

class BestWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Biological Ecosystem Simulator and Tweaker')

        widget = QWidget(self)
        layout = QVBoxLayout(widget)
        layout.addWidget(MainWidget(), Qt.AlignmentFlag.AlignCenter)
        widget.setLayout(layout)

        self.setCentralWidget(widget)

def run() -> None:
    app = QApplication([])

    mainWindow = BestWindow()
    mainWindow.resize(800, 600)
    mainWindow.show()

    sys.exit(app.exec())
