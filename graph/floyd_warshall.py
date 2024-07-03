import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import networkx as nx


def fig_to_image(fig):
    from io import BytesIO
    import PIL.Image

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image = PIL.Image.open(buf)
    return image


def floyd_warshall(graph):
    nodes = list(graph.nodes())
    num_nodes = len(nodes)
    dist = np.full((num_nodes, num_nodes), float('inf'))
    np.fill_diagonal(dist, 0)

    for u, v, data in graph.edges(data=True):
        dist[nodes.index(u)][nodes.index(v)] = data['weight']

    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


def visualize_floyd_warshall(graph, output_file):
    num_nodes = len(graph.nodes())
    dist_matrix = [[float('inf')] * num_nodes for _ in range(num_nodes)]
    for i in range(num_nodes):
        dist_matrix[i][i] = 0

    for u, v, data in graph.edges(data=True):
        dist_matrix[u][v] = data['weight']

    frames = []

    def update(frame):
        k = frame // (num_nodes ** 2)
        i = (frame // num_nodes) % num_nodes
        j = frame % num_nodes

        if dist_matrix[i][j] > dist_matrix[i][k] + dist_matrix[k][j]:
            dist_matrix[i][j] = dist_matrix[i][k] + dist_matrix[k][j]

        fig, ax = plt.subplots()
        pos = nx.shell_layout(graph)
        nx.draw(graph, pos, with_labels=True, ax=ax)
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
        if i != j and i != k and j != k:
            nx.draw_networkx_edges(graph, pos, edgelist=[(i, k), (k, j)], edge_color='r', width=2, ax=ax)

        frames.append(fig_to_image(fig))
        plt.close(fig)  # Close the figure after capturing the image

    anim = FuncAnimation(plt.figure(), update, frames=num_nodes ** 2, repeat=False)
    writer = PillowWriter(fps=1)
    anim.save(output_file, writer=writer)

    return dist_matrix


def main():
    # Example graph setup
    G = nx.Graph()
    G.add_edge(0, 1, weight=4)
    G.add_edge(0, 2, weight=3)
    G.add_edge(1, 2, weight=1)
    G.add_edge(1, 3, weight=2)
    G.add_edge(2, 3, weight=4)
    G.add_edge(3, 4, weight=2)
    output_file = 'floyd_warshall_animation.gif'

    # Compute and visualize Floyd-Warshall algorithm
    shortest_paths = visualize_floyd_warshall(G, output_file)
    print("Shortest paths matrix:")
    print(np.array(shortest_paths))


if __name__ == "__main__":
    main()
