import re

# The creation of this script used Chat-GPT as a coding assistant.

def calc_error(precise_output, approx_output):
    # Parse arrays from the console output
    precise_output = read_array(precise_output)
    approx_output = read_array(approx_output)

    # Ensure both outputs have the same length
    if len(precise_output) != len(approx_output):
        return 1.0  # Maximum error if lengths differ

    # Calculate pixel-by-pixel error
    total_error = 0.0
    num_pixels = len(precise_output)
    for precise_pixel, approx_pixel in zip(precise_output, approx_output):
        # Each pixel is an [R, G, B] array
        pixel_error = sum(abs(p - a) / 255.0 for p, a in zip(precise_pixel, approx_pixel)) / 3.0
        total_error += pixel_error

    # Normalize error by the number of pixels
    error = total_error / num_pixels
    return error

def read_array(console_output):
    """
    Parse an array of [R, G, B] pixel values from the console output.

    Expected format:
        (255, 0, 0) (0, 255, 0) (0, 0, 255)
        (10, 20, 30) (40, 50, 60) ...
    """
    pixel_regex = r'\((\d+),\s*(\d+),\s*(\d+)\)'
    matches = re.findall(pixel_regex, console_output)
    return [[int(r), int(g), int(b)] for r, g, b in matches]
