from dataclasses import dataclass
from enum import Enum
from numpy import pi

DEFAULT_FREQ_RAD_S = 2 * pi  # 2*pi rad natural frequency
DEFAULT_PHASE_THRESHOLD_RAD = 2 * pi  # When phase is >= PHASE_THRESHOLD, firefly is considered to be flashing


class State(Enum):
    FLASHING = 1
    WAITING = 0


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
