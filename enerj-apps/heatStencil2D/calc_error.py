import re
import math

# The creation of this script used ChatGPT as a coding assistant.

def calc_error(precise_output, approx_output):
    # Parse arrays from the console output
    precise_array = read_array(precise_output)
    approx_array = read_array(approx_output)

    # Ensure both outputs have the same shape
    if len(precise_array) != len(approx_array) or \
       any(len(row1) != len(row2) for row1, row2 in zip(precise_array, approx_array)):
        raise ValueError(
    "Precise and approximate outputs must have the same dimensions. "
    "Precise dimensions: {}x{}, Approx dimensions: {}x{}".format(
        len(precise_array), len(precise_array[0]),
        len(approx_array), len(approx_array[0])
    )
)
    # Compute the relative error
    total_error = 0.0
    count = 0
    for row1, row2 in zip(precise_array, approx_array):
        for val1, val2 in zip(row1, row2):
            if val2 >= 333 or val2 < 273 or math.isnan(val2):
                error = 1.0
            else:
                error = abs(val1 - val2) / 60
            total_error += error
            count += 1

    # Return the average relative error
    return total_error / count if count > 0 else float('nan')
    
def read_array(console_output):
    """
    Parse a 2D array of temperatures (in Kelvin) from the console output.

    Expected format:
        300.5 301.2 302.0
        299.8 300.1 300.9
        ...
    Lines containing non-numeric data will be ignored.
    """
    rows = console_output.strip().split("\n")
    numeric_rows = []
    
    for row in rows:
        # Use regex to find all floating-point numbers in the row
        numbers = re.findall(r'-?\d+\.\d+|NaN', row)
        
        if numbers:  # If there are numbers in the row
            try:
                # Convert the list of strings to floats
                numeric_row = [float(num) for num in numbers]
                numeric_rows.append(numeric_row)
            except ValueError:
                # Skip rows with non-numeric data
                continue
    
    return numeric_rows
