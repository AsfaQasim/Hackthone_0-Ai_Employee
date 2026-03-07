@echo off
echo.
echo ========================================
echo   FACEBOOK AUTO-POSTING SOLUTION
echo ========================================
echo.
echo Current Issue: Token expired
echo.
echo Solution Options:
echo.
echo [1] Use Playwright (Works NOW - No token needed!)
echo [2] Get new token (Requires Facebook login)
echo [3] Check app mode
echo [4] Verify posts
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" goto playwright
if "%choice%"=="2" goto token
if "%choice%"=="3" goto appmode
if "%choice%"=="4" goto verify

:playwright
echo.
echo ========================================
echo   PLAYWRIGHT METHOD (RECOMMENDED)
echo ========================================
echo.
echo This method:
echo - Works immediately
echo - No token needed
echo - No API permissions needed
echo - Fully automatic
echo.
set /p message="Enter message to post: "
python facebook_auto_playwright.py "%message%"
goto end

:token
echo.
echo ========================================
echo   GET NEW TOKEN
echo ========================================
echo.
python facebook_token_helper.py
goto end

:appmode
echo.
echo ========================================
echo   CHECK APP MODE
echo ========================================
echo.
python check_facebook_app_mode.py
goto end

:verify
echo.
echo ========================================
echo   VERIFY POSTS
echo ========================================
echo.
python verify_facebook_posts.py
goto end

:end
echo.
echo ========================================
pause
