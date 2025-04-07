from symtable import Function
from typing import Callable

import numpy as np


class Firefly:
    DEFAULT_PHASE_CHANGE = 0.05
    DEFAULT_FLASH_DURATION_SECONDS = 0.1
    DEFAULT_RESETTING_STRENGTH = 0.1
    DEFAULT_ANGULAR_FREQUENCY = 1.0

    class State:
        FLASHING = 0
        WAITING = 1

    def __init__(self, phase, x_cord, y_cord, angular_frequency=1.0, duration=DEFAULT_FLASH_DURATION_SECONDS,
                 resetting_strength=DEFAULT_RESETTING_STRENGTH):
        """
        Firefly class representing a firefly in the network.

        :param phase: Initial phase of the firefly.
        :param x_cord: X coordinate of the firefly in 2D space
        :param y_cord: Y coordinate of the firefly in 2D space
        :param angular_frequency: Angular frequency of the firefly.
        :param duration: Duration of the flash.
        :param resetting_strength: Strength of the resetting effect.
        """
        self.phase = phase
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.angular_frequency = angular_frequency
        self.duration = duration
        self.resetting_strength = resetting_strength
        self.state = self.State.WAITING

    def update(self, neighbours, current_time, dt):
        """
         Update the firefly phase based on neighbors' flashing
         """
        pass

    def increment_phase(self, dt):
        self.phase += self.angular_frequency * dt
        if self.phase >= 1:
            self.phase %= 1
            self._flash()

    """
    The fireflies should call _flash() from the inside of a class and be reset with reset() 
    by the caller after every simulation step
    """

    def _flash(self):
        self.state = self.State.FLASHING

    def reset(self):
        self.state = self.State.WAITING


class LowPassFirefly(Firefly):
    """
    A firefly that uses a low-pass filter to update its phase based on the phases of its neighbours.
    Now supports multiple kernel types for phase modulation.
    """
    MAX_HISTORY_TIME = 1.0  # Only consider flashes within this time window

    def __init__(self, phase, x_cord, y_cord, kernel: Callable, angular_frequency=1.0,
                 duration=Firefly.DEFAULT_FLASH_DURATION_SECONDS,
                 resetting_strength=Firefly.DEFAULT_RESETTING_STRENGTH,
                 ):
        """
        Initialize with optional kernel type selection.

        :param kernel: TODO
        """
        super().__init__(phase, x_cord, y_cord, angular_frequency, duration, resetting_strength)
        self.flash_history = []
        self.kernel = kernel

    def _calculate_kernel(self, time_since_flash):
        """Calculate the kernel value based on selected type"""
        if self.kernel_type == 'sinusoidal':
            # Original phase-sensitive kernel
            return np.sin(self.angular_frequency * time_since_flash) * np.exp(-time_since_flash)
        elif self.kernel_type == 'exponential':
            # Simplified phase-insensitive kernel
            return self.coupling_coeff * np.exp(-time_since_flash)
        else:
            raise ValueError(f"Unknown kernel type: {self.kernel_type}")

    def update(self, neighbours, current_time, dt):
        """
        Update the firefly phase using the selected kernel type.

        :param neighbours: List of neighboring fireflies
        :param current_time: Current simulation time
        :param dt: Time step size
        """
        # Update flash history - record any new flashes
        for neighbour in neighbours:
            if neighbour.state == self.State.FLASHING:
                self.flash_history.append(current_time)

        # Clean up old flash history
        self.flash_history = [t for t in self.flash_history
                              if current_time - t <= self.MAX_HISTORY_TIME]

        # Calculate total influence using selected kernel
        influence = 0
        for flash_time, neighbour in self.flash_history:
            time_since_flash = current_time - flash_time
            influence += self.kernel(time_since_flash)

        self.phase += (self.angular_frequency + self.resetting_strength * influence) * dt

        # Normalize phase to [0, 2π)
        self.phase = self.phase % (2 * np.pi)

        # Update state based on phase
        if 0 <= self.phase < self.duration * self.angular_frequency:
            self.state = self.State.FLASHING
        else:
            self.state = self.State.WAITING
