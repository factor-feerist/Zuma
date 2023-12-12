import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, QRectF
from PyQt6.QtGui import QPainter, QColor, QVector2D


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
        self.flying_balls = []

    def start(self):
        self.timer.start()

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.draw_frog(painter)
        painter.end()

    def draw_frog(self, painter):
        painter.translate(self.frog_position.x(),
                          self.frog_position.y())
        angle = self.get_angle()
        painter.rotate(-angle)
        painter.setBrush(QColor(15, 240, 15))
        painter.drawEllipse(
            QRectF(-35, -25, 70, 50))
        painter.rotate(angle)
        painter.translate(-self.frog_position.x(),
                          -self.frog_position.y())

    def get_angle(self):
        vector = self.mouse_position - self.frog_position
        vector2 = QVector2D(1, 0)
        angle = math.acos(QVector2D.dotProduct(vector, vector2) / (
                    vector.length() * vector2.length()))
        if vector.y() > 0:
            angle = 2 * math.pi - angle
        return (angle + math.pi / 2) * 180 / math.pi

    def mouseMoveEvent(self, event):
        self.mouse_position = QVector2D(event.position())

    def mousePressEvent(self, event):

