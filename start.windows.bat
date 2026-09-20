@echo off
REM Start the PHREEQC Workbench backend + open the frontend in a browser.
REM
REM This is the root-directory launcher (equivalent to workbench\start.windows.bat
REM but invoked directly from the repo root).
REM
REM Tested on:
REM     - Windows 10 / 11  (cmd.exe, Windows Terminal)
REM
REM Usage:
REM     start.windows.bat                   REM default port 8765
REM     start.windows.bat 8780              REM custom port
REM     set PORT=8780 ^&^& start.windows.bat REM via env var

setlocal
set "PORT=%1"
if "%PORT%"=="" set "PORT=8765"
set "HOST=127.0.0.1"

set "ROOT=%~dp0"
pushd "%ROOT%" >nul

set "PYTHONIOENCODING=utf-8"

REM Prefer the project's venv if present.
set "PY="
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"
if "%PY%"=="" set "PY=python"

echo [workbench] Python:    %PY%
echo [workbench] Project:   %ROOT%
echo [workbench] Frontend:  http://%HOST%:%PORT%/

REM Do not launch a second copy on the same port.  Python's HTTP server can
REM otherwise share the listener with an old process, making the browser hit
REM a random (possibly stale) Workbench instance.
powershell -NoProfile -Command "if (Get-NetTCPConnection -LocalAddress '%HOST%' -LocalPort %PORT% -State Listen -ErrorAction SilentlyContinue) { exit 0 }; exit 1" >nul 2>&1
if not errorlevel 1 (
  echo [workbench] An instance is already running on this port; opening it in the browser.
  start "" "http://%HOST%:%PORT%/" >nul 2>&1
  popd >nul
  endlocal & exit /b 0
)

REM Best-effort browser launch for a newly-started server.
start "" "http://%HOST%:%PORT%/" >nul 2>&1

"%PY%" "%ROOT%\workbench\backend\app.py" --host %HOST% --port %PORT%
set "EC=%ERRORLEVEL%"

popd >nul
endlocal & exit /b %EC%
