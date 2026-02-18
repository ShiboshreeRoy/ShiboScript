# ShiboScript Development Guide

## Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Development Setup](#development-setup)
4. [Testing](#testing)
5. [Building](#building)
6. [Packaging](#packaging)
7. [Release Process](#release-process)

## Overview

This document describes the development workflow for ShiboScript, a lightweight scripting language for education and automation.

## Project Structure

```
shiboscript_project/
├── bin/                    # Executable scripts
├── build/                  # Build artifacts
├── config/                 # Configuration files
│   ├── settings.ini        # Application settings
│   └── logging.conf        # Logging configuration
├── coverage/               # Coverage reports
├── docs/                   # Documentation files
├── examples/               # Example scripts
├── scripts/                # Build and deployment scripts
│   ├── build.sh            # Build script
│   ├── install.sh          # Installation script
│   ├── test.sh             # Test runner script
│   └── release.sh          # Release preparation script
├── src/                    # Source code
│   ├── cli/                # Command-line interface
│   │   └── __init__.py     # CLI entry point
│   ├── core/               # Core interpreter (if needed)
│   ├── stdlib/             # Standard library (if needed)
│   ├── shiboscript/        # Main package
│   │   ├── __init__.py     # Package definition
│   │   └── core.py         # Core interpreter implementation
│   └── utils/              # Utility functions (if needed)
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── tools/                  # Development tools
├── benchmark/              # Benchmarking code
├── dist/                   # Distribution artifacts
├── logs/                   # Log files
├── .gitignore             # Git ignore rules
├── LICENSE                # License information
├── Makefile               # Build automation
├── MANIFEST.in            # Package manifest
├── pyproject.toml         # Project configuration
├── README.md              # Project overview
├── requirements.txt       # Dependencies
└── setup.py               # Setup script
```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Initial Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ShiboShreeRoy/ShiboScript.git
   cd shiboscript_project
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # or
   venv\Scripts\activate     # On Windows
   ```

3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

### Development Commands

Using Make:
- `make install` - Install in development mode
- `make dev-install` - Install development dependencies
- `make test` - Run all tests
- `make test-unit` - Run unit tests
- `make lint` - Run code quality checks
- `make format` - Format code
- `make check` - Run type checking
- `make clean` - Clean build artifacts

## Testing

### Running Tests

Unit tests:
```bash
make test-unit
# or
python -m pytest tests/unit/
```

Integration tests:
```bash
python -m pytest tests/integration/
```

All tests:
```bash
make test
# or
python -m pytest tests/
```

### Test Structure

Tests are organized by type:
- `tests/unit/` - Unit tests for individual components
- `tests/integration/` - Integration tests for component interactions

### Adding Tests

1. Place new unit tests in `tests/unit/`
2. Place new integration tests in `tests/integration/`
3. Follow the naming convention `test_*.py`
4. Use descriptive test function names starting with `test_`

## Building

### Building the Package

```bash
python setup.py sdist bdist_wheel
```

Or using build:
```bash
pip install build
python -m build
```

### Building Documentation

```bash
make docs
```

## Packaging

### Creating Distribution

```bash
make clean
python -m build
```

Distribution files will be created in the `dist/` directory.

### Installing from Source

```bash
pip install .
```

For development:
```bash
pip install -e .
```

## Release Process

### Preparing a Release

1. Update version in `src/shiboscript/__init__.py`
2. Update version in `setup.py`
3. Update changelog
4. Run all tests: `make test`
5. Run quality checks: `make lint check`
6. Clean build: `make clean`
7. Build distribution: `python -m build`
8. Test installation from distribution
9. Tag the release in Git

### Versioning

We follow Semantic Versioning (SemVer):
- MAJOR.MINOR.PATCH
- MAJOR for incompatible API changes
- MINOR for backwards-compatible functionality
- PATCH for backwards-compatible bug fixes

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use Black for code formatting
- Use type hints where appropriate
- Write docstrings for all public functions/classes

### Testing Standards

- Aim for high test coverage
- Write both positive and negative test cases
- Keep tests isolated and deterministic
- Use descriptive test names

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Update documentation if needed
6. Run all tests
7. Submit a pull request

## Troubleshooting

### Common Issues

- **Import errors**: Make sure to install in development mode with `pip install -e .`
- **Missing dependencies**: Run `pip install -e ".[dev]"` to install all dependencies
- **Test failures**: Check that you're running tests from the project root directory

