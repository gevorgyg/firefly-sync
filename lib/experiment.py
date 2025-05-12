from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt

from lib.fireflies import Firefly

GRID_WIDTH = 1
GRID_HEIGHT = 1


class Experiment:
    EPSILON = 0.1

    def __init__(self, network: nx.Graph, duration, time_step, epsilon=EPSILON):
        """
        Handling simulation logic.

        """
        self.duration = duration
        self.time_step = time_step
        self.network = network
        self.epsilon = epsilon
        self.counter = 0.0

    def run(self):
        while self.counter <= self.duration:
            self.step()
            self.counter += self.time_step
            # self.plot()

    def step(self):
        """
        Advance the simulation by time_step units.
        """

        # 0. reset all fireflies
        for firefly in self.network.nodes:
            firefly.reset()

        # 1. update phase of each firefly using its natural frequency
        for firefly in self.network.nodes:
            d_theta = firefly.freq * self.time_step
            firefly.advance_phase(d_theta)
        # 2. process cascading flashes: for this we will save fireflies
        #    that have "fired" and update fireflies that are flashing
        fired = set()
        flashing = [f for f in self.network.nodes if f.is_flashing()]
        while flashing:
            current = flashing.pop()
            fired.add(current)
            for neighbour in current.neighbours:
                if neighbour not in fired:
                    neighbour.advance_phase(self.epsilon)
                    if neighbour.is_flashing():
                        flashing.append(neighbour)
