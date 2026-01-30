@echo off
REM Zen Voice Assistant - Windows Startup Script
REM This script starts the Zen Voice Assistant automatically

echo ================================================
echo Starting Zen Voice Assistant...
echo ================================================

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.py first to create the virtual environment.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if activation was successful
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Start Zen Assistant
echo Starting Zen Assistant...
python main.py

REM If the program exits, pause to see any error messages
if errorlevel 1 (
    echo.
    echo Zen Assistant exited with an error.
    pause
)
