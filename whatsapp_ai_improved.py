"""
WhatsApp AI Automation - Improved Version
More robust with better timing and error handling
"""

import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import re

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("❌ Playwright not installed")
    exit(1)


class WhatsAppAI:
    """Improved WhatsApp automation for AI agent."""
    
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
        print("⏳ Starting WhatsApp AI (Improved)...")
        
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch_persistent_context(
            str(self.session_path),
            headless=False,
            channel="chrome",
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
        
        self.page = self.browser.pages[0] if self.browser.pages else await self.browser.new_page()
        
        # Set longer timeout
        self.page.set_default_timeout(60000)
        
        print("⏳ Loading WhatsApp Web...")
        await self.page.goto('https://web.whatsapp.com', wait_until='networkidle', timeout=90000)
        
        # Wait for WhatsApp to load - try multiple indicators
        print("⏳ Waiting for WhatsApp to load...")
        
        loaded = False
        for selector in ['#pane-side', '[data-testid="chat-list"]', 'div[id="app"]']:
            try:
                await self.page.wait_for_selector(selector, timeout=30000)
                print(f"✅ WhatsApp loaded! (found: {selector})")
                loaded = True
                break
            except:
                continue
        
        if not loaded:
            print("❌ WhatsApp didn't load properly")
            return False
        
        # Extra wait for everything to settle
        await asyncio.sleep(5)
        return True
    
    async def get_unread_messages(self) -> List[Dict]:
        """Get all unread messages."""
        print("\n📬 Checking for unread messages...")
        
        unread_messages = []
        
        try:
            await asyncio.sleep(2)
            
            # Get all chat elements
            chats = await self.page.query_selector_all('div[role="listitem"]')
            print(f"   Found {len(chats)} total chats")
            
            for i, chat in enumerate(chats[:15]):  # Check first 15
                try:
                    # Check for unread badge
                    unread_badge = await chat.query_selector('span[data-testid="icon-unread-count"]')
                    if not unread_badge:
                        continue
                    
                    # Get chat name - try multiple selectors
                    name = None
                    for selector in ['span[title]', 'span[dir="auto"]']:
                        try:
                            name_elem = await chat.query_selector(selector)
                            if name_elem:
                                name = await name_elem.get_attribute('title')
                                if not name:
                                    name = await name_elem.inner_text()
                                if name:
                                    break
                        except:
                            continue
                    
                    if not name:
                        continue
                    
                    # Get preview
                    preview = ""
                    try:
                        preview_elem = await chat.query_selector('span[dir="ltr"]')
                        if preview_elem:
                            preview = await preview_elem.inner_text()
                    except:
                        pass
                    
                    print(f"   📩 Unread from: {name}")
                    if preview:
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
        
        # Try to open the chat
        if not await self._open_chat(contact):
            return []
        
        try:
            # Wait for messages to load
            await asyncio.sleep(3)
            
            # Get messages
            message_elements = await self.page.query_selector_all('div[data-testid="msg-container"]')
            
            messages = []
            for elem in message_elements[-count:]:
                try:
                    text = await elem.inner_text()
                    if text:
                        messages.append(text)
                        print(f"   💬 {text[:80]}...")
                except:
                    continue
            
            print(f"\n✅ Read {len(messages)} messages from {contact}")
            
            # Save to inbox
            if messages:
                self._save_to_inbox(contact, messages)
            
            return messages
            
        except Exception as e:
            print(f"❌ Error reading messages: {e}")
            return []
    
    async def send_message(self, recipient: str, message: str) -> bool:
        """Send a message to a contact."""
        print(f"\n📤 Sending message to {recipient}...")
        print(f"💬 Message: {message[:80]}...")
        
        # Try to open the chat
        if not await self._open_chat(recipient):
            return False
        
        try:
            # Wait for chat to fully load
            await asyncio.sleep(3)
            
            # Find message input - try multiple selectors
            message_input = None
            input_selectors = [
                'div[contenteditable="true"][data-tab="10"]',
                'div[contenteditable="true"][data-testid="conversation-compose-box-input"]',
                'div[role="textbox"][contenteditable="true"]',
                'footer div[contenteditable="true"]'
            ]
            
            for selector in input_selectors:
                try:
                    message_input = await self.page.wait_for_selector(selector, timeout=5000)
                    if message_input:
                        print(f"   ✅ Found input: {selector}")
                        break
                except:
                    continue
            
            if not message_input:
                print("   ❌ Message input not found")
                print("   Trying alternative method...")
                
                # Alternative: Click on the chat area first
                try:
                    chat_area = await self.page.query_selector('div[data-testid="conversation-panel-body"]')
                    if chat_area:
                        await chat_area.click()
                        await asyncio.sleep(1)
                        
                        # Try again
                        message_input = await self.page.query_selector('div[contenteditable="true"]')
                except:
                    pass
            
            if not message_input:
                print("   ❌ Could not find message input")
                return False
            
            # Click and focus
            await message_input.click()
            await asyncio.sleep(1)
            
            # Type message
            print("   ⌨️  Typing message...")
            
            # Handle multiline messages
            lines = message.split('\n')
            for i, line in enumerate(lines):
                await self.page.keyboard.type(line, delay=10)  # Slower typing
                if i < len(lines) - 1:
                    await self.page.keyboard.press('Shift+Enter')
                    await asyncio.sleep(0.2)
            
            await asyncio.sleep(1)
            
            # Send
            print("   📨 Sending...")
            await self.page.keyboard.press('Enter')
            await asyncio.sleep(3)
            
            print("   ✅ Message sent!")
            
            # Track the message
            self._save_to_sent(recipient, message)
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error sending message: {e}")
            return False
    
    async def _open_chat(self, contact: str) -> bool:
        """Open a chat with a contact."""
        print(f"   🔍 Opening chat with {contact}...")
        
        try:
            # Find search box - try multiple selectors
            search_box = None
            search_selectors = [
                'div[contenteditable="true"][data-tab="3"]',
                '[data-testid="chat-list-search"]',
                'div[title="Search input textbox"]'
            ]
            
            for selector in search_selectors:
                try:
                    search_box = await self.page.wait_for_selector(selector, timeout=5000)
                    if search_box:
                        print(f"   ✅ Found search: {selector}")
                        break
                except:
                    continue
            
            if not search_box:
                print("   ❌ Search box not found")
                return False
            
            # Click and clear
            await search_box.click()
            await asyncio.sleep(0.5)
            await self.page.keyboard.press('Control+A')
            await self.page.keyboard.press('Backspace')
            await asyncio.sleep(0.5)
            
            # Type contact name slowly
            print(f"   ⌨️  Searching for: {contact}")
            await self.page.keyboard.type(contact, delay=50)  # Slower typing
            await asyncio.sleep(4)  # Wait longer for results
            
            # Look for results - try to find the exact match
            print("   🔍 Looking for chat result...")
            
            # Get all visible chat results
            results = await self.page.query_selector_all('div[role="listitem"]')
            print(f"   Found {len(results)} results")
            
            if len(results) == 0:
                print(f"   ❌ No results for '{contact}'")
                print("   💡 Try using the exact name from WhatsApp")
                return False
            
            # Click first result (most relevant)
            print("   ✅ Clicking first result...")
            await results[0].click()
            await asyncio.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error opening chat: {e}")
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
        safe_name = re.sub(r'[^\w\s-]', '', contact).replace(' ', '_')
        filename = f"message_{timestamp}_from_{safe_name}.md"
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

*Received via WhatsApp AI Automation (Improved)*
"""
        
        filepath.write_text(content, encoding='utf-8')
        print(f"   📝 Saved to: {filepath}")
    
    def _save_to_sent(self, recipient: str, message: str):
        """Save sent message to sent folder."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = re.sub(r'[^\w\s-]', '', recipient).replace(' ', '_')
        filename = f"sent_{timestamp}_{safe_name}.md"
        filepath = self.sent_path / filename
        
        content = f"""---
type: whatsapp_sent
recipient: "{recipient}"
timestamp: "{datetime.now().isoformat()}"
status: "✅ Sent"
method: "ai_automation_improved"
---

# WhatsApp Message to {recipient}

**Status**: ✅ Sent
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Method**: AI Automation (Improved)

## Message
{message}

---

*Sent via WhatsApp AI Automation (Improved)*
"""
        
        filepath.write_text(content, encoding='utf-8')
        print(f"   📝 Tracked: {filepath}")


# CLI Interface
async def main():
    """Main function for AI to use."""
    import sys
    
    if len(sys.argv) < 2:
        print("=" * 70)
        print("WhatsApp AI Automation (Improved)")
        print("=" * 70)
        print()
        print("Commands:")
        print("  python whatsapp_ai_improved.py unread")
        print("  python whatsapp_ai_improved.py read <contact>")
        print("  python whatsapp_ai_improved.py send <contact> <message>")
        print()
        print("Examples:")
        print("  python whatsapp_ai_improved.py unread")
        print("  python whatsapp_ai_improved.py read Anisa")
        print('  python whatsapp_ai_improved.py send "Asyfa Qasim" "Hello!"')
        print()
        print("Tips:")
        print("  - Use exact contact names from WhatsApp")
        print("  - Close other Chrome windows first")
        print("  - Wait for script to complete")
        print()
        return
    
    command = sys.argv[1].lower()
    
    wa = WhatsAppAI()
    
    try:
        if not await wa.start():
            print("\n❌ Failed to start WhatsApp")
            print("   Try: python auth_whatsapp_simple.py")
            return
        
        if command == "unread":
            messages = await wa.get_unread_messages()
            print(f"\n📊 Total unread: {len(messages)}")
            for msg in messages:
                print(f"   • {msg['name']}: {msg['preview'][:50]}...")
        
        elif command == "read":
            if len(sys.argv) < 3:
                print("❌ Usage: python whatsapp_ai_improved.py read <contact>")
                return
            contact = sys.argv[2]
            messages = await wa.read_messages(contact)
            if messages:
                print(f"\n✅ Successfully read {len(messages)} messages")
        
        elif command == "send":
            if len(sys.argv) < 4:
                print("❌ Usage: python whatsapp_ai_improved.py send <contact> <message>")
                return
            recipient = sys.argv[2]
            message = " ".join(sys.argv[3:])
            success = await wa.send_message(recipient, message)
            if success:
                print("\n" + "=" * 70)
                print("✅ SUCCESS!")
                print("=" * 70)
                print(f"\nMessage sent to {recipient}")
                print("Check WhatsApp_Sent folder for tracking")
            else:
                print("\n" + "=" * 70)
                print("❌ FAILED")
                print("=" * 70)
                print("\nTroubleshooting:")
                print("1. Check contact name is exact")
                print("2. Make sure WhatsApp Web is logged in")
                print("3. Try: python test_whatsapp_contacts.py")
        
        else:
            print(f"❌ Unknown command: {command}")
        
        # Keep browser open briefly
        print("\n⏳ Keeping browser open for 5 seconds...")
        await asyncio.sleep(5)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n🧹 Closing browser...")
        await wa.close()
        print("✅ Done!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
