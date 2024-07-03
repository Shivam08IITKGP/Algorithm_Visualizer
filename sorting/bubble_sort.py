import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def visualize_bubble_sort(arr, output_file):
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.set_axis_off()
    ax.set_xlim(-0.5, len(arr) - 0.5)
    ax.set_ylim(-1, 2)

    # Display the array elements as text annotations once
    text_objs = [ax.text(idx, 0, str(num), fontsize=10, ha='center', va='center', color='black') for idx, num in
                 enumerate(arr)]

    i_text = ax.text(-1, -0.5, '', fontsize=10, ha='center', va='center', color='blue')
    j_text = ax.text(-1, -0.5, '', fontsize=10, ha='center', va='center', color='green')

    def update(frame):
        heights = frame['heights']
        i = frame['i']
        j = frame['j']

        # Highlight i and j indices
        if i >= 0:
            i_text.set_position((i, -0.5))
            i_text.set_text('i')
        else:
            i_text.set_text('')

        if j >= 0:
            j_text.set_position((j, -0.5))
            j_text.set_text('j')
        else:
            j_text.set_text('')

        # Update text objects for array values
        for idx, num in enumerate(heights):
            text_objs[idx].set_text(str(num))

    def bubble_sort_anim(arr):
        frames = []
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    # Swap elements
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                # Prepare frame for animation
                frame = {
                    'heights': arr.copy(),
                    'i': j,
                    'j': j + 1,
                    'iteration': len(frames) + 1,
                    'title': f"Iteration {len(frames) + 1}, comparing elements {j} and {j + 1}"
                }
                frames.append(frame.copy())
        return frames

    frames = bubble_sort_anim(arr.copy())
    ani = animation.FuncAnimation(fig, update, frames=frames, repeat=False, interval=500)
    ani.save(output_file, writer='pillow', savefig_kwargs={'pad_inches': 0.1})
    plt.close(fig)


def main():
    # Generate a random array
    arr = random.sample(range(1, 101), 10)
    print(f"Original Array: {arr}")

    # Sort the array using bubble sort
    sorted_arr = bubble_sort(arr.copy())
    print(f"Sorted Array: {sorted_arr}")

    # Visualize bubble sort
    output_file = 'bubble_sort_animation.gif'
    visualize_bubble_sort(arr, output_file)
    print(f"Animation saved as {output_file}")


if __name__ == "__main__":
    main()
