.PHONY: help install dev-install test test-unit test-integration lint format check clean distclean docs benchmark release

# Default target
help:
@echo "ShiboScript - Professional Edition"
@echo ""
@echo "Usage:"
@echo "  make install          Install ShiboScript in development mode"
@echo "  make dev-install      Install development dependencies"
@echo "  make test             Run all tests"
@echo "  make test-unit        Run unit tests only"
@echo "  make test-integration Run integration tests only"
@echo "  make lint             Run code quality checks"
@echo "  make format           Format code with black"
@echo "  make check            Run type checking with mypy"
@echo "  make clean            Clean build artifacts"
@echo "  make distclean        Clean everything including dependencies"
@echo "  make docs             Build documentation"
@echo "  make benchmark        Run benchmarks"
@echo "  make release          Prepare release"

# Install in development mode
install:
pip install -e .

# Install development dependencies
dev-install:
pip install -e ".[dev]"

# Run all tests
test:
python -m pytest tests/

# Run unit tests
test-unit:
python -m pytest tests/unit/

# Run integration tests
test-integration:
python -m pytest tests/integration/

# Run linting
lint:
flake8 src/ tests/
pylint src/

# Format code
format:
black src/ tests/
isort src/ tests/

# Type checking
check:
mypy src/

# Clean build artifacts
clean:
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/
find . -type d -name __pycache__ -delete
find . -type f -name "*.pyc" -delete

# Clean everything
distclean: clean
rm -rf venv/
rm -rf .tox/
rm -rf .pytest_cache/
rm -rf .mypy_cache/

# Build documentation
docs:
@echo "Building documentation..."
@echo "Documentation would be built here in a real project"

# Run benchmarks
benchmark:
@echo "Running benchmarks..."
python -m benchmark.run

# Prepare release
release: clean test lint check
@echo "Preparing release..."
@echo "Version: $$(python -c 'import shiboscript; print(shiboscript.__version__)')"

# Run all checks
ci-checks: test lint check
@echo "All checks passed!"

# Install and run tests
ci: dev-install ci-checks
@echo "CI pipeline completed successfully!"
