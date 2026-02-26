@echo off
echo ========================================
echo    GitHub Push Error Fix
echo ========================================
echo.

echo Step 1: Removing sensitive files from git...
git rm --cached config/gmail-token.json 2>nul
git rm --cached config/gmail-credentials.json 2>nul
git rm --cached .env 2>nul
git rm --cached -r .whatsapp_session/ 2>nul

echo.
echo Step 2: Checking git status...
git status

echo.
echo Step 3: Committing changes...
git add .gitignore
git commit -m "Remove sensitive files from git tracking"

echo.
echo Step 4: Attempting to push...
git push origin main

echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS! Push completed.
) else (
    echo FAILED! Trying alternative method...
    echo.
    echo Creating new branch instead...
    git checkout -b bronze-tier-complete
    git push origin bronze-tier-complete
    echo.
    echo Branch pushed! Create Pull Request on GitHub:
    echo https://github.com/AsfaQasim/Hackthone_0-AI_Employee/pulls
)
echo ========================================

pause
