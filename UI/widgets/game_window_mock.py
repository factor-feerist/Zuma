import sys
from PyQt6.QtWidgets import QApplication
import math
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import QTimer, QRectF
from PyQt6.QtGui import QPainter, QColor, QVector2D
from balls import Ball, BallRepresentation, RollingBall, FlyingBall

from route import RouteLine, ComplexRoute
from PyQt6.QtGui import QImage
from frog import Frog
from PyQt6.QtCore import pyqtSlot, Qt


class GameWindowMock(QWidget):
    def __init__(self, on_win, on_lose):
        super().__init__()
        self.on_win = on_win
        self.on_lose = on_lose
        self.init_ui()
        pass

    def init_ui(self):
        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box.setSpacing(20)

        text_button = QPushButton(text='will you win or will you lose?', parent=self)
        text_button.clicked.connect(lambda: print('do something!'))
        box.addWidget(text_button)

        win_button = QPushButton(text='win')
        win_button.clicked.connect(self.on_win)
        box.addWidget(win_button)

        lose_button = QPushButton(text='lose', parent=self)
        lose_button.clicked.connect(self.on_lose)
        box.addWidget(lose_button)
        pass
    pass
