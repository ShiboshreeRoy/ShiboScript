#!/bin/bash

echo
echo "================================"
echo "ShiboScript Installer for Linux"
echo "================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH."
    echo "Please install Python 3.8+:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "pip is not available. Installing pip..."
    python3 -m ensurepip --upgrade
    if [ $? -ne 0 ]; then
        echo "Failed to install pip."
        exit 1
    fi
fi

echo "Installing ShiboScript dependencies..."
pip3 install -r requirements.txt

echo "Installing ShiboScript globally..."
pip3 install -e .

# Make the shiboc executable available in PATH
echo "Creating symbolic link for shiboc command..."
sudo ln -sf $(pwd)/shiboc /usr/local/bin/shiboc 2>/dev/null || echo "Could not create system-wide symlink. You may need to add $(pwd) to your PATH."

echo
echo "================================"
echo "ShiboScript Installation Complete!"
echo "================================"
echo
echo "You can now use ShiboScript with these commands:"
echo
echo "  shiboscript          - Start the REPL"
echo "  shiboscript file.shibo  - Run a script"
echo "  shiboc               - Use the compiler"
echo
echo "Example: shiboscript hello_world.shibo"
echo