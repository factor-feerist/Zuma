from PyQt6.QtGui import QVector2D, QImage

from balls import Ball, RollingBall, BallRepresentation, FlyingBall
from route import ComplexRoute
from random import randint
from frog import Frog


class UpdateManager:
    def __init__(self, route: ComplexRoute, mouse_rel_pos_getter, frog_position, balls_count):
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
        self.balls_count = balls_count
        self.end_of_game = False
        self.balls_on_route = []
        self.flying_balls = []
        self.last_attached_ball_index = -1

        self.frog = Frog(lambda: next(self.generate_next_frog_ball()), frog_position, mouse_rel_pos_getter)
        self.ball_summoner = self.try_summon_ball_at_route()
        pass

    def update(self):
        # what is this?
        self.resolve_collisions()

        self.update_rolling_balls_position()
        next(self.ball_summoner)
        self.frog.update()
        for ball in self.flying_balls:
            flying = FlyingBall.get_instance(ball)
            flying.update_position_with_time(1 / 60)

        # delta = 1 / (60 * 15)
        # self.update_last_attached_ball_index()
        # if self.last_attached_ball_index == len(self.balls_on_route) - 1:
        #     for ball in self.balls_on_route:
        #         r = RollingBall.get_instance(ball)
        #         r.update_position_on_route(delta)
        #         ball.position = self.route.get_position(
        #             r.position_on_route)
        # else:
        #     for ball in self.balls_on_route[self.last_attached_ball_index + 1:]:
        #         r = RollingBall.get_instance(ball)
        #         r.update_position_on_route(-delta)
        #         ball.position = self.route.get_position(
        #             r.position_on_route)
        # for ball in self.flying_balls:
        #     flying = FlyingBall.get_instance(ball)
        #     flying.update_position_with_time(1 / 60)
        # if self.can_add_ball(Ball(0.08, 0, self.route.routes[0].from_point)):
        #     new_ball = next(self.generate_next_ball_on_route())
        #     self.balls_by_color_id[new_ball.color_id] += 1
        #     self.balls_on_route.insert(0, new_ball)
        #     self.last_attached_ball_index += 1

    def draw(self, painter, width, height):
        self.frog.draw(painter, width, height)
        self.draw_balls(self.balls_on_route, painter, width, height)
        self.draw_balls(self.flying_balls, painter, width, height)
        pass

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
            ball.position = self.route.get_position(rolling.position_on_route)
        pass

    def update_last_attached_ball_index(self):
        print(self.last_attached_ball_index)
        for i in range(1, len(self.balls_on_route)):
            previous, current = self.balls_on_route[i - 1:i + 1]
            if not previous.is_intersected_by(current):
                self.last_attached_ball_index = i - 1
                return
        if len(self.balls_on_route) == 1:
            self.last_attached_ball_index = 0
            return
        self.last_attached_ball_index = -1
        pass

    def on_mouse_click(self):
        self.flying_balls.append(self.frog.fire_ball())

    def resolve_collisions(self):
        for flying_ball, index in self.get_collisions():
            self.flying_balls.remove(flying_ball)
            self.insert_ball(index, flying_ball)
            self.update_last_attached_ball_index()
            if self.last_attached_ball_index == len(self.balls_on_route) - 1:
                pass
                #self.remove_same_color_segments()

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
        self.balls_on_route.insert(index, ball)
        for i in range(index + 1, len(self.balls_on_route)):
            RollingBall.get_instance(self.balls_on_route[i]).update_position_on_route(2 * self.balls_on_route[i-1].radius)

    def generate_next_ball_on_route(self):
        for i in range(self.balls_count):
            ball = Ball(0.08,
                        randint(0, len(self.balls_by_color_id.keys()) - 1),
                        QVector2D(0.0, 0.0))
            ball.set_trait(RollingBall(ball))
            ball.set_trait(BallRepresentation(ball, QImage()))
            yield ball

    def generate_next_frog_ball(self):
        ball = Ball(0.08,
                        randint(0, len(self.balls_by_color_id.keys()) - 1),
                        self.frog_position)
        ball.set_trait(BallRepresentation(ball, QImage()))
        yield ball
        while not self.end_of_game:
            allowed = self.get_color_ids_on_route()
            ball = Ball(0.08, allowed[randint(0, len(allowed) - 1)], self.frog_position)
            ball.set_trait(BallRepresentation(ball, QImage()))
            yield ball

    def get_color_ids_on_route(self):
        result = []
        for k in self.balls_by_color_id.keys():
            if self.balls_by_color_id[k] != 0:
                result.append(k)
        return result

    def can_add_ball(self, ball):
        return not any(
            ball.is_intersected_by(other) for other in self.balls_on_route if other != ball)
