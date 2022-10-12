from typing import List, Tuple

import numpy as np

from engine.base import DrawableComponent, UpdatableComponent
from engine.engine import Engine
from engine.movable_addon import MovableAddon
from engine.physics_object import (PhysicalCircle, PhysicalRectangle,
                                   PhysicsObject)


class PlayerController(UpdatableComponent, DrawableComponent):
    def __init__(self, obj: PhysicsObject):
        self.movable = MovableAddon(obj)
        self.obj = obj

    def update(self):
        if not self.engine:
            return
        if self.engine.is_key_pressed('w'):
            self.movable.apply_force((0, -0.2))
        if self.engine.is_key_pressed('s'):
            self.movable.apply_force((0, 0.2))
        if self.engine.is_key_pressed('a'):
            self.movable.apply_force((-0.2, 0))
        if self.engine.is_key_pressed('d'):
            self.movable.apply_force((0.2, 0))
        self.movable.update()

    def draw(self, canvas):
        self.obj.draw(canvas)


class DistanceRay(UpdatableComponent, DrawableComponent):
    def __init__(self, origin: PhysicsObject, direction: Tuple[float, float], hittables: List[PhysicsObject]):
        self.origin = origin
        self.direction = tuple(
            np.divide(direction, np.linalg.norm(direction)))
        self._min_distance = -1
        self.hittables = hittables

    def update(self):
        origin = self.origin.pos

        self._min_distance = -1
        for obj in self.hittables:
            dist = obj.hittable.ray_dist(origin, self.direction)
            if self._min_distance == -1 or (dist != -1 and dist < self._min_distance):
                self._min_distance = dist

    def draw(self, canvas):
        if self._min_distance == -1:
            return
        canvas.create_line(self.origin.pos, tuple(np.add(
            self.origin.pos, np.multiply(self.direction, self._min_distance))), fill='green')
        canvas.create_text(tuple(np.add(self.origin.pos, np.multiply(
            self.direction, 25))), text='{:.02f}'.format(self._min_distance), fill='orange', font=('Arial', 10))


class HitDetector(UpdatableComponent):
    def __init__(self, player: PhysicsObject, bad_objects: List[PhysicsObject], good_objects: List[PhysicsObject]):
        super().__init__()
        self.player = player
        self.bad_objects = bad_objects
        self.good_objects = good_objects
        self.score = 0

    def update(self):
        if not self.engine:
            return

        for o in self.bad_objects:
            if self.player.hittable.hit(o.hittable):
                self.engine.stop()

        for o in self.good_objects:
            if self.player.hittable.hit(o.hittable):
                self.score += 1


def main():
    engine = Engine()

    goals = [
        PhysicalRectangle(5, 250, color='yellow', pos=(250, 375)),
    ]
    engine.add(goals)

    borders = [
        PhysicalRectangle(500, 10, color='black', pos=(250, 5)),
        PhysicalRectangle(500, 10, color='black', pos=(250, 495)),
        PhysicalRectangle(10, 500, color='black', pos=(5, 250)),
        PhysicalRectangle(10, 500, color='black', pos=(495, 250)),
        PhysicalRectangle(250, 250, color='black', pos=(250, 250)),
    ]
    engine.add(borders)

    player = PhysicalCircle(10, color='red', pos=(100, 100))

    hit = HitDetector(player, borders, goals)  # type: ignore
    engine.add(hit)

    dist_right = DistanceRay(player, (1, 0), borders)  # type: ignore
    dist_left = DistanceRay(player, (-1, 0), borders)  # type: ignore
    dist_up = DistanceRay(player, (0, -1), borders)  # type: ignore
    dist_down = DistanceRay(player, (0, 1), borders)  # type: ignore
    dist_up_right = DistanceRay(player, (1, -1), borders)  # type: ignore
    dist_up_left = DistanceRay(player, (-1, -1), borders)  # type: ignore
    dist_down_right = DistanceRay(player, (1, 1), borders)  # type: ignore
    dist_down_left = DistanceRay(player, (-1, 1), borders)  # type: ignore

    engine.add([
        dist_right,
        dist_left,
        dist_up,
        dist_down,
        dist_up_right,
        dist_up_left,
        dist_down_right,
        dist_down_left,
    ])

    engine.add(PlayerController(player))

    engine.start()
    print('Score: {}'.format(hit.score))


if __name__ == "__main__":
    while True:
        main()
