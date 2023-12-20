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


class LevelChoosingWindow(QWidget):
    def __init__(self, levels, on_exit_button, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.levels = levels
        self.on_exit_button = on_exit_button
        self.init_ui()
        pass

    def init_ui(self):
        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(20)

        button = QPushButton(text='choose level [not working]')
        button.clicked.connect(self.do_something)
        box.addWidget(button)

        exit_button = QPushButton(text='exit')
        exit_button.clicked.connect(self.on_exit_button)

        box.addWidget(exit_button)

        # self.setLayout(box)
        pass

    def do_something(self):
        print('unsupported yet')

    pass
