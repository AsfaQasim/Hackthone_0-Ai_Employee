@echo off
REM Quick WhatsApp Commands - Silver Tier

if "%1"=="" (
    echo ============================================
    echo WhatsApp Quick Commands
    echo ============================================
    echo.
    echo Usage:
    echo   wa status       - Check connection
    echo   wa unread       - Show unread chats
    echo   wa read NAME    - Read messages
    echo   wa send NAME MSG - Send message
    echo.
    echo Examples:
    echo   wa status
    echo   wa unread
    echo   wa read Anisa
    echo   wa send Anisa Hello from AI
    echo.
    echo ============================================
    exit /b
)

python whatsapp_final_test.py %*
