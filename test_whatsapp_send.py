"""
Simple WhatsApp Send Test
Bas ek message bhejne ke liye
"""

import asyncio
import logging
from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer

logging.basicConfig(level=logging.INFO)

async def test_send():
    print("=" * 60)
    print("WhatsApp Send Test - Silver Tier")
    print("=" * 60)
    
    server = WhatsAppMCPServer()
    
    try:
        # 1. Check status
        print("\n1. Checking connection...")
        status = await server.execute_tool("check_whatsapp_status", {})
        print(f"   {status.text}")
        
        if "not connected" in status.text.lower():
            print("\n❌ WhatsApp connected nahi hai!")
            print("Pehle authenticate karo:")
            print("   python Skills/whatsapp_watcher.py auth")
            return
        
        # 2. Get unread chats
        print("\n2. Checking unread chats...")
        unread = await server.execute_tool("get_unread_whatsapp_chats", {})
        print(f"   {unread.text}")
        
        # 3. Interactive send
        print("\n" + "=" * 60)
        print("✅ WhatsApp Ready!")
        print("=" * 60)
        print("\nAb message bhejo:")
        print("Format: ContactName|Message")
        print("Example: Anisa|Hello, how are you?")
        print("\nType 'quit' to exit")
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if '|' not in user_input:
                    print("❌ Format: ContactName|Message")
                    continue
                
                contact, message = user_input.split('|', 1)
                contact = contact.strip()
                message = message.strip()
                
                if not contact or not message:
                    print("❌ Contact aur message dono chahiye!")
                    continue
                
                print(f"\n📤 Sending to {contact}...")
                result = await server.execute_tool("send_whatsapp_message", {
                    "recipient": contact,
                    "message": message
                })
                print(f"   {result.text}")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    finally:
        await server.cleanup()
        print("\n✅ Done!")

if __name__ == "__main__":
    asyncio.run(test_send())
