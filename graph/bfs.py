import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def bfs(G, start, visit):
    visited = set()
    queue = [start]

    traversal_order = []

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visit(node)
            visited.add(node)
            traversal_order.append(node)
            queue.extend(list(G.neighbors(node)))

    return traversal_order


def custom_bfs_input(data):
    lines = data.strip().split('\n')
    graph_type = lines[0].lower()
    G = nx.DiGraph() if graph_type == 'directed' else nx.Graph()
    for line in lines[1:]:
        u, v = map(int, line.split())
        G.add_edge(u, v)
        if graph_type == 'undirected':
            G.add_edge(v, u)
    return G


def visualize_bfs(G, output_file):
    visited_nodes = set()
    traversal_order = []

    def traversal_callback(node):
        visited_nodes.add(node)
        traversal_order.append(node)

    start_node = 1
    traversal_order = bfs(G, start_node, traversal_callback)
    def star_layout(G, center_node):
        pos = {center_node: (0, 0)}  # Center node position
        other_nodes = [node for node in G.nodes if node != center_node]
        angle = 2 * np.pi / len(other_nodes)  # Angle between nodes
        for i, node in enumerate(other_nodes):
            theta = i * angle
            pos[node] = (np.cos(theta), np.sin(theta))
        return pos

    pos = star_layout(G,1)  # Use shell layout for star shape
    fig, ax = plt.subplots()

    def update(frame):
        ax.clear()
        nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', edge_color='gray')
        nx.draw_networkx_nodes(G, pos, nodelist=traversal_order[:frame], node_color='green')

    ani = animation.FuncAnimation(fig, update, frames=len(traversal_order) + 1, repeat=False, interval=500)
    ani.save(output_file, writer='pillow')
    plt.close(fig)

    return traversal_order
