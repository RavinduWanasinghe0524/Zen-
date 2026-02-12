@echo off
REM Zen Voice Assistant - High Performance (PySide6) Startup
echo ================================================
echo Starting Zen High-Performance Interface...
echo ================================================

cd /d "%~dp0"

REM Activate Virtual Environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run setup.py/install dependencies first.
    pause
    exit /b 1
)

REM Start the PySide6 Application
python main_qt.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Zen exited with an error.
    pause
)
