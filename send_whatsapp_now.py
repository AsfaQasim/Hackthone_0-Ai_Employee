"""
Quick WhatsApp Message Sender
Uses Playwright to send a message via WhatsApp Web
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


async def send_message(recipient: str, message: str):
    """Send a WhatsApp message."""
    
    session_path = Path(".whatsapp_session")
    
    print(f"📤 Sending message to {recipient}...")
    print(f"💬 Message: {message}")
    print()
    
    try:
        playwright = await async_playwright().start()
        
        # Launch browser with saved session
        browser = await playwright.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            channel="chrome"
        )
        
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        # Go to WhatsApp Web
        print("⏳ Loading WhatsApp Web...")
        await page.goto('https://web.whatsapp.com', timeout=60000)
        
        # Wait for WhatsApp to load
        await page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
        print("✅ WhatsApp loaded!")
        
        # Search for contact
        print(f"🔍 Searching for {recipient}...")
        search_box = await page.wait_for_selector('[data-testid="chat-list-search"]', timeout=10000)
        await search_box.click()
        
        # Clear any existing search
        await page.keyboard.press('Control+A')
        await page.keyboard.press('Backspace')
        
        # Type recipient name
        await page.keyboard.type(recipient)
        await asyncio.sleep(2)
        
        # Click first result
        print("📱 Opening chat...")
        first_result = await page.wait_for_selector('[data-testid="cell-frame-container"]', timeout=10000)
        await first_result.click()
        await asyncio.sleep(2)
        
        # Type message
        print("⌨️  Typing message...")
        message_box = await page.wait_for_selector('[data-testid="conversation-compose-box-input"]', timeout=10000)
        await message_box.click()
        await page.keyboard.type(message)
        await asyncio.sleep(1)
        
        # Send
        print("📨 Sending...")
        await page.keyboard.press('Enter')
        await asyncio.sleep(2)
        
        print("✅ Message sent successfully!")
        
        # Track the message
        track_message(recipient, message)
        
        # Cleanup
        await browser.close()
        await playwright.stop()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def track_message(recipient: str, message: str):
    """Track sent message in WhatsApp_Sent folder."""
    
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
---

# WhatsApp Message to {recipient}

**Status**: ✅ Sent
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Message
{message}

---

*Sent via Kiro AI WhatsApp Integration*
"""
    
    filepath.write_text(content, encoding='utf-8')
    print(f"📝 Message tracked: {filepath}")


async def main():
    """Main function."""
    
    print("=" * 70)
    print("WhatsApp Message Sender - Kiro AI")
    print("=" * 70)
    print()
    
    # Default message to Asyfa
    recipient = "Asyfa"
    message = "Hello! This is a test message from Kiro AI. Testing WhatsApp integration. 🤖"
    
    success = await send_message(recipient, message)
    
    print()
    print("=" * 70)
    if success:
        print("✅ SUCCESS!")
        print()
        print("Message sent and tracked.")
        print("Check WhatsApp_Sent folder for details.")
    else:
        print("❌ FAILED!")
        print()
        print("Please check the error message above.")
    print("=" * 70)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
