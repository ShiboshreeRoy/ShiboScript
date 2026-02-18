#!/bin/bash

# Script to prepare and upload ShiboScript to PyPI
set -e  # Exit on any error

echo "Preparing ShiboScript for PyPI upload..."

# Check if we have the required tools
if ! command -v python &>/dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

if ! command -v pip &>/dev/null; then
    echo "Error: Pip is not installed or not in PATH"
    exit 1
fi

# Install build tools
echo "Installing build tools..."
pip install --upgrade build twine

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/ || true

# Build the package
echo "Building the package..."
python -m build

# Check the built packages
echo "Checking the built packages..."
twine check dist/*

# Ask for confirmation before upload
echo
echo "Package built successfully!"
echo "Files created:"
ls -la dist/
echo
read -p "Do you want to upload to PyPI? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Uploading to PyPI..."
    twine upload dist/*
    echo "Upload completed!"
else
    echo "Upload cancelled. Files are available in dist/ directory."
    echo "To upload manually, run: twine upload dist/*"
fi

echo "Process completed!"
