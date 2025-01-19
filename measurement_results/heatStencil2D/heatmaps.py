import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import numpy as np
import os

# Read the data from file
def read_timestep_data(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Split by blank lines (new timesteps)
    timesteps = re.split(r'\n\s*\n', content.strip())

    data_dict = {}

    for timestep in timesteps:
        lines = timestep.split('\n')
        time_label = lines[0].strip().replace(" ", "_").replace(":", "")
        values = [list(map(float, row.split(','))) for row in lines[1:]]
        data_dict[time_label] = values

    return data_dict

# Function to create heatmaps for 3 selected timesteps in a row with a single colorbar
def create_combined_heatmaps(data_dict, selected_timesteps, output_file='combined_heatmap.png'):
    plt.figure(figsize=(18, 6))  # Adjust size for a row of 3 heatmaps

    # Cap values to the range 273-333 K and convert to DataFrame
    dfs = {timestep: pd.DataFrame(data_dict[timestep]).clip(lower=273, upper=333) for timestep in selected_timesteps}

    # Create subplots for each timestep heatmap
    for idx, timestep in enumerate(selected_timesteps, 1):
        ax = plt.subplot(1, 3, idx)  # 1 row, 3 columns
        sns.heatmap(dfs[timestep], cmap='coolwarm', annot=False, fmt='.2f',
                    cbar=idx == 3, linewidths=0.5, vmin=273, vmax=333)

        # Bold and larger title for each heatmap
        plt.title(f"Heatmap for {timestep}", fontsize=16, fontweight='bold')
        plt.xticks([])  # Remove x-axis ticks
        plt.yticks([])  # Remove y-axis ticks

        # Add colorbar to the last heatmap only
        if idx == 3:
            colorbar = ax.collections[0].colorbar
            colorbar.set_label('Temperature (K)', fontsize=16, fontweight='bold')
            colorbar.set_ticks([273, 283, 293, 303, 313, 323, 333])
            colorbar.set_ticklabels(
                [r'$\leq$ 273 K', '283 K', '293 K', '303 K', '313 K', '323 K', r'$\geq$ 333 K']
            )
            colorbar.ax.tick_params(labelsize=14)  # Increase and bolden legend tick labels
            for label in colorbar.ax.get_yticklabels():
                label.set_fontweight('bold')

    plt.tight_layout()
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()

# Example usage
file_path = 'temperatures_approx_medium1.csv'  # Replace with your actual file path
data_dict = read_timestep_data(file_path)

# Specify three timesteps to visualize
selected_timesteps = ['Timestep_0', 'Timestep_1000', 'Timestep_2000']  # Change based on available keys

create_combined_heatmaps(data_dict, selected_timesteps)
