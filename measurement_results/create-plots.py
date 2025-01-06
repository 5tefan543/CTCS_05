import sys
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict

# The creation of this script used Chat-GPT as a Coding assistant.

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def rename_and_reorder_benchmarks(benchmark_data):
    # Mapping for renaming SciMark2 tests
    rename_mapping = {
        "SciMark2: SMM": "SMM",
        "SciMark2: FFT": "FFT",
        "SciMark2: LU": "LU",
        "SciMark2: MonteCarlo": "MonteCarlo",
        "SciMark2: SOR": "SOR",
        "Plane": "Raytracer"
    }

    # Reordering list
    reorder_list = ["FFT", "SOR", "MonteCarlo", "SMM", "LU", "ZXing", "jME", "ImageJ", "Raytracer"]

    # Rename benchmarks
    renamed_data = {}
    for key, value in benchmark_data.items():
        new_key = rename_mapping.get(key, key)  # Use mapping if available, otherwise keep original
        renamed_data[new_key] = value

    # Reorder benchmarks
    ordered_data = OrderedDict()
    for test_name in reorder_list:
        if test_name in renamed_data:
            ordered_data[test_name] = renamed_data[test_name]

    # Add remaining benchmarks (not in the reorder list) to the end
    for key in renamed_data:
        if key not in ordered_data:
            ordered_data[key] = renamed_data[key]

    return ordered_data

def plot_output_error(benchmark_data, directory=".", filename="output_error_plot.png"):
    # Extract the benchmark names and the corresponding collective values
    benchmark_names = list(benchmark_data.keys())
    values_mild = [benchmark_data[name]["collective"][0] for name in benchmark_names]
    values_medium = [benchmark_data[name]["collective"][1] for name in benchmark_names]
    values_aggressive = [benchmark_data[name]["collective"][2] for name in benchmark_names]

    # X-axis positions for grouped bars
    x_spacing = 0.7  # Reduce spacing between groups
    x = np.arange(len(benchmark_names)) * x_spacing
    bar_width = 0.18  # Narrower bars to reduce overlap and spacing

    # Dynamically adjust plot width based on the number of elements
    plot_width = max(4, len(benchmark_names) * 0.8)
    plt.figure(figsize=(plot_width, 5))

    # Create the bars with black outlines
    plt.bar(x - bar_width, values_mild, width=bar_width, label="Mild", color="darkblue", edgecolor="black")
    plt.bar(x, values_medium, width=bar_width, label="Medium", color="blue", edgecolor="black")
    plt.bar(x + bar_width, values_aggressive, width=bar_width, label="Aggressive", color="lightblue", edgecolor="black")
    
    # Set axis labels
    plt.xlabel("Benchmark", fontsize=12)
    plt.ylabel("Output Error", fontsize=12)

    # Set x-ticks and rotate labels
    plt.xticks(x, benchmark_names, rotation=45, ha="right", fontsize=10)

    plt.gca().spines['top'].set_visible(False)      # Hide the top spine
    plt.gca().spines['right'].set_visible(False)    # Hide the right spine
    plt.gca().spines['bottom'].set_visible(False)   # Hide the bottom spine
    plt.tick_params(axis='x', which='both', length=0)  # Remove x-axis ticks

    # Set y-axis limits to exactly 1.0
    plt.ylim(0.0, 1.0)

    # Add legend above the plot with no outline
    plt.legend(
        fontsize=10,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.10),  # Move above the plot
        ncol=3,  # Align elements horizontally
        frameon=False  # Remove legend outline
    )

    # Save the plot
    output_path = os.path.join(directory, filename)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Plot saved as '{output_path}'.")

