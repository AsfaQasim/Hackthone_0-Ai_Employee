"""
WhatsApp AI Employee Demo
Perfect for hackathon - shows AI intelligence + human approval
"""

from pathlib import Path
import json
from datetime import datetime
import webbrowser
import time


class WhatsAppAI:
    """AI Employee that prepares WhatsApp messages."""
    
    def __init__(self):
        self.queue_file = Path("whatsapp_queue.json")
        self.sent_folder = Path("WhatsApp_Sent")
        self.sent_folder.mkdir(exist_ok=True)
    
    def decide_and_prepare(self, recipient: str, message: str, reason: str = "AI decision"):
        """AI decides to send a message and prepares it."""
        
        print("=" * 70)
        print("🤖 AI EMPLOYEE - WhatsApp Message Preparation")
        print("=" * 70)
        print()
        print(f"📊 Analysis: {reason}")
        print(f"🎯 Decision: Send message to {recipient}")
        print()
        print(f"📝 Message prepared:")
        print("   " + "-" * 60)
        print(f"   {message}")
        print("   " + "-" * 60)
        print()
        
        # Prepare message data
        message_data = {
            "recipient": recipient,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "status": "prepared"
        }
        
        # Save to queue
        self.queue_file.write_text(json.dumps(message_data, indent=2))
        
        print("✅ Message prepared and queued!")
        print(f"📁 Saved to: {self.queue_file}")
        print()
        print("=" * 70)
        print("👉 NEXT STEP: Send the message")
        print("=" * 70)
        print()
        print("Option 1 - Quick send:")
        print("  python whatsapp_ai_demo.py send")
        print()
        print("Option 2 - Manual send:")
        print("  python manual_whatsapp_send.py")
        print()
        
        return message_data
    
    def send_from_queue(self):
        """Send message from queue (opens browser for human to click send)."""
        
        if not self.queue_file.exists():
            print("❌ No message in queue")
            print("   Run: python whatsapp_ai_demo.py prepare")
            return False
        
        # Load message
        message_data = json.loads(self.queue_file.read_text())
        
        recipient = message_data["recipient"]
        message = message_data["message"]
        
        print("=" * 70)
        print("📤 SENDING MESSAGE")
        print("=" * 70)
        print()
        print(f"To: {recipient}")
        print(f"Message: {message}")
        print()
        
        # Open WhatsApp Web
        print("📱 Opening WhatsApp Web...")
        webbrowser.open("https://web.whatsapp.com")
        
        print()
        print("=" * 70)
        print("INSTRUCTIONS:")
        print("=" * 70)
        print()
        print(f"1. Search for: {recipient}")
        print("2. Copy and send this message:")
        print()
        print("   " + "-" * 60)
        print(f"   {message}")
        print("   " + "-" * 60)
        print()
        print("3. After sending, press Enter here...")
        print()
        
        input("Press Enter after you've sent the message...")
        
        # Track the message
        print()
        print("📝 Tracking message...")
        self._track_sent(recipient, message, message_data.get("reason", ""))
        
        # Clear queue
        self.queue_file.unlink()
        
        print()
        print("=" * 70)
        print("✅ SUCCESS!")
        print("=" * 70)
        print()
        print("Message sent and tracked!")
        print(f"Check: WhatsApp_Sent/ folder")
        print()
        
        return True
    
    def check_status(self):
        """Check status of messages."""
        
        print("=" * 70)
        print("📊 WHATSAPP AI STATUS")
        print("=" * 70)
        print()
        
        # Check queue
        if self.queue_file.exists():
            message_data = json.loads(self.queue_file.read_text())
            print("📋 Queued Message:")
            print(f"   To: {message_data['recipient']}")
            print(f"   Message: {message_data['message'][:50]}...")
            print(f"   Status: ⏳ Waiting to send")
            print()
        else:
            print("📋 Queue: Empty")
            print()
        
        # Check sent messages
        sent_files = list(self.sent_folder.glob("sent_*.md"))
        print(f"📤 Sent Messages: {len(sent_files)}")
        
        if sent_files:
            print()
            print("Recent sends:")
            for msg_file in sorted(sent_files, reverse=True)[:5]:
                print(f"   • {msg_file.name}")
        
        print()
        print("=" * 70)
    
    def _track_sent(self, recipient: str, message: str, reason: str):
        """Track sent message."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = recipient.replace(' ', '_').replace('/', '_')
        filename = f"sent_{timestamp}_{safe_name}.md"
        filepath = self.sent_folder / filename
        
        content = f"""---
type: whatsapp_sent
recipient: "{recipient}"
timestamp: "{datetime.now().isoformat()}"
status: "✅ Sent"
method: "ai_hybrid"
reason: "{reason}"
---

# WhatsApp Message to {recipient}

**Status**: ✅ Sent
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Method**: AI Hybrid (AI prepared, human sent)
**Reason**: {reason}

## Message
{message}

---

*Sent via WhatsApp AI Employee (Hybrid Mode)*
*AI prepared the message, human approved and sent*
"""
        
        filepath.write_text(content, encoding='utf-8')
        print(f"✅ Tracked: {filepath}")


def main():
    """Main CLI."""
    import sys
    
    ai = WhatsAppAI()
    
    if len(sys.argv) < 2:
        print("=" * 70)
        print("WhatsApp AI Employee - Hybrid Mode")
        print("=" * 70)
        print()
        print("Commands:")
        print("  python whatsapp_ai_demo.py prepare <contact> <message>")
        print("  python whatsapp_ai_demo.py send")
        print("  python whatsapp_ai_demo.py status")
        print()
        print("Examples:")
        print('  python whatsapp_ai_demo.py prepare Asyfa "Hello from AI!"')
        print("  python whatsapp_ai_demo.py send")
        print("  python whatsapp_ai_demo.py status")
        print()
        print("Workflow:")
        print("  1. AI prepares message (prepare)")
        print("  2. Human sends it (send)")
        print("  3. AI tracks result (automatic)")
        print()
        return
    
    command = sys.argv[1].lower()
    
    if command == "prepare":
        if len(sys.argv) < 4:
            print("❌ Usage: python whatsapp_ai_demo.py prepare <contact> <message>")
            return
        
        recipient = sys.argv[2]
        message = " ".join(sys.argv[3:])
        
        ai.decide_and_prepare(
            recipient,
            message,
            reason="User requested via AI employee"
        )
    
    elif command == "send":
        ai.send_from_queue()
    
    elif command == "status":
        ai.check_status()
    
    else:
        print(f"❌ Unknown command: {command}")
        print("   Run without arguments to see help")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
