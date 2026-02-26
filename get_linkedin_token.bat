@echo off
echo ======================================================================
echo LinkedIn Access Token - Quick Start
echo ======================================================================
echo.
echo This script will help you get your LinkedIn access token.
echo.
echo Steps:
echo 1. A browser window will open with LinkedIn login
echo 2. Sign in and authorize the app
echo 3. Your access token will be displayed here
echo.
echo ======================================================================
echo.
pause
python get_linkedin_token.py
echo.
echo ======================================================================
echo.
echo If successful, your token will be displayed above.
echo Copy it and run: set LINKEDIN_ACCESS_TOKEN=your_token_here
echo.
pause
