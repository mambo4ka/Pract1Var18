@echo off
chcp 65001 >nul
cd /d "%~dp0.."

rem Second Windows OS script for Stage 2.
rem This script also tests BOTH command-line parameters.

python src\main.py --vfs "%CD%\data\vfs" --startup "%CD%\scripts\startup_alt.txt"

if errorlevel 1 (
    echo Emulator finished with an error.
    pause
    exit /b 1
)

echo Emulator finished successfully.
pause