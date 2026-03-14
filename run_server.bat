@echo off
REM AI Public Problem Reporter - Web Server Startup Script (Windows)

echo.
echo ========================================================
echo   AI PUBLIC PROBLEM REPORTER - WEB SERVER
echo ========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Flask not found. Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if port 5000 is available
echo Checking if port 5000 is available...
netstat -ano | findstr :5000 >nul 2>&1
if not errorlevel 1 (
    echo WARNING: Port 5000 is already in use
    echo You can try a different port or close the application using that port
    echo.
)

REM Start the server
echo.
echo Starting AI Public Problem Reporter Web Server...
echo.
echo ========================================================
echo   Opening URL: http://localhost:5000
echo ========================================================
echo.
echo Press Ctrl+C to stop the server
echo.

python server.py

pause
