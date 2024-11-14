#!/bin/bash
# Script that loops over a set of sample numbers and
# searches the IRODS server for associated files.
# 
# The associated files are placed in a output CSV file 
# with full path to the project.
# 
# The script also logs any errors to a separate error log file.
# 
# Author: Mark van de Streek
# GitHub-Organization: RIVM-Bioinformatics

# Enable error checking
set -eu

csv_file="secrid_path_to_file.csv"

# Output file
output_file="secrid_path_to_file_output.csv"
error_log="secrid_path_to_file_error.log"

# Remove output file if it exists
if [ -f "$output_file" ]; then
    echo "Removing existing output file: $output_file"
    rm "$output_file"
fi

# Step 1: Extract values from the first column of the CSV file
echo "Step 1: Extracting values from the first column of the CSV file"
column_values=$(awk -F ',' '{print $1}' "$csv_file")
echo "Column values:"
echo "$column_values"

# Step 2: Split the column_values into an array
echo "Step 2: Splitting column_values into an array"
mapfile -t values_array <<< "$column_values"
echo "Values in the array:"
for value in "${values_array[@]}"; do
    echo "$value"
done

# Step 4: Loop over each value and execute iquest command
echo "Step 4: Looping over each value and executing iquest command"
for value in "${values_array[@]}"; do
    # Remove leading and trailing whitespace from the current value
    value=$(echo "$value" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    
    # Print the current value
    echo "Current value: $value"
    
    # Construct and execute the iquest command for both fastq.gz and fasta files
    for extension in "fastq.gz" "fasta"; do
        iquest_command="iquest \"%s/%s\" \"SELECT COLL_NAME, DATA_NAME WHERE DATA_NAME LIKE '%$value%.$extension'\""
        # Echo the constructed iquest command
        echo "Running iquest command for value: $value and extension: $extension"
        echo "Command: $iquest_command"
        
        # Execute the iquest command
        eval "$iquest_command" | awk -v val="$value" '{print val "," $0}' >> "$output_file" 2>> "$error_log"
    done
done