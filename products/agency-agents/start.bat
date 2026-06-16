@echo off
echo ========================================================
echo        AGENCY AGENTS: DIGITAL FACTORY EDITION
echo ========================================================
echo.
echo [1] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python from python.org and try again.
    pause
    exit /b
)

echo [2] Installing necessary libraries (Streamlit)...
pip install -r requirements.txt >nul 2>&1

echo [3] Launching the Explorer...
echo The app will open in your browser shortly.
echo.
streamlit run app.py
pause
