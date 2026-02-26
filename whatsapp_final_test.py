"""
WhatsApp Final Test - Silver Tier
Robust implementation with proper cleanup
"""

import asyncio
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed")
    print("Run: pip install playwright")
    exit(1)


class WhatsAppTester:
    """Simple WhatsApp tester with proper cleanup."""
    
    def __init__(self):
        self.session_path = Path(".whatsapp_session")
        self.tracking_dir = Path("WhatsApp_Sent")
        self.tracking_dir.mkdir(exist_ok=True)
        self.playwright = None
        self.browser = None
        self.page = None
    
    async def start(self):
        """Start browser and load WhatsApp Web."""
        try:
            print("⏳ Starting Chrome browser...")
            self.playwright = await async_playwright().start()
            
            self.browser = await self.playwright.chromium.launch_persistent_context(
                str(self.session_path),
                headless=False,  # Visible browser
                channel="chrome",
                args=['--disable-blink-features=AutomationControlled']
            )
            
            if len(self.browser.pages) > 0:
                self.page = self.browser.pages[0]
            else:
                self.page = await self.browser.new_page()
            
            print("⏳ Loading WhatsApp Web...")
            await self.page.goto('https://web.whatsapp.com', timeout=60000)
            
            # Wait for WhatsApp to load
            print("⏳ Waiting for WhatsApp to load (30 seconds max)...")
            try:
                await self.page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                print("✅ WhatsApp Web loaded successfully!")
                return True
            except:
                print("❌ WhatsApp Web did not load properly")
                print("   Please check if you're logged in")
                return False
        
        except Exception as e:
            print(f"❌ Error starting browser: {e}")
            return False
    
    async def check_status(self):
        """Check if WhatsApp is connected."""
        if not await self.start():
            return False
        
        try:
            # Check for chat list
            chat_list = await self.page.query_selector('[data-testid="chat-list"]')
            if chat_list:
                print("\n✅ WhatsApp Web is connected and ready!")
                return True
            else:
                print("\n❌ WhatsApp Web not connected")
                return False
        except Exception as e:
            print(f"❌ Error checking status: {e}")
            return False
    
    async def get_unread_chats(self):
        """Get unread chats."""
        if not await self.start():
            return []
        
        try:
            print("\n📬 Checking for unread chats...")
            
            # Wait a bit for chats to load
            await asyncio.sleep(2)
            
            # Find unread indicators
            unread_elements = await self.page.query_selector_all('[aria-label*="unread"]')
            
            if not unread_elements:
                print("   No unread chats found")
                return []
            
            chats = []
            for elem in unread_elements[:5]:  # Limit to 5
                try:
                    name_elem = await elem.query_selector('[data-testid="cell-frame-title"]')
                    name = await name_elem.inner_text() if name_elem else "Unknown"
                    
                    preview_elem = await elem.query_selector('[data-testid="last-msg-text"]')
                    preview = await preview_elem.inner_text() if preview_elem else ""
                    
                    chats.append({'name': name, 'preview': preview})
                    print(f"   📩 {name}: {preview[:50]}...")
                except:
                    continue
            
            return chats
        
        except Exception as e:
            print(f"❌ Error getting unread chats: {e}")
            return []
    
    async def read_messages(self, contact, count=10):
        """Read messages from a contact."""
        if not await self.start():
            return []
        
        try:
            print(f"\n📖 Reading messages from {contact}...")
            
            # Search for contact
            search_box = await self.page.wait_for_selector('[data-testid="chat-list-search"]', timeout=5000)
            await search_box.click()
            await self.page.keyboard.type(contact)
            await asyncio.sleep(1)
            
            # Click first result
            first_result = await self.page.wait_for_selector('[data-testid="cell-frame-container"]', timeout=5000)
            await first_result.click()
            await asyncio.sleep(2)
            
            # Get messages
            message_elements = await self.page.query_selector_all('[data-testid="msg-container"]')
            
            messages = []
            for elem in message_elements[-count:]:
                try:
                    text = await elem.inner_text()
                    messages.append(text)
                    print(f"   💬 {text[:100]}...")
                except:
                    continue
            
            print(f"\n✅ Read {len(messages)} messages from {contact}")
            return messages
        
        except Exception as e:
            print(f"❌ Error reading messages: {e}")
            return []
    
    async def send_message(self, recipient, message):
        """Send a message to a contact."""
        if not await self.start():
            return False
        
        try:
            print(f"\n📤 Sending message to {recipient}...")
            
            # Search for contact
            search_box = await self.page.wait_for_selector('[data-testid="chat-list-search"]', timeout=5000)
            await search_box.click()
            
            # Clear search first
            await self.page.keyboard.press('Control+A')
            await self.page.keyboard.press('Backspace')
            
            await self.page.keyboard.type(recipient)
            await asyncio.sleep(1)
            
            # Click first result
            first_result = await self.page.wait_for_selector('[data-testid="cell-frame-container"]', timeout=5000)
            await first_result.click()
            await asyncio.sleep(1)
            
            # Type message
            message_box = await self.page.wait_for_selector('[data-testid="conversation-compose-box-input"]', timeout=5000)
            await message_box.click()
            await self.page.keyboard.type(message)
            
            # Send
            await self.page.keyboard.press('Enter')
            await asyncio.sleep(1)
            
            print(f"✅ Message sent to {recipient}!")
            
            # Track the message
            self._track_message(recipient, message, True)
            
            return True
        
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            self._track_message(recipient, message, False)
            return False
    
    def _track_message(self, recipient, message, success):
        """Track sent message."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"whatsapp_{timestamp}_{recipient[:20].replace(' ', '_')}.md"
        filepath = self.tracking_dir / filename
        
        status = "✅ Sent" if success else "❌ Failed"
        
        content = f"""---
