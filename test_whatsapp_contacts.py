"""
Test WhatsApp Contacts
See what contacts are available
"""

import asyncio
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed")
    exit(1)


async def list_contacts():
    """List all visible contacts."""
    
    session_path = Path(".whatsapp_session")
    
    print("=" * 70)
    print("WhatsApp Contacts Viewer")
    print("=" * 70)
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
        
        print("⏳ Loading WhatsApp Web...")
        await page.goto('https://web.whatsapp.com', wait_until='domcontentloaded', timeout=60000)
        
        # Wait for WhatsApp
        await page.wait_for_selector('#pane-side', timeout=60000)
        print("✅ WhatsApp loaded!")
        
        await asyncio.sleep(3)
        
        print()
        print("=" * 70)
        print("VISIBLE CONTACTS/CHATS:")
        print("=" * 70)
        print()
        
        # Get all chat elements
        chats = await page.query_selector_all('div[role="listitem"]')
        
        for i, chat in enumerate(chats[:15], 1):  # First 15 chats
            try:
                # Get chat name
                name_elem = await chat.query_selector('span[title]')
                if name_elem:
                    name = await name_elem.get_attribute('title')
                    print(f"{i}. {name}")
            except:
                continue
        
        print()
        print("=" * 70)
        print()
        print("Use these exact names when sending messages!")
        print()
        print("Example:")
        print('  python whatsapp_ai_automation.py send "Asyfa Qasim" "Hello!"')
        print()
        
        # Keep browser open
        print("Keeping browser open for 10 seconds...")
        await asyncio.sleep(10)
        
        await browser.close()
        await playwright.stop()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()


if __name__ == "__main__":
    try:
        asyncio.run(list_contacts())
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
