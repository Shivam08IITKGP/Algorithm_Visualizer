import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def shell_sort(arr):
    frames = []
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
                frames.append({'arr': arr.copy(), 'color': ['blue' if x == j or x == j - gap else 'black' for x in range(len(arr))], 'title': f'Shell Sort - Gap {gap}'})
            arr[j] = temp
            frames.append({'arr': arr.copy(), 'color': ['red' if x == j else 'black' for x in range(len(arr))], 'title': f'Shell Sort - Gap {gap}'})
        gap //= 2
    return frames

def visualize_shell_sort(arr, output_file):
    frames = shell_sort(arr)
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
    output_file = "shell_sort_visualization.gif"
    visualize_shell_sort(arr, output_file)
