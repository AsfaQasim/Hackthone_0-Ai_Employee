@echo off
REM Facebook Auto Post - Quick Launcher

echo ======================================================================
echo   FACEBOOK AUTO POST
echo ======================================================================
echo.
echo This script will post a message to your Facebook page.
echo.

set /p message="Enter your message: "

if "%message%"=="" (
    echo.
    echo ❌ No message provided
    pause
    exit /b
)

echo.
echo 📤 Posting to Facebook...
echo.

python facebook_auto_post.py "%message%"

echo.
pause
