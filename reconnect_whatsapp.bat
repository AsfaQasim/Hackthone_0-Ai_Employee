@echo off
echo ============================================
echo WhatsApp Reconnect - QR Code Scan
echo ============================================
echo.
echo Browser khulega, QR code scan karo
echo Apne phone se WhatsApp open karo:
echo   1. Settings ^> Linked Devices
echo   2. Link a Device
echo   3. QR code scan karo
echo.
echo Press any key to start...
pause > nul
echo.
echo Starting authentication...
python Skills/whatsapp_watcher.py auth
echo.
echo Done!
pause
