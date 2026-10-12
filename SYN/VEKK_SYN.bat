@echo off
cd /d D:\AI-Agent
start "SYN Agent" cmd /k python agent.py
timeout /t 2 /nobreak >nul
start "SYN Web" cmd /k python web_agent.py
exit
