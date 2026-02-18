# ShiboScript Project Structure

This document describes the professional folder structure for the ShiboScript project.

## Directory Structure

```
ShiboScript/
├── src/                    # Source code
│   ├── __init__.py        # Package metadata
│   ├── shiboscript/       # Core interpreter package
│   │   ├── __init__.py    # Package init
│   │   └── core.py        # Main interpreter implementation
│   └── cli/               # Command line interface
│       └── __init__.py    # CLI entry point
├── examples/              # Example scripts
│   ├── hello.shibo        # Hello world example
│   ├── calculator.shibo   # Calculator example
│   ├── classes.shibo      # OOP example
│   └── ...                # Other examples
├── docs/                  # Documentation
│   ├── README.md          # Main documentation
│   └── technical_notes.txt # Technical details
├── tests/                 # Test files
│   └── test_basic.py      # Basic functionality tests
├── config/                # Configuration files
│   ├── LICENSE            # License file
│   └── shiboscript.ico    # Icon file
├── build/                 # Build artifacts
├── dist_new/              # Distribution packages
├── setup.py              # Installation script
├── requirements.txt      # Dependencies
├── Makefile              # Build commands
├── .gitignore            # Git ignore rules
└── PROJECT_STRUCTURE.md  # This file
```

## Key Components

### Source Code (`src/`)
- **`shiboscript/core.py`**: Contains the main interpreter, lexer, parser, and AST nodes
- **`cli/__init__.py`**: Command line interface with main entry point

### Development Tools
- **`setup.py`**: Standard Python package setup script
- **`requirements.txt`**: Project dependencies
- **`Makefile`**: Common development commands
- **`tests/`**: Unit tests for verification

### Documentation
- **`README.md`**: Main project documentation
- **`docs/`**: Additional documentation files
- **`examples/`**: Example scripts demonstrating language features

### Build & Distribution
- **`build/`**: Build artifacts
- **`dist_new/`**: Distribution packages
- **`.gitignore`**: Git exclusion rules

## Installation

```bash
# Install in development mode
pip install -e .

# Or use make
make install
```

## Usage

```bash
# Start REPL
shiboscript

# Run a script
shiboscript examples/hello.shibo

# Run tests
make test
```

## Development Commands

```bash
make help          # Show available commands
make install       # Install package
make test          # Run tests
make dev           # Install and start REPL
make examples      # Run all examples
make clean         # Clean build artifacts
```

This structure follows Python packaging best practices and provides a professional, maintainable codebase suitable for production use.