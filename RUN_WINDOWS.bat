@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo [1/5] Creating Python environment...
if not exist .venv\Scripts\python.exe py -m venv .venv
if errorlevel 1 goto error
echo [2/5] Installing requirements...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error
echo [3/5] Applying Django ORM migrations...
.venv\Scripts\python.exe manage.py migrate
if errorlevel 1 goto error
echo [4/5] Importing PR7 data through ORM...
.venv\Scripts\python.exe manage.py import_pr7
if errorlevel 1 goto error
echo [5/5] Checking Django configuration...
.venv\Scripts\python.exe manage.py check
if errorlevel 1 goto error
echo.
echo Open http://127.0.0.1:8000/
.venv\Scripts\python.exe manage.py runserver
pause
exit /b 0
:error
echo Setup failed. Check the message above and make sure Python and Internet are available.
pause
exit /b 1
