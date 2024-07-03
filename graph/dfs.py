import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def dfs(G, start):
    visited = []
    stack = [start]

    while stack:
        node = stack.pop()  # Pop the current node from the stack
        if node not in visited:
            visited.append(node)  # Mark the node as visited
            print(node)  # Optional: Print the current node for debugging

            # Add neighbors to the stack in reverse order to maintain DFS order
            for neighbour in reversed(list(G[node])):
                if neighbour not in visited:
                    stack.append(neighbour)

    return visited


def custom_dfs_input(data):
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


def visualize_dfs(G, output_file):
    traversal_order = dfs(G, 1)
    pos = nx.shell_layout(G)
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.set_title('DFS Traversal Order')
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
