import utils

from PyQt6.QtGui import QVector2D, QImage, QColor
from PyQt6.QtCore import QRectF

from balls import Ball, RollingBall, BallRepresentation, FlyingBall
from route import ComplexRoute
from random import randint
from frog import Frog
from skull import Skull


class WinException(Exception):
    pass


class UpdateManager:
    def __init__(self, route: ComplexRoute, mouse_rel_pos_getter, frog_position, skull: Skull, balls_count):
        self.route = route
        self.balls_by_color_id = \
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
        self.frog_position = frog_position
        #self.skull_position = skull_position
        self.skull = skull
        #self.draw_skull_func = draw_skull_func
        self.balls_count = balls_count
        self.end_of_game = False
        self.balls_on_route = []
        self.flying_balls = []

        generator = self.generate_next_frog_ball()
        self.frog = Frog(lambda: next(generator), frog_position, mouse_rel_pos_getter)
        self.ball_summoner = self.try_summon_ball_at_route()
        self.balls_generator_stopped = False
        self.score = 0
        pass

    def update(self):
        # what is this?
        self.check_if_win()

        self.resolve_collisions()

        self.update_rolling_balls_position()
        next(self.ball_summoner)
        self.frog.update()
        for ball in self.flying_balls:
            flying = FlyingBall.get_instance(ball)
            flying.update_position_with_time(1 / 60)

    def draw(self, painter, width, height):
        painter.setBrush(QColor(255, 0, 0))
        self.skull.draw(painter, width, height)
        self.frog.draw(painter, width, height)
        self.draw_balls(self.balls_on_route, painter, width, height)
        self.draw_balls(self.flying_balls, painter, width, height)
        pass

    def check_if_win(self):
        if self.balls_generator_stopped and len(self.balls_on_route) == 0:
            raise WinException

    def draw_balls(self, balls, painter, width, height):
        for b in balls:
            BallRepresentation.get_instance(b).draw(painter, width, height)

    def try_summon_ball_at_route(self):
        def summon_ball(b):
            self.balls_on_route.insert(0, b)
        for ball in self.generate_next_ball_on_route():
            while True:
                if len(self.balls_on_route) == 0:
                    break
                first_rolling = RollingBall.get_instance(self.balls_on_route[0])
                if first_rolling.position_on_route >= ball.radius + first_rolling.ball.radius:
                    break
                yield False
            summon_ball(ball)
            yield True
        self.balls_generator_stopped = True
        while True:
            yield False
        pass

    def update_rolling_balls_position(self):
        delta = 1 / (60 * 15)
        previous_ball = None
        for b in self.balls_on_route:
            ball: Ball = b
            rolling = RollingBall.get_instance(ball)
            if (previous_ball is None) or (ball.is_intersected_by(previous_ball)):
                rolling.update_position_on_route(delta=delta)
            else:
                rolling.update_position_on_route(delta=-delta)
            previous_ball = ball
            ball.position = self.route.get_position(rolling.position_on_route)
        pass

    def on_mouse_click(self):
        self.flying_balls.append(self.frog.fire_ball())

    def resolve_collisions(self):
        for flying_ball, index in self.get_collisions():
            self.flying_balls.remove(flying_ball)
            self.insert_ball(index, flying_ball)
        self.remove_same_color_segments()

    def get_collisions(self):
        collisions = {}
        for flying_ball in self.flying_balls:
            for index, ball in enumerate(self.balls_on_route):
                distance = flying_ball.position.distanceToPoint(ball.position)
                previous = self.balls_on_route[collisions.get(flying_ball, index)]
                if flying_ball.position.distanceToPoint(previous.position) <= distance < flying_ball.radius:
                    collisions[flying_ball] = index
        return collisions.items()

    def insert_ball(self, index, ball):
        ball.set_trait(RollingBall(ball))
        ball.position = QVector2D(self.balls_on_route[index].position)
        RollingBall.get_instance(ball).position_on_route = RollingBall.get_instance(self.balls_on_route[index]).position_on_route
        self.balls_on_route.insert(index, ball)
        for i in range(index + 1, len(self.balls_on_route)):
            rolling = RollingBall.get_instance(self.balls_on_route[i])
            rolling.update_position_on_route(2 * self.balls_on_route[i-1].radius)
            self.balls_on_route[i].position = self.route.get_position(rolling.position_on_route)

    def remove_same_color_segments(self):
        if len(self.balls_on_route) < 3:
            return
        streak = 0
        previous_color_id = None
        for i, b in enumerate(self.balls_on_route):
            if previous_color_id is None:
                streak = 1
                previous_color_id = b.color_id
                continue
            if b.color_id == previous_color_id:
                streak += 1
                continue
            previous_color_id = b.color_id
            if streak > 2:
                for j in range(streak):
                    self.balls_on_route.remove(self.balls_on_route[i-j-1])
                    self.score += 5
                self.on_balls_removed()
                return
            streak = 1
        if streak > 2:
            for j in range(streak):
                self.balls_on_route.remove(self.balls_on_route[i - j])
                self.score += 5
            self.on_balls_removed()
            return
        return

    def on_balls_removed(self):
        utils.play_sound(utils.Sounds.BALLS_DESTROYED)
        pass

    def generate_next_ball_on_route(self):
        for i in range(self.balls_count):
            color_id = randint(0, len(self.balls_by_color_id.keys()) - 1)
            if len(self.balls_on_route) > 1:
                if self.balls_on_route[0].color_id == self.balls_on_route[1].color_id == color_id:
                    while color_id == self.balls_on_route[0].color_id:
                        color_id = randint(0,
                                           len(self.balls_by_color_id.keys()) - 1)
            ball = Ball(0.02,
                        color_id,
                        self.route.routes[0].from_point)
            ball.set_trait(RollingBall(ball))
            ball.set_trait(BallRepresentation(ball, QImage()))
            yield ball

    def generate_next_frog_ball(self):
        ball = Ball(0.02,
                        randint(0, len(self.balls_by_color_id.keys()) - 1),
                        self.frog_position)
        ball.set_trait(BallRepresentation(ball, QImage()))
        print('start')
        yield ball
        while not self.end_of_game:
            allowed = self.get_color_ids_on_route()
            ball = Ball(0.02, allowed[randint(0, len(allowed) - 1)], self.frog_position)
            ball.set_trait(BallRepresentation(ball, QImage()))
            yield ball

    def get_color_ids_on_route(self):
        result = set()
        for b in self.balls_on_route:
            result.add(b.color_id)
        # result = []
        # for k in self.balls_by_color_id.keys():
        #     if self.balls_by_color_id[k] != 0:
        #         result.append(k)
        return list(result)

    def can_add_ball(self, ball):
        return not any(
            ball.is_intersected_by(other) for other in self.balls_on_route if other != ball)
