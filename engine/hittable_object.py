
import typing

from engine.base import Positionable


class HittableObject(Positionable):
    def __init__(self, pos=(0, 0)):
        self.pos = pos

    def hit(self, other) -> bool:
        if isinstance(self, HittableCircle):
            if isinstance(other, HittableCircle):
                return HittableObject._hit_circle_circle(self, other)
            elif isinstance(other, HittableRectangle):
                return HittableObject._hit_circle_rectangle(self, other)
            else:
                raise TypeError("Unknown type")
        elif isinstance(self, HittableRectangle):
            if isinstance(other, HittableCircle):
                return HittableObject._hit_circle_rectangle(other, self)
            elif isinstance(other, HittableRectangle):
                return HittableObject._hit_rectangle_rectangle(self, other)
            else:
                raise TypeError("Unknown type")
        return False

    @staticmethod
    def _hit_circle_circle(c1: 'HittableCircle', c2: 'HittableCircle') -> bool:
        return (c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2 <= (c1.radius + c2.radius) ** 2

    @staticmethod
    def _hit_circle_rectangle(c: 'HittableCircle', r: 'HittableRectangle') -> bool:
        dist_x = abs(c.x - r.x)
        dist_y = abs(c.y - r.y)

        if dist_x > (r.width / 2 + c.radius) or dist_y > (r.height / 2 + c.radius):
            return False

        if dist_x <= (r.width / 2) or dist_y <= (r.height / 2):
            return True

        corner_distance_sq = (dist_x - r.width / 2) ** 2 + \
            (dist_y - r.height / 2) ** 2
        return corner_distance_sq <= (c.radius ** 2)

    @staticmethod
    def _hit_rectangle_rectangle(r1: 'HittableRectangle', r2: 'HittableRectangle') -> bool:
        dist_x = abs(r1.x - r2.x)
        dist_y = abs(r1.y - r2.y)

        return not (dist_x > (r1.width / 2 + r2.width / 2) or dist_y > (r1.height / 2 + r2.height / 2))


class HittableCircle(HittableObject):
    def __init__(self, radius: float, pos=(0, 0)):
        super().__init__(pos)
        self.radius = radius


class HittableRectangle(HittableObject):
    def __init__(self, width: float, height: float, rotation: float = 0, pos=(0, 0)):
        super().__init__(pos)
        self.width = width
        self.height = height
        self.rotation = rotation
