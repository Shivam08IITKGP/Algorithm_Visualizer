import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
from PIL import Image
import numpy as np


def find_bridges(graph):
    def dfs(node, parent, visited, discovery, low, bridges, time, frames):
        visited[node] = True
        discovery[node] = low[node] = time[0]
        time[0] += 1
        stack.append(node)

        # Append current state of discovery and low arrays to frames
        frames.append((list(stack), dict(discovery), dict(low), None, None))

        for neighbor in graph[node]:
            if not visited[neighbor]:
                frames.append((list(stack), dict(discovery), dict(low), node, neighbor))
                dfs(neighbor, node, visited, discovery, low, bridges, time, frames)

                # Update low value after subtree traversal
                low[node] = min(low[node], low[neighbor])

                if low[neighbor] > discovery[node]:
                    bridges.append((node, neighbor))
            elif neighbor != parent:
                # Back edge found
                frames.append((list(stack), dict(discovery), dict(low), node, neighbor))

                # Update low value with the neighbor's discovery time
                low[node] = min(low[node], discovery[neighbor])

        # Capture the state before popping the stack (backtracking)
        frames.append((list(stack), dict(discovery), dict(low), parent, None))
        stack.pop()

    visited = {node: False for node in graph}
    discovery = {node: float('inf') for node in graph}
    low = {node: float('inf') for node in graph}
    bridges = []
    time = [0]
    frames = []
    stack = []

    # Start DFS from the first node
    for start_node in graph:
        if not visited[start_node]:
            dfs(start_node, None, visited, discovery, low, bridges, time, frames)

    return bridges, frames


def update(frame, ax, ax_box, frames, bridges):
    stack, discovery, low, parent, next_node = frame
    ax.clear()
    pos = nx.shell_layout(G)

    # Draw graph
    nx.draw(G, pos, with_labels=True, node_color='green', ax=ax)

    # Color the path used to reach the current node
    if parent is not None and next_node is not None:
        path_nodes = stack + [next_node]
        edge_list = [(path_nodes[i], path_nodes[i + 1]) for i in range(len(path_nodes) - 1)]
        nx.draw_networkx_nodes(G, pos, nodelist=path_nodes, node_color='blue', ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='blue', ax=ax)

    # Highlight bridges in violet at the end
    if frame == frames[-1]:
        nx.draw_networkx_edges(G, pos, edgelist=bridges, edge_color='purple', width=2, ax=ax)

    # Change color of nodes that have been visited
    visited_nodes = [node for node in G if node not in stack]
    nx.draw_networkx_nodes(G, pos, nodelist=visited_nodes, node_color='green', ax=ax)

    # Update the 2D box with discovery and low arrays
    ax_box.clear()
    ax_box.axis('off')
    ax_box.set_title('DFS Progress: Discovery and Low Arrays')

    # Convert dictionary data to list for display
    discovery_values = list(discovery.values())
    low_values = list(low.values())
    nodes = list(discovery.keys())

    # Create a table-like plot for discovery and low arrays
    table_data = [
        ['Node', 'T in', 'T low']
    ]
    for node, disc, low_val in zip(nodes, discovery_values, low_values):
        table_data.append([node, disc, low_val])

    table = ax_box.table(cellText=table_data, loc='center', colLabels=None, cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    # Highlight current node being processed
    if next_node is not None:
        node_index = nodes.index(next_node)
        cell_disc = table.get_celld()[(node_index + 1, 1)]
        cell_low = table.get_celld()[(node_index + 1, 2)]
        cell_disc.set_facecolor('yellow')
        cell_low.set_facecolor('yellow')


def visualize_bridges(graph, filename='bridges_animation.gif'):
    fig, (ax, ax_box) = plt.subplots(1, 2, figsize=(7, 4))

    global G
    G = graph

    bridges, frames = find_bridges(graph)
    print("Bridges:", bridges)

    ani = FuncAnimation(fig, update, frames=frames, fargs=(ax, ax_box, frames, bridges),
                        repeat=False, interval=1000)

    # Save animation as GIF
    ani.save(filename, writer='pillow', fps=1)

    plt.title("Bridges Visualization")
    return bridges
    # plt.show()


def main():
    # Example graph setup
    G = nx.DiGraph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (1, 5), (5, 6), (6, 7), (7, 5)])

    # Visualize the bridges discovery process and save as GIF
    visualize_bridges(G, filename='bridges_animation.gif')


if __name__ == "__main__":
    main()
