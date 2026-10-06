@echo off
chcp 65001 >nul
cd /d "%~dp0.."

rem Stage 2 test: pass both supported command-line parameters.
rem --vfs     - physical VFS location.
rem --startup - startup script location.

python src\main.py --vfs "data\vfs" --startup "scripts\startup.txt"

if errorlevel 1 (
    echo Emulator finished with an error.
    pause
    exit /b 1
)

echo Emulator finished successfully.
pause