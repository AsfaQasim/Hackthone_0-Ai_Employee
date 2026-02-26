"""
WhatsApp AI - Direct Click Method
Clicks directly on visible chats instead of using search
"""

import asyncio
from pathlib import Path
from datetime import datetime
import re

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed")
    exit(1)


async def send_message_direct(recipient: str, message: str):
    """Send message by directly clicking on visible chat."""
    
    session_path = Path(".whatsapp_session")
    
    print("=" * 70)
    print("WhatsApp AI - Direct Click Method")
    print("=" * 70)
    print()
    print(f"📤 Recipient: {recipient}")
    print(f"💬 Message: {message[:80]}...")
    print()
    
    playwright = None
    browser = None
    
    try:
        print("⏳ Starting browser...")
        playwright = await async_playwright().start()
        
        browser = await playwright.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            channel="chrome"
        )
        
        page = browser.pages[0] if browser.pages else await browser.new_page()
        page.set_default_timeout(60000)
        
        print("⏳ Loading WhatsApp Web...")
        await page.goto('https://web.whatsapp.com', wait_until='networkidle', timeout=90000)
        
        # Wait for WhatsApp
        await page.wait_for_selector('#pane-side', timeout=60000)
        print("✅ WhatsApp loaded!")
        
        await asyncio.sleep(5)
        
        # Get all visible chats
        print(f"\n🔍 Looking for '{recipient}' in visible chats...")
        chats = await page.query_selector_all('div[role="listitem"]')
        print(f"   Found {len(chats)} visible chats")
        
        # Find matching chat
        found_chat = None
        for i, chat in enumerate(chats):
            try:
                # Get chat name
                name_elem = await chat.query_selector('span[title]')
                if not name_elem:
                    continue
                
                name = await name_elem.get_attribute('title')
                if not name:
                    name = await name_elem.inner_text()
                
                print(f"   {i+1}. {name}")
                
                # Check if this is our recipient (partial match)
                if recipient.lower() in name.lower() or name.lower() in recipient.lower():
                    print(f"   ✅ Found match: {name}")
                    found_chat = chat
                    break
                    
            except:
                continue
        
        if not found_chat:
            print(f"\n   ❌ '{recipient}' not found in visible chats")
            print("   💡 Make sure the chat is visible on screen")
            print("   💡 Or scroll down to find it")
            await asyncio.sleep(10)
            await browser.close()
            await playwright.stop()
            return False
        
        # Click on the chat
        print(f"\n   📱 Opening chat...")
        await found_chat.click()
        await asyncio.sleep(3)
        
        # Find message input
        print("   ⌨️  Finding message input...")
        message_input = None
        
        for selector in [
            'div[contenteditable="true"][data-tab="10"]',
            'footer div[contenteditable="true"]',
            'div[role="textbox"]'
        ]:
            try:
                message_input = await page.wait_for_selector(selector, timeout=5000)
                if message_input:
                    print(f"   ✅ Found input: {selector}")
                    break
            except:
                continue
        
        if not message_input:
            print("   ❌ Message input not found")
            await asyncio.sleep(10)
            await browser.close()
            await playwright.stop()
            return False
        
        # Type message
        print("   ⌨️  Typing message...")
        await message_input.click()
        await asyncio.sleep(1)
        
        # Type slowly with delays
        lines = message.split('\n')
        for i, line in enumerate(lines):
            await page.keyboard.type(line, delay=20)
            if i < len(lines) - 1:
                await page.keyboard.press('Shift+Enter')
                await asyncio.sleep(0.3)
        
        await asyncio.sleep(1)
        
        # Send
        print("   📨 Sending...")
        await page.keyboard.press('Enter')
        await asyncio.sleep(3)
        
        print("   ✅ Message sent!")
        
        # Track message
        sent_folder = Path("WhatsApp_Sent")
        sent_folder.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = re.sub(r'[^\w\s-]', '', recipient).replace(' ', '_')
        filename = f"sent_{timestamp}_{safe_name}.md"
        filepath = sent_folder / filename
        
        content = f"""---
type: whatsapp_sent
recipient: "{recipient}"
timestamp: "{datetime.now().isoformat()}"
status: "✅ Sent"
method: "ai_direct_click"
---

# WhatsApp Message to {recipient}

**Status**: ✅ Sent
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Method**: AI Direct Click

## Message
{message}

---

*Sent via WhatsApp AI (Direct Click Method)*
"""
        
        filepath.write_text(content, encoding='utf-8')
        print(f"   📝 Tracked: {filepath}")
        
        # Keep browser open
        print("\n⏳ Keeping browser open for 5 seconds...")
        await asyncio.sleep(5)
        
        await browser.close()
        await playwright.stop()
        
        print()
        print("=" * 70)
        print("✅ SUCCESS!")
        print("=" * 70)
        print()
        print(f"Message sent to {recipient}!")
        print("Check WhatsApp_Sent folder.")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()
        
        return False


async def main():
    import sys
    
    if len(sys.argv) < 3:
        print("=" * 70)
        print("WhatsApp AI - Direct Click Method")
        print("=" * 70)
        print()
        print("Usage:")
        print('  python whatsapp_ai_direct.py <contact> <message>')
        print()
        print("Examples:")
        print('  python whatsapp_ai_direct.py Asyfa "Hello!"')
        print('  python whatsapp_ai_direct.py "Asyfa Qasim" "Hello from AI!"')
        print()
        print("Note: Contact must be visible in your recent chats")
        print()
        return
    
    recipient = sys.argv[1]
    message = " ".join(sys.argv[2:])
    
    success = await send_message_direct(recipient, message)
    
    if not success:
        print("❌ Failed to send message")
        print()
        print("Tips:")
        print("1. Make sure the contact is in your recent chats")
        print("2. Try scrolling to make the chat visible")
        print("3. Use partial name (e.g., 'Asyfa' instead of 'Asyfa Qasim')")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
