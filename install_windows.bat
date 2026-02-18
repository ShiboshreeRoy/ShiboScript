@echo off
echo.
echo ================================
echo ShiboScript Installer for Windows
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is not available. Installing pip...
    python -m ensurepip --upgrade
    if errorlevel 1 (
        echo Failed to install pip.
        pause
        exit /b 1
    )
)

echo Installing ShiboScript dependencies...
pip install -r requirements.txt

echo Installing ShiboScript globally...
pip install -e .

echo.
echo ================================
echo ShiboScript Installation Complete!
echo ================================
echo.
echo You can now use ShiboScript with these commands:
echo.
echo   shiboscript          - Start the REPL
echo   shiboscript file.shibo  - Run a script
echo   shiboc               - Use the compiler
echo.
echo Example: shiboscript hello_world.shibo
echo.
pause