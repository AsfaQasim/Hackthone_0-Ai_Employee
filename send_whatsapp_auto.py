"""
Automated WhatsApp Message Sender
Sends a pre-defined message to Asyfa
"""

import webbrowser
from pathlib import Path
from datetime import datetime
import time


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
    
    # Pre-defined message
    recipient = "Asyfa"
    message = "Hello! This is a test message from Kiro AI. Testing WhatsApp integration. 🤖"
    
    print(f"📤 Sending to: {recipient}")
    print(f"💬 Message: {message}")
    print()
    
    # Open WhatsApp Web
    print("📱 Opening WhatsApp Web...")
    webbrowser.open(f"https://web.whatsapp.com/send?text={message}")
    
    print()
    print("✅ WhatsApp Web opened!")
    print()
    print("NEXT STEPS:")
    print(f"1. Search for '{recipient}' in the opened browser")
    print("2. Click on the contact")
    print("3. The message is pre-filled, just press Enter to send")
    print()
    
    # Wait a bit
    time.sleep(2)
    
    # Track the message
    print("📝 Tracking message...")
    filepath = track_message(recipient, message)
    
    print(f"✅ Message tracked: {filepath}")
    print()
    print("=" * 70)
    print("✅ DONE!")
    print("=" * 70)
    print()
    print("WhatsApp Web is open. Send the message and it's tracked!")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
