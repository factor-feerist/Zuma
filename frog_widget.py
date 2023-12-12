import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, QRectF
from PyQt6.QtGui import QPainter, QColor, QVector2D


class FlyingBall:
    diameter = 20#0

    def __init__(self, initial_position: QVector2D, velocity: QVector2D):
        self.position = initial_position
        self.velocity = velocity
        self.existence_time = 0
        pass

    def update(self, delta_time=1):
        self.position += self.velocity * delta_time
        self.existence_time += delta_time
    pass


class FrogWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.setInterval(int(1000 / 60))
        self.timer.timeout.connect(self.update)
        self.start()
        self.frog_position = QVector2D(self.width() // 2, self.height() // 2)
        self.mouse_position = QVector2D(0, 0)
        self.setMouseTracking(True)
        self.flying_balls = [] #: list[FlyingBall] = []
        self.flying_ball_speed = 10
        self.flying_balls_lifetime = 100
        pass

    def start(self):
        self.timer.start()
        pass

    def update(self) -> None:
        self.update_frog_position()
        self.update_all_flying_balls()
        self.kill_some_flying_balls()
        super().update()
        pass

    def update_frog_position(self):
        self.frog_position = QVector2D(self.width() // 2, self.height() // 2)
        pass

    def update_all_flying_balls(self):
        for ball in self.flying_balls:
            ball.update()
        pass

    def kill_some_flying_balls(self):
        for ball in self.flying_balls:
            if ball.existence_time > self.flying_balls_lifetime:
                self.flying_balls.remove(ball)
        pass

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.draw_frog(painter)
        for ball in self.flying_balls:
            self.draw_flying_ball(painter, ball)
        painter.end()

    def draw_frog(self, painter):
        painter.translate(self.frog_position.x(),
                          self.frog_position.y())
        angle = self.get_angle()
        painter.rotate(-angle)
        painter.setBrush(QColor(15, 240, 15))
        painter.drawEllipse(
            QRectF(-25, -35, 50, 70))
        painter.rotate(angle)
        painter.translate(-self.frog_position.x(),
                          -self.frog_position.y())
        pass

    def draw_flying_ball(self, painter, ball: FlyingBall):
        painter.setBrush(QColor(0, 200, 200))
        x = ball.position.x() - ball.diameter // 2
        y = ball.position.y() - ball.diameter // 2
        painter.drawEllipse(QRectF(x, y, ball.diameter, ball.diameter))
        pass

    def get_mouse_vector(self):
        return (self.mouse_position - self.frog_position).normalized()

    def get_angle(self):
        vector = self.get_mouse_vector()
        vector2 = QVector2D(1, 0)
        angle = math.acos(QVector2D.dotProduct(vector, vector2) / (
                    vector.length() * vector2.length()))
        if vector.y() > 0:
            angle = 2 * math.pi - angle
        return (angle + math.pi / 2) * 180 / math.pi

    def mouseMoveEvent(self, event):
        self.mouse_position = QVector2D(event.position())

    def mousePressEvent(self, event):
        direction = self.get_mouse_vector()
        velocity = direction * self.flying_ball_speed
        position = QVector2D(self.frog_position)
        ball = FlyingBall(position, velocity)
        self.flying_balls.append(ball)
        pass

