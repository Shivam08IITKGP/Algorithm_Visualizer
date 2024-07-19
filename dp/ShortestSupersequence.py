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

def scs(A, B):
    n = len(A)
    m = len(B)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif A[i - 1] == B[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1])

    i, j = n, m
    scs_str = []
    while i > 0 and j > 0:
        if A[i - 1] == B[j - 1]:
            scs_str.append(A[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] < dp[i][j - 1]:
            scs_str.append(A[i - 1])
            i -= 1
        else:
            scs_str.append(B[j - 1])
            j -= 1

    while i > 0:
        scs_str.append(A[i - 1])
        i -= 1

    while j > 0:
        scs_str.append(B[j - 1])
        j -= 1

    return dp, scs_str[::-1]

def visualize_scs(A, B, output_file):
    n = len(A)
    m = len(B)
    dp, scs_str = scs(A, B)
    frames = []

    rows = n + 1
    cols = m + 1
    fig_width = cols * 0.5
    fig_height = rows * 0.5 + 0.5
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    plt.subplots_adjust(top=0.95, bottom=0.05)  # Adjust the top and bottom margins

    def update(frame):
        ax.clear()
        ax.axis('off')
        i, j = frame
        table_data = [[f'{dp[i][j]}' if j > 0 else '0' for j in range(cols)] for i in range(rows)]

        uniform_col_width = 0.1
        table = ax.table(cellText=table_data, loc='center', cellLoc='center',
                         colLabels=[f'{j}' for j in range(cols)], rowLabels=[f'{i}' for i in range(rows)],
                         colWidths=[uniform_col_width] * cols, bbox=[0, 0.3, 1, 0.7])

        table.auto_set_font_size(False)
        table.set_fontsize(6)
        table.scale(1, 1)

        if i > 0 and j > 0 and i <= n and j <= m:
            table.get_celld()[(i + 1, j)].set_facecolor('lightgreen')
            if A[i - 1] == B[j - 1]:
                table.get_celld()[(i, j - 1)].set_facecolor('lightblue')
            elif dp[i - 1][j] < dp[i][j - 1]:
                table.get_celld()[(i, j)].set_facecolor('yellow')
            else:
                table.get_celld()[(i + 1, j - 1)].set_facecolor('yellow')

        highlighted_A = ''.join([f'[{char}]' if idx == i - 1 else char for idx, char in enumerate(A)])
        highlighted_B = ''.join([f'[{char}]' if idx == j - 1 else char for idx, char in enumerate(B)])
        ax.text(0.5, 0.25, f'A: {highlighted_A}', ha='center', va='center', fontsize=8, transform=ax.transAxes)  # Adjusted position and font size
        ax.text(0.5, 0.2, f'B: {highlighted_B}', ha='center', va='center', fontsize=8, transform=ax.transAxes)  # Adjusted position and font size

        frames.append(fig_to_image(fig))
        plt.close(fig)

    ani = FuncAnimation(fig, update, frames=[(i, j) for i in range(1, rows) for j in range(1, cols)],
                        repeat=False)
    writer = PillowWriter(fps=1)
    ani.save(output_file, writer=writer, dpi=200)
    plt.close(fig)

    return scs_str

def main():
    A = "AGGTAB"
    B = "GXTXAYB"
    output_file = 'scs.gif'
    visualize_scs(A, B, output_file)

if __name__ == "__main__":
    main()
