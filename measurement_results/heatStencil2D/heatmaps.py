import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec
import os
import sys
from datetime import datetime

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

# Function to create heatmaps and save the image with a timestamp
def create_combined_heatmaps(data_dict, selected_timesteps, output_file):
    plt.figure(figsize=(22, 6), constrained_layout=True)  # Increased figure width

    # Cap values outside the range [273, 333] to 250 and 350
    capped_dfs = {
        timestep: pd.DataFrame(np.clip(data_dict[timestep], 250, 350))
        for timestep in selected_timesteps
    }

    # Define a continuous colormap with significantly darker endpoint colors
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "custom_cmap",
        ['midnightblue', 'blue', 'lightblue', 'lightcoral', 'red', '#660000']
    )

    # Normalize values including the artificial bounds of 250 and 350
    norm = mcolors.Normalize(vmin=250, vmax=350)

    # Create grid layout with an extra column for the colorbar
    gs = gridspec.GridSpec(1, 4, width_ratios=[0.9, 0.9, 0.9, 0.1])  # Last column for the colorbar
    gs.update(wspace=0.05)

    # Create subplots for each timestep heatmap
    for idx, timestep in enumerate(selected_timesteps):
        ax = plt.subplot(gs[idx])
        sns.heatmap(capped_dfs[timestep], cmap=cmap, norm=norm, annot=False, fmt='.2f',
                    cbar=False, linewidths=0.5)

        # Bold and larger title for each heatmap
        plt.title(f"{timestep}", fontsize=24, fontweight='bold')
        plt.xticks([])  # Remove x-axis ticks
        plt.yticks([])  # Remove y-axis ticks

    # Add a separate subplot for the colorbar
    cbar_ax = plt.subplot(gs[3])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cbar = plt.colorbar(sm, cax=cbar_ax)

    # Customize colorbar labels
    cbar.set_label('Temperature (K)', fontsize=20, fontweight='bold')
    cbar.set_ticks([250, 273, 300, 333, 350])
    cbar.set_ticklabels(
        [r'$\leq$273K', '273K', '300K', '333K', r'$\geq$333K']
    )

    cbar.ax.tick_params(labelsize=18)  # Increase and bolden legend tick labels
    for label in cbar.ax.get_yticklabels():
        label.set_fontweight('bold')

    # Save the figure to the specified output file
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()

# Main script to handle command-line arguments and generate output filename
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python generate_heatmaps.py <file_path> <timestep_1> <timestep_2> <timestep_3>")
        sys.exit(1)

    # Get command-line arguments
    file_path = sys.argv[1]

    # Ensure the file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)

    try:
        timestep_numbers = [int(sys.argv[i]) for i in range(2, 5)]
    except ValueError:
        print("Error: Timesteps should be integers.")
        sys.exit(1)

    # Format the timesteps to match the expected keys in the data dictionary
    selected_timesteps = [f"Timestep_{num}" for num in timestep_numbers]

    # Read data from file
    data_dict = read_timestep_data(file_path)

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Extract base file name without extension
    base_filename = os.path.splitext(os.path.basename(file_path))[0]

    # Define output directory
    output_dir = "heatmaps"
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

    # Create output file name with timestamp
    output_file = os.path.join(output_dir, f"{base_filename}_{timestamp}.png")

    # Generate and save the heatmap
    create_combined_heatmaps(data_dict, selected_timesteps, output_file)

    print(f"Heatmap saved as: {output_file}")
