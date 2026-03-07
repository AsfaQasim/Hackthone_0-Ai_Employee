@echo off
echo ======================================================================
echo   TEST FACEBOOK AUTO POST
echo ======================================================================
echo.
echo This will post a TEST message to your Facebook page.
echo.
echo Message: "🤖 Testing auto-post from my AI Employee system! #AI #Automation"
echo.
set /p confirm="Continue? (y/n): "

if /i not "%confirm%"=="y" (
    echo.
    echo ❌ Cancelled
    pause
    exit /b
)

echo.
echo 📤 Posting to Facebook...
echo.

python facebook_auto_post.py "🤖 Testing auto-post from my AI Employee system! #AI #Automation"

echo.
echo ======================================================================
pause
