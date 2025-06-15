import networkx as nx
import matplotlib.pyplot as plt

from lib.fireflies import Firefly

GRID_WIDTH = 1
GRID_HEIGHT = 1


class Experiment:
    EPSILON_RAD = 0.1

    def __init__(self, network: nx.Graph, duration, time_step, epsilon_rad=EPSILON_RAD):
        """
        Handling simulation logic.

        """
        self.duration = duration
        self.time_step = time_step
        self.network = network
        self.epsilon = epsilon_rad
        self.counter = 0.0
        # results
        self.time_to_labels = {}  # counter: [labels of fireflies that flashed]
        self.time_to_phase = {}  # counter: [phase of each firefly]

    def run(self):
        while self.counter <= self.duration:
            self.step()
            self.counter += self.time_step
            # self.plot()

    def step(self):
        """
        Advance the simulation by time_step units.
        """
        # 0. reset all flashing fireflies
        for node in self.network.nodes:
            firefly = self.network.nodes[node]['firefly']
            if firefly.is_flashing():
                firefly.reset()
        # 1. update phase of each firefly using its natural frequency
        for node in self.network.nodes:
            firefly = self.network.nodes[node]['firefly']
            d_theta = firefly.freq_rad_s * self.time_step
            firefly.advance_phase(d_theta)
        # 2. process cascading flashes: for this we will save fireflies
        #    that have "fired" and update fireflies that are flashing
        fired = set()
        flashing = [n for n in self.network.nodes if self.network.nodes[n]['firefly'].is_flashing()]
        while flashing:
            current = flashing.pop()
            fired.add(current)
            for neighbour in nx.neighbors(self.network, current):
                if neighbour not in fired:
                    neighbour_firefly = self.network.nodes[neighbour]['firefly']
                    neighbour_firefly.advance_phase(self.epsilon)
                    if neighbour_firefly.is_flashing():
                        flashing.append(neighbour)
        self.time_to_labels[self.counter] = [1 if self.network.nodes[n]['firefly'].is_flashing() else 0 for n in
                                             self.network.nodes]
        self.time_to_phase[self.counter] = [self.network.nodes[n]['firefly'].phase_rad for n in
                                            self.network.nodes]
