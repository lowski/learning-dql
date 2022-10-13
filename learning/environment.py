from typing import Any

import numpy as np
from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
from tf_agents.typing import types

from engine.engine import Engine
from engine.physics_object import PhysicalCircle, PhysicalRectangle
from learning.agent import Agent


class Environment(py_environment.PyEnvironment):
    def __init__(self):
        super().__init__()
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=4, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(4, ), dtype=np.float32, minimum=[0, 0, -10, -10], maximum=[500, 500, 10, 10], name='observation')

    def observation_spec(self) -> types.NestedArraySpec:
        return self._observation_spec

    def action_spec(self) -> types.NestedArraySpec:
        return self._action_spec

    @property
    def _state(self):
        state = self._agent.observation + list(self._agent.velocity)
        return np.array(state, dtype=np.float32)

    def _step(self, action: types.NestedArray) -> ts.TimeStep:
        # reset if episode ended
        if self._episode_ended:
            return self._reset()

        # run the action on the agent
        self._agent.run_action(action)
        self._engine.update_objects()

        # terminate episode if agent collided with borders
        for border in self._borders:
            if border.hittable.hit(self._agent.obj.hittable):
                return ts.termination(self._state, reward=0)

        # increase score if the agent collided with goals
        reward = 0.0
        for goal in self._goals:
            if goal.hittable.hit(self._agent.obj.hittable):
                reward += 1.0

        return ts.transition(self._state, reward=reward, discount=1.0)

    def _reset(self) -> ts.TimeStep:
        self._setup_engine()
        self._episode_ended = False
        return ts.restart(self._state)

    def _setup_engine(self):
        self._engine = Engine()

        self._borders = [
            PhysicalRectangle(500, 10, color='black', pos=(250, 150)),
            PhysicalRectangle(500, 10, color='black', pos=(250, 350)),
            PhysicalRectangle(10, 210, color='black', pos=(5, 250)),
            PhysicalRectangle(10, 210, color='black', pos=(495, 250)),
        ]
        self._goals = [
            PhysicalRectangle(2, 210, color='yellow', pos=(75, 250)),
            PhysicalRectangle(2, 210, color='yellow', pos=(150, 250)),
            PhysicalRectangle(2, 210, color='yellow', pos=(225, 250)),
            PhysicalRectangle(2, 210, color='yellow', pos=(300, 250)),
            PhysicalRectangle(2, 210, color='yellow', pos=(375, 250)),
            PhysicalRectangle(2, 210, color='yellow', pos=(450, 250)),
        ]
        self._agent = Agent(PhysicalCircle(10, color='red', pos=(25, 250)), self._borders)

        self._engine.add(self._borders)
        self._engine.add(self._goals)
        self._engine.add(self._agent)

