@echo off
cls
echo ========================================
echo    Git Authentication Setup Helper
echo ========================================
echo.
echo Current Git Configuration:
git config --list | findstr user
echo.
echo ========================================
echo Choose your authentication method:
echo ========================================
echo 1. Personal Access Token (Recommended)
echo 2. Configure credential storage
echo 3. Test current setup
echo 4. Show repository clone examples
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto token_setup
if "%choice%"=="2" goto credential_setup
if "%choice%"=="3" goto test_setup
if "%choice%"=="4" goto examples
if "%choice%"=="5" goto end

:token_setup
echo.
echo ========================================
echo    Personal Access Token Setup
echo ========================================
echo 1. Go to: https://github.com/settings/tokens
echo 2. Click "Generate new token (classic)"
echo 3. Select "repo" scope
echo 4. Copy the generated token
echo.
echo Then use this format to clone:
echo git clone https://USERNAME:TOKEN@github.com/owner/repo.git
echo.
pause
goto menu

:credential_setup
echo.
echo Setting up credential storage...
git config --global credential.helper store
echo Done! Now when you clone, enter your username and token as password.
echo.
pause
goto menu

:test_setup
echo.
echo Testing with a public repository...
git clone https://github.com/octocat/Hello-World.git test-repo
if exist test-repo (
    echo SUCCESS! Git is working.
    rmdir /s /q test-repo
) else (
    echo FAILED! Check your internet connection.
)
echo.
pause
goto menu

:examples
echo.
echo ========================================
echo    Clone Examples
echo ========================================
echo Public repo:
echo git clone https://github.com/owner/repo.git
echo.
echo Private repo with token:
echo git clone https://username:token@github.com/owner/repo.git
echo.
echo SSH (if configured):
echo git clone git@github.com:owner/repo.git
echo.
pause
goto menu

:menu
cls
goto start

:end
echo Goodbye!