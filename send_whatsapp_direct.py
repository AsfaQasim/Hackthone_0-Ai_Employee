"""
Direct WhatsApp Message Sender
Actually sends the message automatically using Playwright
"""

import asyncio
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed")
    print("Run: pip install playwright")
    exit(1)


async def send_message_now():
    """Send message to Asyfa right now."""
    
    recipient = "Asyfa"
    message = "Hello! This is a test message from Kiro AI. Testing WhatsApp integration. 🤖"
    
    session_path = Path(".whatsapp_session")
    
    print("=" * 70)
    print("WhatsApp Direct Message Sender")
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
        
        # Launch browser with saved session
        browser = await playwright.chromium.launch_persistent_context(
            str(session_path),
            headless=False,  # Visible so you can see it working
            channel="chrome"
        )
        
        # Get or create page
        if browser.pages:
            page = browser.pages[0]
        else:
            page = await browser.new_page()
        
        # Go to WhatsApp Web
        print("⏳ Loading WhatsApp Web...")
        await page.goto('https://web.whatsapp.com', timeout=60000)
        
        # Wait for WhatsApp to load
        print("⏳ Waiting for WhatsApp to load...")
        await page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
        print("✅ WhatsApp loaded!")
        
        # Wait a bit for everything to settle
        await asyncio.sleep(2)
        
        # Search for contact
        print(f"🔍 Searching for {recipient}...")
        search_box = await page.wait_for_selector('[data-testid="chat-list-search"]', timeout=10000)
        await search_box.click()
        await asyncio.sleep(0.5)
        
        # Clear any existing search
        await page.keyboard.press('Control+A')
        await page.keyboard.press('Backspace')
        await asyncio.sleep(0.5)
        
        # Type recipient name
        await page.keyboard.type(recipient)
        await asyncio.sleep(2)
        
        # Click first result
        print("📱 Opening chat...")
        first_result = await page.wait_for_selector('[data-testid="cell-frame-container"]', timeout=10000)
        await first_result.click()
        await asyncio.sleep(2)
        
        # Find and click message input box
        print("⌨️  Typing message...")
        message_box = await page.wait_for_selector('[data-testid="conversation-compose-box-input"]', timeout=10000)
        await message_box.click()
        await asyncio.sleep(0.5)
        
        # Type the message
        await page.keyboard.type(message)
        await asyncio.sleep(1)
        
        # Send the message
        print("📨 Sending message...")
        await page.keyboard.press('Enter')
        await asyncio.sleep(2)
        
        print("✅ Message sent!")
        
        # Track the message
        print("📝 Tracking message...")
        track_message(recipient, message)
        
        # Keep browser open for a moment so you can see it worked
        print("⏳ Keeping browser open for 3 seconds...")
        await asyncio.sleep(3)
        
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
        print("1. Make sure WhatsApp Web is authenticated")
        print("2. Check if 'Asyfa' contact exists")
        print("3. Try running: python authenticate_whatsapp.py")
        print()
        
        # Cleanup on error
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()
        
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
method: "automated_playwright"
---

# WhatsApp Message to {recipient}

**Status**: ✅ Sent
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Method**: Automated via Playwright

## Message
{message}

---

*Sent via Kiro AI WhatsApp Integration*
"""
    
    filepath.write_text(content, encoding='utf-8')
    print(f"✅ Tracked: {filepath}")


if __name__ == "__main__":
    try:
        asyncio.run(send_message_now())
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
