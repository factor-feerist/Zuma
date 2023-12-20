import abc
from PyQt6.QtGui import QVector2D, QImage, QPainter, QColor
from PyQt6.QtCore import QRectF
from traits.trait import Trait
from traits.trait_holder import TraitHolder


class Ball(TraitHolder):
    def __init__(self, radius, color_id, position: QVector2D):
        super().__init__()
        self.radius = radius
        self.color_id = color_id
        self.position = QVector2D(position)
        pass


class RollingBall(Trait):
    def __init__(self, ball: Ball, position_on_route=0):
        self.ball = ball
        self.position_on_route = position_on_route
        pass

    def update_position_on_route(self, delta):
        self.position_on_route += delta
        pass

    name = 'rolling_ball'


class BallRepresentation(Trait):
    name = 'ballRepresentation'

    def __init__(self, ball: Ball, image: QImage):
        self.ball = ball
        self.image = image
        pass

    def draw(self, painter: QPainter, width, height):
        eps = 0.1
        ball_diameter = 2 * self.ball.radius
        painter.setBrush(QColor(0, 200, 200))
        rect = QRectF(self.ball.position.x() * width, self.ball.position.y() * height,
                      ball_diameter * width + eps, ball_diameter * height + eps)
        # painter.drawImage(rect, self.image)
        painter.drawEllipse(rect)


class Coin(Trait):
    name = 'coin'


# ball = Ball(4, 3, QVector2D(0, 0))
#
# ball.set_trait(Coin())
#
# Coin.get_instance(ball)
