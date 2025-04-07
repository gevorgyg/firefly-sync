import numpy as np
from typing import Callable, List


class Firefly:
    DEFAULT_RESET_STRENGTH = 0.1
    DEFAULT_ANGULAR_FREQ = 2 * np.pi  # 1Hz natural frequency

    class State:
        FLASHING = 0
        WAITING = 1

    def __init__(self, phase: float, x: float, y: float, dt: float,
                 freq: float = DEFAULT_ANGULAR_FREQ,
                 reset_strength: float = DEFAULT_RESET_STRENGTH):
        """
        Base firefly class with core phase advancement logic
        """
        self.phase = phase
        self.x = x
        self.y = y
        self.dt = dt
        self.freq = freq
        self.reset_strength = reset_strength
        self.state = self.State.WAITING
        self.flash_times = []

    def advance_phase(self):
        """
        Advance phase by dt using natural frequency
        """
        self.phase += self.freq * self.dt

    def wrap_and_flash(self, current_time):
        if self.phase >= 2 * np.pi:
            self.phase %= 2 * np.pi
            self.state = self.State.FLASHING
            self.flash_times.append(current_time)

    def correct_phase(self, neighbors: List['Firefly'], current_time: float):
        """
        Base phase correction method - intentionally empty to be overridden
        """
        pass

    def reset_state(self):
        """Reset flashing state after each simulation step"""
        self.state = self.State.WAITING


class LowPassFirefly(Firefly):
    DEFAULT_DECAY = 2.0

    def __init__(self, phase: float, x: float, y: float,
                 freq: float = Firefly.DEFAULT_ANGULAR_FREQ,
                 reset_strength: float = Firefly.DEFAULT_RESET_STRENGTH,
                 memory_window: float = 2.0):
        """
        Firefly with low-pass filtered flash processing

        Args:
            memory_window: Time window for flash memory (seconds)
        """
        super().__init__(phase, x, y, freq, reset_strength)
        self.kernel = self._sin_kernel
        self.memory_window = memory_window
        self.observed_flashes = []  # Times of observed neighbor flashes

    def _exp_kernel(self, t: float, decay=DEFAULT_DECAY):
        return np.exp(-decay * t) if t >= 0 else 0

    def _sin_kernel(self, t, decay=DEFAULT_DECAY):
        return np.sin(2 * np.pi * t) * np.exp(-decay * t) if t >= 0 else 0

    def correct_phase(self, neighbors: List[Firefly], current_time: float):
        t = current_time
        # Record new flashes from neighbors
        for neighbor in neighbors:
            if neighbor.state == self.State.FLASHING:
                self.observed_flashes.append(t)

        # Remove old flashes
        self.observed_flashes = [flash_t for flash_t in self.observed_flashes
                                 if t - flash_t <= self.memory_window]

        # Compute convolution (S ∗ h)(t), where S is an impulse train which is modeled
        influence = sum(self.kernel(t - flash_t)
                        for flash_t in self.observed_flashes)

        # Modify phase based on influence
        self.phase += self.reset_strength * influence * self.dt
