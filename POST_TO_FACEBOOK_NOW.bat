@echo off
echo.
echo ========================================
echo   POST TO FACEBOOK NOW
echo ========================================
echo.
echo This will open Facebook and help you post.
echo.
set /p message="Enter your message: "

if "%message%"=="" (
    echo.
    echo ❌ No message entered!
    pause
    exit
)

echo.
echo ========================================
echo   POSTING...
echo ========================================
echo.

python facebook_post_guaranteed.py "%message%"

echo.
echo ========================================
echo   DONE!
echo ========================================
echo.
echo Check your post at:
echo https://www.facebook.com/profile.php?id=967740493097470
echo.
pause
