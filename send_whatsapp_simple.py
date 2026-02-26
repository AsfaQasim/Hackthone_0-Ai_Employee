"""
Simple WhatsApp Message Sender
Opens WhatsApp Web and helps you send a message
"""

import webbrowser
from pathlib import Path
from datetime import datetime


def track_message(recipient: str, message: str):
    """Track sent message."""
    sent_folder = Path("WhatsApp_Sent")
    sent_folder.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sent_{timestamp}_{recipient.replace(' ', '_')}.md"
    filepath = sent_folder / filename
    
    content = f"""---
type: whatsapp_sent
recipient: "{recipient}"
timestamp: "{datetime.now().isoformat()}"
status: "✅ Sent"
---

# WhatsApp Message to {recipient}

**Status**: ✅ Sent
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Message
{message}

---

*Sent via Kiro AI WhatsApp Integration*
"""
    
    filepath.write_text(content, encoding='utf-8')
    return filepath


def main():
    print("=" * 70)
    print("WhatsApp Message Sender - Kiro AI")
    print("=" * 70)
    print()
    
    # Get recipient and message
    recipient = input("Enter recipient name (e.g., Asyfa): ").strip()
    if not recipient:
        recipient = "Asyfa"
    
    print()
    print("Enter your message (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "" and lines:
            break
        lines.append(line)
    
    message = "\n".join(lines)
    
    if not message:
        message = "Hello! This is a test message from Kiro AI. 🤖"
    
    print()
    print("=" * 70)
    print(f"Recipient: {recipient}")
    print(f"Message: {message}")
    print("=" * 70)
    print()
    
    # Open WhatsApp Web
    print("📱 Opening WhatsApp Web...")
    webbrowser.open("https://web.whatsapp.com")
    
    print()
    print("INSTRUCTIONS:")
    print("1. WhatsApp Web should open in your browser")
    print(f"2. Search for '{recipient}'")
    print("3. Copy and send this message:")
    print()
    print("   " + "-" * 60)
    print(f"   {message}")
    print("   " + "-" * 60)
    print()
    
    input("Press Enter after you've sent the message...")
    
    # Track the message
    print()
    print("📝 Tracking message...")
    filepath = track_message(recipient, message)
    
    print(f"✅ Message tracked: {filepath}")
    print()
    print("=" * 70)
    print("✅ SUCCESS!")
    print("=" * 70)
    print()
    print("Message sent and tracked.")
    print("Check WhatsApp_Sent folder for details.")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
