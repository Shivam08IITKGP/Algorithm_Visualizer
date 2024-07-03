import networkx as nx
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


class UnionFind:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root1] = root2
                if self.rank[root1] == self.rank[root2]:
                    self.rank[root2] += 1
            return True
        return False


def kruskal(graph, visit=None):
    edges = sorted(graph.edges(data=True), key=lambda x: x[2]['weight'])
    mst = nx.Graph()
    union_find = UnionFind(list(graph.nodes()))

    for u, v, data in edges:
        if union_find.find(u) != union_find.find(v):
            union_find.union(u, v)
            if visit:
                visit((u, v, data['weight']))
            mst.add_edge(u, v, weight=data['weight'])
    return mst


def fig_to_image(fig):
    from io import BytesIO
    import PIL.Image

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image = PIL.Image.open(buf)
    return image


def visualize_kruskal(graph, output_file):
    if not graph:
        return []

    mst = nx.Graph()
    frames = []

    fig, ax = plt.subplots()

    def draw_graph(edge):
        u, v, weight = edge
        if not mst.has_edge(u, v):
            mst.add_edge(u, v, weight=weight)
            pos = nx.shell_layout(graph)
            ax.clear()
            nx.draw(graph, pos, with_labels=True, ax=ax)
            edge_labels = nx.get_edge_attributes(graph, 'weight')
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
            nx.draw_networkx_edges(graph, pos, edgelist=mst.edges(), edge_color='r', width=2, ax=ax)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False,
                           labelleft=False)
            frames.append(fig_to_image(fig))

    kruskal(graph, visit=draw_graph)

    def update(num):
        ax.clear()
        ax.imshow(frames[num])

    ani = FuncAnimation(fig, update, frames=len(frames), repeat=False)
    writer = PillowWriter(fps=1)
    ani.save(output_file, writer=writer)
    plt.close(fig)
    print(type(mst))
    return mst


def main():
    graph = nx.Graph()
    graph.add_edge(0, 1, weight=4)
    graph.add_edge(0, 2, weight=3)
    graph.add_edge(1, 2, weight=1)
    graph.add_edge(1, 3, weight=2)
    graph.add_edge(2, 3, weight=4)
    graph.add_edge(3, 4, weight=2)

    output_file = 'kruskal_animation.gif'
    mst = visualize_kruskal(graph, output_file)

    # JSON serialization example
    result_data = {
        'mst_nodes': list(mst.nodes()),
        'mst_edges': [(u, v, mst[u][v]['weight']) for u, v in mst.edges()]
    }

    # Convert result_data to JSON
    result_json = json.dumps(result_data, indent=4)
    print(result_json)


if __name__ == "__main__":
    main()
