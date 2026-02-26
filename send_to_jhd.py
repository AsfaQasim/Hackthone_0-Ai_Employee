"""
Send Message to JHD - Automated Test
"""

import asyncio
import logging
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwright not installed!")
    exit(1)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def send_to_jhd():
    """Send message to JHD via WhatsApp Web."""
    
    recipient = "JHD"
    message = "Hello! This is a test message from my AI assistant. Testing WhatsApp automation. 🤖"
    
    session_path = Path(".whatsapp_session")
    sent_folder = Path("WhatsApp_Sent")
    sent_folder.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("SENDING MESSAGE TO JHD")
    print("=" * 70)
    print()
    print(f"📱 Recipient: {recipient}")
    print(f"💬 Message: {message}")
    print()
    
    playwright = None
    browser = None
    
    try:
        print("🚀 Starting browser...")
        playwright = await async_playwright().start()
        
        # Launch with persistent context
        browser = await playwright.chromium.launch_persistent_context(
            str(session_path),
            headless=False,  # Keep visible
            channel="chrome",  # Use system Chrome
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ],
            slow_mo=500  # Slow down actions to avoid detection
        )
        
        # Get page
        if len(browser.pages) > 0:
            page = browser.pages[0]
        else:
            page = await browser.new_page()
        
        print("🌐 Loading WhatsApp Web...")
        await page.goto('https://web.whatsapp.com', timeout=60000)
        
        # Wait for WhatsApp to load - try multiple times
        print("⏳ Waiting for WhatsApp to load...")
        loaded = False
        
        for attempt in range(3):
            try:
                await page.wait_for_selector('[data-testid="chat-list"]', timeout=15000)
                print("✅ WhatsApp loaded!")
                loaded = True
                break
            except:
                print(f"   Attempt {attempt + 1}/3 failed, retrying...")
                await asyncio.sleep(2)
        
        if not loaded:
            print("❌ WhatsApp didn't load properly")
            print("   Browser window is open - you can manually send the message")
            print("   Press Enter when done...")
            input()
            
            # Track manual send
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"whatsapp_{timestamp}_{recipient}.md"
            filepath = sent_folder / filename
            
            content = f"""---
type: whatsapp_sent
recipient: "{recipient}"
timestamp: "{datetime.now().isoformat()}"
status: "✅ Sent (Manual)"
---

# WhatsApp Message to {recipient}

**Status**: ✅ Sent (Manual)
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Message
{message}

---

*Manually sent via browser*
"""
            filepath.write_text(content, encoding='utf-8')
            print(f"✅ Tracked in: {filepath}")
            return True
        
        # Search for contact
        print(f"🔍 Searching for {recipient}...")
        await asyncio.sleep(1)
        
        search_box = await page.wait_for_selector('[data-testid="chat-list-search"]', timeout=10000)
        await search_box.click()
        await asyncio.sleep(1)
        
        # Type contact name slowly
        for char in recipient:
            await page.keyboard.type(char)
            await asyncio.sleep(0.1)
        
        await asyncio.sleep(2)  # Wait for search results
        
        # Click first result
        print(f"📱 Opening chat with {recipient}...")
        first_result = await page.wait_for_selector('[data-testid="cell-frame-container"]', timeout=10000)
        await first_result.click()
        await asyncio.sleep(2)
        
        # Find message input
        print("✍️  Typing message...")
        message_box = await page.wait_for_selector('[data-testid="conversation-compose-box-input"]', timeout=10000)
        await message_box.click()
        await asyncio.sleep(1)
        
        # Type message slowly
        for char in message:
            await page.keyboard.type(char)
            await asyncio.sleep(0.05)
        
        await asyncio.sleep(1)
        
        # Send
        print("📨 Sending message...")
        await page.keyboard.press('Enter')
        await asyncio.sleep(3)
        
        print("✅ Message sent successfully!")
        
        # Track the sent message
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"whatsapp_{timestamp}_{recipient}.md"
        filepath = sent_folder / filename
        
        content = f"""---
type: whatsapp_sent
recipient: "{recipient}"
timestamp: "{datetime.now().isoformat()}"
status: "✅ Sent"
---

# WhatsApp Message to {recipient}

**Status**: ✅ Sent Successfully
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Message
{message}

---

*Sent via WhatsApp Automation*
"""
        
        filepath.write_text(content, encoding='utf-8')
        print(f"📝 Tracked in: {filepath}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error occurred: {e}")
        print()
        print("Browser is still open. You can:")
        print("1. Manually send the message to JHD")
        print("2. Press Enter when done to track it")
        input()
        
        # Track manual send
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"whatsapp_{timestamp}_{recipient}.md"
        filepath = sent_folder / filename
        
        content = f"""---
type: whatsapp_sent
recipient: "{recipient}"
timestamp: "{datetime.now().isoformat()}"
status: "✅ Sent (Manual after error)"
---

# WhatsApp Message to {recipient}

**Status**: ✅ Sent (Manual)
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Message
{message}

## Notes
Automated sending encountered an error, sent manually.

---

*Manually sent via browser*
"""
        filepath.write_text(content, encoding='utf-8')
        print(f"✅ Tracked in: {filepath}")
        
        return False
        
    finally:
        if browser:
            print()
            print("Closing browser in 3 seconds...")
            await asyncio.sleep(3)
            await browser.close()
        if playwright:
            await playwright.stop()


async def main():
    print()
    success = await send_to_jhd()
    
    print()
    print("=" * 70)
    if success:
        print("🎉 SUCCESS!")
    else:
        print("⚠️  Completed with manual intervention")
    print("=" * 70)
    print()
    print("Check WhatsApp_Sent folder for tracking file")
    print()


if __name__ == "__main__":
    asyncio.run(main())
