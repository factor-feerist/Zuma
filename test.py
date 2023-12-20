import sys
from PyQt6.QtWidgets import QApplication, QWidget
import math
from PyQt6.QtCore import QTimer, QRectF
from PyQt6.QtGui import QPainter, QColor, QVector2D, QImage

from update_manager import UpdateManager
from balls import Ball, BallRepresentation, RollingBall, FlyingBall

from route import RouteLine, ComplexRoute
from frog import Frog


class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.timer = QTimer(self)
        self.timer.setInterval(int(1000 / 60))
        self.timer.timeout.connect(self.update)
        self.timer.start()

        r1 = RouteLine(QVector2D(0.03, 0), QVector2D(0.03, 0.97))
        r2 = RouteLine(QVector2D(0.03, 0.97), QVector2D(0.97, 0.97))
        r3 = RouteLine(QVector2D(0.97, 0.97), QVector2D(0.97, 0.07))
        r4 = RouteLine(QVector2D(0.97, 0.07), QVector2D(0.07, 0.07))
        r5 = RouteLine(QVector2D(0.07, 0.07), QVector2D(0.07, 0.93))
        r6 = RouteLine(QVector2D(0.07, 0.93), QVector2D(0.93, 0.93))
        r7 = RouteLine(QVector2D(0.93, 0.93), QVector2D(0.93, 0.11))
        r8 = RouteLine(QVector2D(0.93, 0.11), QVector2D(0.11, 0.11))
        route = ComplexRoute(r1, r2, r3, r4, r5, r6, r7, r8)
        skull_position = QVector2D(0.11, 0.11)
        draw_skull_func = lambda painter, width, height: painter.drawEllipse(QRectF((skull_position.x() - 0.025) * width, (skull_position.y() - 0.025) * height, 0.07 * width, 0.07 * height))
        frog_position = QVector2D(0.5, 0.5)
        balls_count = 60

        self.mouse_position = QVector2D(0, 0)
        self.update_manager = UpdateManager(route, self.get_mouse_relative_position, frog_position, skull_position, draw_skull_func, balls_count)
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
        self.update_manager.update()
        super().update()

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.update_manager.draw(painter, self.width(), self.height())
        painter.end()


app = QApplication([])
#window = MainWindow()
frog_widget = GameWidget()
#window.show()
frog_widget.show()
sys.exit(app.exec())
