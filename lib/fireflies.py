import numpy as np
from typing import Callable, List


class Firefly:
    DEFAULT_RESET_STRENGTH = 0.1
    DEFAULT_ANGULAR_FREQ = 2 * np.pi  # 1Hz natural frequency
    PHASE_THRESHOLD = 2 * np.pi  # When phase is >= PHASE_THRESHOLD, firefly is considered to be flashing

    class State:
        FLASHING = 1
        WAITING = 0

    def __init__(self, phase: float, x: float, y: float,
                 neighbours: List['Firefly'],
                 freq: float = DEFAULT_ANGULAR_FREQ,
                 phase_threshold: float = PHASE_THRESHOLD):
        """
        Base firefly class with core phase advancement logic
        """
        self.phase = phase
        self.neighbours = neighbours
        self.freq = freq
        self.phase_threshold = phase_threshold
        self.state = self.State.WAITING

    def advance_phase(self, epsilon):
        if self.state == self.State.FLASHING:
            return
        self.phase += epsilon
        if self.phase >= self.phase_threshold:
            self.state = self.State.FLASHING

    def is_flashing(self):
        return self.state == self.State.FLASHING

    def reset(self):
        self.phase = 0
        self.state = self.State.WAITING
