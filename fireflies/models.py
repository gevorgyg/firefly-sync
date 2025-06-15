from dataclasses import dataclass
from enum import Enum
import numpy as np
from numpy import pi
import networkx as nx

from utils import DEFAULT_FREQ_RAD_S, DEFAULT_PHASE_THRESHOLD_RAD, State


@dataclass
class Firefly:
    id: int
    phase_rad: float
    freq_rad_s: float = DEFAULT_FREQ_RAD_S
    flash_threshold: float = DEFAULT_PHASE_THRESHOLD_RAD
    state: State = State.WAITING

    def advance_phase(self, t_s: float):
        """
        Advance the phase of the firefly by a given number of seconds.
        If the phase exceeds the threshold, set the state to FLASHING.
        The firefly is resetted manually after it flashes (i.e. the user need to call reset() to
        update the state and clip the phase overshoot).
        """
        self.phase_rad += self.freq_rad_s * t_s
        if self.phase_rad >= self.flash_threshold:
            self.state = State.FLASHING

    def is_flashing(self):
        return self.state == State.FLASHING

    def is_waiting(self):
        return self.state == State.WAITING

    def reset(self):
        """ Reset the firefly's phase and state. """
        self.phase_rad = 0.0
        self.state = State.WAITING
