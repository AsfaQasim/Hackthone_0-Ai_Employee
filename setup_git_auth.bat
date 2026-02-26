@echo off
echo Setting up Git authentication...
echo.
echo OPTION 1: Use Personal Access Token
echo 1. Go to https://github.com/settings/tokens
echo 2. Click "Generate new token (classic)"
echo 3. Select "repo" scope
echo 4. Copy the token
echo 5. Use it as password when git prompts
echo.
echo OPTION 2: Configure Git with token directly
echo Run: git config --global credential.helper store
echo Then clone with: git clone https://username:token@github.com/owner/repo.git
echo.
echo OPTION 3: Download GitHub CLI manually
echo 1. Go to https://cli.github.com/
echo 2. Download Windows installer
echo 3. Install and run: gh auth login
echo.
pause