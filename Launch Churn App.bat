@echo off
title Customer Churn Analyzer
color 0A
echo ==========================================
echo    Customer Churn Analysis Project
echo ==========================================
echo.
echo Starting Flask server...
echo.

cd /d "C:\Users\shash\Customer Churn Analysis Project"

REM Open browser in a separate window after 5 seconds
start /B cmd /C "timeout /t 5 /nobreak >nul && start chrome http://127.0.0.1:5000"

REM Start Flask (this stays running in foreground)
"C:\Users\shash\AppData\Local\Programs\Python\Python311\python.exe" churn_app.py