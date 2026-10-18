@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo [1/4] Creating local Python environment...
if not exist .venv\Scripts\python.exe py -m venv .venv
if errorlevel 1 goto error
echo [2/4] Installing Django and tests...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error
echo [3/4] Applying Django's system migrations...
.venv\Scripts\python.exe manage.py migrate
if errorlevel 1 goto error
echo [4/4] Checking configuration...
.venv\Scripts\python.exe manage.py check
if errorlevel 1 goto error
echo.
echo Open in browser: http://127.0.0.1:8000/
echo Starting Django development server...
.venv\Scripts\python.exe manage.py runserver
pause
exit /b 0
:error
echo.
echo Setup failed. Check the error above and make sure Python 3.12+ and Internet are available.
pause
exit /b 1
