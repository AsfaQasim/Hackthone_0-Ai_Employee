"""
WhatsApp AI Automation
Fully automated WhatsApp operations for AI agent
- Read unread messages
- Send messages
- Track everything
"""

import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import json

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("❌ Playwright not installed")
    print("Run: pip install playwright")
    exit(1)


class WhatsAppAI:
    """WhatsApp automation for AI agent."""
    
    def __init__(self):
        self.session_path = Path(".whatsapp_session")
        self.inbox_path = Path("WhatsApp_Inbox")
        self.sent_path = Path("WhatsApp_Sent")
        self.inbox_path.mkdir(exist_ok=True)
        self.sent_path.mkdir(exist_ok=True)
        
        self.playwright = None
        self.browser = None
        self.page = None
    
    async def start(self):
        """Start browser and load WhatsApp."""
        print("⏳ Starting WhatsApp AI...")
        
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch_persistent_context(
            str(self.session_path),
            headless=False,  # Visible for debugging
            channel="chrome",
            args=['--disable-blink-features=AutomationControlled']
        )
        
        self.page = self.browser.pages[0] if self.browser.pages else await self.browser.new_page()
        
        print("⏳ Loading WhatsApp Web...")
        await self.page.goto('https://web.whatsapp.com', wait_until='domcontentloaded', timeout=60000)
        
        # Wait for WhatsApp to load
        print("⏳ Waiting for WhatsApp...")
        try:
            await self.page.wait_for_selector('#pane-side', timeout=60000)
            print("✅ WhatsApp loaded!")
            await asyncio.sleep(3)
            return True
        except:
            print("❌ WhatsApp didn't load")
            return False
    
    async def get_unread_messages(self) -> List[Dict]:
        """Get all unread messages."""
        print("\n📬 Checking for unread messages...")
        
        unread_messages = []
        
        try:
            # Find all unread chats
            await asyncio.sleep(2)
            
            # Get all chat elements
            chats = await self.page.query_selector_all('div[role="listitem"]')
            
            for chat in chats[:10]:  # Check first 10 chats
                try:
                    # Check if chat has unread indicator
                    unread_badge = await chat.query_selector('span[data-testid="icon-unread-count"]')
                    if not unread_badge:
                        continue
                    
                    # Get chat name
                    name_elem = await chat.query_selector('span[title]')
                    if not name_elem:
                        continue
                    
                    name = await name_elem.get_attribute('title')
                    
                    # Get preview text
                    preview_elem = await chat.query_selector('span[dir="ltr"]')
                    preview = await preview_elem.inner_text() if preview_elem else ""
                    
                    print(f"   📩 Unread from: {name}")
                    print(f"      Preview: {preview[:50]}...")
                    
                    unread_messages.append({
                        'name': name,
                        'preview': preview,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    continue
            
            print(f"\n✅ Found {len(unread_messages)} unread messages")
            return unread_messages
            
        except Exception as e:
            print(f"❌ Error getting unread messages: {e}")
            return []
    
    async def read_messages(self, contact: str, count: int = 10) -> List[str]:
        """Read messages from a specific contact."""
        print(f"\n📖 Reading messages from {contact}...")
        
        try:
            # Search for contact
            search_box = await self.page.query_selector('div[contenteditable="true"][data-tab="3"]')
            if not search_box:
                print("❌ Search box not found")
                return []
            
            await search_box.click()
            await asyncio.sleep(0.5)
            
            # Clear and type
            await self.page.keyboard.press('Control+A')
            await self.page.keyboard.press('Backspace')
            await asyncio.sleep(0.5)
            await self.page.keyboard.type(contact)
            await asyncio.sleep(2)
            
            # Click first result
            first_result = await self.page.query_selector('div[role="listitem"]')
            if not first_result:
                print(f"❌ Contact '{contact}' not found")
                return []
            
            await first_result.click()
            await asyncio.sleep(2)
            
            # Get messages
            message_elements = await self.page.query_selector_all('div[data-testid="msg-container"]')
            
            messages = []
            for elem in message_elements[-count:]:
                try:
                    text = await elem.inner_text()
                    messages.append(text)
                    print(f"   💬 {text[:80]}...")
                except:
                    continue
            
            print(f"\n✅ Read {len(messages)} messages from {contact}")
            
            # Save to inbox
            self._save_to_inbox(contact, messages)
            
            return messages
            
        except Exception as e:
            print(f"❌ Error reading messages: {e}")
            return []
    
    async def send_message(self, recipient: str, message: str) -> bool:
        """Send a message to a contact."""
        print(f"\n📤 Sending message to {recipient}...")
        print(f"💬 Message: {message[:50]}...")
        
        try:
            # Search for contact
            search_box = await self.page.query_selector('div[contenteditable="true"][data-tab="3"]')
            if not search_box:
                print("❌ Search box not found")
                return False
            
            await search_box.click()
            await asyncio.sleep(0.5)
            
            # Clear and type
            await self.page.keyboard.press('Control+A')
            await self.page.keyboard.press('Backspace')
            await asyncio.sleep(0.5)
            await self.page.keyboard.type(recipient)
            await asyncio.sleep(3)
            
            # Click first result
            first_result = await self.page.query_selector('div[role="listitem"]')
            if not first_result:
                print(f"❌ Contact '{recipient}' not found")
                return False
            
            await first_result.click()
            await asyncio.sleep(2)
            
            # Find message input
            message_input = await self.page.query_selector('div[contenteditable="true"][data-tab="10"]')
            if not message_input:
                print("❌ Message input not found")
                return False
            
            # Type and send
            await message_input.click()
            await asyncio.sleep(0.5)
            
            # Type message line by line to handle multiline
            lines = message.split('\n')
            for i, line in enumerate(lines):
                await self.page.keyboard.type(line)
                if i < len(lines) - 1:
                    await self.page.keyboard.press('Shift+Enter')
            
            await asyncio.sleep(1)
            await self.page.keyboard.press('Enter')
            await asyncio.sleep(2)
            
            print("✅ Message sent!")
            
            # Track the message
            self._save_to_sent(recipient, message)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    async def close(self):
        """Close browser."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    def _save_to_inbox(self, contact: str, messages: List[str]):
        """Save received messages to inbox."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"message_{timestamp}_from_{contact.replace(' ', '_')}.md"
        filepath = self.inbox_path / filename
        
        messages_text = '\n\n'.join([f"> {msg}" for msg in messages])
        
        content = f"""---
type: whatsapp_received
from: "{contact}"
timestamp: "{datetime.now().isoformat()}"
message_count: {len(messages)}
---

# WhatsApp Messages from {contact}

**Received**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Message Count**: {len(messages)}

## Messages

{messages_text}

---

*Received via WhatsApp AI Automation*
"""
        
        filepath.write_text(content, encoding='utf-8')
        print(f"   📝 Saved to: {filepath}")
    
    def _save_to_sent(self, recipient: str, message: str):
        """Save sent message to sent folder."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sent_{timestamp}_{recipient.replace(' ', '_')}.md"
        filepath = self.sent_path / filename
        
        content = f"""---
type: whatsapp_sent
recipient: "{recipient}"
timestamp: "{datetime.now().isoformat()}"
status: "✅ Sent"
method: "ai_automation"
---

# WhatsApp Message to {recipient}

**Status**: ✅ Sent
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Method**: AI Automation

## Message
{message}

---

*Sent via WhatsApp AI Automation*
"""
        
        filepath.write_text(content, encoding='utf-8')
        print(f"   📝 Tracked: {filepath}")


# CLI Interface for AI
async def main():
    """Main function for AI to use."""
    import sys
    
    if len(sys.argv) < 2:
        print("=" * 70)
        print("WhatsApp AI Automation")
        print("=" * 70)
        print()
        print("Commands:")
        print("  python whatsapp_ai_automation.py unread")
        print("  python whatsapp_ai_automation.py read <contact>")
        print("  python whatsapp_ai_automation.py send <contact> <message>")
        print()
        print("Examples:")
        print("  python whatsapp_ai_automation.py unread")
        print("  python whatsapp_ai_automation.py read Anisa")
        print('  python whatsapp_ai_automation.py send Asyfa "Hello from AI!"')
        print()
        return
    
    command = sys.argv[1].lower()
    
    wa = WhatsAppAI()
    
    try:
        if not await wa.start():
            print("❌ Failed to start WhatsApp")
            return
        
        if command == "unread":
            messages = await wa.get_unread_messages()
            print(f"\n📊 Total unread: {len(messages)}")
        
        elif command == "read":
            if len(sys.argv) < 3:
                print("❌ Usage: python whatsapp_ai_automation.py read <contact>")
                return
            contact = sys.argv[2]
            messages = await wa.read_messages(contact)
        
        elif command == "send":
            if len(sys.argv) < 4:
                print("❌ Usage: python whatsapp_ai_automation.py send <contact> <message>")
                return
            recipient = sys.argv[2]
            message = " ".join(sys.argv[3:])
            success = await wa.send_message(recipient, message)
            if success:
                print("\n✅ Message sent successfully!")
            else:
                print("\n❌ Failed to send message")
        
        else:
            print(f"❌ Unknown command: {command}")
        
        # Keep browser open for a moment
        await asyncio.sleep(3)
        
    finally:
        await wa.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
