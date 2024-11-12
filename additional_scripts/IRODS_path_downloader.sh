#!/bin/bash
# Script that downloads files from the IRODS using
# the paths created by the IRODS_path_collector.sh script.
# The full paths are retrieved from a output CSV file and
# the iget command is used to download the files.
# 
# Files are downloaded in the current directory.
# For using: make sure to initialize the irods environment:
#     iinit
# 
# Author: Mark van de Streek
# GitHub-Organization: RIVM-Bioinformatics

# CSV file path
csv_file="secrid_path_to_file_output.csv"

# Read CSV file into a variable
csv_content=$(<"$csv_file")

# Define array to store paths
paths=()

# Loop through CSV content and extract paths
while IFS=',' read -r id path || [[ -n "$id" && -n "$path" ]]; do
    # Trim leading and trailing whitespace from path
    path=$(echo "$path" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    if [ -n "$path" ]; then
        paths+=("$path")
    fi
done <<< "$csv_content"

# Use iget command for each path
for path in "${paths[@]}"; do
    trimmed_path=$(echo "$path" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    echo "Searching for: $trimmed_path"
    iget -r -v "$trimmed_path"
done
