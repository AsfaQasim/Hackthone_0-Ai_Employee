@echo off
echo ========================================
echo    Force Push to Same Repository
echo ========================================
echo.
echo This will COMPLETELY OVERWRITE your GitHub repository
echo Repository: Hackthone_0-AI_Employee
echo.
echo ⚠️  WARNING: This will delete ALL history on GitHub!
echo.
pause

echo.
echo Step 1: Removing ALL git history...
rmdir /s /q .git
rmdir /s /q .git_backup
echo ✓ Git history deleted

echo.
echo Step 2: Creating fresh git repository...
git init
echo ✓ Fresh git created

echo.
echo Step 3: Staging files...
git add .
echo ✓ Files staged

echo.
echo Step 4: Showing what will be committed...
echo.
echo Files to be committed:
git ls-files
echo.
echo ⚠️  CRITICAL CHECK - These should NOT be in above list:
echo    - config/gmail-token.json
echo    - config/gmail-credentials.json
echo    - .env
echo.
set /p CHECK="Do you see any sensitive files above? (y/n): "
if /i "%CHECK%"=="y" (
    echo.
    echo ❌ STOP! Sensitive files detected!
    echo.
    echo Run these commands:
    echo git rm --cached config/gmail-token.json
    echo git rm --cached config/gmail-credentials.json
    echo git rm --cached .env
    echo.
    echo Then run this script again.
    pause
    exit /b 1
)

echo.
echo Step 5: Creating commit...
git commit -m "Bronze Tier Complete - Clean history without secrets"
echo ✓ Commit created

echo.
echo Step 6: Adding remote repository...
git remote add origin https://github.com/AsfaQasim/Hackthone_0-AI_Employee.git
echo ✓ Remote added

echo.
echo Step 7: Preparing to force push...
git branch -M main
echo ✓ Branch renamed to main

echo.
echo ⚠️  FINAL WARNING: This will OVERWRITE GitHub repository!
echo    All old commits will be deleted.
echo    New clean history will be created.
echo.
set /p CONFIRM="Are you ABSOLUTELY sure? Type YES to continue: "
if /i not "%CONFIRM%"=="YES" (
    echo.
    echo Aborted. No changes made to GitHub.
    pause
    exit /b 1
)

echo.
echo Step 8: Force pushing to GitHub...
git push -u origin main --force

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ SUCCESS! Repository pushed!
    echo ========================================
    echo.
    echo Your repository is now clean and on GitHub!
    echo URL: https://github.com/AsfaQasim/Hackthone_0-AI_Employee
    echo.
    echo ✅ Bronze Tier complete and submitted!
    echo.
) else (
    echo.
    echo ========================================
    echo ❌ PUSH FAILED
    echo ========================================
    echo.
    echo GitHub is still blocking the push.
    echo.
    echo This means sensitive files are STILL in the commit.
    echo.
    echo Check what's committed:
    git ls-files | findstr gmail
    git ls-files | findstr .env
    echo.
    echo If you see files above, remove them:
    echo git rm --cached config/gmail-token.json
    echo git rm --cached config/gmail-credentials.json
    echo git commit --amend -m "Bronze Tier Complete"
    echo git push -u origin main --force
)

echo.
pause
