from typing import List

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

    # bottom line
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
    engine.add(PlayerController(player))

    hit = HitDetector(player, borders, goals)
    engine.add(hit)

    engine.start()
    print('Score: {}'.format(hit.score))


if __name__ == "__main__":
    while True:
        main()
