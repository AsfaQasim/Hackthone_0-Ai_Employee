@echo off
echo ======================================
echo WhatsApp Send Test
echo ======================================
echo.
echo Anisa ko reply bhej rahe hain...
echo.
python -c "import asyncio; from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer; asyncio.run((lambda: asyncio.create_task(WhatsAppMCPServer().execute_tool('send_whatsapp_message', {'recipient': 'Anisa', 'message': 'Thanks for your message! This is an automated reply from my AI assistant.'})))())"
echo.
echo Done! Check WhatsApp_Sent folder
pause
