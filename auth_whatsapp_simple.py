"""
Simple WhatsApp Authentication
Scan QR code to authenticate
"""

import asyncio
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed")
    print("Run: pip install playwright")
    exit(1)


async def authenticate():
    """Authenticate with WhatsApp Web."""
    
    session_path = Path(".whatsapp_session")
    session_path.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("WhatsApp Authentication")
    print("=" * 70)
    print()
    print("This will open WhatsApp Web in your browser.")
    print("If you see a QR code, scan it with your phone.")
    print()
    
    playwright = None
    browser = None
    
    try:
        print("⏳ Starting browser...")
        playwright = await async_playwright().start()
        
        # Launch browser with saved session
        browser = await playwright.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
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
        
        print()
        print("=" * 70)
        print("INSTRUCTIONS:")
        print("=" * 70)
        print()
        print("1. If you see a QR code, scan it with your phone:")
        print("   - Open WhatsApp on your phone")
        print("   - Go to Settings > Linked Devices")
        print("   - Tap 'Link a Device'")
        print("   - Scan the QR code")
        print()
        print("2. If you're already logged in, you'll see your chats")
        print()
        print("3. Wait for WhatsApp to fully load...")
        print()
        print("=" * 70)
        print()
        
        # Wait for authentication
        print("⏳ Waiting for WhatsApp to load (up to 2 minutes)...")
        
        try:
            # Wait for chat list to appear (means we're logged in)
            await page.wait_for_selector('[data-testid="chat-list"]', timeout=120000)
            
            print()
            print("=" * 70)
            print("✅ SUCCESS!")
            print("=" * 70)
            print()
            print("WhatsApp Web is authenticated and ready!")
            print(f"Session saved to: {session_path}")
            print()
            print("You can now close this browser window.")
            print("Press Enter to continue...")
            print()
            
            # Wait for user to press Enter
            await asyncio.sleep(5)
            
            # Cleanup
            await browser.close()
            await playwright.stop()
            
            return True
            
        except Exception as e:
            print()
            print("=" * 70)
            print("❌ TIMEOUT")
            print("=" * 70)
            print()
            print("WhatsApp Web didn't load in time.")
            print()
            print("Please try again and make sure to:")
            print("1. Scan the QR code quickly")
            print("2. Have a stable internet connection")
            print("3. Keep the browser window open")
            print()
            
            # Cleanup
            if browser:
                await browser.close()
            if playwright:
                await playwright.stop()
            
            return False
            
    except Exception as e:
        print()
        print(f"❌ Error: {e}")
        print()
        
        # Cleanup
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()
        
        return False


if __name__ == "__main__":
    try:
        result = asyncio.run(authenticate())
        if result:
            print("✅ Authentication complete!")
            print()
            print("You can now send messages using:")
            print("  python send_whatsapp_direct.py")
        else:
            print("❌ Authentication failed")
            print()
            print("Please try again")
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
