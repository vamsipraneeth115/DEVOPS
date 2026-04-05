@echo off
REM Disease Prediction System - Setup Script (Windows)
REM This script automates the complete setup process

setlocal enabledelayedexpansion

color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║ Disease Prediction System - Setup Script              ║
echo ║              Windows Batch Version                    ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check Python version
echo [1] Checking Python version...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo ✓ Python found
echo.

REM Create virtual environment
echo [2] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo ✓ Virtual environment created
)
echo.

REM Activate virtual environment
echo [3] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Upgrade pip
echo [4] Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo ✓ pip upgraded
echo.

REM Install dependencies
echo [5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Check data files
echo [6] Checking data files...
if exist "data\Training.csv" if exist "data\Testing.csv" (
    echo ✓ Data files found
    for /f %%A in ('find /c /v "" ^< data\Training.csv') do echo   - Training samples: %%A
    for /f %%A in ('find /c /v "" ^< data\Testing.csv') do echo   - Testing samples: %%A
) else (
    echo ✗ Data files not found
    echo   Please copy Training.csv and Testing.csv to the 'data' directory
    echo   Current contents of data\:
    if exist data (
        dir data
    ) else (
        echo   (data directory not found)
    )
)
echo.

REM Create directories
echo [7] Creating necessary directories...
if not exist data mkdir data
if not exist logs mkdir logs
echo ✓ Directories created
echo.

REM Display next steps
echo ════════════════════════════════════════════════════════
echo NEXT STEPS:
echo ════════════════════════════════════════════════════════
echo.
echo 1. Ensure data files are in place:
echo    copy "C:\path\to\Training.csv" data\
echo    copy "C:\path\to\Testing.csv" data\
echo.
echo 2. Train the machine learning model:
echo    python train.py
echo.
echo 3. Run the Streamlit application:
echo    streamlit run app.py
echo.
echo 4. Build Docker image:
echo    docker build -t disease-predictor:latest .
echo.
echo 5. Run with Docker Compose:
echo    docker-compose up -d
echo.
echo ════════════════════════════════════════════════════════
echo.
echo Setup completed successfully!
echo Press any key to continue...
pause >nul
