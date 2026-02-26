@echo off
echo ========================================
echo    Complete Git History Fix
echo ========================================
echo.
echo This will remove sensitive files from ALL git history
echo.
pause

echo Step 1: Going back to main branch...
git checkout main

echo.
echo Step 2: Deleting bronze-tier-complete branch...
git branch -D bronze-tier-complete

echo.
echo Step 3: Removing sensitive files from git history...
echo This may take a few minutes...

git filter-branch --force --index-filter "git rm --cached --ignore-unmatch config/gmail-token.json" --prune-empty --tag-name-filter cat -- --all

git filter-branch --force --index-filter "git rm --cached --ignore-unmatch config/gmail-credentials.json" --prune-empty --tag-name-filter cat -- --all

git filter-branch --force --index-filter "git rm --cached --ignore-unmatch .env" --prune-empty --tag-name-filter cat -- --all

echo.
echo Step 4: Cleaning up...
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo.
echo Step 5: Creating fresh branch...
git checkout -b bronze-complete-clean

echo.
echo Step 6: Force pushing...
git push origin bronze-complete-clean --force

echo.
echo ========================================
echo Done! Check GitHub for your new branch.
echo ========================================
pause
