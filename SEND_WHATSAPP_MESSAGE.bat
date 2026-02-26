@echo off
echo ======================================================================
echo WhatsApp Message Sender - Kiro AI
echo ======================================================================
echo.
echo This will open WhatsApp Web in your browser.
echo.
echo INSTRUCTIONS:
echo 1. Browser will open with WhatsApp Web
echo 2. Search for the contact you want to message
echo 3. Send your message
echo 4. Come back here and press Enter to track it
echo.
pause
echo.
echo Opening WhatsApp Web...
start https://web.whatsapp.com
echo.
echo After sending your message, press Enter to continue...
pause
echo.
set /p RECIPIENT="Enter recipient name: "
set /p MESSAGE="Enter message you sent: "
echo.
echo Tracking message...
python -c "from pathlib import Path; from datetime import datetime; sent_folder = Path('WhatsApp_Sent'); sent_folder.mkdir(exist_ok=True); timestamp = datetime.now().strftime('%%Y%%m%%d_%%H%%M%%S'); filename = f'sent_{timestamp}_%RECIPIENT%.md'; filepath = sent_folder / filename; content = f'''---\ntype: whatsapp_sent\nrecipient: \"%RECIPIENT%\"\ntimestamp: \"{datetime.now().isoformat()}\"\nstatus: \"✅ Sent\"\n---\n\n# WhatsApp Message to %RECIPIENT%\n\n**Status**: ✅ Sent\n**Sent**: {datetime.now().strftime('%%Y-%%m-%%d %%H:%%M:%%S')}\n\n## Message\n%MESSAGE%\n\n---\n\n*Sent via Kiro AI WhatsApp Integration*\n'''; filepath.write_text(content, encoding='utf-8'); print(f'✅ Message tracked: {filepath}')"
echo.
echo ======================================================================
echo ✅ Message sent and tracked!
echo ======================================================================
echo.
echo Check WhatsApp_Sent folder for details.
echo.
pause
