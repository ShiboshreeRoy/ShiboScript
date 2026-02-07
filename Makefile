# Makefile for ShiboScript

.PHONY: install test clean build docs

# Install the package in development mode
install:
	pip install -e .

# Run tests
test:
	python -m pytest tests/ -v

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

# Build distribution packages
build:
	python setup.py sdist bdist_wheel

# Install in development mode and run REPL
dev:
	pip install -e .
	shiboscript

# Run a specific example
example/%:
	shiboscript examples/$*.shibo

# Run all examples
examples:
	shiboscript examples/hello.shibo
	shiboscript examples/calculator.shibo
	shiboscript examples/classes.shibo

# Show help
help:
	@echo "Available commands:"
	@echo "  make install     - Install package in development mode"
	@echo "  make test        - Run tests"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make build       - Build distribution packages"
	@echo "  make dev         - Install and run REPL"
	@echo "  make examples    - Run all example scripts"
	@echo "  make example/%   - Run specific example (e.g., make example/hello)"