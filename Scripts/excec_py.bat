@echo off

cd %~dp0
call ..\.venv\scripts\activate.bat
call python %1
pause