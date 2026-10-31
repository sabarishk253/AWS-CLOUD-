@echo off
title EduCloud - AI Student Document & Assignment Management System
cd /d "%~dp0"

echo ======================================================================
echo          EduCloud: Academic Document & Assignment Platform
echo ======================================================================
echo.

:: 1. Check Python virtual environment
if not exist "backend\.venv\Scripts\python.exe" (
    echo [1/4] Setting up Python virtual environment...
    python -m venv backend\.venv
    echo Installing backend dependencies...
    backend\.venv\Scripts\pip.exe install -r backend\requirements.txt
) else (
    echo [1/4] Python virtual environment verified.
)

:: 2. Ensure database is initialized & seeded
if not exist "backend\data\educloud.db" (
    echo [2/4] Database not found. Initializing and seeding demo records...
    backend\.venv\Scripts\python.exe backend\seed.py
) else (
    echo [2/4] SQLite database detected.
)

:: 3. Ensure frontend production bundle exists
if not exist "frontend\dist\index.html" (
    echo [3/4] Building frontend static bundle...
    cd frontend && cmd /c npm.cmd run build && cd ..
) else (
    echo [3/4] Frontend bundle verified.
)

:: 4. Start EduCloud unified server
echo [4/4] Starting EduCloud Unified Server on http://127.0.0.1:8000...
echo.
echo ======================================================================
echo  EduCloud is running!
echo  URL: http://127.0.0.1:8000
echo  API Documentation: http://127.0.0.1:8000/docs
echo.
echo  Demo Credentials:
echo   - Administrator:    admin@educloud.local / Admin@123456
echo   - Senior Faculty:   prof.sharma@educloud.local / Teacher@123456
echo   - New Faculty:      prof.roy@educloud.local / Teacher@123456
echo   - Student:          rahul.verma@educloud.local / Student@123456
echo   - Student (AI/ML):  rohan.gupta@educloud.local / Student@123456
echo.
echo  Key Features:
echo   - Individual Role Portals (Student, Faculty, Admin)
echo   - Manual Online Assignment Submission & AI Pre-Check
echo   - Dedicated New Teacher Monitoring & Workload Supervision
echo   - Interactive AI Document Intelligence Studio
echo.
echo  Press Ctrl+C in this window to stop the server at any time.
echo ======================================================================
echo.

:: Launch browser in background after short delay
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:8000"

:: Start Uvicorn
backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
