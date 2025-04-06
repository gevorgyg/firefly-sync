from itertools import combinations

import numpy as np
import networkx as nx

from lib.fireflies import EuclideanFirefly
import matplotlib.pyplot as plt

GRID_WIDTH = 1
GRID_HEIGHT = 1


class Visualiser:
    # Constants
    DEFAULT_FIGURE_WIDTH = 10
    DEFAULT_FIGURE_HEIGHT = 8
    DEFAULT_NODE_SIZE = 500
    DEFAULT_NODE_COLOR = 'blue'
    DEFAULT_FONT_SIZE = 10

    def __init__(self,
                 min_x, max_x, min_y, max_y,
                 figure_width=DEFAULT_FIGURE_WIDTH,
                 figure_height=DEFAULT_FIGURE_HEIGHT):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.figure_width = figure_width
        self.figure_height = figure_height

    def visualize_network(self, network, title="Firefly Network",
                          node_size=DEFAULT_NODE_SIZE,
                          node_color=DEFAULT_NODE_COLOR,
                          font_size=DEFAULT_FONT_SIZE):
        plt.figure(figsize=(self.figure_width, self.figure_height))
        pos = {firefly: firefly.coordinates for firefly in network.nodes}
        nx.draw(network, pos, with_labels=True,
                node_size=node_size, node_color=node_color,
                font_size=font_size)
        plt.xlim(self.min_x, self.max_x)
        plt.ylim(self.min_y, self.max_y)
        plt.title(title)
        plt.show()


class Experiment:

    def __init__(self, epsilon):
        """
        Main class of the program.

        :param epsilon: Threshold distance for firefly interaction (in spatial units).
                        Defines the maximum distance at which fireflies can perceive and
                        respond to each other's flashes. I.e., if two fireflies are in proximity of epsilon,
                        they are considered neighbours in the network

        """
        self.min_x = 0
        self.max_x = GRID_WIDTH - self.min_x
        self.min_y = 0
        self.max_y = GRID_HEIGHT - self.min_y
        self.epsilon = epsilon
        self.network: nx.Graph = nx.Graph()
        self.visualiser = Visualiser(self.min_x, self.max_x, self.min_y, self.max_y)

    def add_firefly(self, firefly: EuclideanFirefly):
        if not self.is_valid_position(firefly.coordinates[0], firefly.coordinates[1]):
            raise ValueError("Firefly position is out of bounds.")
        self.network.add_node(firefly)

    def draw_network(self):
        self.visualiser.visualize_network(self.network)

    def form_network(self):
        """
        Form a network of fireflies by connecting them based on their distance
        """
        self.network.clear()
        for firefly1, firefly2 in combinations(self.network.nodes, 2):
            distance = np.linalg.norm(firefly1.coordinates - firefly2.coordinates)
            if distance <= self.epsilon:
                self.network.add_edge(firefly1, firefly2)

    def is_valid_position(self, x, y):
        # do not allow fireflies to be placed on boundary
        return self.min_x < x < self.max_x and self.min_y < y < self.max_y
