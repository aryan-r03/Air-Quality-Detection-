@echo off
REM Air Quality Prediction App - Startup Script for Windows

echo ==================================
echo Air Quality Prediction System
echo ==================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet

REM Run the application
echo.
echo Starting Flask application...
echo.
python app.py

pause
