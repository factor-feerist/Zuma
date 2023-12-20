from route import Route, RouteLine, ComplexRoute
from PyQt6.QtGui import QVector2D
from PyQt6.QtCore import QRectF


class Level:
    def __init__(self, name, route: Route, skull_pos: QVector2D, frog_pos: QVector2D, balls_count):
        self.name = name
        self.route = route
        self.skull_pos = QVector2D(skull_pos)
        self.frog_pos = QVector2D(frog_pos)
        self.balls_count = balls_count
        pass

    def __str__(self):
        return self.name
    pass


def make_first_level():
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
    frog_position = QVector2D(0.5, 0.5)
    balls_count = 60
    return Level(name='level 1', route=route, skull_pos=skull_position,
                 frog_pos=frog_position, balls_count=balls_count)

