@echo off
echo ========================================
echo    Create New GitHub Repository
echo ========================================
echo.
echo This will create a BRAND NEW repository
echo.
echo Steps:
echo 1. Delete current .git folder
echo 2. Create fresh git
echo 3. Push to NEW repository
echo.
echo ⚠️  You need to create new repo on GitHub first!
echo.
echo Go to: https://github.com/new
echo Repository name: AI-Employee-Bronze-Tier
echo Make it Public
echo DON'T initialize with README
echo.
set /p READY="Have you created new repo on GitHub? (y/n): "
if /i not "%READY%"=="y" (
    echo.
    echo Please create repository first, then run this script again.
    pause
    exit /b 1
)

echo.
set /p REPO_NAME="Enter repository name (e.g., AI-Employee-Bronze-Tier): "

echo.
echo Step 1: Removing old .git...
rmdir /s /q .git
rmdir /s /q .git_backup
echo ✓ Old git removed

echo.
echo Step 2: Initializing fresh git...
git init
echo ✓ Git initialized

echo.
echo Step 3: Adding files...
git add .
echo ✓ Files staged

echo.
echo Step 4: Checking staged files...
echo.
git status
echo.
echo ⚠️  Check above - should NOT see:
echo    - config/gmail-token.json
echo    - config/gmail-credentials.json
echo    - .env
echo.
pause

echo.
echo Step 5: Creating commit...
git commit -m "Bronze Tier Complete - Initial commit"
echo ✓ Committed

echo.
echo Step 6: Adding remote...
git remote add origin https://github.com/AsfaQasim/%REPO_NAME%.git
echo ✓ Remote added

echo.
echo Step 7: Pushing to GitHub...
git branch -M main
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ SUCCESS!
    echo ========================================
    echo.
    echo Repository URL:
    echo https://github.com/AsfaQasim/%REPO_NAME%
    echo.
    echo Your Bronze Tier is now on GitHub!
    echo.
) else (
    echo.
    echo ========================================
    echo ❌ PUSH FAILED
    echo ========================================
    echo.
    echo Possible issues:
    echo 1. Repository doesn't exist on GitHub
    echo 2. Wrong repository name
    echo 3. Sensitive files still in commit
    echo.
    echo Check what was committed:
    git ls-files | findstr gmail
    git ls-files | findstr .env
)

pause
