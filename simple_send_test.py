"""
Simple Send Test - Reply to Anisa
"""

import asyncio
from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer

async def send_reply():
    print("=" * 60)
    print("Sending test message to Anisa...")
    print("=" * 60)
    
    server = WhatsAppMCPServer()
    
    try:
        # Send message
        result = await server.execute_tool("send_whatsapp_message", {
            "recipient": "Anisa",
            "message": "Thanks for your message! This is an automated reply from my AI assistant. 🤖"
        })
        
        print(f"\nResult: {result.text}")
        print("\n✅ Check WhatsApp_Sent folder for tracking!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    finally:
        await server.cleanup()

if __name__ == "__main__":
    asyncio.run(send_reply())
