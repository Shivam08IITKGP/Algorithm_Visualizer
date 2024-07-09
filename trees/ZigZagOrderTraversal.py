import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike.

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is undirected and not given,
      an arbitrary node will be chosen as the root and used

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
        if not nx.is_tree(G):
            raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                     pos=pos, parent=root, parsed=parsed)
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


def zig_zag_traversal(graph):
    visited = [1]
    queue = [1]
    ans = []
    left = True
    while queue:
        size = len(queue)
        reverse = []
        for _ in range(size):
            node = queue.pop(0)
            if not left:
                reverse.append(node)
            else:
                ans.append(node)
            for neighbour in graph[node]:
                if neighbour not in visited:
                    visited.append(neighbour)
                    queue.append(neighbour)
        if not left:
            ans.extend(reverse[::-1])
        left = not left
    return ans


def visualize_zig_zag_order_traversal(graph, output_file):
    traversal_order = zig_zag_traversal(graph)
    G = nx.DiGraph()
    for node in graph:
        G.add_node(node)
        for neighbour in graph[node]:
            G.add_edge(node, neighbour)

    fig, ax = plt.subplots(figsize=(4, 2))

    def update(frame):
        ax.clear()
        ax.axis('off')
        pos = hierarchy_pos(G, 1)
        node_colors = ['green' if node in traversal_order[:frame + 1] else 'red' for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=node_colors, ax=ax, edge_color='gray', width=0.5)
        plt.tight_layout()

    ani = FuncAnimation(fig, update, frames=len(traversal_order), repeat=False)
    writer = PillowWriter(fps=1)
    ani.save(output_file, writer=writer, dpi=200)  # Adjust dpi for quality
    plt.close(fig)
    return traversal_order


def main():
    # Example input data
    graph = {
        1: [2, 3],
        2: [4, 5],
        3: [6, 7],
        4: [],
        5: [],
        6: [],
        7: []
    }
    output_file = 'zig_zag_order_traversal.gif'
    result = visualize_zig_zag_order_traversal(graph, output_file)
    print(result)
        


if __name__ == "__main__":
    main()
