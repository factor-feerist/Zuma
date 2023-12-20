import abc
from PyQt6.QtGui import QVector2D, QImage, QPainter, QColor
from PyQt6.QtCore import QRectF
from traits.trait import Trait
from traits.trait_holder import TraitHolder


COLORS = \
    {
        0: QColor(175, 175, 175),
        1: QColor(0, 0, 0),
        2: QColor(255, 255, 255),
        3: QColor(255, 175, 25),
        4: QColor(255, 255, 0),
        5: QColor(25, 255, 175),
        6: QColor(0, 255, 255),
        7: QColor(150, 25, 255),
        8: QColor(255, 0, 255),
        9: QColor(175, 255, 25),
        10: QColor(25, 175, 255),
        11: QColor(255, 25, 125)
    }


class Ball(TraitHolder):
    def __init__(self, radius, color_id, position: QVector2D):
        super().__init__()
        self.radius = radius
        self.color_id = color_id
        self.position = QVector2D(position)
        pass

    def is_intersected_by(self, other):
        eps = 1e-5
        return self.position.distanceToPoint(other.position) - eps <= self.radius + other.radius


class RollingBall(Trait):
    name = 'rolling_ball'

    def __init__(self, ball: Ball, position_on_route=0):
        self.ball = ball
        self.position_on_route = position_on_route
        pass

    def update_position_on_route(self, delta):
        self.position_on_route += delta
        pass

    @classmethod
    def get_instance(cls, holder):
        value: RollingBall = super().get_instance(holder)
        return value


class BallRepresentation(Trait):
    name = 'ballRepresentation'

    def __init__(self, ball: Ball, image: QImage):
        self.ball = ball
        self.image = image
        pass

    def draw(self, painter: QPainter, width, height):
        eps = 0.1
        ball_diameter = 2 * self.ball.radius
        painter.setBrush(COLORS[self.ball.color_id])
        rect = QRectF((self.ball.position.x() - self.ball.radius) * width, (self.ball.position.y() - self.ball.radius) * height,
                      ball_diameter * width + eps, ball_diameter * height + eps)
        # painter.drawImage(rect, self.image)
        painter.drawEllipse(rect)
        pass

    @classmethod
    def get_instance(cls, holder):
        value: BallRepresentation = super().get_instance(holder)
        return value


class FlyingBall(Trait):
    name = 'flyingBall'

    def __init__(self, ball: Ball, direction: QVector2D, speed=0.5):
        self.ball = ball
        self.direction = QVector2D(direction.normalized())
        self.speed = speed
        pass

    def update_position_with_time(self, delta_time: float):
        self.update_position_with_distance(self.speed * delta_time)
        pass

    def update_position_with_distance(self, distance: float):
        self.ball.position += self.direction * distance
        pass

    @classmethod
    def get_instance(cls, holder):
        value: FlyingBall = super().get_instance(holder)
        return value


class FlyingToPlayerBall(Trait):
    name = 'flying-in-the-face-of-player-ball'

    def __init__(self, ball: Ball, scaling_speed=0.5):
        self.ball = ball
        self.scaling_speed = scaling_speed
        pass

    def update_size_with_time(self, delta_time):
        self.update_size_with_scalar(delta_time*self.scaling_speed)
        pass

    def update_size_with_scalar(self, radius_delta):
        self.ball.radius += radius_delta
        pass

    @classmethod
    def get_instance(cls, holder):
        value = super().get_instance(holder)
        return value


class Coin(Trait):
    name = 'coin'


# ball = Ball(4, 3, QVector2D(0, 0))
#
# ball.set_trait(Coin())
#
# Coin.get_instance(ball)
