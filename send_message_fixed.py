"""
Fixed Send Message - Uses existing session properly
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_whatsapp_message(recipient: str, message: str):
    """Send WhatsApp message using persistent session."""
    
    session_path = Path(".whatsapp_session")
    sent_folder = Path("WhatsApp_Sent")
    sent_folder.mkdir(exist_ok=True)
    
    print(f"📤 Sending message to {recipient}...")
    print(f"💬 Message: {message}")
    print()
    
    playwright = None
    browser = None
    
    try:
        playwright = await async_playwright().start()
        
        # Launch with persistent context (uses saved session)
        browser = await playwright.chromium.launch_persistent_context(
            str(session_path),
            headless=False,  # Keep visible to avoid detection
            channel="chrome",  # Use system Chrome
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox'
            ]
        )
        
        # Get or create page
        if len(browser.pages) > 0:
            page = browser.pages[0]
        else:
            page = await browser.new_page()
        
        # Go to WhatsApp Web
        print("🌐 Loading WhatsApp Web...")
        await page.goto('https://web.whatsapp.com', wait_until='networkidle', timeout=60000)
        
        # Wait for WhatsApp to load
        print("⏳ Waiting for WhatsApp to load...")
        await page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
        print("✅ WhatsApp loaded!")
        
        # Search for contact
        print(f"🔍 Searching for {recipient}...")
        search_box = await page.wait_for_selector('[data-testid="chat-list-search"]', timeout=10000)
        await search_box.click()
        await asyncio.sleep(0.5)
        
        # Type contact name
        await page.keyboard.type(recipient)
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
        await asyncio.sleep(0.5)
        
        # Type message
        await page.keyboard.type(message)
        await asyncio.sleep(1)
        
        # Send (press Enter)
        print("📨 Sending...")
        await page.keyboard.press('Enter')
        await asyncio.sleep(2)
        
        print("✅ Message sent successfully!")
        
        # Track the sent message
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"whatsapp_{timestamp}_{recipient[:20]}.md"
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

*Sent via WhatsApp MCP Server*
"""
        
        filepath.write_text(content, encoding='utf-8')
        print(f"📝 Tracked in: {filepath}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        print(f"❌ Error: {e}")
        return False
        
    finally:
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()


async def main():
    print("=" * 60)
    print("WhatsApp Send Test - Silver Tier")
    print("=" * 60)
    print()
    
    # Send test message to Anisa
    success = await send_whatsapp_message(
        recipient="Anisa",
        message="Thanks for your message! This is an automated reply from my AI assistant. 🤖"
    )
    
    if success:
        print()
        print("=" * 60)
        print("🎉 SUCCESS! Message sent and tracked!")
        print("=" * 60)
        print()
        print("Check:")
        print("  📂 WhatsApp_Sent folder - tracking file created")
        print("  📱 WhatsApp on your phone - message delivered")
        print()
        print("✅ Silver Tier COMPLETE!")
    else:
        print()
        print("❌ Failed to send message")
        print("Try reconnecting: python Skills/whatsapp_watcher.py auth")


if __name__ == "__main__":
    asyncio.run(main())
