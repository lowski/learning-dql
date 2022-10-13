from typing import Any

import numpy as np
from tf_agents.environments import py_environment
from tf_agents.policies import TFPolicy
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
from tf_agents.typing import types

from engine.engine import Engine
from engine.physics_object import PhysicalCircle, PhysicalRectangle
from learning.agent import Agent
from learning.scene import Scene


class Environment(py_environment.PyEnvironment):
    def __init__(self, scene: Scene):
        super().__init__()
        self._scene = scene
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
        state = self._scene.agent.observation + list(self._scene.agent.velocity)
        return np.array(state, dtype=np.float32)

    def _step(self, action: types.NestedArray) -> ts.TimeStep:
        # reset if episode ended
        if self._episode_ended:
            return self._reset()

        # run the action on the agent
        self._scene.agent.run_action(action)
        self._engine.update_objects()

        # terminate episode if agent collided with borders
        if self._scene.agent_hit_border:
            return ts.termination(self._state, reward=-50)

        # increase score if the agent collided with goals
        reward = 1.0
        if self._scene.agent_hit_goal:
            reward += 10.0

        return ts.transition(self._state, reward=reward, discount=1.0)

    def _reset(self) -> ts.TimeStep:
        self._setup_engine()
        self._episode_ended = False
        return ts.restart(self._state)

    def _setup_engine(self):
        self._engine = Engine()
        self._scene.reset()
        self._engine.add(self._scene)


