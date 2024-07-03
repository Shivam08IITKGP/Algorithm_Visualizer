import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def visualize_insertion_sort(arr, output_file):
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.set_xlim(-1, len(arr))
    ax.set_ylim(-1, 2)
    ax.axis('off')  # Turn off the axis

    # Initial text elements
    text_elements = []
    for i, value in enumerate(arr):
        text = ax.text(i, 0, str(value), ha='center', va='center', fontsize=12)
        text_elements.append(text)

    # Annotate text elements for i and j
    i_annotation = ax.text(0, 1, '', ha='center', va='center', fontsize=12, color='red')
    j_annotation = ax.text(0, 1, '', ha='center', va='center', fontsize=12, color='blue')

    def update(frame):
        array, annotations = frame['array'], frame['annotations']
        for text_element, value in zip(text_elements, array):
            text_element.set_text(str(value))

        if 'i' in annotations:
            i_index = annotations['i']
            i_annotation.set_position((i_index, 1))
            i_annotation.set_text('i')
        else:
            i_annotation.set_text('')

        if 'j' in annotations:
            j_index = annotations['j']
            j_annotation.set_position((j_index, 1.2))
            j_annotation.set_text('j')
        else:
            j_annotation.set_text('')

    def insertion_sort_anim(arr):
        frames = []
        for i in range(1, len(arr)):
            annotations = {'i': i}
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                annotations['j'] = j
                frames.append({'array': arr.copy(), 'annotations': annotations.copy()})
                j -= 1
            arr[j + 1] = key
            frames.append({'array': arr.copy(), 'annotations': annotations.copy()})
        frames.append({'array': arr.copy(), 'annotations': {}})
        return frames

    frames = insertion_sort_anim(arr.copy())
    ani = animation.FuncAnimation(fig, update, frames=frames, repeat=False, interval=500)
    ani.save(output_file, writer='pillow')
    plt.close(fig)

def main():
    arr = [random.randint(1, 20) for _ in range(10)]
    print("Original array:", arr)
    output_file = 'insertion_sort.gif'
    visualize_insertion_sort(arr, output_file)
    print(f"Animation saved to {output_file}")

if __name__ == "__main__":
    main()
