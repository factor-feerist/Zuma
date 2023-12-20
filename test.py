import sys
from PyQt6.QtWidgets import QApplication
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, QRectF
from PyQt6.QtGui import QPainter, QColor, QVector2D
from balls import Ball, BallRepresentation, RollingBall

from route import RouteLine, ComplexRoute
from PyQt6.QtGui import QImage


class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.setInterval(int(1000 / 60))
        self.timer.timeout.connect(self.update)
        self.timer.start()

        r1 = RouteLine(QVector2D(0, 0), QVector2D(0.5, 0.5))
        r2 = RouteLine(QVector2D(0.5, 0.5), QVector2D(1, 0))
        self.route = ComplexRoute(r1, r2)

        self.ball = Ball(0.2, 1, QVector2D(0.5, 0.5))
        self.ball.set_trait(RollingBall(self.ball))
        self.ball.set_trait(BallRepresentation(self.ball, QImage()))
        pass

    def update(self) -> None:
        delta = 1 / (60 * 5)
        r = RollingBall.get_instance(self.ball)
        r.update_position_on_route(delta)
        self.ball.position = self.route.get_position(r.position_on_route)

        super().update()
        pass

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        representer = BallRepresentation.get_instance(self.ball)

        representer.draw(painter, self.width(), self.height())
        painter.end()


app = QApplication([])
#window = MainWindow()
frog_widget = GameWidget()
#window.show()
frog_widget.show()
sys.exit(app.exec())
