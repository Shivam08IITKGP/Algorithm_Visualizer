import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
from io import BytesIO
import PIL.Image


def fig_to_image(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image = PIL.Image.open(buf)
    return image


def lcsu(A, B):
    A = A.upper()
    B = B.upper()
    n = len(A)
    m = len(B)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    max_length = 0
    end_pos = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if A[i - 1] == B[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    end_pos = i
            else:
                dp[i][j] = 0

    longest_common_substring = A[end_pos - max_length:end_pos]
    return dp, longest_common_substring


def visualize_lcsu(A, B, output_file):
    A = A.upper()
    B = B.upper()
    n = len(A)
    m = len(B)
    dp, string = lcsu(A, B)
    frames = []

    # Calculate figure size based on DP table dimensions and text size
    rows = n + 1
    cols = m + 1
    fig_width = cols * 0.5  # Adjust based on capacity
    fig_height = rows * 0.5  # Adjust based on total items and text size

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    def update(frame):
        ax.clear()
        ax.axis('off')
        i, j = frame
        table_data = [[f'{dp[i][j]}' if j > 0 else '0' for j in range(cols)] for i in range(rows)]

        uniform_col_width = 0.1
        table = ax.table(cellText=table_data, loc='center', cellLoc='center',
                         colLabels=[f'{j}' for j in range(cols)], rowLabels=[f'{i}' for i in range(rows)],
                         colWidths=[uniform_col_width] * cols)

        table.auto_set_font_size(False)
        table.set_fontsize(6)
        table.scale(1, 1)

        if i > 0 and j > 0 and i <= n and j <= m:
            table.get_celld()[(i + 1, j)].set_facecolor('lightgreen')
            if A[i - 1] == B[j - 1]:
                table.get_celld()[(i, j - 1)].set_facecolor('lightblue')

        highlighted_A = ''.join([f'[{char}]' if idx == i - 1 else char for idx, char in enumerate(A)])
        highlighted_B = ''.join([f'[{char}]' if idx == j - 1 else char for idx, char in enumerate(B)])
        ax.text(0.5, 0.1, f'A: {highlighted_A}', ha='center', va='center', fontsize=10)
        ax.text(0.5, 0.05, f'B: {highlighted_B}', ha='center', va='center', fontsize=10)

        frames.append(fig_to_image(fig))
        plt.close(fig)

    ani = FuncAnimation(fig, update, frames=[(i, j) for i in range(1, rows) for j in range(1, cols)],
                        repeat=False)
    writer = PillowWriter(fps=1)
    ani.save(output_file, writer=writer, dpi=120)  # Adjust dpi for quality
    plt.close(fig)

    return string


def main():
    # Example input data
    A = "ABCBDAB"
    B = "BDCAB"
    output_file = 'lcs_2.gif'
    visualize_lcsu(A, B, output_file)
    # print(f"Longest Common Subsequence: {dp_table[0]}")
    # print(f"DP Table:\n {np.array(dp_table)}")


if __name__ == "__main__":
    main()
