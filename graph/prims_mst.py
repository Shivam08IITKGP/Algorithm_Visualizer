import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import networkx as nx
import heapq


def fig_to_image(fig):
    from io import BytesIO
    import PIL.Image

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image = PIL.Image.open(buf)
    return image


def prim_mst(graph, start_node=0, visit=None):
    mst = nx.Graph()
    visited = set([start_node])
    edges = [(data['weight'], start_node, to) for to, data in graph[start_node].items()]
    heapq.heapify(edges)

    while edges:
        weight, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst.add_edge(frm, to, weight=weight)
            if visit:
                visit((frm, to, weight))
            for to_next, data in graph[to].items():
                if to_next not in visited:
                    heapq.heappush(edges, (data['weight'], to, to_next))
    return mst


def visualize_prim(graph, output_file, fig_width=6, fig_height=4, dpi=100):
    if not graph:
        return []

    frames = []
    mst = nx.Graph()

    # Adjust figure size
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    def draw_graph(edge):
        ax.clear()
        frm, to, weight = edge
        mst.add_edge(frm, to, weight=weight)
        pos = nx.shell_layout(graph)

        # Draw the graph
        nx.draw(graph, pos, with_labels=True, ax=ax)

        # Draw edge labels
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)

        # Draw MST edges in red
        nx.draw_networkx_edges(graph, pos, edgelist=mst.edges(), edge_color='r', width=2, ax=ax)

        # Remove spines and ticks
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False,
                       labelleft=False)

        # Turn off the axis and box
        ax.axis('off')

        frames.append(fig_to_image(fig))

    prim_mst(graph, start_node=0, visit=draw_graph)

    def update(num):
        ax.clear()
        ax.imshow(frames[num])

    ani = FuncAnimation(fig, update, frames=len(frames), repeat=False)

    # Save the animation as a GIF
    writer = PillowWriter(fps=1, dpi=dpi)
    ani.save(output_file, writer=writer)
    plt.close(fig)

    return mst


# Example usage
if __name__ == "__main__":
    G = nx.Graph()
    G.add_edge(0, 1, weight=4)
    G.add_edge(0, 2, weight=3)
    G.add_edge(1, 2, weight=1)
    G.add_edge(1, 3, weight=2)
    G.add_edge(2, 3, weight=4)
    G.add_edge(3, 4, weight=2)

    mst = visualize_prim(G, "prim_mst.gif", fig_width=4, fig_height=3, dpi=80)
    print("Minimum Spanning Tree:", mst.edges(data=True))
