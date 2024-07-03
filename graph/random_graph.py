import random
import networkx as nx


def generate_random_connected_directed_graph_no_self_loops(n, m):
    if m < n - 1:
        raise ValueError("Number of edges must be at least n-1 to ensure connectivity.")

    G = nx.DiGraph()
    nodes = list(range(1, n + 1))
    G.add_nodes_from(nodes)

    # Ensure connectivity from node 1
    for i in range(1, n):
        weight = random.randint(1, 10)
        G.add_edge(1, nodes[i], weight=weight)

    edges_added = n - 1
    while edges_added < m:
        u, v = random.sample(nodes, 2)
        if u != v and not G.has_edge(u, v) and not G.has_edge(v, u):
            weight = random.randint(1, 10)
            G.add_edge(u, v, weight=weight)
            edges_added += 1

    return G


def generate_random_connected_directed_unweighted_graph_no_self_loops(n, m):
    if m < n - 1:
        raise ValueError("Number of edges must be at least n-1 to ensure connectivity.")

    G = nx.DiGraph()
    nodes = list(range(1, n + 1))
    G.add_nodes_from(nodes)

    # Ensure connectivity from node 1
    for i in range(1, n):
        G.add_edge(1, nodes[i])

    edges_added = n - 1
    while edges_added < m:
        u, v = random.sample(nodes, 2)
        if u != v and not G.has_edge(u, v) and not G.has_edge(v, u):
            G.add_edge(u, v)
            edges_added += 1

    return G
