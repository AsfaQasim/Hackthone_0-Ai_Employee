@echo off
REM LinkedIn Quick Post - Uses existing session
REM No re-authentication needed

echo ================================================================
echo LINKEDIN QUICK POST
echo ================================================================
echo.

if "%~1"=="" (
    echo Usage: linkedin_quick_post.bat "Your post content"
    echo.
    echo Example:
    echo   linkedin_quick_post.bat "Hello LinkedIn!"
    echo.
    echo ================================================================
    pause
    exit /b 1
)

python linkedin_quick_post.py %*

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================
    echo Post published successfully!
    echo ================================================================
) else (
    echo.
    echo ================================================================
    echo Posting failed.
    echo ================================================================
)

pause
