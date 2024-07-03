import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def visualize_merge_sort(arr, output_file):
    fig, ax = plt.subplots(figsize=(6, 4))

    ax.set_axis_off()
    ax.set_xlim(-0.5, len(arr) - 0.5)
    ax.set_ylim(-0.5, 2.5)

    text_objs = [ax.text(idx, 1, str(num), fontsize=12, ha='center', va='center', color='black') for idx, num in enumerate(arr)]
    lines = []

    def update(frame):
        heights = frame['heights']
        indices = frame['indices']
        lines.extend(ax.plot(indices, [-0.5] * len(indices), color='gray', linestyle='-', linewidth=2))

        # Update array text objects
        for idx, num in enumerate(heights):
            text_objs[idx].set_text(str(num))

    def merge_sort_anim(arr):
        frames = []

        def helper(arr, left, right):
            if left >= right:
                return
            mid = (left + right) // 2
            helper(arr, left, mid)
            helper(arr, mid + 1, right)
            merge(arr, left, mid, right)

        def merge(arr, left, mid, right):
            temp = arr[left:right + 1]
            i, j, k = 0, mid - left + 1, left
            while i < mid - left + 1 and j < right - left + 1:
                frame = {'heights': arr.copy(), 'indices': list(range(left, right + 1))}
                frames.append(frame)
                if temp[i] <= temp[j]:
                    arr[k] = temp[i]
                    i += 1
                else:
                    arr[k] = temp[j]
                    j += 1
                k += 1
            while i < mid - left + 1:
                arr[k] = temp[i]
                i += 1
                k += 1
            while j < right - left + 1:
                arr[k] = temp[j]
                j += 1
                k += 1
            frames.append({'heights': arr.copy(), 'indices': list(range(left, right + 1))})

        helper(arr, 0, len(arr) - 1)
        return frames

    frames = merge_sort_anim(arr.copy())
    ani = animation.FuncAnimation(fig, update, frames=frames, repeat=False, interval=1000)
    ani.save(output_file, writer='pillow', savefig_kwargs={'pad_inches': 0.1})
    plt.close(fig)

def main():
    # Generate a random array
    arr = random.sample(range(1, 101), 8)
    print(f"Original Array: {arr}")

    # Sort the array using merge sort
    sorted_arr = merge_sort(arr.copy())
    print(f"Sorted Array: {sorted_arr}")

    # Visualize merge sort
    output_file = 'merge_sort_animation_tree.gif'
    visualize_merge_sort(arr, output_file)
    print(f"Animation saved as {output_file}")

if __name__ == "__main__":
    main()
