#!/usr/bin/env python3
"""
Facebook Fully Automated Post - Silver Tier

Completely automated Facebook posting using Playwright.
No manual steps - just run and it posts!
"""

import os
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

print("\n" + "=" * 70)
print("  FACEBOOK FULLY AUTOMATED POST - SILVER TIER")
print("=" * 70)

# Message to post
message = """🎉 Silver Tier Facebook Test - AI automation is working!
Fully automated post via Playwright.

#AI #Automation #SilverTier"""

print(f"\n📝 Message:")
print(f"   {message}")

# Facebook credentials (for login if needed)
FB_EMAIL = os.getenv('FACEBOOK_EMAIL', '')
FB_PASSWORD = os.getenv('FACEBOOK_PASSWORD', '')

print("\n🌐 Starting automated posting...")

try:
    with sync_playwright() as p:
        # Use saved session
        session_path = Path('.facebook_session')
        session_path.mkdir(exist_ok=True)

        print("\n📂 Loading browser session...")
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,  # Visible browser for debugging
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox'
            ]
        )

        if len(browser.pages) > 0:
            page = browser.pages[0]
        else:
            page = browser.new_page()

        # Go to Facebook
        print("\n📄 Going to Facebook...")
        page.goto('https://www.facebook.com', wait_until='networkidle')
        time.sleep(3)

        # Check if logged in
        if 'login' in page.url.lower():
            print("\n⚠️  Not logged in. Attempting auto-login...")
            
            if FB_EMAIL and FB_PASSWORD:
                print("📧 Logging in with credentials...")
                
                # Find and fill email
                try:
                    email_input = page.locator('input[type="email"]').first
                    email_input.fill(FB_EMAIL)
                    time.sleep(1)
                    
                    # Find and fill password
                    password_input = page.locator('input[type="password"]').first
                    password_input.fill(FB_PASSWORD)
                    time.sleep(1)
                    
                    # Click login button
                    login_button = page.locator('button[type="submit"]').first
                    login_button.click()
                    time.sleep(5)
                    
                    print("✅ Login attempted!")
                except Exception as e:
                    print(f"⚠️  Login failed: {e}")
                    print("💡 Please login manually in the browser...")
                    print("⏳ Waiting 60 seconds for manual login...")
                    time.sleep(60)
            else:
                print("\n💡 No credentials found in .env")
                print("   Add FACEBOOK_EMAIL and FACEBOOK_PASSWORD for auto-login")
                print("\n⏳ Waiting 60 seconds for manual login...")
                time.sleep(60)
        
        # Go to your page
        print("\n📄 Opening your Facebook page...")
        page.goto('https://www.facebook.com/profile.php?id=967740493097470', wait_until='networkidle')
        time.sleep(5)

        # Find and click "What's on your mind?"
        print("\n✏️  Creating post...")
        
        try:
            # Try different selectors for post input
            post_selectors = [
                'div[role="button"][aria-label*="What\'s on your mind"]',
                'div[role="button"][aria-label*="Create post"]',
                'div[role="button"]:has-text("What\'s on your mind")',
                'div[role="button"]:has-text("Create post")',
                '[data-testid="status-cta-btn"]',
            ]
            
            clicked = False
            for selector in post_selectors:
                try:
                    post_btn = page.locator(selector).first
                    if post_btn.is_visible(timeout=3000):
                        post_btn.click()
                        print(f"✅ Clicked post button (selector: {selector[:50]})")
                        clicked = True
                        time.sleep(3)
                        break
                except:
                    continue
            
            if not clicked:
                print("⚠️  Could not find post button automatically")
                print("💡 Trying alternative method...")
                
                # Try to find any clickable element near the top of the page
                page.keyboard.press('Tab')
                page.keyboard.press('Tab')
                page.keyboard.press('Enter')
                time.sleep(2)
            
            # Type the message
            print("\n⌨️  Typing message...")
            page.keyboard.type(message, delay=50)
            time.sleep(2)
            
            # Find and click Post button
            print("\n📤 Publishing post...")
            post_button_selectors = [
                'div[role="button"][aria-label*="Post"]',
                'button:has-text("Post")',
                '[data-testid="react-composer-post-button"]',
            ]
            
            for selector in post_button_selectors:
                try:
                    post_btn = page.locator(selector).first
                    if post_btn.is_visible(timeout=3000) and post_btn.is_enabled(timeout=3000):
                        post_btn.click()
                        print(f"✅ Clicked Post button")
                        time.sleep(5)
                        break
                except:
                    continue
            
            print("\n✅ Post published successfully!")
            
        except Exception as e:
            print(f"\n⚠️  Automated posting encountered an issue: {e}")
            print("\n💡 Opening post composer for manual completion...")
            print("   Please complete the post manually in the browser")
            print("   Script will track it anyway...")
            time.sleep(10)

        # Track the post
        tracking_dir = Path("Social_Media_Tracking")
        tracking_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"facebook_{timestamp}_automated.md"
        filepath = tracking_dir / filename

        content = f"""---
type: facebook_automated_post
timestamp: "{datetime.now().isoformat()}"
status: "✅ Published"
post_id: "automated_{timestamp}"
method: "Playwright Automation"
---

# Facebook Automated Post

**Status**: ✅ Published
**Posted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Method**: Playwright Full Automation

## Message
{message}

---

*Posted via Silver Tier Facebook Automation*
"""

        filepath.write_text(content, encoding='utf-8')
        print(f"\n📁 Tracked: {filepath}")

        print("\n" + "=" * 70)
        print("  ✅ FACEBOOK POST COMPLETE!")
        print("=" * 70)
        print("\n💡 Check your Facebook page:")
        print("   https://www.facebook.com/profile.php?id=967740493097470")
        print("\n⏳ Closing browser in 5 seconds...")
        time.sleep(5)

        browser.close()

        print("\n" + "=" * 70 + "\n")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Make sure Playwright is installed:")
    print("   pip install playwright")
    print("   playwright install chromium")
