# ShiboScript Installation Guide

## Quick Installation

### For Windows
1. Download and install Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Open Command Prompt as Administrator
3. Navigate to the ShiboScript directory
4. Run: `install_windows.bat`

### For Linux/MacOS
1. Ensure Python 3.8+ is installed:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3 python3-pip
   
   # CentOS/RHEL
   sudo yum install python3 python3-pip
   
   # Fedora
   sudo dnf install python3 python3-pip
   ```
2. Navigate to the ShiboScript directory
3. Run: `./install_linux.sh`

## Manual Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps
1. Clone or download the ShiboScript repository
2. Navigate to the ShiboScript directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install ShiboScript:
   ```bash
   pip install -e .
   ```

## Verification

After installation, verify that ShiboScript is working:

```bash
# Start the interactive REPL
shiboscript

# Run a sample script
shiboscript hello_world.shibo

# Use the compiler
shiboc -c hello_world.shibo
shiboc -r hello_world.shibo
```

## Troubleshooting

### Common Issues

1. **Command not found**: If `shiboscript` or `shiboc` commands are not found, try adding the installation directory to your PATH, or use the runner script:
   ```bash
   python3 run_shiboscript.py
   ```

2. **Permission errors**: On Linux, you may need to run with sudo for global installation, or install in user mode:
   ```bash
   pip install --user -e .
   ```

3. **Missing dependencies**: If you encounter import errors, ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

## Uninstallation

To uninstall ShiboScript:
```bash
pip uninstall shiboscript
```

## Platform-Specific Notes

### Windows
- The installer creates shortcuts for easy access
- Make sure to run the installer as Administrator for global installation
- If you encounter issues, try installing in a virtual environment

### Linux
- The installer attempts to create system-wide symlinks
- If symlinks fail, add the ShiboScript directory to your PATH manually
- You can run without global installation using the run script

## Virtual Environment (Recommended)

For isolated installation, use a virtual environment:

```bash
# Create virtual environment
python3 -m venv shiboscript-env

# Activate (Linux/MacOS)
source shiboscript-env/bin/activate

# Activate (Windows)
shiboscript-env\Scripts\activate

# Install ShiboScript
pip install -r requirements.txt
pip install -e .
```

Enjoy using ShiboScript!