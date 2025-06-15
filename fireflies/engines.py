import numpy as np
from abc import ABC, abstractmethod


class BaseEngine(ABC):
    """Abstract base class for simulation engines."""

    def __init__(self, adjacency_matrix=None, laplacian=None):
        """
        Initialize the engine with network matrices.

        Args:
            adjacency_matrix (np.array, optional): Network adjacency matrix.
            laplacian (np.array, optional): Network Laplacian matrix.
        """
        self.adjacency_matrix = adjacency_matrix
        self.laplacian = laplacian

    @abstractmethod
    def update(self, phases, time_step_s):
        """
        Update phases based on the model.

        Args:
            phases (np.array): Current phases of fireflies
            time_step_s (float): Time step in seconds
        Returns:
            np.array: Updated phases.
        """
        pass


class TrivialEngine(BaseEngine):
    def __init__(self, phase_increment_per_second=1.0, adjacency_matrix=None, laplacian=None):
        """
        Initialize with phase increment rate and network matrices.

        Args:
            phase_increment_per_second (float): Rate of phase change per second.
            adjacency_matrix (np.array, optional): Network adjacency matrix.
            laplacian (np.array, optional): Network Laplacian matrix.
        """
        super().__init__(adjacency_matrix, laplacian)
        self.phase_increment_per_second = phase_increment_per_second

    def update(self, phases, time_step_s):
        """
        Increment phases based on time step.

        Args:
            phases (np.array): Current phases of fireflies.
            time_step_s (float): Time step in seconds.

        Returns:
            np.array: Updated phases.
        """
        increment = self.phase_increment_per_second * time_step_s
        return phases + increment


class ZeroEngine(BaseEngine):
    """Engine that zeroes phases and brings the system to phase
        synchronization in 1 step"""

    def __init__(self, adjacency_matrix=None, laplacian=None):
        """
        Initialize with network matrices.

        Args:
            adjacency_matrix (np.array, optional): Network adjacency matrix.
            laplacian (np.array, optional): Network Laplacian matrix.
        """
        super().__init__(adjacency_matrix, laplacian)

    def update(self, phases, time_step_s):
        """
        Return the phases unchanged.

        Args:
            phases (np.array): Current phases of fireflies
            time_step_s (float): Time step in seconds
        Returns:
            np.array: Zero array
        """
        return np.zeros_like(phases)
