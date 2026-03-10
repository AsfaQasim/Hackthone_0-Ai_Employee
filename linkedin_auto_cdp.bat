@echo off
REM LinkedIn Auto Post - Chrome CDP Method
REM Uses your existing Chrome with login

echo ================================================================
echo LINKEDIN AUTO POST (Chrome Debug Method)
echo ================================================================
echo.
echo Yeh script:
echo   1. Chrome ko debug mode mein kholega
echo   2. LinkedIn feed page par jayega
echo   3. Aap login karein (10 minutes time)
echo   4. Auto-post ho jayega
echo.
echo ================================================================
echo IMPORTANT: Chrome band karein agar pehle se khula hai
echo ================================================================
echo.

REM Close existing Chrome
taskkill /F /IM chrome.exe 2>nul
timeout /t 2 /nobreak >nul

REM Run the script
python linkedin_auto_cdp.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================
    echo ✅ POST SUCCESSFUL!
    echo ================================================================
) else (
    echo.
    echo ================================================================
    echo ❌ Post failed
    echo ================================================================
)

pause
