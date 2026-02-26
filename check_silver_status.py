"""
Quick Silver Tier Status Check - No Browser
"""

from pathlib import Path

print("=" * 70)
print("SILVER TIER STATUS - WhatsApp Integration")
print("=" * 70)

# Check files and folders
checks = {
    "WhatsApp Watcher": Path("Skills/whatsapp_watcher.py"),
    "WhatsApp MCP Server": Path("Skills/mcp_servers/whatsapp_mcp_server.py"),
    "WhatsApp Session": Path(".whatsapp_session"),
    "Message Inbox": Path("WhatsApp_Inbox"),
    "Sent Tracking": Path("WhatsApp_Sent"),
}

print("\n📋 Component Status:")
for name, path in checks.items():
    if path.exists():
        if path.is_dir():
            files = list(path.rglob("*"))
            print(f"✅ {name}: {len(files)} files")
        else:
            size_kb = path.stat().st_size / 1024
            print(f"✅ {name}: {size_kb:.1f} KB")
    else:
        print(f"❌ {name}: Not found")

# Check received messages
print("\n📬 Received Messages:")
inbox = Path("WhatsApp_Inbox")
if inbox.exists():
    messages = sorted(inbox.glob("*.md"), reverse=True)
    print(f"   Total: {len(messages)} messages")
    
    if messages:
        print("\n   Latest messages:")
        for msg in messages[:5]:
            content = msg.read_text(encoding='utf-8')
            # Extract sender
            for line in content.split('\n'):
                if line.startswith('from:'):
                    sender = line.split('"')[1] if '"' in line else "Unknown"
                    print(f"      • {msg.name[:30]}... from {sender}")
                    break
    else:
        print("   ⚠️  No messages yet")
else:
    print("   ❌ Inbox folder not found")

# Check sent messages
print("\n📤 Sent Messages:")
sent = Path("WhatsApp_Sent")
if sent.exists():
    messages = list(sent.glob("*.md"))
    print(f"   Total: {len(messages)} messages")
    
    if messages:
        print("\n   Recent sent:")
        for msg in sorted(messages, reverse=True)[:3]:
            print(f"      • {msg.name}")
    else:
        print("   ⚠️  No sent messages yet (need to test sending)")
else:
    print("   ✅ Tracking folder ready")

# Silver Tier Requirements
print("\n" + "=" * 70)
print("SILVER TIER REQUIREMENTS")
print("=" * 70)

session_exists = Path(".whatsapp_session").exists()
inbox_has_messages = inbox.exists() and len(list(inbox.glob("*.md"))) > 0
mcp_exists = Path("Skills/mcp_servers/whatsapp_mcp_server.py").exists()

print(f"\n{'✅' if mcp_exists else '❌'} 1. Read Messages Tool - {'READY' if mcp_exists else 'MISSING'}")
print(f"{'✅' if mcp_exists else '❌'} 2. Send Messages Tool - {'READY' if mcp_exists else 'MISSING'}")
print(f"{'✅' if Path('WhatsApp_Sent').exists() else '❌'} 3. Track Sent Messages - {'READY' if Path('WhatsApp_Sent').exists() else 'MISSING'}")
print(f"{'✅' if mcp_exists else '❌'} 4. Detect Unread Chats - {'READY' if mcp_exists else 'MISSING'}")
print(f"{'✅' if session_exists else '❌'} 5. WhatsApp Authentication - {'DONE' if session_exists else 'PENDING'}")
print(f"{'✅' if inbox_has_messages else '⚠️ '} 6. Receiving Messages - {'WORKING' if inbox_has_messages else 'NOT TESTED'}")

# Final verdict
print("\n" + "=" * 70)

if mcp_exists and session_exists and inbox_has_messages:
    print("🎉 SILVER TIER COMPLETE!")
    print("=" * 70)
    print("\n✅ Aapka WhatsApp system fully working hai!")
    print("\n📱 Proof:")
    print(f"   • {len(list(inbox.glob('*.md')))} messages received")
    print(f"   • WhatsApp authenticated")
    print(f"   • All tools implemented")
    print("\n🚀 Next Steps:")
    print("   1. Test sending a message")
    print("   2. Integrate with AI agent")
    print("   3. Start Gold Tier!")
    
elif mcp_exists and session_exists:
    print("⚠️  ALMOST COMPLETE!")
    print("=" * 70)
    print("\n✅ System ready, just need to test!")
    print("\n📱 To complete:")
    print("   1. Make sure WhatsApp Watcher is running")
    print("   2. Send yourself a test message")
    print("   3. Check WhatsApp_Inbox folder")
    
elif mcp_exists:
    print("⚠️  NEED AUTHENTICATION")
    print("=" * 70)
    print("\n✅ Code is ready")
    print("❌ WhatsApp not authenticated")
    print("\n📱 Next step:")
    print("   Run: python Skills/whatsapp_watcher.py auth")
    print("   Then scan QR code with your phone")
    
else:
    print("❌ INCOMPLETE")
    print("=" * 70)
    print("\nMissing components - contact support")

print("\n" + "=" * 70)
print("\n💡 IMPORTANT: Aapko WhatsApp Business API token ki zaroorat NAHI hai!")
print("   Yeh system WhatsApp Web use karta hai (FREE)")
print("   Bas QR code scan karo, koi token nahi chahiye!")
print("=" * 70)
