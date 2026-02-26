@echo off
echo Setting Playwright to use F: drive for browsers...
echo.

REM Set environment variable to use F: drive
set PLAYWRIGHT_BROWSERS_PATH=F:\playwright-browsers

echo Installing Chromium to F:\playwright-browsers
echo This will download ~173 MB
echo.

python -m playwright install chromium

echo.
echo Done!
pause
