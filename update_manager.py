from PyQt6.QtGui import QVector2D

from balls import Ball, RollingBall
from route import ComplexRoute
from random import randint


class UpdateManager:
    def __init__(self, route: ComplexRoute, balls):
        self.route = route
        self.end_of_game = False
        self.balls = balls
        self.last_attached_ball_index = -1
        self.balls_by_color_id =\
            {
                0: 0,
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
                6: 0,
                7: 0,
                8: 0,
                9: 0,
                10: 0,
                11: 0
            }

    def update(self):
        self.update_detached_balls()
        for ball in self.balls[:self.last_attached_ball_index + 1]:
            ball.update_position_on_route()
        # Не забыть всех отрисовать (BallRepresentation)

    def update_detached_balls(self):
        for i in range(1, len(self.balls)):
            previous, current = self.balls[i - 1:i + 1]
            if not previous.ball.is_intersected_by(current.ball):
                self.last_attached_ball_index = i - 1
                return

    def generate_next_ball_on_route(self):
        for i in range(60):
            ball = Ball(0.2,
                        randint(0, len(self.balls_by_color_id.keys()) - 1),
                        QVector2D(0.0, 0.0))
            yield RollingBall(ball)

    def generate_next_frog_ball(self):
        while not self.end_of_game:
            allowed = self.get_color_ids_on_screen()
            yield allowed[randint(0, len(allowed) - 1)]

    def get_color_ids_on_screen(self):
        result = []
        for k in self.balls_by_color_id.keys():
            if self.balls_by_color_id[k] != 0:
                result.append(k)
        return result
