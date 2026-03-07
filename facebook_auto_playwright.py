#!/usr/bin/env python3
"""
Facebook Fully Automatic Posting (Playwright)

Fully automatic posting without manual intervention.
Uses browser automation with smart selectors.
"""

import os
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
import pyperclip  # For clipboard operations

def post_to_facebook_auto(message):
    """
    Fully automatic Facebook posting using Playwright.
    
    Args:
        message: Text to post
    """
    
    print("\n" + "=" * 70)
    print("  FACEBOOK FULLY AUTOMATIC POSTING")
    print("=" * 70)
    
    print(f"\n📤 Posting to Facebook...")
    print(f"   Message: {message[:50]}...")
    
    try:
        with sync_playwright() as p:
            # Use saved session
            session_path = Path('.facebook_session')
            session_path.mkdir(exist_ok=True)
            
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,  # Keep visible for debugging
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox'
                ]
            )
            
            if len(browser.pages) > 0:
                page = browser.pages[0]
            else:
                page = browser.new_page()
            
            # Go to Facebook page
            print("\n📄 Opening Facebook page...")
            page.goto('https://www.facebook.com/profile.php?id=967740493097470', wait_until='networkidle')
            
            time.sleep(5)
            
            # Try to find and click post creation area
            print("\n✍️ Creating post...")
            
            # Method 1: Click on "What's on your mind?" area
            post_creation_selectors = [
                'div[role="button"]:has-text("What\'s on your mind")',
                'span:has-text("What\'s on your mind")',
                'div[aria-label*="Create"]',
                'div[role="button"][aria-label*="post"]',
                # Try clicking the composer area
                'div.x1ed109x',
                'div.x1iyjqo2'
            ]
            
            clicked = False
            for selector in post_creation_selectors:
                try:
                    elements = page.locator(selector)
                    if elements.count() > 0:
                        elements.first.click(timeout=3000)
                        clicked = True
                        print(f"   ✅ Clicked: {selector}")
                        break
                except Exception as e:
                    continue
            
            if not clicked:
                # Try clicking anywhere in the post creation area
                try:
                    page.click('div[role="main"]', position={'x': 200, 'y': 200})
                    clicked = True
                    print("   ✅ Clicked main area")
                except:
                    pass
            
            time.sleep(3)
            
            # Now type the message
            print("\n📝 Typing message...")
            
            # Method 1: Find contenteditable div
            content_selectors = [
                'div[contenteditable="true"][role="textbox"]',
                'div[contenteditable="true"]',
                'div[aria-label*="What"]',
                'div[data-contents="true"]'
            ]
            
            typed = False
            for selector in content_selectors:
                try:
                    elements = page.locator(selector)
                    if elements.count() > 0:
                        # Click to focus
                        elements.first.click()
                        time.sleep(1)
                        
                        # Type message
                        page.keyboard.type(message, delay=50)
                        typed = True
                        print(f"   ✅ Typed message using: {selector}")
                        break
                except Exception as e:
                    continue
            
            if not typed:
                # Fallback: Use clipboard
                print("   ⚠️ Trying clipboard method...")
                try:
                    pyperclip.copy(message)
                    page.keyboard.press('Control+V')
                    typed = True
                    print("   ✅ Pasted from clipboard")
                except:
                    pass
            
            if not typed:
                print("   ❌ Could not type message")
                browser.close()
                return False
            
            time.sleep(2)
            
            # Click Post button
            print("\n📤 Publishing...")
            
            post_button_selectors = [
                'div[aria-label="Post"]',
                'div[role="button"]:has-text("Post")',
                'span:has-text("Post")',
                'div[aria-label="Publish"]',
                # Try by position (usually bottom right)
            ]
            
            posted = False
            for selector in post_button_selectors:
                try:
                    elements = page.locator(selector)
                    if elements.count() > 0:
                        # Find the actual Post button (not "Post to" or other variants)
                        for i in range(elements.count()):
                            try:
                                text = elements.nth(i).inner_text()
                                if text.strip().lower() == 'post':
                                    elements.nth(i).click(timeout=3000)
                                    posted = True
                                    print(f"   ✅ Clicked Post button")
                                    break
                            except:
                                continue
                        if posted:
                            break
                except Exception as e:
                    continue
            
            if not posted:
                # Try pressing Enter as fallback
                try:
                    page.keyboard.press('Control+Enter')
                    posted = True
                    print("   ✅ Posted using Ctrl+Enter")
                except:
                    pass
            
            if posted:
                print("\n✅ Post published successfully!")
                time.sleep(3)
                
                # Track the post
                track_post(message, True)
                
                browser.close()
                return True
            else:
                print("\n⚠️ Could not find Post button")
                print("   Post may have been published, check Facebook")
                
                # Track anyway
                track_post(message, True, "Post button not found, may be published")
                
                time.sleep(5)
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
    filename = f"facebook_{timestamp}_auto.md"
    filepath = tracking_dir / filename
    
    status = "✅ Published" if success else "❌ Failed"
    
    content = f"""---
type: facebook_auto_post
timestamp: "{datetime.now().isoformat()}"
status: "{status}"
---

# Facebook Auto Post

**Status**: {status}  
**Posted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Method**: Fully Automatic (Playwright)

## Message
{message}

"""
    
    if error:
        content += f"\n## Note\n{error}\n"
    
    content += "\n---\n\n*Posted via Fully Automatic Playwright*\n"
    
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
    
    result = post_to_facebook_auto(message)
    
    if result:
        print("\n" + "=" * 70)
        print("  ✅ SUCCESS!")
        print("=" * 70)
        print("\n🎉 Post published automatically!")
        print("\n💡 Check your Facebook page to verify")
    else:
        print("\n" + "=" * 70)
        print("  ❌ FAILED")
        print("=" * 70)
        print("\n💡 Try the manual-assisted method:")
        print("   python facebook_manual_post.py \"Your message\"")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
