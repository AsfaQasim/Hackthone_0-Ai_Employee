"""
Test WhatsApp MCP Server - Read and Send Messages
Silver Tier Requirement Test
"""

import asyncio
import logging
from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_whatsapp_functionality():
    """Test WhatsApp read and send functionality."""
    
    print("=" * 60)
    print("WhatsApp MCP Server Test - Silver Tier")
    print("=" * 60)
    
    # Initialize server
    server = WhatsAppMCPServer(
        session_path=".whatsapp_session",
        vault_path="."
    )
    
    try:
        # 1. Check connection status
        print("\n1. Checking WhatsApp connection status...")
        status_result = await server.execute_tool("check_whatsapp_status", {})
        print(f"   {status_result.text}")
        
        # 2. Get unread chats
        print("\n2. Getting unread chats...")
        unread_result = await server.execute_tool("get_unread_whatsapp_chats", {})
        print(f"   {unread_result.text}")
        
        # 3. Read messages from a contact (example)
        print("\n3. Reading messages (example)...")
        print("   To read messages, use:")
        print('   await server.execute_tool("read_whatsapp_messages", {')
        print('       "contact": "Contact Name",')
        print('       "count": 10')
        print('   })')
        
        # 4. Send message (example)
        print("\n4. Sending message (example)...")
        print("   To send a message, use:")
        print('   await server.execute_tool("send_whatsapp_message", {')
        print('       "recipient": "Contact Name",')
        print('       "message": "Your message here"')
        print('   })')
        
        print("\n" + "=" * 60)
        print("✅ WhatsApp MCP Server is ready!")
        print("=" * 60)
        
        # Interactive mode
        print("\n📱 Interactive Mode")
        print("Commands:")
        print("  status - Check connection status")
        print("  unread - Show unread chats")
        print("  read <contact> - Read messages from contact")
        print("  send <contact> <message> - Send message to contact")
        print("  quit - Exit")
        
        while True:
            try:
                command = input("\n> ").strip().lower()
                
                if not command:
                    continue
                
                if command == "quit" or command == "exit":
                    print("Exiting...")
                    break
                
                elif command == "status":
                    print("Checking status...")
                    result = await server.execute_tool("check_whatsapp_status", {})
                    print(result.text)
                
                elif command == "unread":
                    print("Getting unread chats...")
                    result = await server.execute_tool("get_unread_whatsapp_chats", {})
                    print(result.text)
                
                elif command.startswith("read "):
                    contact = command[5:].strip()
                    if contact:
                        print(f"Reading messages from {contact}...")
                        result = await server.execute_tool("read_whatsapp_messages", {
                            "contact": contact,
                            "count": 10
                        })
                        print(result.text)
                    else:
                        print("❌ Usage: read <contact>")
                
                elif command.startswith("send "):
                    parts = command[5:].split(maxsplit=1)
                    if len(parts) == 2:
                        contact, message = parts
                        print(f"Sending message to {contact}...")
                        result = await server.execute_tool("send_whatsapp_message", {
                            "recipient": contact,
                            "message": message
                        })
                        print(result.text)
                    else:
                        print("❌ Usage: send <contact> <message>")
                
                else:
                    print(f"❌ Unknown command: '{command}'")
                    print("Available commands: status, unread, read, send, quit")
            
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    finally:
        # Cleanup
        await server.cleanup()
        print("\n✅ Server cleaned up successfully")


if __name__ == "__main__":
    asyncio.run(test_whatsapp_functionality())
