@echo off
setlocal
cd /d "%~dp0"
uv run uvicorn model:app --host 127.0.0.1 --port 8001 --reload