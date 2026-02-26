"""Simple WhatsApp Status Check"""
import asyncio
from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer

async def check():
    print("Checking WhatsApp connection...")
    server = WhatsAppMCPServer()
    try:
        result = await server.execute_tool("check_whatsapp_status", {})
        print(result.text)
    finally:
        await server.cleanup()

asyncio.run(check())
