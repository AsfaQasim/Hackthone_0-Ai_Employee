"""
Simple WhatsApp Test - With Visible Browser
This keeps the browser visible to avoid WhatsApp's automation detection
"""

import asyncio
import sys
from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer

async def test_status():
    """Test WhatsApp connection status."""
    print("=" * 60)
    print("Testing WhatsApp Connection")
    print("=" * 60)
    print("\n⏳ Opening Chrome browser (will be visible)...")
    print("⏳ Loading WhatsApp Web...")
    print("⏳ Please wait 10-15 seconds...\n")
    
    server = WhatsAppMCPServer()
    
    try:
        result = await server.execute_tool("check_whatsapp_status", {})
        print(result.text)
        
        if "✅" in result.text:
            print("\n" + "=" * 60)
            print("SUCCESS! WhatsApp is connected!")
            print("=" * 60)
            print("\nYou can now:")
            print("  1. Get unread chats")
            print("  2. Read messages")
            print("  3. Send messages")
            print("\nKeep the browser window open!")
            return True
        else:
            print("\n" + "=" * 60)
            print("Connection Failed")
            print("=" * 60)
            print("\nPlease:")
            print("  1. Make sure you scanned QR code")
            print("  2. Check if WhatsApp Web is working in regular browser")
            print("  3. Try authentication again: python authenticate_whatsapp.py")
            return False
    
    finally:
        # Don't close browser yet - keep it open for further commands
        print("\n⚠️  Keep the browser window open for testing!")
        # await server.cleanup()

async def test_unread():
    """Test getting unread chats."""
    print("\n⏳ Getting unread chats...")
    
    server = WhatsAppMCPServer()
    
    try:
        result = await server.execute_tool("get_unread_whatsapp_chats", {})
        print(result.text)
    finally:
        await server.cleanup()

async def test_read(contact):
    """Test reading messages from a contact."""
    print(f"\n⏳ Reading messages from {contact}...")
    
    server = WhatsAppMCPServer()
    
    try:
        result = await server.execute_tool("read_whatsapp_messages", {
            "contact": contact,
            "count": 10
        })
        print(result.text)
    finally:
        await server.cleanup()

async def test_send(contact, message):
    """Test sending a message."""
    print(f"\n⏳ Sending message to {contact}...")
    
    server = WhatsAppMCPServer()
    
    try:
        result = await server.execute_tool("send_whatsapp_message", {
            "recipient": contact,
            "message": message
        })
        print(result.text)
        
        if "✅" in result.text:
            print(f"\n📝 Message tracked in: WhatsApp_Sent/")
    finally:
        await server.cleanup()

async def main():
    """Main test function."""
    
    if len(sys.argv) < 2:
        print("=" * 60)
        print("WhatsApp Simple Test - Silver Tier")
        print("=" * 60)
        print("\nUsage:")
        print("  python test_whatsapp_simple.py status")
        print("  python test_whatsapp_simple.py unread")
        print("  python test_whatsapp_simple.py read <contact>")
        print("  python test_whatsapp_simple.py send <contact> <message>")
        print("\nExamples:")
        print("  python test_whatsapp_simple.py status")
        print("  python test_whatsapp_simple.py unread")
        print("  python test_whatsapp_simple.py read Anisa")
        print('  python test_whatsapp_simple.py send Anisa "Hello from AI"')
        print("\n⚠️  Browser will be VISIBLE (not headless)")
        print("=" * 60)
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        await test_status()
    
    elif command == "unread":
        await test_unread()
    
    elif command == "read":
        if len(sys.argv) < 3:
            print("❌ Usage: python test_whatsapp_simple.py read <contact>")
            return
        contact = sys.argv[2]
        await test_read(contact)
    
    elif command == "send":
        if len(sys.argv) < 4:
            print("❌ Usage: python test_whatsapp_simple.py send <contact> <message>")
            return
        contact = sys.argv[2]
        message = " ".join(sys.argv[3:])
        await test_send(contact, message)
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Available: status, unread, read, send")

if __name__ == "__main__":
    asyncio.run(main())
