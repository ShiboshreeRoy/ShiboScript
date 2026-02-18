#!/bin/bash

echo
echo "================================="
echo "ShiboScript Runner (No Installation)"
echo "================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH."
    echo "Please install Python 3.8+"
    exit 1
fi

# Install dependencies if not already installed
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Run ShiboScript
if [ $# -eq 0 ]; then
    # No arguments - start REPL
    echo "Starting ShiboScript REPL..."
    python3 run_shiboscript.py
else
    # Run the provided script
    echo "Running $1..."
    python3 run_shiboscript.py "$1"
fi