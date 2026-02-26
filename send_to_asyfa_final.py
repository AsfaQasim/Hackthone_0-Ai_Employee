"""
Final WhatsApp Sender - Send to Asyfa
Uses the exact contact name from WhatsApp
"""

import asyncio
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed")
    exit(1)


async def send_now():
    """Send message to Asyfa."""
    
    # Try different variations of the name
    recipient_variations = ["Asyfa", "Asyfa Qasim", "Asyfa Qasim (You)"]
    message = "Hello! This is a test message from Kiro AI. Testing WhatsApp integration. 🤖"
    
    session_path = Path(".whatsapp_session")
    
    print("=" * 70)
    print("Send Message to Asyfa - Final Version")
    print("=" * 70)
    print()
    print(f"💬 Message: {message}")
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
        print("⏳ Waiting for WhatsApp...")
        await page.wait_for_selector('#pane-side', timeout=60000)
        print("✅ WhatsApp loaded!")
        
        await asyncio.sleep(3)
        
        # Try each name variation
        for recipient in recipient_variations:
            print(f"\n🔍 Trying: {recipient}")
            
            try:
                # Find search box
                search_box = await page.query_selector('div[contenteditable="true"][data-tab="3"]')
                if not search_box:
                    print("   ❌ Search box not found")
                    continue
                
                # Click and clear
                await search_box.click()
                await asyncio.sleep(0.5)
                await page.keyboard.press('Control+A')
                await page.keyboard.press('Backspace')
                await asyncio.sleep(0.5)
                
                # Type name
                await page.keyboard.type(recipient)
                await asyncio.sleep(3)
                
                # Look for chat result
                chat_result = await page.query_selector('div[role="listitem"]')
                if not chat_result:
                    print(f"   ❌ No results for '{recipient}'")
                    continue
                
                print(f"   ✅ Found chat!")
                
                # Click chat
                await chat_result.click()
                await asyncio.sleep(2)
                
                # Find message input
                message_input = await page.query_selector('div[contenteditable="true"][data-tab="10"]')
                if not message_input:
                    print("   ❌ Message input not found")
                    continue
                
                print("   ⌨️  Typing message...")
                await message_input.click()
                await asyncio.sleep(0.5)
                await page.keyboard.type(message)
                await asyncio.sleep(1)
                
                # Send
                print("   📨 Sending...")
                await page.keyboard.press('Enter')
                await asyncio.sleep(3)
                
                print("   ✅ Message sent!")
                
                # Track
                track_message(recipient, message)
                
                # Success!
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
                print(f"   ❌ Error with '{recipient}': {e}")
                continue
        
        # If we get here, none worked
        print()
        print("=" * 70)
        print("❌ Could not send automatically")
        print("=" * 70)
        print()
        print("The browser is still open. You can:")
        print("1. Manually search for 'Asyfa'")
        print("2. Send the message manually")
        print("3. It will still be tracked")
        print()
        print("Keeping browser open for 30 seconds...")
        await asyncio.sleep(30)
        
        await browser.close()
        await playwright.stop()
        
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        
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
    filename = f"sent_{timestamp}_Asyfa.md"
    filepath = sent_folder / filename
    
    content = f"""---
type: whatsapp_sent
recipient: "Asyfa"
timestamp: "{datetime.now().isoformat()}"
status: "✅ Sent"
method: "automated_playwright_final"
---

# WhatsApp Message to Asyfa

**Status**: ✅ Sent
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Method**: Automated via Playwright

## Message
{message}

---

*Sent via Kiro AI WhatsApp Integration*
"""
    
    filepath.write_text(content, encoding='utf-8')
    print(f"   📝 Tracked: {filepath}")


if __name__ == "__main__":
    try:
        asyncio.run(send_now())
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
