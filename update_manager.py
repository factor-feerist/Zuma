from route import ComplexRoute


class UpdateManager:
    def __init__(self, route: ComplexRoute, balls):
        self.route = route
        self.balls = balls
        self.last_attached_ball_index = -1

    def update_detached_balls(self):
        for i in range(1, len(self._balls)):
            previous, current = self._balls[i - 1:i + 1]
            if not previous.ball.is_intersected_by(current.ball):
                self.last_attached_ball_index = i - 1
                return

    def update(self):
        self.update_detached_balls()
        for ball in self.balls[:self.last_attached_ball_index + 1]:
            ball.update_position_on_route()
