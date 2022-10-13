import tkinter

from engine.base import UpdatableComponent, DrawableComponent
from engine.physics_object import PhysicalCircle
from learning.agent import Agent


class Scene(UpdatableComponent, DrawableComponent):
    def __init__(self, borders, goals, starting_pos, num_rays=2):
        super().__init__()
        self._borders = borders
        self._goals = goals
        self._starting_pos = starting_pos
        self._num_rays = num_rays
        self._agent = Agent(PhysicalCircle(10, color='red', pos=self._starting_pos), self._borders, num_rays=self._num_rays)
        self.reset()

    def update(self):
        for x in self._borders + self._goals + [self._agent]:
            if isinstance(x, UpdatableComponent):
                x.update()

    def draw(self, canvas: tkinter.Canvas):
        for x in self._borders + self._goals + [self._agent]:
            if isinstance(x, DrawableComponent):
                x.draw(canvas)

    def reset(self):
        self._agent = Agent(PhysicalCircle(10, color='red', pos=self._starting_pos), self._borders, num_rays=self._num_rays)

    @property
    def agent(self):
        return self._agent

    @property
    def agent_hit_border(self):
        for border in self._borders:
            if border.hittable.hit(self._agent.obj.hittable):
                return True
        return False

    @property
    def agent_hit_goal(self):
        for goal in self._goals:
            if goal.hittable.hit(self._agent.obj.hittable):
                return True
        return False
