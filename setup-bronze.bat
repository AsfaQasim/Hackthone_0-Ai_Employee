@echo off
REM Bronze Tier Quick Setup Script (Windows)
REM Run this to set up your AI Employee foundation

echo 🚀 Bronze Tier AI Employee Setup
echo =================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    exit /b 1
)
echo ✅ Python found
python --version
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pyyaml html2text

echo.
echo ✅ Setup complete!
echo.
echo 📋 Next Steps:
echo 1. Set up Gmail API credentials (see BRONZE_TIER_SETUP.md)
echo 2. Save credentials to: config\gmail-credentials.json
echo 3. Run: python Skills\gmail_watcher.py auth
echo 4. Test: python Skills\gmail_watcher.py poll --dry-run
echo.
echo 📖 Full guide: BRONZE_TIER_SETUP.md
pause
