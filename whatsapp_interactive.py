"""
WhatsApp Interactive Test - Silver Tier
Simple interactive interface for testing WhatsApp functionality
"""

import asyncio
import logging
from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def interactive_mode():
    """Run interactive WhatsApp test mode."""
    
    print("=" * 60)
    print("WhatsApp Interactive Test - Silver Tier")
    print("=" * 60)
    print("\nInitializing WhatsApp MCP Server...")
    
    server = WhatsAppMCPServer()
    
    print("\n✅ Server initialized!")
    print("\nCommands:")
    print("  status  - Check WhatsApp connection")
    print("  unread  - Show unread chats")
    print("  read <contact> - Read messages from contact")
    print("  send <contact> <message> - Send message")
    print("  quit    - Exit")
    print("\n" + "=" * 60)
    
    try:
        while True:
            try:
                command = input("\n> ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ["quit", "exit", "q"]:
                    print("\n👋 Exiting...")
                    break
                
                parts = command.split(maxsplit=1)
                cmd = parts[0].lower()
                
                if cmd == "status":
                    print("⏳ Checking status...")
                    result = await server.execute_tool("check_whatsapp_status", {})
                    print(result.text)
                
                elif cmd == "unread":
                    print("⏳ Getting unread chats...")
                    result = await server.execute_tool("get_unread_whatsapp_chats", {})
                    print(result.text)
                
                elif cmd == "read":
                    if len(parts) < 2:
                        print("❌ Usage: read <contact>")
                        continue
                    
                    contact = parts[1]
                    print(f"⏳ Reading messages from {contact}...")
                    result = await server.execute_tool("read_whatsapp_messages", {
                        "contact": contact,
                        "count": 10
                    })
                    print(result.text)
                
                elif cmd == "send":
                    if len(parts) < 2:
                        print("❌ Usage: send <contact> <message>")
                        continue
                    
                    args = parts[1].split(maxsplit=1)
                    if len(args) < 2:
                        print("❌ Usage: send <contact> <message>")
                        continue
                    
                    contact, message = args
                    print(f"⏳ Sending message to {contact}...")
                    result = await server.execute_tool("send_whatsapp_message", {
                        "recipient": contact,
                        "message": message
                    })
                    print(result.text)
                    
                    if "✅" in result.text:
                        print(f"📝 Message tracked in: WhatsApp_Sent/")
                
                else:
                    print(f"❌ Unknown command: {cmd}")
                    print("Available: status, unread, read, send, quit")
            
            except KeyboardInterrupt:
                print("\n\n👋 Exiting...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    finally:
        print("\n🧹 Cleaning up...")
        await server.cleanup()
        print("✅ Done!")

if __name__ == "__main__":
    print("\n🚀 Starting WhatsApp Interactive Test...")
    asyncio.run(interactive_mode())
