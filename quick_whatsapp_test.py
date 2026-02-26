"""
Quick WhatsApp Test - Simple Command Line Interface
Silver Tier Testing
"""

import asyncio
import sys
import logging
from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer

# Suppress verbose logging
logging.basicConfig(level=logging.WARNING)

async def main():
    """Quick test interface for WhatsApp."""
    
    server = WhatsAppMCPServer()
    
    if len(sys.argv) < 2:
        print("=" * 60)
        print("WhatsApp Quick Test - Silver Tier")
        print("=" * 60)
        print("\nUsage:")
        print("  python quick_whatsapp_test.py status")
        print("  python quick_whatsapp_test.py unread")
        print("  python quick_whatsapp_test.py read <contact>")
        print("  python quick_whatsapp_test.py send <contact> <message>")
        print("\nExamples:")
        print('  python quick_whatsapp_test.py read Anisa')
        print('  python quick_whatsapp_test.py send Anisa "Hello from AI"')
        print("=" * 60)
        return
    
    command = sys.argv[1].lower()
    
    try:
        if command == "status":
            print("Checking WhatsApp status...")
            result = await server.execute_tool("check_whatsapp_status", {})
            print(result.text)
        
        elif command == "unread":
            print("Getting unread chats...")
            result = await server.execute_tool("get_unread_whatsapp_chats", {})
            print(result.text)
        
        elif command == "read":
            if len(sys.argv) < 3:
                print("❌ Usage: python quick_whatsapp_test.py read <contact>")
                return
            
            contact = sys.argv[2]
            print(f"Reading messages from {contact}...")
            result = await server.execute_tool("read_whatsapp_messages", {
                "contact": contact,
                "count": 10
            })
            print(result.text)
        
        elif command == "send":
            if len(sys.argv) < 4:
                print("❌ Usage: python quick_whatsapp_test.py send <contact> <message>")
                return
            
            contact = sys.argv[2]
            message = " ".join(sys.argv[3:])
            print(f"Sending message to {contact}...")
            result = await server.execute_tool("send_whatsapp_message", {
                "recipient": contact,
                "message": message
            })
            print(result.text)
            
            # Show tracking file location
            print(f"\n📝 Message tracked in: WhatsApp_Sent/")
        
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: status, unread, read, send")
    
    finally:
        await server.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
