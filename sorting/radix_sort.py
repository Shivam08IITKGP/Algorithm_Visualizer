import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def counting_sort(arr, exp, frames):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]
        frames.append({'arr': arr.copy(), 'color': ['red' if x == i else 'black' for x in range(len(arr))], 'title': f'Radix Sort - Exp {exp}'})

def radix_sort(arr):
    frames = []
    max1 = max(arr)
    exp = 1
    while max1 // exp > 0:
        counting_sort(arr, exp, frames)
        exp *= 10
    return frames

def visualize_radix_sort(arr, output_file):
    frames = radix_sort(arr)
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
    arr = random.sample(range(1, 100), 10)
    output_file = "radix_sort_visualization.gif"
    visualize_radix_sort(arr, output_file)
