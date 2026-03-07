@echo off
echo.
echo ========================================
echo   FACEBOOK COMPLETE TEST
echo ========================================
echo.
echo Testing all Facebook posting methods...
echo.

echo [1/4] Checking token status...
python diagnose_facebook_token.py
echo.

echo [2/4] Checking app mode...
python check_facebook_app_mode.py
echo.

echo [3/4] Verifying existing posts...
python verify_facebook_posts.py
echo.

echo [4/4] Ready to post!
echo.
echo ========================================
echo   POSTING OPTIONS
echo ========================================
echo.
echo Choose a method:
echo.
echo [1] Manual-Assisted (WORKS 100%%)
echo [2] Fully Automatic (May need fixes)
echo [3] API Method (Needs token refresh)
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" goto manual
if "%choice%"=="2" goto auto
if "%choice%"=="3" goto api

:manual
echo.
set /p msg="Enter message to post: "
python facebook_post_now.py "%msg%"
goto end

:auto
echo.
set /p msg="Enter message to post: "
python facebook_auto_playwright.py "%msg%"
goto end

:api
echo.
echo First, refresh your token:
python facebook_token_helper.py
echo.
echo Now try posting:
set /p msg="Enter message to post: "
python facebook_auto_post.py "%msg%"
goto end

:end
echo.
echo ========================================
echo   VERIFY YOUR POST
echo ========================================
echo.
echo Check your Facebook page:
echo https://www.facebook.com/profile.php?id=967740493097470
echo.
pause
