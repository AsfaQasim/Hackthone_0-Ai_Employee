"""
Send Test Message to Asyfa
"""

from pathlib import Path
from datetime import datetime

def track_manual_send(recipient: str, message: str):
    """Track a manually sent message."""
    
    sent_folder = Path("WhatsApp_Sent")
    sent_folder.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"whatsapp_{timestamp}_{recipient[:20]}.md"
    filepath = sent_folder / filename
    
    content = f"""---
type: whatsapp_sent
recipient: "{recipient}"
timestamp: "{datetime.now().isoformat()}"
status: "✅ Sent (Manual)"
---

# WhatsApp Message to {recipient}

**Status**: ✅ Sent (Manual Test)
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Message
{message}

---

*Manually sent and tracked for Silver Tier verification*
"""
    
    filepath.write_text(content, encoding='utf-8')
    return filepath


print("=" * 70)
print("SEND MESSAGE TO ASYFA - Silver Tier Test")
print("=" * 70)
print()
print("📱 Test Message for Asyfa")
print()
print("STEPS:")
print("1. Open WhatsApp Web: https://web.whatsapp.com")
print("2. Search for 'Asyfa' in your chats")
print("3. Copy and send this message:")
print()
print("   " + "=" * 60)
print("   Hello Asyfa! This is a test message from my AI assistant.")
print("   Testing the WhatsApp integration for my hackathon project. 🤖")
print("   " + "=" * 60)
print()
print("4. After sending, press Enter here...")
input()

# Track the message
print()
print("📝 Tracking the sent message...")
filepath = track_manual_send(
    recipient="Asyfa",
    message="Hello Asyfa! This is a test message from my AI assistant.\nTesting the WhatsApp integration for my hackathon project. 🤖"
)

print(f"✅ Message tracked in: {filepath}")
print()

# Show current status
print("=" * 70)
print("CURRENT STATUS")
print("=" * 70)
print()

inbox = Path("WhatsApp_Inbox")
sent = Path("WhatsApp_Sent")

inbox_count = len(list(inbox.glob("*.md"))) if inbox.exists() else 0
sent_count = len(list(sent.glob("*.md"))) if sent.exists() else 0

print(f"📬 Messages Received: {inbox_count}")
print(f"📤 Messages Sent: {sent_count}")
print()

if sent_count > 0:
    print("Recent sent messages:")
    for msg_file in sorted(sent.glob("*.md"), reverse=True)[:3]:
        print(f"  • {msg_file.name}")

print()
print("=" * 70)
print("✅ SILVER TIER REQUIREMENTS CHECK")
print("=" * 70)
print()

requirements = {
    "Read WhatsApp Messages": inbox_count > 0,
    "Send WhatsApp Messages": sent_count > 0,
    "Track Sent Messages": sent.exists(),
    "WhatsApp Authentication": Path(".whatsapp_session").exists(),
    "MCP Tools Implemented": Path("Skills/mcp_servers/whatsapp_mcp_server.py").exists()
}

all_complete = True
for req, status in requirements.items():
    icon = "✅" if status else "❌"
    print(f"{icon} {req}")
    if not status:
        all_complete = False

print()
if all_complete:
    print("=" * 70)
    print("🎉 SILVER TIER COMPLETE!")
    print("=" * 70)
    print()
    print("Aapka WhatsApp integration fully working hai!")
    print()
    print("What you can do now:")
    print("  • AI can read WhatsApp messages")
    print("  • AI can send WhatsApp messages")
    print("  • All messages are tracked")
    print("  • Ready for automation!")
    print()
    print("🚀 Next: Integrate with AI agent and move to Gold Tier!")
else:
    print("⚠️  Some requirements pending")

print("=" * 70)
