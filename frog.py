import sys
from PyQt6.QtWidgets import QApplication
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, QRectF
from PyQt6.QtGui import QPainter, QColor, QVector2D
from balls import Ball, BallRepresentation, RollingBall, FlyingBall

from route import RouteLine, ComplexRoute
from PyQt6.QtGui import QImage


class Frog:
    def __init__(self, ball_getter_func, position: QVector2D, mouse_abs_position_getter):
        self.ball_getter_func = ball_getter_func
        self.current_ball: Ball = self.ball_getter_func()
        # self.next_ball: Ball = self.ball_getter_func()
        self.position = QVector2D(position)
        self.mouse_abs_position_getter = mouse_abs_position_getter
        self.forward_direction = QVector2D(1, 0)
        pass

    def update(self):
        self._update_forward_direction()
        pass

    def _update_forward_direction(self):
        vector: QVector2D = self.mouse_abs_position_getter() - self.position
        if vector.x() != 0 or vector.y() != 0:
            self.forward_direction = vector.normalized()
        pass

    def _draw_frog_ball(self, painter: QPainter, width, height):
        representation = BallRepresentation.get_instance(self.current_ball)
        if representation is not None:
            representation.draw(painter, width, height)
        pass

    def fire_ball(self):
        ball = self.current_ball
        self.current_ball: Ball = self.ball_getter_func()
        ball.set_trait(FlyingBall(ball, direction=self.forward_direction))
        return ball

    def draw(self, painter: QPainter, width, height):
        painter.translate(self.position.x() * width,
                          self.position.y() * height)
        angle = self.get_angle()
        painter.rotate(-angle)
        painter.setBrush(QColor(15, 240, 15))
        painter.drawEllipse(
            QRectF(-25, -35, 50, 70))
        painter.rotate(angle)
        painter.translate(-self.position.x() * width,
                          -self.position.y() * height)
        self._draw_frog_ball(painter, width, height)
        pass

    def get_angle(self):
        vector = self.forward_direction
        vector2 = QVector2D(1, 0)
        angle = math.acos(QVector2D.dotProduct(vector, vector2) / (
                    vector.length() * vector2.length()))
        if vector.y() > 0:
            angle = 2 * math.pi - angle
        return (angle + math.pi / 2) * 180 / math.pi
    pass
