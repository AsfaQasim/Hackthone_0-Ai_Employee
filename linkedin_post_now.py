"""
LinkedIn Auto-Post - Simple Version
Posts directly to LinkedIn using Playwright
"""

import sys
import codecs
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
import time

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def post_to_linkedin(content: str, session_path: str = ".linkedin_session"):
    """
    Post to LinkedIn using browser automation
    
    Args:
        content: Content to post
        session_path: Path to LinkedIn session directory
    """
    print("="*70)
    print("LINKEDIN AUTO-POST")
    print("="*70)
    print()
    print(f"📝 Content to post:\n{content}\n")
    
    # Create tracking file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    tracking_dir = Path("Social_Media_Tracking")
    tracking_dir.mkdir(exist_ok=True)
    tracking_file = tracking_dir / f"linkedin_{timestamp}_linkedin.md"
    
    print("🌐 Opening LinkedIn...")
    
    with sync_playwright() as p:
        # Launch browser with persistent session
        browser = p.chromium.launch_persistent_context(
            session_path,
            headless=False,
            viewport={'width': 1280, 'height': 720}
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        try:
            # Go to LinkedIn
            page.goto('https://www.linkedin.com/feed/', timeout=30000)
            time.sleep(3)
            
            # Check if logged in
            if 'login' in page.url or 'authwall' in page.url:
                print("❌ Not logged in!")
                print("\n💡 Please login manually in the browser...")
                print("Press Enter after logging in...")
                input()
                page.goto('https://www.linkedin.com/feed/')
                time.sleep(3)
            
            print("✅ Logged in to LinkedIn")
            
            # Click "Start a post" button
            print("📝 Opening post composer...")
            
            # Try multiple selectors for the post button
            post_button_selectors = [
                'button:has-text("Start a post")',
                'button[aria-label*="Start a post"]',
                '.share-box-feed-entry__trigger',
                '[data-control-name="share_box_trigger"]',
                '.share-box-feed-entry'
            ]
            
            clicked = False
            for selector in post_button_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.click(timeout=5000)
                        clicked = True
                        print(f"✅ Clicked post button")
                        break
                except Exception as e:
                    continue
            
            if not clicked:
                print("⚠️ Could not find 'Start a post' button automatically")
                print("Please click 'Start a post' manually and press Enter...")
                input()
            
            # Wait for editor to appear
            time.sleep(3)
            
            # Find and fill the post editor
            print("✍️ Writing post content...")
            
            editor_selectors = [
                '.ql-editor[contenteditable="true"]',
                'div[role="textbox"][contenteditable="true"]',
                '.share-creation-state__text-editor'
            ]
            
            filled = False
            for selector in editor_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        editor = page.locator(selector).first
                        editor.click()
                        time.sleep(1)
                        
                        # Type content character by character for better reliability
                        editor.fill("")  # Clear first
                        editor.type(content, delay=50)
                        
                        print(f"✅ Content filled")
                        filled = True
                        break
                except Exception as e:
                    continue
            
            if not filled:
                print("⚠️ Could not fill content automatically")
                print("\n📋 Please paste this content manually:")
                print("-"*70)
                print(content)
                print("-"*70)
                print("\nPress Enter after pasting...")
                input()
            
            time.sleep(2)
            
            # Click Post button
            print("📤 Publishing post...")
            
            post_submit_selectors = [
                'button:has-text("Post")',
                'button[aria-label*="Post"]',
                '.share-actions__primary-action'
            ]
            
            posted = False
            for selector in post_submit_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.click(timeout=5000)
                        posted = True
                        print(f"✅ Clicked Post button")
                        break
                except Exception as e:
                    continue
            
            if not posted:
                print("⚠️ Please click 'Post' button manually and press Enter...")
                input()
            
            # Wait for post to publish
            print("⏳ Waiting for post to publish...")
            time.sleep(5)
            
            # Save tracking file
            tracking_content = f"""---
platform: linkedin
timestamp: {timestamp}
status: posted
method: playwright_auto
---

# LinkedIn Post

## Content
{content}

## Metadata
- Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Method: Playwright Automation
- Session: {session_path}

## Engagement
- Views: (check later)
- Likes: (check later)
- Comments: (check later)
- Shares: (check later)

## Post URL
Check your LinkedIn profile: https://www.linkedin.com/in/me/recent-activity/shares/

---
*Posted by LinkedIn Auto-Poster*
"""
            
            tracking_file.write_text(tracking_content, encoding='utf-8')
            
            print("\n" + "="*70)
            print("✅ POST SUCCESSFUL!")
            print("="*70)
            print(f"📝 Tracked: {tracking_file}")
            print(f"🔗 Check your post: https://www.linkedin.com/feed/")
            print("="*70)
            
            # Keep browser open for 10 seconds to see result
            print("\n💡 Browser will close in 10 seconds...")
            time.sleep(10)
            browser.close()
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print(f"📝 Tracked: {tracking_file}")
            
            # Save error tracking
            tracking_content = f"""---
platform: linkedin
timestamp: {timestamp}
status: failed
error: {str(e)}
---

# LinkedIn Post (FAILED)

## Content
{content}

## Error
{str(e)}

---
*Failed to post*
"""
            tracking_file.write_text(tracking_content, encoding='utf-8')
            
            print("\n💡 Browser will stay open for debugging...")
            time.sleep(30)
            browser.close()
            return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("="*70)
        print("LINKEDIN AUTO-POST")
        print("="*70)
        print()
        print("Usage: python linkedin_post_now.py \"Your message\"")
        print()
        print("Example:")
        print('   python linkedin_post_now.py "Excited to share my AI project! #AI"')
        print()
        print("="*70)
        sys.exit(1)
    
    content = " ".join(sys.argv[1:])
    post_to_linkedin(content)
