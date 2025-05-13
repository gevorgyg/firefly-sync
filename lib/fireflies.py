import numpy as np
import networkx as nx
from typing import Callable, List


class Firefly:
    DEFAULT_FREQ = 1  # 1Hz natural frequency
    PHASE_THRESHOLD = 1.0  # When phase is >= PHASE_THRESHOLD, firefly is considered to be flashing

    class State:
        FLASHING = 1
        WAITING = 0

    def __init__(self, id: int, phase: float,
                 freq: float = DEFAULT_FREQ,
                 phase_threshold: float = PHASE_THRESHOLD):
        """
        Base firefly class with core phase advancement logic
        """
        self.id = id
        self.phase = phase
        self.freq = freq
        self.phase_threshold = phase_threshold
        self.state = self.State.WAITING

    def advance_phase(self, epsilon):
        if self.state == self.State.FLASHING:
            return
        self.phase += epsilon
        if self.phase >= self.phase_threshold:
            self.phase = self.PHASE_THRESHOLD
            self.state = self.State.FLASHING

    def is_flashing(self):
        return self.state == self.State.FLASHING

    def reset(self):
        self.phase = 0
        self.state = self.State.WAITING


def create_d_regular_network(phases: np.array, degree, seed=None) -> nx.Graph:
    """
    Create a d-regular random graph on nodes_num nodes. We use a regular graph so that
    each firefly has the same number of neighbours, and as such we don't have to think about
    topology of the network.
    """
    G = nx.random_regular_graph(degree, len(phases), seed=seed)
    firefly_dict = {node: Firefly(node, phase) for (node, phase) in zip(G.nodes(), phases)}
    nx.set_node_attributes(G, firefly_dict, 'firefly')
    return G
