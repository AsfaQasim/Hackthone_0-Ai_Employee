@echo off
echo ============================================
echo WhatsApp Authentication - Silver Tier Setup
echo ============================================
echo.
echo This will:
echo 1. Open Chrome browser
echo 2. Load WhatsApp Web
echo 3. Show QR code
echo 4. Wait for you to scan with your phone
echo.
echo Press any key to continue...
pause > nul
echo.
echo Starting authentication...
python Skills/whatsapp_watcher.py auth
echo.
echo ============================================
echo Authentication complete!
echo ============================================
echo.
echo Now you can test with:
echo   python test_whatsapp_mcp.py
echo.
pause
