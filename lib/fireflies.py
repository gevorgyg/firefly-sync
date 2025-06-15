import numpy as np
from numpy import pi
import networkx as nx


class Firefly:
    DEFAULT_FREQ_RAD_S = 2 * pi  # 2*pi rad natural frequency
    PHASE_THRESHOLD_RAD = 2 * pi  # When phase is >= PHASE_THRESHOLD, firefly is considered to be flashing

    class State:
        FLASHING = 1
        WAITING = 0

    def __init__(self, id: int, phase: float,
                 freq_rad_s: float = DEFAULT_FREQ_RAD_S,
                 phase_threshold_rad: float = PHASE_THRESHOLD_RAD):
        self.id = id
        self.phase = phase
        self.freq_rad_s = freq_rad_s
        self.phase_threshold_rad = phase_threshold_rad
        self.state = self.State.WAITING

    def advance_phase(self, epsilon):
        if self.state == self.State.FLASHING:
            return
        self.phase += epsilon
        if self.phase >= self.phase_threshold_rad:
            self.phase = self.PHASE_THRESHOLD_RAD
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
