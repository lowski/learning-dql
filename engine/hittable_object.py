
from typing import Tuple, Union

import numpy as np

from engine import util
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

    def ray_dist(self, origin, direction) -> float:
        if isinstance(self, HittableCircle):
            return HittableObject._ray_dist_circle(origin, direction, self)
        elif isinstance(self, HittableRectangle):
            return HittableObject._ray_dist_rectangle(origin, direction, self)
        raise NotImplementedError('Unknown type')

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

    @staticmethod
    def _ray_dist_circle(origin: Tuple[float, float], direction: Tuple[float, float],
                         c: 'HittableCircle') -> float:
        np_origin = np.asarray(origin)
        np_direction = np.asarray(direction)
        np_pos = np.asarray(c.pos)

        projection = util.project(np.subtract(np_pos, np_origin), np_direction)
        if np.dot(projection, np_direction) < 0:
            return -1
        print(projection)
        dist = np.subtract(np_origin + projection, np_pos)
        dist_norm = np.linalg.norm(dist)

        print()

        if abs(dist_norm) > c.radius:
            return -1

        w = (c.radius ** 2 - dist_norm ** 2) ** 0.5

        collision = np_pos + dist - w * \
            (np_direction / np.linalg.norm(np_direction))

        return float(np.linalg.norm(collision - np_origin))

    @staticmethod
    def _ray_dist_rectangle(origin: Tuple[float, float], direction: Tuple[float, float],
                            r: 'HittableRectangle') -> float:
        np_origin = np.asarray(origin)
        np_pos = np.asarray(r.pos)

        # check if origin is inside rectangle
        if np_origin[0] >= np_pos[0] - r.width / 2 and np_origin[0] <= np_pos[0] + r.width / 2 and \
                np_origin[1] >= np_pos[1] - r.height / 2 and np_origin[1] <= np_pos[1] + r.height / 2:
            return -1

        # return -1 if ray does not point toward rectangle

        shortest_dist = -1

        upper_left_corner = tuple(
            np_pos + np.asarray([-r.width / 2, -r.height / 2]))
        upper_right_corner = tuple(
            np_pos + np.asarray([r.width / 2, -r.height / 2]))
        lower_left_corner = tuple(
            np_pos + np.asarray([-r.width / 2, r.height / 2]))
        lower_right_corner = tuple(
            np_pos + np.asarray([r.width / 2, r.height / 2]))

        if np_origin[0] < np_pos[0]:
            # check left line
            intersection = util.ray_line_intersection(
                origin, direction, (upper_left_corner, lower_left_corner))
            if intersection is not None:
                dist = np.linalg.norm(np.subtract(intersection, np_origin))
                if shortest_dist == -1 or dist < shortest_dist:
                    shortest_dist = dist
        else:
            # check right line
            intersection = util.ray_line_intersection(
                origin, direction, (upper_right_corner, lower_right_corner))
            if intersection is not None:
                dist = np.linalg.norm(np.subtract(intersection, np_origin))
                if shortest_dist == -1 or dist < shortest_dist:
                    shortest_dist = dist

        if np_origin[1] < np_pos[1]:
            # check top line
            intersection = util.ray_line_intersection(
                origin, direction, (upper_left_corner, upper_right_corner))
            if intersection is not None:
                dist = np.linalg.norm(np.subtract(intersection, np_origin))
                if shortest_dist == -1 or dist < shortest_dist:
                    shortest_dist = dist
        else:
            # check bottom line
            intersection = util.ray_line_intersection(
                origin, direction, (lower_left_corner, lower_right_corner))
            if intersection is not None:
                dist = np.linalg.norm(np.subtract(intersection, np_origin))
                if shortest_dist == -1 or dist < shortest_dist:
                    shortest_dist = dist

        return float(shortest_dist)


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
