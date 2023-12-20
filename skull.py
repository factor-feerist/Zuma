from PyQt6.QtGui import QVector2D, QPainter
from PyQt6.QtCore import QRectF


class Skull:
    def __init__(self, position: QVector2D):
        self.position = QVector2D(position)
        pass

    def draw(self, painter: QPainter, width, height):
        painter.drawEllipse(QRectF((self.position.x() - 0.025) * width,
                           (self.position.y() - 0.025) * height, 0.07 * width,
                           0.07 * height))
        pass

