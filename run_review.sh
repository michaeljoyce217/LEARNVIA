#!/bin/bash
# Wrapper script for run_review.py with new directory structure

if [ $# -lt 2 ]; then
    echo "Usage: ./run_review.sh <module_name> <xml_file>"
    echo "Example: ./run_review.sh Power_Series power_series_original.xml"
    exit 1
fi

MODULE_NAME=$1
XML_FILE=$2

# Check if module exists in test directory
if [ ! -d "modules/test/$MODULE_NAME" ]; then
    echo "Error: Module not found: modules/test/$MODULE_NAME"
    exit 1
fi

# Create symlink in Testing directory for backward compatibility
if [ ! -L "Testing/$MODULE_NAME" ]; then
    ln -s "../modules/test/$MODULE_NAME" "Testing/$MODULE_NAME"
fi

# Run the review
cd Testing
python run_review.py "$MODULE_NAME" "$XML_FILE"

# Clean up symlink
rm -f "$MODULE_NAME"