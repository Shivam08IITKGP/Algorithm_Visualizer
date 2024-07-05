import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import numpy as np


class SegmentTree:
    def __init__(self, data=[1, 3, 5, 7, 9]):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)  # Increased size to accommodate complete binary tree
        self.lazy = [0] * (4 * self.n)
        self.build(data)
        self.G = nx.DiGraph()
        self.position = {}
        self.frames = []

    def build(self, data):
        # Build the segment tree
        self.build_tree(data, 0, 0, self.n - 1)

    def build_tree(self, data, node, start, end):
        if start == end:
            # Leaf node
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            self.build_tree(data, left_child, start, mid)
            self.build_tree(data, right_child, mid + 1, end)
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def update_range(self, l, r, value, queryctr):
        # Update range [l, r) with value
        l -= 1
        r -= 1
        self.update_range_util(0, 0, self.n - 1, l, r, value, queryctr, l + 1, r + 1)

    def update_range_util(self, node, start, end, l, r, value, queryctr, orig_l=None, orig_r=None):
        self.add_frame(node, f"Updating node {node}, range [{start}, {end}]",
                       f"Query {queryctr}: {orig_l} {orig_r} {value}")
        if self.lazy[node] != 0:
            self.tree[node] += (end - start + 1) * self.lazy[node]
            if start != end:
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
            self.lazy[node] = 0
            self.add_frame(node, f"Applying lazy value at node {node}, new value {self.tree[node]}",
                           f"Query {queryctr}: {orig_l} {orig_r} {value}")

        if start > end or start > r or end < l:
            return

        if start >= l and end <= r:
            self.tree[node] += (end - start + 1) * value
            if start != end:
                self.lazy[2 * node + 1] += value
                self.lazy[2 * node + 2] += value
            self.add_frame(node, f"Updated node {node}, range [{start}, {end}], new value {self.tree[node]}",
                           f"Query {queryctr}: {orig_l} {orig_r} {value}")
            return

        mid = (start + end) // 2
        self.update_range_util(2 * node + 1, start, mid, l, r, value, queryctr, orig_l, orig_r)
        self.update_range_util(2 * node + 2, mid + 1, end, l, r, value, queryctr, orig_l, orig_r)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
        self.add_frame(node, f"Updated node {node} after recursion, new value {self.tree[node]}",
                       f"Query {queryctr}: {orig_l} {orig_r} {value}")

    def query_range(self, l, r, queryctr):
        # Query range [l, r)
        l -= 1
        return self.query_range_util(0, 0, self.n - 1, l, r - 1, queryctr, l + 1, r)

    def query_range_util(self, node, start, end, l, r, queryctr, orig_l, orig_r):
        self.add_frame(node, f"Querying node {node}, range [{start}, {end}]", f"Query {queryctr}: {orig_l} {orig_r}")
        if self.lazy[node] != 0:
            self.tree[node] += (end - start + 1) * self.lazy[node]
            if start != end:
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
            self.lazy[node] = 0
            self.add_frame(node, f"Applying lazy value at node {node}, new value {self.tree[node]}",
                           f"Query {queryctr}: {orig_l} {orig_r}")

        if start > end or start > r or end < l:
            return 0

        if start >= l and end <= r:
            self.add_frame(node, f"Returning value from node {node}, range [{start}, {end}], value {self.tree[node]}",
                           f"Query {queryctr}: {orig_l} {orig_r}")
            return self.tree[node]

        mid = (start + end) // 2
        left_query = self.query_range_util(2 * node + 1, start, mid, l, r, queryctr, orig_l, orig_r)
        right_query = self.query_range_util(2 * node + 2, mid + 1, end, l, r, queryctr, orig_l, orig_r)
        self.add_frame(node, f"Returning value from node {node} after recursion, value {left_query + right_query}",
                       f"Query {queryctr}: {orig_l} {orig_r}")
        return left_query + right_query

    def add_frame(self, node, operation_text, query_text):
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_alpha(0)  # Make figure background transparent

        # Remove all axes details
        ax.axis('off')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_frame_on(False)

        self.update_tree_visualization(ax, operation_text, node)

        # Add query text below the tree visualization
        fig.text(0.5, 0.05, query_text, ha='center', fontsize=12, wrap=True)

        fig.tight_layout(pad=0)  # Ensure no padding
        fig.canvas.draw()
        self.frames.append(np.array(fig.canvas.buffer_rgba()))
        plt.axis('off')
        plt.xticks([])
        plt.yticks([])
        plt.close(fig)

    def visualize_segment_tree_operations(self, queries=[[2, 5, 5], [2, 4], [1, 4]],
                                          output_file='segment_tree_lazy_operations.gif'):
        print("Building tree visualization...")
        self.build_tree_visualization(0, 0, self.n - 1)

        query_counter = 0
        ans = []

        for query in queries:
            query_counter += 1
            if len(query) == 3:
                l, r, value = query
                self.update_range(l, r, value, query_counter)
            else:
                l, r = query
                result = self.query_range(l, r, query_counter)
                ans.append(result)

        if not self.frames:
            print("No frames to animate. Exiting...")
            return ans

        fig = plt.figure(figsize=(8, 5), frameon=False)
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)  # Remove padding
        anim = animation.ArtistAnimation(fig, [[plt.imshow(frame, aspect='auto')] for frame in self.frames],
                                         interval=1500, repeat=False)

        print(f"Saving animation to {output_file}...")
        anim.save(output_file, writer='pillow', dpi=100,
                  savefig_kwargs={'transparent': True, 'facecolor': 'none', 'pad_inches': 0})

        print("Animation saved successfully.")
        return ans

    def build_tree_visualization(self, node, start, end):
        if start == end:
            self.G.add_node(node)
            self.position[node] = (start, node)
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            self.G.add_node(node)
            self.position[node] = (mid, node)
            self.G.add_edge(node, left_child)
            self.G.add_edge(node, right_child)
            self.build_tree_visualization(left_child, start, mid)
            self.build_tree_visualization(right_child, mid + 1, end)

    def update_tree_visualization(self, ax, operation_text, current_node=None):
        ax.clear()
        ax.axis('off')
        ax.set_frame_on(False)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

        pos = hierarchy_pos(self.G, root=0)  # Assuming 0 is the root node index
        node_labels = {node: f"{self.tree[node]}\n(Lazy: {self.lazy[node]})" for node in self.G.nodes()}
        node_colors = ['lightblue' if node != current_node else 'lightgreen' for node in self.G.nodes()]
        nx.draw(self.G, pos, labels=node_labels, with_labels=True, arrows=True, node_size=1500, node_color=node_colors,
                font_size=8, font_color='black', ax=ax)

        plt.title(operation_text, fontsize=12)
        plt.axis('off')
        plt.xticks([])
        plt.yticks([])


def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos


def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
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
            pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc - vert_gap,
                                 xcenter=nextx, pos=pos, parent=root, parsed=parsed)
    return pos


# Example usage
if __name__ == "__main__":
    segment_tree = SegmentTree()
    ans = segment_tree.visualize_segment_tree_operations()
    print(ans)
