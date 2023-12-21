import sys
import time

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
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer, QSoundEffect


class LevelChoosingWindow(QWidget):
    def __init__(self, levels, choose_level_func, on_exit_button, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.levels = levels
        self.choose_level_func = choose_level_func
        self.on_exit_button = on_exit_button
        self.init_ui()
        utils.set_image_to_background(self, utils.Images.FROG_WITH_GUN)
        pass

    def init_ui(self):
        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(20)

        choose_button = QPushButton(text='choose level wisely')
        choose_button.clicked.connect(self.do_something)
        box.addWidget(choose_button)

        for level in self.levels:
            button = QPushButton(text=f'level {level}', parent=self)
            button.clicked.connect(self.choose_level_maker(level))
            box.addWidget(button)

        exit_button = QPushButton(text='exit')
        exit_button.clicked.connect(self.on_exit_button)

        box.addWidget(exit_button)

        # self.setLayout(box)
        pass

    def do_something(self):
        print('unsupported yet')

    def choose_level_maker(self, level):
        return lambda: self.choose_level_func(level)

    pass
