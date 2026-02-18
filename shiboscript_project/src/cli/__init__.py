"""Command Line Interface for ShiboScript"""
import sys
import os
from shiboscript.core import run_file, repl

def main():
    """Main CLI entry point"""
    if len(sys.argv) > 1:
        # Check if it's a command
        command = sys.argv[1]
        
        if command == "repl":
            repl()
        elif command == "run":
            if len(sys.argv) > 2:
                run_file(sys.argv[2])
            else:
                print("Usage: shiboscript run <filename>")
        elif command == "version":
            print("ShiboScript v1.0.0")
        elif command == "help":
            print_help()
        elif command == "--version":
            print("ShiboScript v1.0.0")
        elif command == "--help":
            print_help()
        else:
            # Assume it's a filename
            if os.path.exists(command):
                run_file(command)
            else:
                print(f"File not found: {command}")
                print("Use 'shiboscript help' for usage information")
    else:
        repl()

def print_help():
    """Print help information"""
    help_text = """
ShiboScript - A lightweight scripting language

Usage:
    shiboscript                    # Start REPL
    shiboscript repl              # Start REPL
    shiboscript run <file>        # Run a .shibo file
    shiboscript <file>            # Run a .shibo file
    shiboscript version           # Show version
    shiboscript --version         # Show version
    shiboscript help              # Show this help
    shiboscript --help            # Show this help

Examples:
    shiboscript hello.shibo       # Run hello.shibo
    shiboscript                   # Start interactive mode
    
In REPL mode:
    Type 'exit' to quit
    Type 'help' to see available functions
    Type 'cls' or 'clear' to clear screen
    """
    print(help_text)

if __name__ == "__main__":
    main()
