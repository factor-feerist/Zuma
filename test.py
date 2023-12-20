import sys
from PyQt6.QtWidgets import QApplication
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, QRectF
from PyQt6.QtGui import QPainter, QColor, QVector2D
from balls import Ball, BallRepresentation, RollingBall, FlyingBall

from route import RouteLine, ComplexRoute
from PyQt6.QtGui import QImage
from frog import Frog


class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
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

        self.mouse_position = QVector2D(0, 0)

        self.frog = Frog(self.get_ball_generator(), QVector2D(0.5, 0.5),
                         mouse_abs_position_getter=self.get_mouse_relative_position)
        self.flying_balls = []
        pass

    def mouseMoveEvent(self, event):
        self.mouse_position = QVector2D(event.position())
        pass

    def get_mouse_relative_position(self):
        return QVector2D(self.mouse_position.x()/self.width(), self.mouse_position.y()/self.height())

    def mousePressEvent(self, event):
        self.flying_balls.append(self.frog.fire_ball())
        pass

    def get_ball_generator(self):
        def ball_generator():
            ball = Ball(0.1, 1, QVector2D(0, 0))
            ball.set_trait(BallRepresentation(ball, QImage()))
            return ball
        return ball_generator


    def update(self) -> None:
        delta = 1 / (60 * 15)
        r = RollingBall.get_instance(self.ball)
        r.update_position_on_route(delta)
        self.ball.position = self.route.get_position(r.position_on_route)

        self.frog.update()

        for ball in self.flying_balls:
            flying = FlyingBall.get_instance(ball)
            flying.update_position_with_time(1/60)
        super().update()
        pass

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        representer = BallRepresentation.get_instance(self.ball)

        representer.draw(painter, self.width(), self.height())

        self.frog.draw(painter, self.width(), self.height())

        for ball in self.flying_balls:
            repres = BallRepresentation.get_instance(ball)
            repres.draw(painter, self.width(), self.height())

        painter.end()


app = QApplication([])
#window = MainWindow()
frog_widget = GameWidget()
#window.show()
frog_widget.show()
sys.exit(app.exec())
