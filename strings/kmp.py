import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def fig_to_image(fig):
    from io import BytesIO
    import PIL.Image

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image = PIL.Image.open(buf)
    return image


def compute_kmp_array(s):
    n = len(s)
    lps = [0] * n
    length = 0
    i = 1

    while i < n:
        if s[i] == s[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def visualize_kmp_array(text, output_file):
    pi = compute_kmp_array(text)
    text_len = len(text)

    # Calculate figure size based on text length
    fig_width = max(6, text_len * 0.6)  # Ensure a minimum width of 6 inches
    fig_height = max(2, text_len * 0.3)  # Ensure a minimum height of 2 inches

    def update(frame):
        ax.clear()

        # Display the original string with reduced separation between characters
        for idx, char in enumerate(text):
            ax.text(idx * (1.0 / text_len), 0.5, char, fontsize=12, ha='center', va='center')


        for j in range(pi[frame]):
            ax.text(j * (1.0 / text_len), 0.5, text[j], fontsize=12, ha='center', va='center', color='green')

        for j in range(frame-pi[frame]+1, frame+1):
            ax.text(j * (1.0 / text_len), 0.5, text[j], fontsize=12, ha='center', va='center', color='blue')

        # Calculate positions relative to the length of the text and pi[frame]
        i_pos = frame * (1.0 / text_len)
        pi_pos = (frame - pi[frame]) * (1.0 / text_len)

        # Ensure positions are within the bounds of the plot
        i_pos = max(0.00, min(1.0 - (1.0 / text_len), i_pos))
        pi_pos = max(0.00, min(1.0 - (1.0 / text_len), pi_pos))

        # Highlight indices i and pi[i] in smaller font just below the letters
        ax.text(i_pos, 0.4, 'i', fontsize=8, ha='center', color='blue')
        ax.text(pi_pos, 0.3, 'i - pref[i]', fontsize=8, ha='center', color='green')  # Fixed alignment

        # Add arrows above the array for clarity
        arrow_length = 0.1  # Adjust arrow length manually
        ax.annotate('', xy=(i_pos, 0.5), xytext=(i_pos, 0.8 + arrow_length),
                    arrowprops=dict(facecolor='blue', width=2, headwidth=8))
        ax.annotate('', xy=(pi_pos, 0.5), xytext=(pi_pos, 0.8 + arrow_length),
                    arrowprops=dict(facecolor='green', width=2, headwidth=8))

        # Display the prefix array value at index frame
        ax.text(0.5, 0.2, f'Prefix-array at index {frame}: {pi[frame]}', fontsize=10, ha='center')  # Center alignment

        ax.set_axis_off()

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ani = FuncAnimation(fig, update, frames=len(text), repeat=False)
    writer = PillowWriter(fps=1)
    ani.save(output_file, writer=writer)
    plt.close(fig)
    return pi


def main():
    text = "abababca"
    output_file = 'kmp_animation.gif'
    visualize_kmp_array(text, output_file)
    print(f"Prefix-array animation saved as {output_file}")


if __name__ == "__main__":
    main()
