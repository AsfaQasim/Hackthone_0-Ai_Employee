"""
Manual WhatsApp Send Helper
Opens WhatsApp and helps you send manually
"""

import webbrowser
from pathlib import Path
from datetime import datetime


def main():
    print("=" * 70)
    print("WhatsApp Manual Send Helper")
    print("=" * 70)
    print()
    
    recipient = "Asyfa"
    message = "Hello! This is a test message from Kiro AI. Testing WhatsApp integration. 🤖"
    
    print(f"📤 Recipient: {recipient}")
    print(f"💬 Message: {message}")
    print()
    
    # Open WhatsApp Web
    print("📱 Opening WhatsApp Web...")
    webbrowser.open("https://web.whatsapp.com")
    
    print()
    print("=" * 70)
    print("INSTRUCTIONS:")
    print("=" * 70)
    print()
    print("1. WhatsApp Web will open in your browser")
    print("2. Search for 'Asyfa' in the search box")
    print("3. Click on Asyfa's chat")
    print("4. Copy this message and send:")
    print()
    print("   " + "-" * 60)
    print(f"   {message}")
    print("   " + "-" * 60)
    print()
    print("5. After sending, come back here and press Enter")
    print()
    print("=" * 70)
    print()
    
    input("Press Enter after you've sent the message...")
    
    # Track the message
    print()
    print("📝 Tracking message...")
    
    sent_folder = Path("WhatsApp_Sent")
    sent_folder.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sent_{timestamp}_Asyfa.md"
    filepath = sent_folder / filename
    
    content = f"""---
type: whatsapp_sent
recipient: "Asyfa"
timestamp: "{datetime.now().isoformat()}"
status: "✅ Sent"
method: "manual_with_helper"
---

# WhatsApp Message to Asyfa

**Status**: ✅ Sent
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Method**: Manual with Helper Script

## Message
{message}

---

*Sent via Kiro AI WhatsApp Integration*
"""
    
    filepath.write_text(content, encoding='utf-8')
    
    print(f"✅ Message tracked: {filepath}")
    print()
    print("=" * 70)
    print("✅ DONE!")
    print("=" * 70)
    print()
    print("Message sent and tracked successfully!")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
