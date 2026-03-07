#!/usr/bin/env python3
"""
Facebook Playwright Posting

Post to Facebook using browser automation (no API needed).
Works without pages_manage_posts permission!
"""

import os
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

def post_to_facebook_playwright(message, email=None, password=None):
    """
    Post to Facebook using Playwright (browser automation).
    
    Args:
        message: Text to post
        email: Facebook email (optional, will prompt if not provided)
        password: Facebook password (optional, will prompt if not provided)
    """
    
    print("\n" + "=" * 70)
    print("  FACEBOOK PLAYWRIGHT POSTING")
    print("=" * 70)
    
    if not email:
        email = input("\n📧 Facebook Email: ").strip()
    if not password:
        password = input("🔐 Facebook Password: ").strip()
    
    print(f"\n📤 Posting to Facebook...")
    print(f"   Message: {message[:50]}...")
    
    try:
        with sync_playwright() as p:
            # Launch browser with persistent context (saves session)
            session_path = Path('.facebook_session')
            session_path.mkdir(exist_ok=True)
            
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            if len(browser.pages) > 0:
                page = browser.pages[0]
            else:
                page = browser.new_page()
            
            # Check if already logged in
            page.goto('https://www.facebook.com/')
            time.sleep(3)
            
            # Check if login needed
            if 'login' in page.url.lower() or page.locator('input[name="email"]').count() > 0:
                print("\n🔐 Logging in...")
                
                # Fill login form
                page.fill('input[name="email"]', email)
                page.fill('input[name="pass"]', password)
                
                # Try different login button selectors
                login_selectors = [
                    'button[name="login"]',
                    'button[type="submit"]',
                    'button:has-text("Log In")',
                    'button:has-text("Log in")',
                    'div[role="button"]:has-text("Log")'
                ]
                
                logged_in = False
                for selector in login_selectors:
                    try:
                        page.click(selector, timeout=2000)
                        logged_in = True
                        break
                    except:
                        continue
                
                if not logged_in:
                    print("\n⚠️ Could not find login button")
                    print("   Please login manually in the browser")
                    input("\nPress Enter after logging in...")
                
                # Wait for login
                time.sleep(5)
            else:
                print("\n✅ Already logged in!")
            
            # Go to your page
            print("\n📄 Opening your page...")
            page.goto('https://www.facebook.com/profile.php?id=967740493097470')
            
            time.sleep(3)
            
            # Click on "What's on your mind?" or post box
            print("\n✍️ Writing post...")
            
            # Try different selectors for post box
            selectors = [
                'div[role="button"][aria-label*="What"]',
                'div[role="button"][aria-label*="Create"]',
                'span:has-text("What\'s on your mind")',
                'div[contenteditable="true"]'
            ]
            
            clicked = False
            for selector in selectors:
                try:
                    page.click(selector, timeout=2000)
                    clicked = True
                    break
                except:
                    continue
            
            if not clicked:
                print("❌ Could not find post box")
                browser.close()
                return False
            
            time.sleep(2)
            
            # Type message
            page.keyboard.type(message)
            
            time.sleep(2)
            
            # Click Post button
            print("\n📤 Publishing...")
            
            post_selectors = [
                'div[aria-label="Post"]',
                'div[role="button"]:has-text("Post")',
                'span:has-text("Post")'
            ]
            
            posted = False
            for selector in post_selectors:
                try:
                    page.click(selector, timeout=2000)
                    posted = True
                    break
                except:
                    continue
            
            if posted:
                print("\n✅ Post published successfully!")
                time.sleep(3)
                
                # Track the post
                track_post(message, True)
                
                browser.close()
                return True
            else:
                print("\n⚠️ Could not find Post button")
                print("   Please click Post button manually in the browser")
                input("\nPress Enter after posting...")
                
                track_post(message, True)
                
                browser.close()
                return True
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        track_post(message, False, str(e))
        return False

def track_post(message, success, error=None):
    """Track posted message."""
    tracking_dir = Path("Social_Media_Tracking")
    tracking_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"facebook_{timestamp}_playwright.md"
    filepath = tracking_dir / filename
    
    status = "✅ Published" if success else "❌ Failed"
    
    content = f"""---
type: facebook_playwright_post
timestamp: "{datetime.now().isoformat()}"
status: "{status}"
---

# Facebook Post (Playwright)

**Status**: {status}  
**Posted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Method**: Browser Automation

## Message
{message}

"""
    
    if error:
        content += f"\n## Error\n{error}\n"
    
    content += "\n---\n\n*Posted via Playwright Automation*\n"
    
    filepath.write_text(content, encoding='utf-8')
    print(f"\n📝 Tracked: {filepath}")

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = input("\n📝 Enter message to post: ").strip()
    
    if not message:
        print("❌ No message provided")
        return
    
    # Get credentials from environment or prompt
    email = os.getenv('FACEBOOK_EMAIL')
    password = os.getenv('FACEBOOK_PASSWORD')
    
    post_to_facebook_playwright(message, email, password)
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
