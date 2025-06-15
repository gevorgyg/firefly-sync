def test_create_d_regular_network():
    import numpy as np
    import networkx as nx
    from fireflies import create_d_regular_network, Firefly

    # Test parameters
    phases = np.array([0.0, np.pi / 2, np.pi, 3 * np.pi / 2])
    degree = 2
    seed = 42

    # Create the network
    G = create_d_regular_network(phases, degree, seed)

    # Check if the graph is connected and regular
    assert nx.is_connected(G)
    assert all(degree == G.degree(node) for node in G.nodes())

    # Check if fireflies are correctly assigned to nodes
    for node in G.nodes():
        firefly = G.nodes[node]['firefly']
        assert isinstance(firefly, Firefly)
        assert firefly.id == node
        assert firefly.phase_rad in phases
