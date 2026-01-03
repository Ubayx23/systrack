@echo off
REM SysTrack Setup Script for Windows
REM This script sets up a virtual environment and installs dependencies

echo SysTrack Setup Script
echo ====================
echo.

REM Check if Python 3 is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3 first.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ==========================================
echo Setup complete!
echo ==========================================
echo.
echo To use SysTrack:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate
echo.
echo   2. Run SysTrack:
echo      python src\systrack.py --summary
echo.
echo   3. When done, deactivate:
echo      deactivate
echo.

pause