type: whatsapp_sent
recipient: "{recipient}"
timestamp: "{datetime.now().isoformat()}"
status: "{status}"
---

# WhatsApp Message to {recipient}

**Status**: {status}
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Message
{message}

---

*Sent via WhatsApp Silver Tier*
"""
        
        filepath.write_text(content, encoding='utf-8')
        print(f"📝 Message tracked: {filepath}")
    
    async def cleanup(self):
        """Cleanup resources."""
        try:
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except:
            pass


async def main():
    """Main test function."""
    
    if len(sys.argv) < 2:
        print("=" * 60)
        print("WhatsApp Final Test - Silver Tier")
        print("=" * 60)
        print("\nCommands:")
        print("  python whatsapp_final_test.py status")
        print("  python whatsapp_final_test.py unread")
        print("  python whatsapp_final_test.py read <contact>")
        print("  python whatsapp_final_test.py send <contact> <message>")
        print("\nExamples:")
        print("  python whatsapp_final_test.py status")
        print("  python whatsapp_final_test.py unread")
        print("  python whatsapp_final_test.py read Anisa")
        print('  python whatsapp_final_test.py send Anisa "Hello!"')
        print("\n⚠️  Browser will open (visible mode)")
        print("=" * 60)
        return
    
    command = sys.argv[1].lower()
    tester = WhatsAppTester()
    
    try:
        if command == "status":
            await tester.check_status()
        
        elif command == "unread":
            await tester.get_unread_chats()
        
        elif command == "read":
            if len(sys.argv) < 3:
                print("❌ Usage: python whatsapp_final_test.py read <contact>")
                return
            contact = sys.argv[2]
            await tester.read_messages(contact)
        
        elif command == "send":
            if len(sys.argv) < 4:
                print("❌ Usage: python whatsapp_final_test.py send <contact> <message>")
                return
            contact = sys.argv[2]
            message = " ".join(sys.argv[3:])
            await tester.send_message(contact, message)
        
        else:
            print(f"❌ Unknown command: {command}")
    
    finally:
        print("\n🧹 Cleaning up...")
        await tester.cleanup()
        print("✅ Done!")
        
        # Give time for cleanup
        await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        pass