@echo off
REM LinkedIn Auto-Post - Quick Command
REM Usage: linkedin_post.bat "Your topic here"

if "%~1"=="" (
    echo ======================================================================
    echo LINKEDIN AUTO-POST
    echo ======================================================================
    echo.
    echo Usage: linkedin_post.bat "Your topic here"
    echo.
    echo Example:
    echo   linkedin_post.bat "Just completed Silver Tier!"
    echo.
    echo ======================================================================
    exit /b 1
)

echo ======================================================================
echo GENERATING LINKEDIN POST...
echo ======================================================================
echo.

REM Set topic in environment variable
set LINKEDIN_POST_TOPIC=%*

REM Run Python script
python linkedin_post_cli.py "%LINKEDIN_POST_TOPIC%"

echo.
echo ======================================================================
echo.
echo NOW POST TO LINKEDIN:
echo 1. Copy the content above
echo 2. Go to: https://www.linkedin.com/
echo 3. Click "Start a post"
echo 4. Paste and click "Post"
echo.
echo ======================================================================
pause
