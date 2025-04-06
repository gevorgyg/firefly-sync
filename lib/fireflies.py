from dataclasses import dataclass, field

import numpy as np


@dataclass
class Parameters:
    FLASH_DURATION_SECONDS = 0.1
    RESETTING_STRENGTH = 0.5

    angular_frequency: float
    phase: float
    duration: float = field(default=FLASH_DURATION_SECONDS)
    resetting_strength: float = field(default=RESETTING_STRENGTH)


class Firefly:
    class State:
        FLASHING = 0
        WAITING = 1

    def __init__(self, flash_parameters):
        """
        :param flash_parameters: A dictionary containing parameters of firefly flashing
        """
        self.parameters = flash_parameters
        self.state = self.State.WAITING

    def should_flash(self):
        pass

    def flash(self):
        self.state = self.State.FLASHING

    def reset(self):
        self.state = self.State.WAITING


class EuclideanFirefly(Firefly):
    def __init__(self, flash_parameters, coordinates: np.array):
        """
        EuclideanFirefly is a subclass of Firefly that represents a firefly in a
         euclidean (2D or 3D) space

        :param flash_parameters: A dictionary containing parameters of firefly flashing
        :param coordinates: A tuple containing the x and y coordinates of the firefly
        """
        super().__init__(flash_parameters)
        self.coordinates: np.array = coordinates
