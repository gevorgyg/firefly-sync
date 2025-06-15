import networkx as nx
import numpy as np

from models import Firefly


def create_d_regular_network(phases: np.array, degree, seed=None) -> nx.Graph:
    """
    Create a d-regular connected random graph on nodes_num nodes. We use a regular graph so that
    each firefly has the same number of neighbours, and as such we don't have to think about
    topology of the network.
    """
    G = nx.random_regular_expander_graph(len(phases), degree, seed=seed)  # we use expander graph to ensure connectivity
    firefly_dict = {node: Firefly(node, phase) for (node, phase) in zip(G.nodes(), phases)}
    nx.set_node_attributes(G, firefly_dict, 'firefly')
    return G
