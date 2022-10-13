from typing import Tuple

import numpy as np

from .base import Positionable, UpdatableComponent


class MovableAddon(UpdatableComponent):
    def __init__(self, positionable: Positionable, drag: float = 0.035):
        super().__init__()
        self._positionable = positionable
        self._speed = 0
        self._direction = (0, 0)
        self.velocity: Tuple[float, float] = (0, 0)
        self._drag = drag

    def update(self):
        self._positionable.pos = self._positionable.pos[0] + \
            self.velocity[0], self._positionable.pos[1] + self.velocity[1]
        self.velocity = self.velocity[0] * \
            (1 - self._drag), self.velocity[1] * (1 - self._drag)

    def apply_force(self, force: Tuple[float, float]):
        self.velocity = self.velocity[0] + \
            force[0], self.velocity[1] + force[1]

    def move(self, vec: Tuple[float, float]):
        self._positionable.pos = self._positionable.pos[0] + vec[0], self._positionable.pos[1] + vec[1]
