import networkx as nx

import fireflies

DEFAULT_DURATION_S = 10.0  # Default duration of the experiment in seconds
DEFAULT_TIME_STEP_S = 0.1  # Default time step in seconds


class Experiment:

    def __init__(self, network: nx.Graph, engine, duration_s=DEFAULT_DURATION_S, time_step_s=DEFAULT_TIME_STEP_S):
        """
        Initialize the experiment with a network, duration, engine, and time step.

        Args:
            network (nx.Graph): The network of fireflies.
            engine: The engine to use for updating firefly phases.
            duration_s (float): Duration of the experiment in seconds.
            time_step_s (float): Time step of the simulation in seconds.
        """
        self.network = network
        self.engine = engine
        self.duration_s = duration_s
        self.time_step_s = time_step_s
        self.current_time = 0.0  # Track the current simulation time

    def run(self):
        while self.current_time <= self.duration_s:
            self.step()
            self.current_time += self.time_step_s

    def step(self):
        phases = fireflies.network.get_phases(self.network)
        updated_phases = self.engine.update(phases)
        fireflies.network.set_phases(self.network, updated_phases)
