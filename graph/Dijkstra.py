import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import heapq
import os
import numpy as np



def dijkstra(G, start, visit):
    queue = [(0, start)]
    distances = {node: float('inf') for node in G.nodes}
    distances[start] = 0
    visited = set()

    while queue:
        (dist, current) = heapq.heappop(queue)
        if current in visited:
            continue

        visited.add(current)
        visit(current)
        for neighbor in G.neighbors(current):
            distance = G[current][neighbor].get('weight', 1)
            if distances[neighbor] > dist + distance:
                distances[neighbor] = dist + distance
                heapq.heappush(queue, (distances[neighbor], neighbor))

    return distances


def visualize_dijkstra(G, output_file):
    visited_nodes = set()
    traversal_order = []

    def traversal_callback(node):
        visited_nodes.add(node)
        traversal_order.append(node)

    start_node = 1
    distances = dijkstra(G, start_node, traversal_callback)

    def star_layout(G, center_node):
        pos = {center_node: (0, 0)}  # Center node position
        other_nodes = [node for node in G.nodes if node != center_node]
        angle = 2 * np.pi / len(other_nodes)  # Angle between nodes
        for i, node in enumerate(other_nodes):
            theta = i * angle
            pos[node] = (np.cos(theta), np.sin(theta))
        return pos

    pos = star_layout(G, 1)
    fig, ax = plt.subplots()

    def update(frame):
        ax.clear()
        nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', edge_color='gray')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='black', arrows=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8,
                                     bbox=dict(facecolor='white', edgecolor='none'))
        nx.draw_networkx_nodes(G, pos, nodelist=traversal_order[:frame], node_color='green')

    ani = animation.FuncAnimation(fig, update, frames=len(traversal_order) + 1, repeat=False, interval=500)
    ani.save(output_file, writer='pillow')
    plt.close(fig)

    for node, distance in distances.items():
        if distance != float('inf'):
            distances[node] = int(distance)

    return distances, traversal_order

