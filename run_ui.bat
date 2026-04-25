@echo off
echo.
echo  ============================================
echo   Agentic AI Researcher - Starting UI
echo  ============================================

:: Kill anything already on port 8502
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8502 " 2^>nul') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo  UI will open at: http://localhost:8502
echo  (Groq API key loaded from .env)
echo.

cd /d "%~dp0"
set PYTHONPATH=%~dp0
streamlit run ui/app.py --server.port 8502
pause