def plot_operation_fractions(benchmark_data, directory=".", filename="operation_fractions_plot.png"):
    """
    Creates and saves a plot showing operation fractions for DRAM, SRAM, Integer operations, and FP operations.

    :param benchmark_data: Dictionary containing benchmark data with "approximateness" values.
    :param filename: Name of the file to save the plot.
    """
    # Extract the benchmark names and calculate the fractions of approximate operations
    benchmark_names = list(benchmark_data.keys())
    dram_storage = [
        benchmark_data[name]["approximateness"]["heap"][1] /
        (benchmark_data[name]["approximateness"]["heap"][0] + benchmark_data[name]["approximateness"]["heap"][1])
        if (benchmark_data[name]["approximateness"]["heap"][0] + benchmark_data[name]["approximateness"]["heap"][1]) != 0 else 0
        for name in benchmark_names
    ]
    sram_storage = [
        benchmark_data[name]["approximateness"]["stack"][1] /
        (benchmark_data[name]["approximateness"]["stack"][0] + benchmark_data[name]["approximateness"]["stack"][1])
        if (benchmark_data[name]["approximateness"]["stack"][0] + benchmark_data[name]["approximateness"]["stack"][1]) != 0 else 0
        for name in benchmark_names
    ]
    int_operations = [
        benchmark_data[name]["approximateness"]["alu"][1] /
        (benchmark_data[name]["approximateness"]["alu"][0] + benchmark_data[name]["approximateness"]["alu"][1])
        if (benchmark_data[name]["approximateness"]["alu"][0] + benchmark_data[name]["approximateness"]["alu"][1]) != 0 else 0
        for name in benchmark_names
    ]
    fp_operations = [
        benchmark_data[name]["approximateness"]["fpu"][1] /
        (benchmark_data[name]["approximateness"]["fpu"][0] + benchmark_data[name]["approximateness"]["fpu"][1])
        if (benchmark_data[name]["approximateness"]["fpu"][0] + benchmark_data[name]["approximateness"]["fpu"][1]) != 0 else 0
        for name in benchmark_names
    ]

    # X-axis positions for grouped bars
    x_spacing = 1.0  # Increased spacing between groups
    x = np.arange(len(benchmark_names)) * x_spacing
    bar_width = 0.2  # Slightly wider bars

    # Dynamically adjust plot width based on the number of elements
    plot_width = max(6, len(benchmark_names) * 1.2)
    plt.figure(figsize=(plot_width, 6))

    # Create the bars with black outlines
    plt.bar(x - 1.5 * bar_width, dram_storage, width=bar_width, label="DRAM Storage", color="darkblue", edgecolor="black")
    plt.bar(x - 0.5 * bar_width, sram_storage, width=bar_width, label="SRAM Storage", color="blue", edgecolor="black")
    plt.bar(x + 0.5 * bar_width, int_operations, width=bar_width, label="Integer Operations", color="skyblue", edgecolor="black")
    plt.bar(x + 1.5 * bar_width, fp_operations, width=bar_width, label="FP Operations", color="lightblue", edgecolor="black")

    # Set axis labels
    plt.xlabel("Benchmark", fontsize=12)
    plt.ylabel("Fraction Approximate", fontsize=12)

    # Set x-ticks and rotate labels
    plt.xticks(x, benchmark_names, rotation=45, ha="right", fontsize=10)

    plt.gca().spines['top'].set_visible(False)      # Hide the top spine
    plt.gca().spines['right'].set_visible(False)    # Hide the right spine
    plt.gca().spines['bottom'].set_visible(False)   # Hide the bottom spine
    plt.tick_params(axis='x', which='both', length=0)  # Remove x-axis ticks

    # Set y-axis limits to exactly 1.0
    plt.ylim(0.0, 1.0)

    # Add legend even higher above the plot with no outline
    plt.legend(
        fontsize=10,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.2),  # Adjusted even higher
        ncol=2,  # Align elements horizontally
        frameon=False  # Remove legend outline
    )

    # Save the plot
    output_path = os.path.join(directory, filename)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Plot saved as '{output_path}'.")

