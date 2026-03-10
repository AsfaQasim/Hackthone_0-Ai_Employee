@echo off
echo ======================================================================
echo SOCIAL MEDIA AUTO-POSTING TEST
echo ======================================================================
echo.
echo This will test posting to all social media platforms.
echo.
echo Platforms:
echo   1. LinkedIn
echo   2. Facebook  
echo   3. Twitter
echo.
echo Choose an option:
echo   1 - Test LinkedIn only
echo   2 - Test Facebook only
echo   3 - Test Twitter only
echo   4 - Test ALL platforms
echo   5 - Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Testing LinkedIn...
    python social_media_auto_poster.py "🚀 Testing LinkedIn auto-post! This is a real test from my AI Employee system. #AI #Automation #Testing" linkedin
)

if "%choice%"=="2" (
    echo.
    echo Testing Facebook...
    python social_media_auto_poster.py "🚀 Testing Facebook auto-post! This is a real test from my AI Employee system. #AI #Automation" facebook
)

if "%choice%"=="3" (
    echo.
    echo Testing Twitter...
    python social_media_auto_poster.py "🚀 Testing Twitter auto-post! This is a real test from my AI Employee system. #AI #Automation" twitter
)

if "%choice%"=="4" (
    echo.
    echo Testing ALL platforms...
    python social_media_auto_poster.py "🚀 Testing multi-platform auto-post! This is a real test from my AI Employee system. #AI #Automation #Testing" all
)

if "%choice%"=="5" (
    echo.
    echo Exiting...
    exit /b
)

echo.
echo ======================================================================
echo.
echo NEXT STEPS:
echo 1. Check your social media accounts to verify posts
echo 2. Review tracking files in Social_Media_Tracking folder
echo 3. Update engagement metrics in tracking files
echo.
echo ======================================================================
pause
