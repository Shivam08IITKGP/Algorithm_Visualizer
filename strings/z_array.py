import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def compute_z_array(s):
    z = [0] * len(s)
    l, r, k = 0, 0, 0
    for i in range(1, len(s)):
        if i > r:
            l, r = i, i
            while r < len(s) and s[r] == s[r - l]:
                r += 1
            z[i] = r - l
            r -= 1
        else:
            k = i - l
            if z[k] < r - i + 1:
                z[i] = z[k]
            else:
                l = i
                while r < len(s) and s[r] == s[r - l]:
                    r += 1
                z[i] = r - l
                r -= 1
    return z


def visualize_z_array(text, output_file):
    z = compute_z_array(text)
    max_z = max(z)  # Maximum value in the Z-array

    # Calculate figure size based on text length
    text_len = len(text)
    fig_width = text_len * 0.2 + 2  # Adjusted width based on text length and spacing
    fig_height = 3  # Fixed height, adjust as needed

    def update(frame):
        ax.clear()

        # Display the original string with increased separation between characters
        for idx, char in enumerate(text):
            ax.text(idx * 0.2, 0.5, char, fontsize=16, ha='center', va='center')

        # Highlight the matching prefix and substring
        for j in range(z[frame]):
            ax.text(j * 0.2, 0.5, text[j], fontsize=16, ha='center', va='center', color='green')

        for j in range(frame, frame + z[frame]):
            ax.text(j * 0.2, 0.5, text[j], fontsize=16, ha='center', va='center', color='blue')

        # Calculate positions relative to the length of the text and max_z
        i_pos = frame * 0.2
        z_pos = (max(frame, frame + z[frame] - 1)) * 0.2

        # Ensure positions are within the bounds of the plot
        i_pos = max(0.00, min(text_len * 0.2 - 0.2, i_pos))
        z_pos = max(0.00, min(text_len * 0.2 - 0.2, z_pos))

        # Highlight indices i and pi[i] in smaller font just below the letters
        ax.text(i_pos, 0.4, 'i', fontsize=12, ha='center', color='blue')
        ax.text(z_pos, 0.3, 'z_pos[i]', fontsize=12, ha='center', color='green')

        # Add arrows above the array for clarity
        ax.annotate('', xy=(i_pos, 0.5), xytext=(i_pos, 0.6),
                    arrowprops=dict(facecolor='blue', shrink=0.05, width=0.5, headwidth=5))
        ax.annotate('', xy=(z_pos, 0.5), xytext=(z_pos, 0.7),
                    arrowprops=dict(facecolor='green', shrink=0.05, width=0.5, headwidth=5))

        # Display the Z-array value at index frame
        ax.text(text_len * 0.2 / 2, 0.1, f'Z-array at index {frame}: {z[frame]}', fontsize=12, ha='center')

        ax.set_axis_off()
        ax.set_xlim(-0.5, text_len * 0.2 + 0.5)
        ax.set_ylim(-0.5, 1)

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ani = FuncAnimation(fig, update, frames=len(text), repeat=False)
    writer = PillowWriter(fps=1)
    ani.save(output_file, writer=writer)
    plt.close(fig)
    return z


def main():
    text = "abababca"
    output_file = 'z_array_animation.gif'
    visualize_z_array(text, output_file)
    print(f"Z-array animation saved as {output_file}")


if __name__ == "__main__":
    main()
