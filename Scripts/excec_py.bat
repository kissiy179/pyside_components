@echo off

cd /d %~dp0
call ..\.venv\scripts\activate.bat
call python %1

@REM 管理者権限実行の場合ポーズする
openfiles > NUL 2>&1 

if %ERRORLEVEL%==0 pause
