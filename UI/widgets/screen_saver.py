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
from PyQt6.QtCore import Qt
from utils import Images
import utils


class ScreenSaver(QWidget):
    def __init__(self, on_play):
        super().__init__()
        self.on_play = on_play
        self.init_ui()
        utils.set_image_to_background(self, Images.FROG_WITH_GUN)
        pass

    def init_ui(self):
        box = QVBoxLayout(self)
        box.setContentsMargins(50, 50, 50, 50)
        box.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        button = QPushButton('PLAY', parent=self)
        button.clicked.connect(self.on_play)

        box.addWidget(button)
        pass

    pass
