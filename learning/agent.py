import typing

from engine.base import UpdatableComponent, DrawableComponent
from engine.movable_addon import MovableAddon
from engine.physics_object import PhysicsObject


class Agent(UpdatableComponent, DrawableComponent):
    def __init__(self, obj: PhysicsObject, hittables: typing.List[PhysicsObject]):
        super().__init__()
        self.movable = MovableAddon(obj)
        self.obj = obj
        self.hittables = hittables
        self._rays = [(0, -1), (0, 1)]

    @property
    def observation(self) -> typing.List[float]:
        """
        Return the observation of the agent. This will be the distance in the direction of self._rays.
        """
        distances = []

        for ray in self._rays:
            min_dist = -1
            for obj in self.hittables:
                dist = obj.hittable.ray_dist(self.obj.pos, ray)
                if min_dist == -1 or (dist != -1 and dist < min_dist):
                    min_dist = dist
            distances.append(min_dist)
        return distances

    @property
    def velocity(self) -> typing.Tuple[float, float]:
        return self.movable.velocity

    def run_action(self, idx):
        """
        Execute the given action
        :param idx:  ID of the desired action (0, 1, 2, 3, 4 = left, up, right, down, nothing)
        :return:
        """
        if idx == 0:
            self.movable.apply_force((0, -0.2))
        elif idx == 1:
            self.movable.apply_force((0, 0.2))
        elif idx == 2:
            self.movable.apply_force((-0.2, 0))
        elif idx == 3:
            self.movable.apply_force((0.2, 0))
        elif idx == 4:
            pass
        else:
            raise ValueError('Can only run actions 0 to 4. Unknown action: {}'.format(idx))

    def update(self):
        self.movable.update()

    def draw(self, canvas):
        self.obj.draw(canvas)
