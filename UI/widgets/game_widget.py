import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
import math
from PyQt6.QtCore import QTimer, QRectF, Qt
from PyQt6.QtGui import QPainter, QColor, QVector2D, QImage

from update_manager import UpdateManager
from balls import Ball, BallRepresentation, RollingBall, FlyingBall

from route import RouteLine, ComplexRoute
from frog import Frog
from skull import Skull
from route import EndOfRouteError
from update_manager import WinException
import utils
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


class GameWidget(QWidget):
    def __init__(self, on_end_of_game):
        super().__init__()
        self.on_end_of_game = on_end_of_game
        self.setMouseTracking(True)
        self.timer = QTimer(self)
        self.timer.setInterval(int(1000 / 60))
        self.timer.timeout.connect(self.update)

        self.timer_label = QLabel(parent=self)
        # self.timer_label.hide()
        self.passed_time = 0
        self.time_limit = 0

        self.score_label = QLabel(self)
        self.init_ui()

        self.mouse_position = None
        self.update_manager = None
        pass

    def init_ui(self):
        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        box.addWidget(self.timer_label)
        box.addWidget(self.score_label)
        pass

    def run_game(self, level):
        scull = Skull(level.skull_pos)
        self.passed_time = 0
        self.time_limit = None
        if level.time_limit is not None:
            self.timer_label.show()
            self.time_limit = level.time_limit
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
        utils.play_sound(utils.Sounds.SPIT)
        self.update_manager.on_mouse_click()
        pass

    def update(self) -> None:
        super().update()
        self.score_label.setText(f'scores: {self.update_manager.score}')
        try:
            self.update_manager.update()
            self.passed_time += 1/60
            if self.time_limit is not None:
                self.timer_label.setText(f"{self.time_limit - self.passed_time}")
                if self.time_limit <= self.passed_time:
                    self.end_game(False)
        except EndOfRouteError:
            self.end_game(False)
        except WinException:
            self.end_game(True)
        pass

    def end_game(self, is_win):
        self.timer.stop()
        self.on_end_of_game(is_win)
        self.timer_label.hide()
        pass

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.update_manager.draw(painter, self.width(), self.height())
        painter.end()