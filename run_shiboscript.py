#!/usr/bin/env python3
"""
ShiboScript Runner
A simple script to easily run ShiboScript REPL or execute .shibo files
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from shiboscript.core import repl, run_file
    
    def main():
        if len(sys.argv) > 1:
            # If a file is provided, run it
            filename = sys.argv[1]
            if os.path.exists(filename):
                print(f"Running {filename}...")
                run_file(filename)
            else:
                print(f"File not found: {filename}")
                print("Usage: python3 run_shiboscript.py [filename.shibo]")
                print("Or run without arguments to start REPL")
        else:
            # Otherwise, start the REPL
            print("Starting ShiboScript REPL...")
            print("Type 'exit' to quit, 'help' for help")
            repl()
            
except ImportError as e:
    print(f"Error importing ShiboScript: {e}")
    print("Make sure you're running this from the ShiboScript project directory")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)

if __name__ == "__main__":
    main()
