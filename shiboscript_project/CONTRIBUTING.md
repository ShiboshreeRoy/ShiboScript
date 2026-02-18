# Contributing to ShiboScript

Thank you for your interest in contributing to ShiboScript! This document outlines the process for contributing code, reporting issues, and participating in the community.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Pull Request Process](#pull-request-process)
6. [Issue Reporting](#issue-reporting)
7. [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [contact email].

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip package manager

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ShiboScript.git
   cd shiboscript_project
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # or
   venv\Scripts\activate     # On Windows
   ```

4. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

5. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Making Changes

1. Make sure your branch is up to date:
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/your-feature-name
   git rebase main
   ```

2. Make your changes in the appropriate files

3. Add tests for your changes if applicable

4. Run the test suite to ensure your changes don't break existing functionality:
   ```bash
   make test
   ```

5. Run code quality checks:
   ```bash
   make lint
   make check
   ```

6. Format your code:
   ```bash
   make format
   ```

7. Commit your changes with a clear, descriptive commit message

### Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting
- Aim for high test coverage
- Test both positive and negative cases

### Documentation

- Update documentation for any new features or changes
- Include docstrings for public functions and classes
- Update README.md if necessary

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use Black for code formatting (enforced via CI)
- Use type hints for all function signatures
- Write clear, descriptive variable and function names
- Keep functions focused and small when possible

### Testing

- Write tests using pytest
- Follow the arrange-act-assert pattern
- Use descriptive test function names
- Test edge cases and error conditions

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

## Pull Request Process

1. Ensure your branch is up to date with the main branch
2. Run all tests and code quality checks
3. Squash commits if necessary to create a clean history
4. Open a pull request to the main branch
5. Fill out the pull request template completely
6. Link any related issues
7. Wait for reviews and address feedback
8. Your PR will be merged after approval

### Pull Request Template

When creating a pull request, please follow this template:

```
## Description
Brief description of changes made

## Related Issue
Fixes # (issue number)

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New functionality tested
- [ ] Existing functionality still works

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
```

## Issue Reporting

### Bug Reports

When reporting a bug, please include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Python version
- Operating system
- Any relevant error messages or logs

### Feature Requests

When requesting a new feature, please include:

- A clear, descriptive title
- A detailed description of the proposed feature
- Why this feature would be useful
- Any alternatives you've considered

## Community

- Join our discussions on GitHub Issues
- Feel free to ask questions in pull requests
- Be respectful and constructive in all interactions

## Questions?

If you have questions that aren't covered in this document, feel free to open an issue with the "question" label.

Thank you for contributing to ShiboScript!
