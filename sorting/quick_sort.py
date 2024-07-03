import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def partition(arr, low, high, frames):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            frames.append({
                'arr': arr.copy(),
                'pivot_idx': high,
                'i': i,
                'j': j,
                'start': low,
                'end': high,
                'partition_done': False
            })

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    frames.append({
        'arr': arr.copy(),
        'pivot_idx': i + 1,
        'i': i + 1,
        'j': high,
        'start': low,
        'end': high,
        'partition_done': True
    })

    return i + 1


def quick_sort(arr, low, high, frames):
    if low < high:
        pi = partition(arr, low, high, frames)

        quick_sort(arr, low, pi - 1, frames)
        quick_sort(arr, pi + 1, high, frames)


def visualize_quick_sort(arr, output_file):
    frames = []
    quick_sort(arr, 0, len(arr) - 1, frames)

    fig, ax = plt.subplots()
    ax.set_axis_off()

    def update(frame):
        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])

        for idx, num in enumerate(frame['arr']):
            color = 'red' if idx == frame['i'] or idx == frame['j'] or idx == frame['pivot_idx'] else 'black'
            ax.text(idx, 0, str(num), fontsize=12, ha='center', va='center', color=color)

            if idx == frame['i']:
                ax.text(idx, -0.2, 'i', fontsize=10, ha='center', va='center', color='blue')
            elif idx == frame['j']:
                ax.text(idx, -0.2, 'j', fontsize=10, ha='center', va='center', color='green')
            elif idx == frame['pivot_idx']:
                ax.text(idx, -0.2, 'pivot', fontsize=10, ha='center', va='center', color='purple')

        ax.axvline(frame['start'] - 0.5, color='orange', linestyle='--')
        ax.axvline(frame['end'] + 0.5, color='orange', linestyle='--')

        if frame.get('partition_done', False):
            ax.set_title(f"Partition {frame['start']} to {frame['end']} Sorted")
            ax.text((frame['start'] + frame['end']) / 2, -0.4, 'Partition Sorted', fontsize=12, ha='center',
                    va='center', color='blue')
        else:
            ax.set_title(f"Sorting Partition {frame['start']} to {frame['end']}")

        ax.set_xlim(-0.5, len(frame['arr']) - 0.5)
        ax.set_ylim(-0.5, 0.5)

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=1000, repeat=False)
    ani.save(output_file, writer='pillow', savefig_kwargs={'pad_inches': 0.0})
    plt.close(fig)


# Example usage:
if __name__ == "__main__":
    arr = [random.randint(1, 100) for _ in range(10)]  # Generate a random array
    output_file = "quick_sort_visualization.gif"
    visualize_quick_sort(arr, output_file)