def plot_normalized_total_energy(benchmark_data, energy_save_data, directory=".", filename="normalized_total_energy_plot.png"):
    """
    Creates and saves a plot showing energy consumption for DRAM, SRAM, Integer, and FP components.

    :param benchmark_data: Dictionary containing benchmark data with operation counts.
    :param energy_save_data: Dictionary containing energy savings for levels 1, 2, 3.
    :param filename: Name of the file to save the plot.
    """
    # Extract benchmark names
    benchmark_names = list(benchmark_data.keys())

    # Initialize energy components
    energy_base = {"DRAM": [], "SRAM": [], "Integer": [], "FP": []}
    energy_approx = {1: {"DRAM": [], "SRAM": [], "Integer": [], "FP": []},
                     2: {"DRAM": [], "SRAM": [], "Integer": [], "FP": []},
                     3: {"DRAM": [], "SRAM": [], "Integer": [], "FP": []}}

    for name in benchmark_names:
        # Total operations for scaling
        total_operations = (
            sum(benchmark_data[name]["approximateness"]["heap"]) +
            sum(benchmark_data[name]["approximateness"]["stack"]) +
            sum(benchmark_data[name]["approximateness"]["alu"]) +
            sum(benchmark_data[name]["approximateness"]["fpu"])
        )

        # Operation counts and fractions
        num_dram_approx = benchmark_data[name]["approximateness"]["heap"][1]
        num_dram_total = sum(benchmark_data[name]["approximateness"]["heap"])
        dram_fraction_approx = num_dram_approx / num_dram_total if num_dram_total != 0 else 0

        num_sram_approx = benchmark_data[name]["approximateness"]["stack"][1]
        num_sram_total = sum(benchmark_data[name]["approximateness"]["stack"])
        sram_fraction_approx = num_sram_approx / num_sram_total if num_sram_total != 0 else 0

        num_int_approx = benchmark_data[name]["approximateness"]["alu"][1]
        num_int_total = sum(benchmark_data[name]["approximateness"]["alu"])
        num_fp_approx = benchmark_data[name]["approximateness"]["fpu"][1]
        num_fp_total = sum(benchmark_data[name]["approximateness"]["fpu"])

        total_weighted_ops = (num_fp_total * 40 + num_int_total * 37)

        # Base case energy contributions
        energy_base["DRAM"].append(0.45)  # DRAM is always 45% in the base case
        energy_base["SRAM"].append(0.35)  # SRAM is 35%

        int_fraction = (num_int_total * 37 / total_weighted_ops) * 0.20 if total_weighted_ops != 0 else 0
        fp_fraction = (num_fp_total * 40 / total_weighted_ops) * 0.20 if total_weighted_ops != 0 else 0

        energy_base["Integer"].append(int_fraction)
        energy_base["FP"].append(fp_fraction)

        # Levels 1, 2, 3 energy reductions
        for level, reduction in zip([1, 2, 3], ["mild", "medium", "aggressive"]):
            # DRAM reduction
            dram_reduction = energy_base["DRAM"][-1] * dram_fraction_approx * energy_save_data["DRAM"][reduction]
            energy_approx[level]["DRAM"].append(energy_base["DRAM"][-1] - dram_reduction)

            # SRAM reduction
            sram_reduction = energy_base["SRAM"][-1] * sram_fraction_approx * energy_save_data["SRAM"][reduction]
            energy_approx[level]["SRAM"].append(energy_base["SRAM"][-1] - sram_reduction)

            # Integer reduction
            int_reduction = (
                (num_int_approx * (37 - 22) / total_weighted_ops) *0.2 * energy_save_data["INT"][reduction]
            ) if total_weighted_ops != 0 else 0
            energy_approx[level]["Integer"].append(energy_base["Integer"][-1] - int_reduction)

            # FP reduction
            fp_reduction = (
                (num_fp_approx * (40 - 22) / total_weighted_ops)*0.2 * energy_save_data["FLOAT"][reduction]
            ) if total_weighted_ops != 0 else 0
            energy_approx[level]["FP"].append(energy_base["FP"][-1] - fp_reduction)

    # X-axis positions for grouped bars
    x = np.arange(len(benchmark_names)) * 0.75
    bar_width = 0.18

    # Dynamically adjust plot width based on the number of elements
    plot_width = len(benchmark_names) * 1.0
    plt.figure(figsize=(plot_width, 6))

    # Create stacked bars for Base (B)
    plt.bar(x - 1.5 * bar_width, energy_base["DRAM"], width=bar_width, label="DRAM", color="darkblue", edgecolor="black")
    plt.bar(
        x - 1.5 * bar_width,
        energy_base["SRAM"],
        width=bar_width,
        bottom=energy_base["DRAM"],
        label="SRAM",
        color="blue",
        edgecolor="black"
    )
    plt.bar(
        x - 1.5 * bar_width,
        energy_base["Integer"],
        width=bar_width,
        bottom=[dr + sr for dr, sr in zip(energy_base["DRAM"], energy_base["SRAM"])],
        label="Integer",
        color="skyblue",
        edgecolor="black"
    )
    plt.bar(
        x - 1.5 * bar_width,
        energy_base["FP"],
        width=bar_width,
        bottom=[
            dr + sr + intg
            for dr, sr, intg in zip(energy_base["DRAM"], energy_base["SRAM"], energy_base["Integer"])
        ],
        label="FP",
        color="lightblue",
        edgecolor="black"
    )

    # Create stacked bars for levels 1, 2, 3
    for level, offset in zip([1, 2, 3], [-0.5, 0.5, 1.5]):
        plt.bar(x + offset * bar_width, energy_approx[level]["DRAM"], width=bar_width, color="darkblue", edgecolor="black")
        plt.bar(
            x + offset * bar_width,
            energy_approx[level]["SRAM"],
            width=bar_width,
            bottom=energy_approx[level]["DRAM"],
            color="blue",
            edgecolor="black"
        )
        plt.bar(
            x + offset * bar_width,
            energy_approx[level]["Integer"],
            width=bar_width,
            bottom=[
                dr + sr for dr, sr in zip(energy_approx[level]["DRAM"], energy_approx[level]["SRAM"])
            ],
            color="skyblue",
            edgecolor="black"
        )
        plt.bar(
            x + offset * bar_width,
            energy_approx[level]["FP"],
            width=bar_width,
            bottom=[
                dr + sr + intg for dr, sr, intg in zip(
                    energy_approx[level]["DRAM"],
                    energy_approx[level]["SRAM"],
                    energy_approx[level]["Integer"]
                )
            ],
            color="lightblue",
            edgecolor="black"
        )

    # Set axis labels and ticks
    plt.ylabel("Normalized Total Energy", fontsize=12)
    plt.xticks(
        x,
        benchmark_names,  # Only show benchmark names
        rotation=45,
        ha="right",
        fontsize=10
    )

    # Adjust y-axis limit and move x-axis
    plt.ylim(-0.05, 1.0)  # Extend y-limit slightly upward
    plt.gca().spines['bottom'].set_position(('outward', 10))  # Move x-axis slightly higher

    # Add labels under each bar
    for i, benchmark in enumerate(benchmark_names):
        # Base case
        plt.text(x[i] - 1.5 * bar_width, -0.02, "B", ha="center", va="center", fontsize=10)
        # Level 1
        plt.text(x[i] - 0.5 * bar_width, -0.02, "1", ha="center", va="center", fontsize=10)
        # Level 2
        plt.text(x[i] + 0.5 * bar_width, -0.02, "2", ha="center", va="center", fontsize=10)
        # Level 3
        plt.text(x[i] + 1.5 * bar_width, -0.02, "3", ha="center", va="center", fontsize=10)



    plt.yticks(np.arange(0, 1.1, 0.2), ["0%", "20%", "40%", "60%", "80%", "100%"], fontsize=10)

    # Set y-axis limit to 1.0
    plt.ylim(0.0, 1.0)

    # Hide unnecessary plot spines
    plt.gca().spines['top'].set_visible(False)    # Hide the top spine
    plt.gca().spines['right'].set_visible(False)  # Hide the right spine
    plt.gca().spines['bottom'].set_visible(False) # Hide the bottom spine
    plt.tick_params(axis='x', which='both', length=0)  # Remove x-axis ticks

    # Add legend above the plot with no outline
    plt.legend(
        fontsize=10,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.1),  # Move legend even higher above the plot
        ncol=4,  # Align elements horizontally
        frameon=False  # Remove legend outline
    )

    # Save the plot
    output_path = os.path.join(directory, filename)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Plot saved as '{output_path}'.")

def print_usage():
    print("Usage: python script.py [<directory>]")
    print("  <directory>: Directory where results.json and energy_save.json are located, and where plots will be saved (default: current directory)")

def main():
    directory = os.getcwd()

    args = sys.argv[1:]
    if len(args) > 1:
        print("Error: Too many arguments.")
        print_usage()
        sys.exit(1)

    if len(args) == 1:
        directory = args[0]

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)

    results_file = os.path.join(directory, 'results.json')
    energy_save_file = os.path.join(directory, 'energy_save.json')

    if not os.path.isfile(results_file):
        print(f"Error: File '{results_file}' does not exist.")
        sys.exit(1)
    if not os.path.isfile(energy_save_file):
        print(f"Error: File '{energy_save_file}' does not exist.")
        sys.exit(1)

    # Load JSON files
    benchmarks_data = load_json(results_file)
    benchmarks_data = rename_and_reorder_benchmarks(benchmarks_data)

    energy_save_data = load_json(energy_save_file)

    # Generate plots
    plot_output_error(benchmarks_data, directory=directory)
    plot_operation_fractions(benchmarks_data, directory=directory)
    plot_normalized_total_energy(benchmarks_data, energy_save_data, directory=directory)

if __name__ == "__main__":
    main()