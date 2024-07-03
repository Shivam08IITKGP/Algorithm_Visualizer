import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def bellman_ford(graph, start):
    distance = {node: float('inf') for node in graph.nodes()}
    distance[start] = 0

    for _ in range(len(graph.nodes()) - 1):
        for u, v, data in graph.edges(data=True):
            if distance[u] + data['weight'] < distance[v]:
                distance[v] = distance[u] + data['weight']

    # Check for negative weight cycles
    for u, v, data in graph.edges(data=True):
        if distance[u] + data['weight'] < distance[v]:
            raise ValueError("Graph contains a negative weight cycle")

    return distance


def visualize_bellman_ford(graph, start_node, output_file):
    edges = list(graph.edges(data=True))
    num_edges = len(edges)
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start_node] = 0

    frames = []
    fig, ax = plt.subplots()

    def update(frame):
        ax.clear()
        iteration_edges = edges[:frame + 1]
        for u, v, data in iteration_edges:
            nx.draw(graph, pos=nx.spring_layout(graph), with_labels=True, ax=ax)
            edge_labels = nx.get_edge_attributes(graph, 'weight')
            nx.draw_networkx_edge_labels(graph, pos=nx.spring_layout(graph), edge_labels=edge_labels, ax=ax)
            nx.draw_networkx_edges(graph, pos=nx.spring_layout(graph), edgelist=[(u, v)], edge_color='r', width=2,
                                   ax=ax)

    anim = FuncAnimation(fig, update, frames=num_edges, interval=1000, repeat=False)
    anim.save(output_file,
              writer='imagemagick')  # Adjust writer as per your system setup (e.g., 'imagemagick' or 'pillow')

    plt.close(fig)

    return distances
