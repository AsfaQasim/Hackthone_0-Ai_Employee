@echo off
REM Quick WhatsApp Test Commands

if "%1"=="" (
    echo ============================================
    echo WhatsApp Quick Commands - Silver Tier
    echo ============================================
    echo.
    echo Usage:
    echo   test_whatsapp status
    echo   test_whatsapp unread
    echo   test_whatsapp read ContactName
    echo   test_whatsapp send ContactName Message here
    echo.
    echo Examples:
    echo   test_whatsapp status
    echo   test_whatsapp unread
    echo   test_whatsapp read Anisa
    echo   test_whatsapp send Anisa Hello from AI
    echo.
    echo ============================================
    exit /b
)

python quick_whatsapp_test.py %*
