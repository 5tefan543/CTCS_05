import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import numpy as np
import matplotlib.colors as mcolors
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

# Function to create a heatmap for a single timestep and save it
def create_single_heatmap(data, timestep, output_file):
    plt.figure(figsize=(8, 6), constrained_layout=True)  # Smaller figure size for individual plots

    # Cap values outside the range [273, 333] to 250 and 350
    df = pd.DataFrame(np.clip(data, 250, 350))

    # Define a continuous colormap with significantly darker endpoint colors
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "custom_cmap",
        ['midnightblue', 'blue', 'lightblue', 'lightcoral', 'red', '#660000']
    )

    # Normalize values including the artificial bounds of 250 and 350
    norm = mcolors.Normalize(vmin=250, vmax=350)

    # Create the heatmap
    ax = sns.heatmap(df, cmap=cmap, norm=norm, annot=False, fmt='.2f', linewidths=0.5, cbar=True)

    # Add title
    plt.title(f"{timestep}", fontsize=64, fontweight='bold')
    plt.xticks([])  # Remove x-axis ticks
    plt.yticks([])  # Remove y-axis ticks

    # Customize colorbar
    colorbar = ax.collections[0].colorbar
    colorbar.set_label('Temperature (K)', fontsize=14, fontweight='bold')
    colorbar.set_ticks([250, 273, 300, 333, 350])
    colorbar.set_ticklabels(
        [r'$\leq$ 273 K', '273 K', '300 K', '333 K', r'$\geq$ 333 K']
    )
    colorbar.ax.tick_params(labelsize=30)  # Increase legend tick label size
    for label in colorbar.ax.get_yticklabels():
        label.set_fontweight('bold')

    # Save the figure to the specified output file
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()

# Main script to process all timesteps and save heatmaps
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_single_timestep_heatmaps.py <file_path>")
        sys.exit(1)

    # Get command-line argument for file path
    file_path = sys.argv[1]

    # Ensure the file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)

    # Read data from file
    data_dict = read_timestep_data(file_path)

    # Define output directory
    output_dir = "timesteps"
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

    # Extract base file name without extension
    base_filename = os.path.splitext(os.path.basename(file_path))[0]

    # Loop through all available timesteps and save them individually
    for timestep, data in data_dict.items():
        # Extract numeric part of timestep for filename
        timestep_number = timestep.split('_')[1]

        # Create output filename with timestep number
        output_file = os.path.join(output_dir, f"{base_filename}_Timestep_{timestep_number}.png")

        # Generate and save the heatmap for the current timestep
        create_single_heatmap(data, timestep, output_file)

        print(f"Saved heatmap: {output_file}")

    print("All timesteps processed and saved successfully.")
