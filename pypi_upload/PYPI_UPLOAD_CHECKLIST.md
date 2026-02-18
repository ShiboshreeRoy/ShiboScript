# PyPI Upload Checklist

## Pre-Upload Checklist

### Repository Structure
- [x] `setup.py` with proper metadata
- [x] `pyproject.toml` for modern Python packaging
- [x] `README.md` with comprehensive documentation
- [x] `LICENSE` file included
- [x] `HISTORY.md` or `CHANGELOG.md` file
- [x] `AUTHORS.md` file
- [x] `MANIFEST.in` for including/excluding files
- [x] `.gitignore` file
- [x] Proper source code structure (`src/` layout)

### Package Metadata
- [x] Package name follows PyPI conventions
- [x] Version number follows semantic versioning
- [x] Author and email information
- [x] Proper description and long description
- [x] Keywords and classifiers
- [x] Python version requirements
- [x] Dependencies listed correctly

### Code Quality
- [x] Code passes linting (flake8, pylint)
- [x] Type hints added where appropriate
- [x] Tests cover major functionality
- [x] Documentation is comprehensive
- [x] Examples provided
- [x] Entry points configured for console scripts

### Legal Compliance
- [x] License file included
- [x] Copyright notices
- [x] Third-party licenses (if applicable)
- [x] Code of Conduct
- [x] Security Policy

### Build and Distribution
- [x] Can build source distribution (`python setup.py sdist`)
- [x] Can build wheel distribution (`python setup.py bdist_wheel`)
- [x] Can install locally (`pip install .`)
- [x] Entry points work correctly
- [x] All necessary files included in distribution

### Testing
- [x] Tests pass locally
- [x] Tests pass in CI (GitHub Actions)
- [x] Code coverage is adequate
- [x] Integration tests pass

## Upload Steps

### 1. Prepare the Release
```bash
# Update version in setup.py and __init__.py
# Update CHANGELOG.md
# Commit and tag the release
git add .
git commit -m "Prepare release v1.0.0"
git tag -a v1.0.0 -m "Version 1.0.0"
```

### 2. Build Distribution Packages
```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Install build tools
pip install build twine

# Build the packages
python -m build
```

### 3. Check Distribution Files
```bash
# Check the built packages
twine check dist/*
```

### 4. Upload to Test PyPI (Optional but Recommended)
```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*
```

### 5. Install from Test PyPI to Verify
```bash
pip install --index-url https://test.pypi.org/simple/ shiboscript-pro
```

### 6. Upload to PyPI
```bash
# Upload to PyPI
twine upload dist/*
```

## Post-Upload Verification

### 1. Check PyPI Page
- [ ] Package page displays correctly
- [ ] Description renders properly
- [ ] Metadata is correct
- [ ] Download files are available

### 2. Install Fresh Copy
```bash
# Create fresh environment and install
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate
pip install shiboscript-pro
```

### 3. Test Installation
- [ ] Package installs correctly
- [ ] Import works: `import shiboscript`
- [ ] Console scripts work: `shiboscript --version`
- [ ] All functionality works as expected

## Troubleshooting Common Issues

### Invalid Distribution Format
- Ensure `build` tool is used instead of `setup.py`
- Check that `pyproject.toml` is properly formatted

### Missing Files
- Verify `MANIFEST.in` includes necessary files
- Check that `package_data` in `setup.py` is correct

### Rendering Issues
- Ensure README.md uses supported Markdown syntax
- Test rendering with `twine check`

### Name Availability
- Check that package name is available on PyPI
- Consider alternative names if taken

## Additional Resources

- [PyPA's guide to packaging Python projects](https://packaging.python.org/tutorials/packaging-projects/)
- [PyPI's help page](https://pypi.org/help/)
- [Twine documentation](https://twine.readthedocs.io/)

## Security Considerations

- [ ] Store API tokens securely (never commit to repo)
- [ ] Use trusted publishing when possible
- [ ] Maintain secure development practices
- [ ] Monitor for security vulnerabilities
