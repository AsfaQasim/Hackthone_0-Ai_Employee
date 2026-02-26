@echo off
echo Downloading GitHub CLI...
bitsadmin /transfer "GitHub CLI" https://github.com/cli/cli/releases/latest/download/gh_2.62.0_windows_amd64.msi "%CD%\gh-cli.msi"
if exist gh-cli.msi (
    echo Download complete. Installing...
    msiexec /i gh-cli.msi /quiet
    echo Installation complete. Please restart your command prompt.
) else (
    echo Download failed. Trying alternative method...
    echo Please manually download from: https://cli.github.com/
)
pause