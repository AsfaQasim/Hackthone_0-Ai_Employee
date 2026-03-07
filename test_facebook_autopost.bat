@echo off
REM Test Facebook/Instagram Auto-Posting
REM Gold Tier - Social Media Integration Test

echo ========================================
echo  Facebook/Instagram Auto-Posting Test
echo ========================================
echo.

cd /d "%~dp0"

REM Check if .env file exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo.
    echo Please create .env file with:
    echo FACEBOOK_PAGE_ACCESS_TOKEN=your_token_here
    echo INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id_here
    echo.
    echo See FACEBOOK_INSTAGRAM_AUTOPOST_GUIDE.md for setup instructions.
    pause
    exit /b 1
)

echo Running Facebook/Instagram tests...
echo.
echo This will test:
echo  1. Simple Facebook post
echo  2. Facebook post with image
echo  3. Get recent posts
echo  4. Get Facebook insights
echo  5. Instagram post (if configured)
echo  6. Instagram insights (if configured)
echo  7. Generate social media summary
echo.
echo NOTE: This will actually post to your Facebook/Instagram!
echo.
pause

python test_facebook_autopost.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo  Tests failed! Check errors above.
    echo ========================================
) else (
    echo.
    echo ========================================
    echo  All tests completed!
    echo ========================================
)

echo.
pause
