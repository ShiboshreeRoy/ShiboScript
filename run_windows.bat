@echo off
echo.
echo =================================
echo ShiboScript Runner (No Installation)
echo =================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Install dependencies if not already installed
echo Installing dependencies...
pip install -r requirements.txt

REM Run ShiboScript
if "%1"=="" (
    REM No arguments - start REPL
    echo Starting ShiboScript REPL...
    python run_shiboscript.py
) else (
    REM Run the provided script
    echo Running %1...
    python run_shiboscript.py %1
)

pause