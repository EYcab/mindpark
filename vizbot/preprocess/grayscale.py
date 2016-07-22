import numpy as np
from gym.spaces import Box
from vizbot.core import Preprocess


class Grayscale(Preprocess):

    def __init__(self, env):
        super().__init__(env)
        low, high = self._env.states.low, self._env.states.high
        self._low, self._high = low.flatten()[0], high.flatten()[0]
        assert (low == self._low).all()
        assert (high == self._high).all()

    @property
    def states(self):
        return Box(self._low, self._high, self._env.states.shape[: -1])

    @property
    def actions(self):
        return self._env.actions

    def reset(self):
        state = self._env.reset()
        state = self._apply(state)
        return state

    def step(self, action):
        state, reward = self._env.step(action)
        state = self._apply(state)
        return state, reward

    @staticmethod
    def _apply(state):
        return state.mean(-1)
