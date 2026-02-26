@echo off
echo ========================================
echo    Complete GitHub Fix - Fresh Start
echo ========================================
echo.
echo This will create a FRESH repository without sensitive files
echo.
echo WARNING: This will:
echo 1. Delete .git folder (lose all history)
echo 2. Create fresh git repository
echo 3. Push to GitHub with clean history
echo.
pause

echo.
echo Step 1: Backing up current .git folder...
if exist .git_backup rmdir /s /q .git_backup
move .git .git_backup
echo ✓ Backup created: .git_backup

echo.
echo Step 2: Verifying sensitive files are excluded...
echo.
echo Checking .gitignore...
findstr /C:"gmail-token.json" .gitignore >nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ gmail-token.json in .gitignore
) else (
    echo ✗ Adding gmail-token.json to .gitignore
    echo config/gmail-token.json >> .gitignore
)

findstr /C:"gmail-credentials.json" .gitignore >nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ gmail-credentials.json in .gitignore
) else (
    echo ✗ Adding gmail-credentials.json to .gitignore
    echo config/gmail-credentials.json >> .gitignore
)

echo.
echo Step 3: Initializing fresh git repository...
git init
echo ✓ Fresh git initialized

echo.
echo Step 4: Adding files (excluding sensitive data)...
git add .
echo ✓ Files staged

echo.
echo Step 5: Checking what will be committed...
echo.
git status
echo.
echo ⚠️  IMPORTANT: Check above list for sensitive files!
echo    Should NOT see:
echo    - config/gmail-token.json
echo    - config/gmail-credentials.json
echo    - .env
echo.
set /p CONTINUE="Continue with commit? (y/n): "
if /i not "%CONTINUE%"=="y" (
    echo Aborted. Run script again after fixing.
    exit /b 1
)

echo.
echo Step 6: Creating initial commit...
git commit -m "Bronze Tier Complete - Clean history without sensitive files"
echo ✓ Commit created

echo.
echo Step 7: Adding remote...
git remote add origin https://github.com/AsfaQasim/Hackthone_0-AI_Employee.git
echo ✓ Remote added

echo.
echo Step 8: Renaming branch to main...
git branch -M main
echo ✓ Branch renamed

echo.
echo Step 9: Force pushing to GitHub...
echo ⚠️  This will OVERWRITE GitHub repository!
echo.
set /p PUSH="Ready to force push? (y/n): "
if /i not "%PUSH%"=="y" (
    echo Aborted. You can manually push later with:
    echo git push -u origin main --force
    exit /b 1
)

git push -u origin main --force

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ SUCCESS! Repository pushed to GitHub
    echo ========================================
    echo.
    echo Your repository is now clean and pushed!
    echo Old history backed up in: .git_backup
    echo.
    echo GitHub URL:
    echo https://github.com/AsfaQasim/Hackthone_0-AI_Employee
    echo.
) else (
    echo.
    echo ========================================
    echo ❌ PUSH FAILED
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Sensitive files still in commit
    echo 2. Network issue
    echo 3. Authentication problem
    echo.
    echo Check what was staged:
    git ls-files
    echo.
    echo To restore old git:
    echo rmdir /s /q .git
    echo move .git_backup .git
)

pause
