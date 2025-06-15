from enum import Enum
from numpy import pi

DEFAULT_FREQ_RAD_S = 2 * pi  # 2*pi rad natural frequency
DEFAULT_PHASE_THRESHOLD_RAD = 2 * pi  # When phase is >= PHASE_THRESHOLD, firefly is considered to be flashing


class State(Enum):
    FLASHING = 1
    WAITING = 0
