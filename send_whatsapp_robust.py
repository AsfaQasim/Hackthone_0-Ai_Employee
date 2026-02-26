"""
Robust WhatsApp Message Sender
Handles various loading states and errors
"""

import asyncio
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("❌ Playwright not installed")
    print("Run: pip install playwright")
    exit(1)


async def wait_for_whatsapp_load(page, timeout=60000):
    """Wait for WhatsApp to load with multiple fallback selectors."""
    
    selectors = [
        '[data-testid="chat-list"]',
        '#pane-side',
        '[data-testid="chat-list-search"]',
        'div[id="app"]',
    ]
    
    for selector in selectors:
        try:
            await page.wait_for_selector(selector, timeout=timeout)
            print(f"✅ Found: {selector}")
            return True
        except:
            print(f"⏳ Trying next selector...")
            continue
    
    return False


async def send_message_now():
    """Send message to Asyfa."""
    
    recipient = "Asyfa"
    message = "Hello! This is a test message from Kiro AI. Testing WhatsApp integration. 🤖"
    
    session_path = Path(".whatsapp_session")
    
    print("=" * 70)
    print("WhatsApp Robust Message Sender")
    print("=" * 70)
    print()
    print(f"📤 Sending to: {recipient}")
    print(f"💬 Message: {message}")
    print()
    
    playwright = None
    browser = None
    
    try:
        print("⏳ Starting browser...")
        playwright = await async_playwright().start()
        
        # Launch browser
        browser = await playwright.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            channel="chrome",
            args=['--disable-blink-features=AutomationControlled']
        )
        
        # Get or create page
        if browser.pages:
            page = browser.pages[0]
        else:
            page = await browser.new_page()
        
        # Go to WhatsApp Web
        print("⏳ Loading WhatsApp Web...")
        await page.goto('https://web.whatsapp.com', wait_until='domcontentloaded', timeout=60000)
        
        # Wait for WhatsApp to load
        print("⏳ Waiting for WhatsApp to load...")
        loaded = await wait_for_whatsapp_load(page, timeout=60000)
        
        if not loaded:
            print("❌ WhatsApp didn't load properly")
            print("   Please check if you're logged in")
            print("   Run: python auth_whatsapp_simple.py")
            await browser.close()
            await playwright.stop()
            return False
        
        print("✅ WhatsApp loaded!")
        
        # Wait a bit for everything to settle
        await asyncio.sleep(3)
        
        # Try to find and click search box
        print(f"🔍 Searching for {recipient}...")
        
        search_selectors = [
            '[data-testid="chat-list-search"]',
            'div[contenteditable="true"][data-tab="3"]',
            '[title="Search input textbox"]',
        ]
        
        search_box = None
        for selector in search_selectors:
            try:
                search_box = await page.wait_for_selector(selector, timeout=5000)
                if search_box:
                    print(f"✅ Found search box: {selector}")
                    break
            except:
                continue
        
        if not search_box:
            print("❌ Couldn't find search box")
            print("   WhatsApp Web might have changed its layout")
            print("   Keeping browser open for manual sending...")
            await asyncio.sleep(30)
            await browser.close()
            await playwright.stop()
            return False
        
        # Click and type in search
        await search_box.click()
        await asyncio.sleep(0.5)
        
        # Clear any existing search
        await page.keyboard.press('Control+A')
        await page.keyboard.press('Backspace')
        await asyncio.sleep(0.5)
        
        # Type recipient name
        await page.keyboard.type(recipient)
        await asyncio.sleep(3)
        
        # Click first result
        print("📱 Opening chat...")
        
        chat_selectors = [
            '[data-testid="cell-frame-container"]',
            'div[role="listitem"]',
            'div[data-testid="chat"]',
        ]
        
        first_result = None
        for selector in chat_selectors:
            try:
                first_result = await page.wait_for_selector(selector, timeout=5000)
                if first_result:
                    print(f"✅ Found chat: {selector}")
                    break
            except:
                continue
        
        if not first_result:
            print("❌ Couldn't find chat")
            print(f"   Make sure '{recipient}' exists in your contacts")
            await asyncio.sleep(10)
            await browser.close()
            await playwright.stop()
            return False
        
        await first_result.click()
        await asyncio.sleep(3)
        
        # Find message input
        print("⌨️  Typing message...")
        
        input_selectors = [
            '[data-testid="conversation-compose-box-input"]',
            'div[contenteditable="true"][data-tab="10"]',
            '[title="Type a message"]',
        ]
        
        message_box = None
        for selector in input_selectors:
            try:
                message_box = await page.wait_for_selector(selector, timeout=5000)
                if message_box:
                    print(f"✅ Found message box: {selector}")
                    break
            except:
                continue
        
        if not message_box:
            print("❌ Couldn't find message input")
            print("   Keeping browser open for manual sending...")
            await asyncio.sleep(30)
            await browser.close()
            await playwright.stop()
            return False
        
        # Type message
        await message_box.click()
        await asyncio.sleep(0.5)
        await page.keyboard.type(message)
        await asyncio.sleep(1)
        
        # Send
        print("📨 Sending message...")
        await page.keyboard.press('Enter')
        await asyncio.sleep(3)
        
        print("✅ Message sent!")
        
        # Track the message
        print("📝 Tracking message...")
        track_message(recipient, message)
        
        # Keep browser open briefly
        print("⏳ Keeping browser open for 5 seconds...")
        await asyncio.sleep(5)
        
        # Cleanup
        print("🧹 Closing browser...")
        await browser.close()
        await playwright.stop()
        
        print()
        print("=" * 70)
        print("✅ SUCCESS!")
        print("=" * 70)
        print()
        print("Message sent to Asyfa and tracked!")
        print("Check WhatsApp_Sent folder for details.")
        print()
        
        return True
        
    except Exception as e:
        print()
        print(f"❌ Error: {e}")
        print()
        print("Troubleshooting:")
        print("1. Run: python auth_whatsapp_simple.py")
        print("2. Make sure 'Asyfa' contact exists")
        print("3. Check internet connection")
        print()
        
        # Cleanup
        if browser:
            try:
                await browser.close()
            except:
                pass
        if playwright:
            try:
                await playwright.stop()
            except:
                pass
        
        return False


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
method: "automated_playwright_robust"
---

# WhatsApp Message to {recipient}

**Status**: ✅ Sent
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Method**: Automated via Playwright (Robust)

## Message
{message}

---

*Sent via Kiro AI WhatsApp Integration*
"""
    
    filepath.write_text(content, encoding='utf-8')
    print(f"✅ Tracked: {filepath}")


if __name__ == "__main__":
    try:
        result = asyncio.run(send_message_now())
        if not result:
            print("\n⚠️  Message not sent automatically")
            print("   You can send it manually in the browser")
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
