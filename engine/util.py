from typing import Tuple, Union

import numpy as np


def project(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    return (np.dot(u, v) / np.dot(v, v)) * v


def angle(u: np.ndarray, v: Union[np.ndarray, None] = None) -> float:
    v = np.asarray([1, 0]) if v is None else v
    return np.degrees(np.arccos(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))))


def rotation_matrix(rad):
    rad *= np.pi
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c, -s], [s, c]])


def rotate(vec, rad):
    return np.dot(rotation_matrix(rad), vec).round(decimals=5)


def ray_line_intersection(origin: Tuple[float, float], direction: Tuple[float, float], line: Tuple[Tuple[float, float], Tuple[float, float]]) -> Union[None, Tuple[float, float]]:
    """
    Returns the point of intersection between a line and a ray.
    If there is no intersection, returns None.
    If the intersection is outside the the line, returns None.
    """
    p1, p2 = line
    p1 = np.asarray(p1)
    p2 = np.asarray(p2)
    np_origin = np.asarray(origin)
    np_direction = np.asarray(direction)

    (x1, y1), (x2, y2) = line
    (x3, y3), (x4, y4) = origin, (origin[0] +
                                  np_direction[0], origin[1] + np_direction[1])

    # t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / \
    #     ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
    divisor = ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
    if divisor == 0:
        return None

    u = ((x1 - x3)*(y1 - y2) - (y1 - y3)*(x1 - x2)) / divisor

    if u < 0:
        return None

    intersection_point = np_origin + u * np_direction
    # round to 5 decimal places
    intersection_point = round(intersection_point[0], 5), round(
        intersection_point[1], 5)

    # return None if the intersection point is not between p1 and p2
    if not (min(x1, x2) <= intersection_point[0] <= max(x1, x2) and min(y1, y2) <= intersection_point[1] <= max(y1, y2)):
        return None

    return tuple(intersection_point)
