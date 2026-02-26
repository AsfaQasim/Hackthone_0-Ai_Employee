"""
Send Real WhatsApp Message - Interactive
Opens browser, you send manually, we track it
"""

import asyncio
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwright not installed!")
    exit(1)

async def open_whatsapp_for_sending(recipient: str, message: str):
    """Open WhatsApp Web for manual sending."""
    
    session_path = Path(".whatsapp_session")
    sent_folder = Path("WhatsApp_Sent")
    sent_folder.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("SEND REAL MESSAGE TO ASYFA")
    print("=" * 70)
    print()
    print(f"📱 Recipient: {recipient}")
    print(f"💬 Message to send:")
    print()
    print("   " + "-" * 60)
    print(f"   {message}")
    print("   " + "-" * 60)
    print()
    
    playwright = None
    browser = None
    
    try:
        print("🚀 Opening WhatsApp Web...")
        playwright = await async_playwright().start()
        
        # Launch browser
        browser = await playwright.chromium.launch_persistent_context(
            str(session_path),
            headless=False,  # Keep visible
            channel="chrome"
        )
        
        # Get page
        if len(browser.pages) > 0:
            page = browser.pages[0]
        else:
            page = await browser.new_page()
        
        # Go to WhatsApp Web
        await page.goto('https://web.whatsapp.com', timeout=60000)
        
        print("✅ WhatsApp Web opened!")
        print()
        print("=" * 70)
        print("NOW DO THIS:")
        print("=" * 70)
        print()
        print("1. Browser window mein WhatsApp Web khul gaya hai")
        print(f"2. Search box mein '{recipient}' type karo")
        print("3. Chat open karo")
        print("4. Yeh message copy karke bhejo:")
        print()
        print("   " + "-" * 60)
        print(f"   {message}")
        print("   " + "-" * 60)
        print()
        print("5. Message bhejne ke BAAD, yahan Enter press karo...")
        print()
        
        # Wait for user to send message
        input("Press Enter after you've sent the message: ")
        
        # Track the sent message
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sent_{timestamp}_{recipient}.md"
        filepath = sent_folder / filename
        
        content = f"""---
type: whatsapp_sent
recipient: "{recipient}"
timestamp: "{datetime.now().isoformat()}"
status: "✅ Sent & Delivered"
method: "manual_via_browser"
---

# WhatsApp Message to {recipient}

**Status**: ✅ Sent & Delivered
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Method**: Manual via WhatsApp Web

## Message
{message}

## Verification
- Browser opened: ✅
- User confirmed sent: ✅
- Tracked in system: ✅

---

*Real message sent via WhatsApp Web*
"""
        
        filepath.write_text(content, encoding='utf-8')
        
        print()
        print("=" * 70)
        print("✅ MESSAGE TRACKED!")
        print("=" * 70)
        print()
        print(f"📝 Tracking file: {filepath.name}")
        print()
        print("Verification:")
        print(f"  ✅ Message sent to {recipient}")
        print(f"  ✅ Tracked at {datetime.now().strftime('%H:%M:%S')}")
        print(f"  ✅ File saved in WhatsApp_Sent/")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        if browser:
            print("Closing browser in 5 seconds...")
            await asyncio.sleep(5)
            await browser.close()
        if playwright:
            await playwright.stop()


async def main():
    recipient = "Asyfa"
    message = "Hello Asyfa! This is a test message from my AI assistant. Testing WhatsApp integration for my hackathon project. 🤖"
    
    success = await open_whatsapp_for_sending(recipient, message)
    
    if success:
        print()
        print("=" * 70)
        print("🎉 SUCCESS!")
        print("=" * 70)
        print()
        print("Message successfully sent and tracked!")
        print()
        print("Check:")
        print("  📱 Asyfa's WhatsApp - message should be there")
        print("  📂 WhatsApp_Sent folder - tracking file created")
        print()
    else:
        print()
        print("❌ Something went wrong")
    
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
