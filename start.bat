@echo off
title SkillMatch AI - Resume & Skill Gap Matcher
color 0A
echo.
echo  =========================================
echo   SkillMatch AI - Starting Server...
echo  =========================================
echo.

cd /d "%~dp0"

echo  YOUR LOCAL URL:   http://127.0.0.1:5000
echo.
echo  SHARE WITH FRIENDS ON SAME WIFI:
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :found
)
:found
set IP=%IP: =%
echo   http://%IP%:5000
echo.
echo  Tell your friend to open that URL in their browser.
echo  Make sure you are both on the SAME WiFi network.
echo.
echo  Press CTRL+C to stop the server.
echo  =========================================
echo.

start "" "http://127.0.0.1:5000"
python app.py

pause
