import abc
from PyQt6.QtGui import QVector2D


class Route(abc.ABC):
    @abc.abstractmethod
    def get_position(self, distance):
        pass

    @abc.abstractmethod
    def get_len(self):
        pass
    pass


class EndOfRouteError(StopIteration):
    pass


class RouteLine(Route):
    def __init__(self, from_point: QVector2D, to_point: QVector2D):
        self.from_point = from_point
        self.to_point = to_point
        self.delta_vector = to_point - from_point
        self.length = self.delta_vector.length()
        pass

    def get_position(self, distance):
        t = distance / self.length
        if t > 1 + 1e5:
            raise ValueError(f'distance must be <= length')
        return self.from_point + t * self.delta_vector

    def get_len(self):
        return self.length
    pass


class ComplexRoute(Route):
    def __init__(self, *routes):
        self.length = 0
        self.routes = []
        for r in routes:
            route: Route = r
            self.length += route.get_len()
            self.routes.append(route)
        pass

    def get_position(self, distance):
        for route in self.routes:
            if route.get_len() >= distance:
                return route.get_position(distance)
            else:
                distance -= route.get_len()
        raise EndOfRouteError('end of route reached')

    def get_len(self):
        return self.length
