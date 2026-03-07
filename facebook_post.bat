@echo off
echo ======================================================================
echo   FACEBOOK MANUAL POST
echo ======================================================================
echo.

set /p message="Enter your message: "

if "%message%"=="" (
    echo.
    echo ❌ No message provided
    pause
    exit /b
)

echo.
echo 📤 Opening Facebook...
echo.

python facebook_manual_post.py "%message%"

echo.
pause
