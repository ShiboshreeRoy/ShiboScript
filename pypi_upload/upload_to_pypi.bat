@echo off
echo Preparing ShiboScript for PyPI upload...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Install build tools
echo Installing build tools...
pip install --upgrade build twine

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"

REM Build the package
echo Building the package...
python -m build

REM Check the built packages
echo Checking the built packages...
twine check dist/*

REM Ask for confirmation before upload
echo.
echo Package built successfully!
echo Files created:
dir dist\
echo.
set /p CONFIRM=Do you want to upload to PyPI? (y/N): 
if /i "%CONFIRM%"=="y" (
    echo Uploading to PyPI...
    twine upload dist/*
    echo Upload completed!
) else (
    echo Upload cancelled. Files are available in dist/ directory.
    echo To upload manually, run: twine upload dist/*
)

echo Process completed!
