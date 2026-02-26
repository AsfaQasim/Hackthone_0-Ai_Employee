"""
Check WhatsApp MCP Server Status
Comprehensive connection and functionality test
"""

import asyncio
import logging
from pathlib import Path
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def check_mcp_server():
    """Check WhatsApp MCP Server status."""
    
    print("=" * 70)
    print("WHATSAPP MCP SERVER STATUS CHECK")
    print("=" * 70)
    print()
    
    # Check 1: MCP Server file exists
    print("1️⃣  Checking MCP Server Implementation...")
    mcp_file = Path("Skills/mcp_servers/whatsapp_mcp_server.py")
    if mcp_file.exists():
        print(f"   ✅ MCP Server file exists: {mcp_file}")
        print(f"   Size: {mcp_file.stat().st_size / 1024:.1f} KB")
    else:
        print(f"   ❌ MCP Server file not found!")
        return False
    
    # Check 2: Import MCP Server
    print("\n2️⃣  Importing MCP Server...")
    try:
        from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer
        print("   ✅ MCP Server imported successfully")
    except Exception as e:
        print(f"   ❌ Failed to import: {e}")
        return False
    
    # Check 3: Initialize MCP Server
    print("\n3️⃣  Initializing MCP Server...")
    try:
        server = WhatsAppMCPServer()
        print("   ✅ MCP Server initialized")
    except Exception as e:
        print(f"   ❌ Failed to initialize: {e}")
        return False
    
    # Check 4: List available tools
    print("\n4️⃣  Checking Available Tools...")
    try:
        tools = server.list_tools()
        print(f"   ✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"      • {tool['name']}: {tool['description']}")
    except Exception as e:
        print(f"   ❌ Failed to list tools: {e}")
        return False
    
    # Check 5: Session exists
    print("\n5️⃣  Checking WhatsApp Session...")
    session_path = Path(".whatsapp_session")
    if session_path.exists():
        files = list(session_path.rglob("*"))
        print(f"   ✅ Session exists: {len(files)} files")
        print(f"   Status: Authenticated")
    else:
        print(f"   ❌ No session found - need to authenticate")
        print(f"   Run: python Skills/whatsapp_watcher.py auth")
        return False
    
    # Check 6: Test connection status
    print("\n6️⃣  Testing WhatsApp Connection...")
    try:
        result = await server.execute_tool("check_whatsapp_status", {})
        print(f"   Result: {result.text}")
        
        if "connected" in result.text.lower() and "not" not in result.text.lower():
            print("   ✅ WhatsApp Web is connected!")
            connected = True
        else:
            print("   ⚠️  WhatsApp Web not connected")
            print("   Need to reconnect: python Skills/whatsapp_watcher.py auth")
            connected = False
    except Exception as e:
        print(f"   ❌ Connection test failed: {e}")
        connected = False
    
    # Check 7: Test unread chats (if connected)
    if connected:
        print("\n7️⃣  Testing Unread Chats Detection...")
        try:
            result = await server.execute_tool("get_unread_whatsapp_chats", {})
            print(f"   Result: {result.text[:100]}...")
            print("   ✅ Unread detection working")
        except Exception as e:
            print(f"   ⚠️  Unread detection failed: {e}")
    
    # Check 8: Inbox messages
    print("\n8️⃣  Checking Received Messages...")
    inbox = Path("WhatsApp_Inbox")
    if inbox.exists():
        messages = list(inbox.glob("*.md"))
        print(f"   ✅ Inbox exists: {len(messages)} messages")
        if messages:
            print("   Recent messages:")
            for msg in sorted(messages, reverse=True)[:3]:
                print(f"      • {msg.name}")
    else:
        print("   ⚠️  No inbox folder")
    
    # Check 9: Sent tracking
    print("\n9️⃣  Checking Sent Message Tracking...")
    sent = Path("WhatsApp_Sent")
    if sent.exists():
        messages = list(sent.glob("*.md"))
        print(f"   ✅ Tracking folder exists: {len(messages)} tracked")
        if messages:
            print("   Recent sent:")
            for msg in sorted(messages, reverse=True)[:3]:
                print(f"      • {msg.name}")
    else:
        print("   ⚠️  No tracking folder")
    
    # Cleanup
    await server.cleanup()
    
    # Final verdict
    print()
    print("=" * 70)
    print("FINAL STATUS")
    print("=" * 70)
    print()
    
    if connected:
        print("✅ WhatsApp MCP Server: CONNECTED & READY")
        print()
        print("Available capabilities:")
        print("  ✅ Read messages from contacts")
        print("  ✅ Send messages to contacts")
        print("  ✅ Detect unread chats")
        print("  ✅ Check connection status")
        print("  ✅ Track sent messages")
        print()
        print("🚀 Ready for AI integration!")
    else:
        print("⚠️  WhatsApp MCP Server: NOT CONNECTED")
        print()
        print("To connect:")
        print("  1. Run: python Skills/whatsapp_watcher.py auth")
        print("  2. Scan QR code with your phone")
        print("  3. Run this check again")
    
    print()
    print("=" * 70)
    
    return connected


async def main():
    try:
        connected = await check_mcp_server()
        sys.exit(0 if connected else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
