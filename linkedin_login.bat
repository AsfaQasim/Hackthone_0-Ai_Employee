@echo off
REM LinkedIn Login - Setup authentication
echo ========================================
echo LinkedIn Login Setup
echo ========================================
echo.
echo This will open a browser window for you to login to LinkedIn.
echo Please complete the login process including any 2FA challenges.
echo.
pause

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Run login
python Skills\linkedin_auto_poster.py --login --session-path .linkedin_session

echo.
echo ========================================
echo Login complete! You can now use linkedin_auto_post.bat
echo ========================================
pause
