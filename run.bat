@echo off
echo ========================================
echo   Healthline Clone Django Project
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Checking Django installation...
python -c "import django" >nul 2>&1
if errorlevel 1 (
    echo Django not found. Installing Django 2.1.7...
    pip install django==2.1.7 pillow
)

echo.
echo Running database migrations...
python manage.py migrate

echo.
echo Clearing all sessions (forcing re-login)...
python -c "from django.contrib.sessions.models import Session; Session.objects.all().delete(); print('All sessions cleared!')" 2>nul

echo.
echo Checking if articles need to be imported...
python -c "from core.models import Article; exit(0 if Article.objects.count() > 0 else 1)" >nul 2>&1
if errorlevel 1 (
    echo Importing articles from JSON...
    python manage.py import_articles
)

echo.
echo ========================================
echo   Starting Development Server
echo ========================================
echo.
echo   Local:   http://127.0.0.1:8000/
echo   Network: http://10.24.27.77:8000/
echo   Admin:   http://127.0.0.1:8000/admin/
echo   Sign Up: http://127.0.0.1:8000/signup/
echo.
echo   NOTE: All sessions have been cleared.
echo         You will need to login again.
echo.
echo   Mobile: Connect your phone to same WiFi
echo           Then open: http://10.24.27.77:8000/
echo.
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

python manage.py runserver 0.0.0.0:8000

pause
