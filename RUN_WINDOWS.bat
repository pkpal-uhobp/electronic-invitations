@echo off
chcp 65001 >nul
cd /d "%~dp0"
set DJANGO_DEBUG=1
set DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,testserver

echo [1/5] Preparing environment...
if not exist .venv\Scripts\python.exe py -m venv .venv
if errorlevel 1 goto error
echo [2/5] Installing requirements...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error
echo [3/5] Applying migrations, preserving existing db.sqlite3...
.venv\Scripts\python.exe manage.py migrate
if errorlevel 1 goto error
echo [4/5] Importing PR7 data ONLY if ORM events table is empty...
.venv\Scripts\python.exe manage.py import_pr7_if_empty
if errorlevel 1 goto error
echo [5/5] Django checks...
.venv\Scripts\python.exe manage.py check
if errorlevel 1 goto error
echo.
echo Website: http://127.0.0.1:8000/
echo Admin: http://127.0.0.1:8000/admin/
echo SQL debug toolbar is enabled in development.
echo Create your admin user once with: .venv\Scripts\python.exe manage.py createsuperuser
.venv\Scripts\python.exe manage.py runserver
pause
exit /b 0
:error
echo An error occurred. Check the message above.
pause
exit /b 1
