@echo off
echo.
echo  ============================================
echo   Agentic AI Researcher - Starting UI
echo  ============================================
echo.
echo  UI will open at: http://localhost:8502
echo  (Requires GROQ_API_KEY in .env file)
echo.
cd /d "%~dp0"
set PYTHONPATH=%~dp0
streamlit run ui/app.py --server.port 8502
pause
