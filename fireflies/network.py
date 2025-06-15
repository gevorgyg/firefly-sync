import networkx as nx
from networkx.generators.expanders import random_regular_expander_graph
import numpy as np

from fireflies.models import Firefly  # Added 'import' keyword


def create_d_regular_network(phases: np.array, degree, seed=None) -> nx.Graph:
    """
    Create a d-regular connected random graph on nodes_num nodes. We use a regular graph so that
    each firefly has the same number of neighbours, and as such we don't have to think about
    topology of the network.
    """
    # Use the directly imported function instead of accessing through nx
    G = random_regular_expander_graph(len(phases), degree, seed=seed)
    firefly_dict = {node: Firefly(node, phase) for (node, phase) in zip(G.nodes(), phases)}
    nx.set_node_attributes(G, firefly_dict, 'firefly')
    return G


# Extract phases from the graph
def get_phases(network: nx.Graph) -> np.array:
    """
    Extract the phases of fireflies from the graph.

    Args:
        network (nx.Graph): The network graph containing fireflies.

    Returns:
        np.array: Array of firefly phases.
    """
    return np.array([network.nodes[node]['firefly'].phase_rad for node in network.nodes])


def set_phases(network: nx.Graph, updated_phases_rad: np.array):
    for node, phase in zip(network.nodes(), updated_phases_rad):

        network.nodes[node]['firefly'].phase_rad = phase
