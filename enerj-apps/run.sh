#!/bin/bash

# Get the current date in the desired format
DATE=$(date +"%d.%m.%Y")

# Inform the user that measurements are starting
echo "Starting measurements..."
echo "This may take some time. Please wait."

# Run the Python script and capture both stdout and stderr in output.txt
python2.7 collect.py > output.txt 2>&1

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo "Measurements completed successfully!"
else
    echo "An error occurred during the measurements. Check output.txt for details."
    exit 1
fi

# Inform the user about the results
echo "Output is in output.txt."
echo "Measurement results are in results.json."

# Provide instructions for copying the results to the host machine
echo "To copy the results.json to the host machine, run the following command on the host machine:"
echo "mkdir -p measurement_results/$DATE/ && docker cp ctcs05:/CTCS_05/enerj-apps/results.json measurement_results/$DATE/"

# Suggest checking the output
echo "You can check the output file (output.txt) for logs or errors."
