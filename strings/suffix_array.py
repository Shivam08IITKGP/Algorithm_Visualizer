import matplotlib.pyplot as plt
import matplotlib.animation as animation

def suffix_array(text):
    n = len(text)
    sa = list(range(n))
    b = [ord(text[i]) for i in range(n)]

    # Initial sorting based on single characters
    sa.sort(key=lambda x: text[x])  # Sort sa based on character directly from text

    # Visualization setup
    suffix_array_visualization = [''] * n
    sorted_substrings = [''] * n
    ranks_visualization = ['0'] * n
    visualization_steps = []
    for i in range(n):
        suffix_array_visualization[sa[i]] = str(i)
        sorted_substrings[sa[i]] = text[sa[i]]  # Initially, show suffixes as entire remaining text
    visualization_steps.append((f"Iteration 0: Initial sorting based on single characters",
                                ' | '.join(suffix_array_visualization[:]),
                                ' | '.join(sorted_substrings[:]),
                                ' | '.join(ranks_visualization[:])))

    # Sorting by increasing lengths
    b[sa[0]] = 0
    for i in range(1, n):
        b[sa[i]] = b[sa[i - 1]] + 1 if text[sa[i]] != text[sa[i - 1]] else b[sa[i - 1]]
    k = 1
    while k < n:
        bucket = b[:]
        temp = [-1] * n
        for i in range(n):
            bucket[i] = b[i]
            temp[i] = b[(i + k) % n]

        # Sort using the bucket and temp arrays
        sa.sort(key=lambda x: (bucket[x], temp[x]))

        # Update visualization steps incrementally
        suffix_array_visualization = [''] * n
        sorted_substrings = [''] * n
        ranks_visualization = [str(b[i]) for i in range(n)]
        for i in range(n):
            suffix_array_visualization[sa[i]] = str(i)
            # Ensure the substring length matches the current iteration's k value
            substring_end_index = sa[i] + (2 ** k)
            sorted_substrings[sa[i]] = text[sa[i]:min(substring_end_index, n)]
            visualization_steps.append((f"Iteration {k}: Sorting suffixes of length {2 ** k}",
                                        ' | '.join(suffix_array_visualization[:]),
                                        ' | '.join(sorted_substrings[:]),
                                        ' | '.join(ranks_visualization[:])))

        # Update b array
        new_rank = 0
        b[sa[0]] = new_rank
        for i in range(1, n):
            if bucket[sa[i]] != bucket[sa[i - 1]] or temp[sa[i]] != temp[sa[i - 1]]:
                new_rank += 1
            b[sa[i]] = new_rank
        k *= 2

    return sa, visualization_steps


def visualize_suffix_array_construction(text, outputfile='suffix_array_construction.gif'):
    suffix_array_result, visualization_steps = suffix_array(text)
    n = len(text)

    # Create a function to update the plot for each frame of the animation
    def update_frame(frame):
        ax.clear()
        ax.text(0.5, 0.7,
                f"{visualization_steps[frame][0]}\n{text}\n{visualization_steps[frame][1]}\nSorted Substrings:\n{visualization_steps[frame][2]}",
                fontsize=10, family='monospace', ha='center', va='center',
                bbox=dict(facecolor='lightblue', alpha=0.5, pad=5))
        ax.text(0.5, 0.3,
                f"Previous Ranks:\n{visualization_steps[frame][3]}",
                fontsize=10, family='monospace', ha='center', va='center',
                bbox=dict(facecolor='lightgreen', alpha=0.5, pad=5))
        ax.axis('off')

    # Setup figure and axis for the animation
    fig, ax = plt.subplots(figsize=(8, 4))  # Adjusted figsize
    ax.set_title('Suffix Array Construction with Sorted Substrings and Ranks', fontsize=12)
    ax.axis('off')

    # Create animation
    anim = animation.FuncAnimation(fig, update_frame, frames=len(visualization_steps), interval=1000, repeat=False)
    anim.save(outputfile, writer='pillow', dpi=100)  # Adjusted dpi

    return suffix_array_result


if __name__ == '__main__':
    text = "banana"
    s = visualize_suffix_array_construction(text)
    print(s)
