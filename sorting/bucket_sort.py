import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def bucket_sort(arr):
    frames = []
    bucket = []
    n = len(arr)
    max_value = max(arr)
    size = max_value / n

    for i in range(n):
        bucket.append([])

    for i in range(n):
        j = int(arr[i] / size)
        if j != n:
            bucket[j].append(arr[i])
        else:
            bucket[n - 1].append(arr[i])
        frames.append({'arr': arr.copy(), 'color': ['blue' if x == i else 'black' for x in range(len(arr))], 'title': 'Bucket Sort'})

    for i in range(n):
        bucket[i] = sorted(bucket[i])
        frames.append({'arr': arr.copy(), 'color': ['red' for _ in range(len(arr))], 'title': f'Bucket {i} Sorted'})

    result = []
    for i in range(n):
        result += bucket[i]

    for i in range(n):
        arr[i] = result[i]
        frames.append({'arr': arr.copy(), 'color': ['green' if x == i else 'black' for x in range(len(arr))], 'title': 'Bucket Sort'})

    return frames

def visualize_bucket_sort(arr, output_file):
    frames = bucket_sort(arr)
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
    output_file = "bucket_sort_visualization.gif"
    visualize_bucket_sort(arr, output_file)
