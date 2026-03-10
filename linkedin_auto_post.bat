@echo off
REM LinkedIn Auto Post - Quick posting script
echo ========================================
echo LinkedIn Auto Poster
echo ========================================
echo.

REM Check if content is provided
if "%~1"=="" (
    echo Usage: linkedin_auto_post.bat "Your post content here" [image_path]
    echo.
    echo Examples:
    echo   linkedin_auto_post.bat "Hello LinkedIn!"
    echo   linkedin_auto_post.bat "Check out this image" image.jpg
    echo.
    exit /b 1
)

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Post to LinkedIn
if "%~2"=="" (
    python Skills\linkedin_auto_poster.py --post "%~1" --session-path .linkedin_session
) else (
    python Skills\linkedin_auto_poster.py --post "%~1" --image "%~2" --session-path .linkedin_session
)

echo.
echo ========================================
echo Done!
echo ========================================
pause
