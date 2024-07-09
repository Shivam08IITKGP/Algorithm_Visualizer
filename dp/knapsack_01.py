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


def knapsack_01(weights, values, capacity):
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    return dp


def visualize_knapsack_01(weights, values, capacity, output_file):
    n = len(weights)
    dp = knapsack_01(weights, values, capacity)  # Compute DP table
    frames = []

    # Calculate figure size based on DP table dimensions and text size
    rows = len(dp)
    cols = capacity + 1
    fig_width = (cols + 5) * 0.6  # Adjust based on capacity
    fig_height = rows * 0.25 + 2.5  # Adjust based on total items and text size

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    def update(frame):
        ax.clear()
        ax.axis('off')
        i, w = frame
        if i > 0 and w > 0:
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

        # Update DP table visualization
        table_data = [[f'{dp[i][j]}' if j > 0 else '0' for j in range(cols)] for i in range(rows)]

        for j in range(1, n + 1):
            table_data[j][0] = f'{values[j - 1]}'
        table = ax.table(cellText=table_data, loc='center', cellLoc='center',
                         colLabels=[f'{j}' for j in range(cols)],
                         rowLabels=[f'Item {i}' for i in range(rows)])

        table.auto_set_font_size(False)
        table.set_fontsize(6)  # Decrease font size further if needed
        table.scale(1.2, 1.2)  # Scale down table size further if needed

        # Highlight the current cell being updated
        if i > 0 and w > 0:
            table.get_celld()[(i + 1, w)].set_facecolor('lightgreen')  # Highlight current cell
        if i > 1 and w > weights[i - 1]:
            table.get_celld()[(i, w - weights[i - 1])].set_facecolor('yellow')
        if i > 0:
            table.get_celld()[(i, w)].set_facecolor('yellow')

        if i == 0:
            ax.set_title(f'Initialising')
        else:
            ax.set_title(f'0/1 Knapsack DP Table, now at item {i}, capacity {w}')
        frames.append(fig_to_image(fig))
        plt.close(fig)

    ani = FuncAnimation(fig, update, frames=[(i, w) for i in range(1, rows) for w in range(1, cols)],
                        repeat=False)
    writer = PillowWriter(fps=1)
    ani.save(output_file, writer=writer, dpi=100)  # Adjust dpi for quality
    plt.close(fig)

    return dp[n][capacity]


def main():
    # Example input data
    weights = [1, 3, 4, 5]
    values = [10, 40, 50, 70]
    capacity = 8
    output_file = 'knapsack_01_animation.gif'

    # Visualize the 0/1 Knapsack problem
    dp_table = visualize_knapsack_01(weights, values, capacity, output_file)
    print(f"DP Table:\n {np.array(dp_table)}")


if __name__ == "__main__":
    main()
