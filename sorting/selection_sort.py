import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def selection_sort(arr):
    frames = []
    n = len(arr)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
            frames.append({'arr': arr.copy(), 'color': ['blue' if x == j or x == min_idx else 'black' for x in range(len(arr))], 'title': 'Selection Sort'})
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        frames.append({'arr': arr.copy(), 'color': ['red' if x == i else 'black' for x in range(len(arr))], 'title': 'Selection Sort'})
    return frames

def visualize_selection_sort(arr, output_file):
    frames = selection_sort(arr)
    fig, ax = plt.subplots()
    ax.set_axis_off()

    def update(frame):
        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])

        for idx, num in enumerate(frame['arr']):
            color = frame['color'][idx] if 'color' in frame else 'black'
            ax.text(idx, 0, str(num), fontsize=12, ha='center', va='center', color=color)

        if 'title' in frame:
            ax.set_title(frame['title'])

        ax.set_xlim(-0.5, len(frame['arr']) - 0.5)
        ax.set_ylim(-0.5, 0.5)

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=1000, repeat=False)
    ani.save(output_file, writer='pillow', savefig_kwargs={'pad_inches': 0.0})
    plt.close(fig)

if __name__ == "__main__":
    arr = [random.randint(1, 100) for _ in range(10)]
    output_file = "selection_sort_visualization.gif"
    visualize_selection_sort(arr, output_file)
