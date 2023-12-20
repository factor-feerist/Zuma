import sys
from PyQt6.QtWidgets import QApplication, QWidget
import math
from PyQt6.QtCore import QTimer, QRectF
from PyQt6.QtGui import QPainter, QColor, QVector2D, QImage

from update_manager import UpdateManager
from balls import Ball, BallRepresentation, RollingBall, FlyingBall

from route import RouteLine, ComplexRoute
from frog import Frog
from skull import Skull
from route import EndOfRouteError
import utils


class GameWidget(QWidget):
    def __init__(self, on_end_of_game):
        super().__init__()
        self.on_end_of_game = on_end_of_game
        self.setMouseTracking(True)
        self.timer = QTimer(self)
        self.timer.setInterval(int(1000 / 60))
        self.timer.timeout.connect(self.update)

        self.mouse_position = None
        self.update_manager = None
        pass

    def run_game(self, level):
        scull = Skull(level.skull_pos)
        self.mouse_position = QVector2D(0, 0)
        self.update_manager = UpdateManager(level.route, self.get_mouse_relative_position, level.frog_pos, scull, level.balls_count)
        self.timer.start()
        pass

    def mouseMoveEvent(self, event):
        self.mouse_position = QVector2D(event.position())
        pass

    def get_mouse_relative_position(self):
        return QVector2D(self.mouse_position.x()/self.width(), self.mouse_position.y()/self.height())

    def mousePressEvent(self, event):
        self.update_manager.on_mouse_click()
        pass

    def update(self) -> None:
        super().update()
        try:
            self.update_manager.update()
        except EndOfRouteError:
            self.timer.stop()
            self.on_end_of_game(False)
        pass

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.update_manager.draw(painter, self.width(), self.height())
        painter.end()