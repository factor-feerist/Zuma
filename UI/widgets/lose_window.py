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
import utils


class LoseWindow(QWidget):
    def __init__(self, on_back_to_menu):
        super().__init__()
        self.on_back_to_menu = on_back_to_menu
        self.init_ui()
        utils.set_image_to_background(self, utils.Images.SCARED_SNAKE)
        pass

    def init_ui(self):
        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = QPushButton('you lost; go back', parent=self)
        button.clicked.connect(self.on_back_to_menu)
        box.addWidget(button)
        pass

    pass
