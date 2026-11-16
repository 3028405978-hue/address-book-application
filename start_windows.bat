@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
    python -m venv .venv
    if errorlevel 1 goto error
)
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error
echo Open http://127.0.0.1:5000 in your browser.
.venv\Scripts\python.exe app.py
if errorlevel 1 goto error
exit /b 0
:error
echo Startup failed. Check Python 3.11+ and your network connection.
pause
exit /b 1
