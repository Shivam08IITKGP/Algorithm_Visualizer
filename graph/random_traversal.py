import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


def random_traversal(G):
    visited = []
    traversal_order = []

    while len(visited) != len(G.nodes):
        node = random.choice(list(G.nodes))
        if node not in visited:
            visited.append(node)
            traversal_order.append(node)
    return traversal_order


def custom__random_traversal_input(data):
    lines = data.strip().split('\n')
    graph_type = lines[0]
    graph_type = graph_type.strip()
    graph_type = graph_type.lower()
    if graph_type == 'directed':
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    for line in lines[1:]:
        u, v = map(int, line.split())
        G.add_edge(u, v)
        if graph_type == 'undirected':
            G.add_edge(v, u)
    return G


def visualize_random_traversal(G, output_file):
    traversal_order = random_traversal(G)
    pos = nx.shell_layout(G)
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.set_title('Random Traversal Order')
    frame = []

    def update(frame):
        ax.clear()
        ax.axis('off')
        node_colors = ['green' if node in traversal_order[:frame + 1] else 'red' for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=node_colors, ax=ax)

    ani = animation.FuncAnimation(fig, update, frames=len(traversal_order), repeat=False)
    writer = animation.PillowWriter(fps=1)
    ani.save(output_file, writer=writer, dpi=200)
    plt.close(fig)
    return traversal_order
