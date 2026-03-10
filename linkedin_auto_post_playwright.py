"""
LinkedIn Auto-Post with Playwright
Fully automatic posting to LinkedIn using browser automation
"""

import sys
import codecs
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
import time
import os

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Add Skills to path
sys.path.insert(0, str(Path(__file__).parent / "Skills"))

from agent_skills import generate_linkedin_post

def auto_post_linkedin(content: str, session_path: str = ".linkedin_session"):
    """
    Automatically post to LinkedIn using Playwright
    
    Args:
        content: Topic or content to post
        session_path: Path to LinkedIn session directory
    """
    print("="*70)
    print("LINKEDIN AUTO-POST (PLAYWRIGHT)")
    print("="*70)
    print()
    
    # Generate AI post content
    print("🤖 Generating LinkedIn post with AI...")
    post_content = generate_linkedin_post(
        topic=content,
        style="professional",
        include_hashtags=True
    )
    print(f"\n📝 Generated content:\n{post_content}\n")
    
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
                print("Please run: python Skills/linkedin_watcher_simple.py auth")
                browser.close()
                return False
            
            print("✅ Logged in to LinkedIn")
            
            # Click "Start a post" button
            print("📝 Opening post composer...")
            
            # Try multiple selectors for the post button
            post_button_selectors = [
                'button[aria-label*="Start a post"]',
                'button:has-text("Start a post")',
                '.share-box-feed-entry__trigger',
                '[data-control-name="share_box_trigger"]'
            ]
            
            clicked = False
            for selector in post_button_selectors:
                try:
                    page.click(selector, timeout=5000)
                    clicked = True
                    print(f"✅ Clicked post button: {selector}")
                    break
                except:
                    continue
            
            if not clicked:
                print("❌ Could not find 'Start a post' button")
                print("💡 Trying alternative method...")
                
                # Alternative: Navigate directly to post creation
                page.goto('https://www.linkedin.com/feed/?shareActive=true')
                time.sleep(2)
            
            # Wait for editor to appear
            time.sleep(2)
            
            # Find and fill the post editor
            print("✍️ Writing post content...")
            
            editor_selectors = [
                '.ql-editor[contenteditable="true"]',
                'div[role="textbox"][contenteditable="true"]',
                '.share-creation-state__text-editor',
                '[data-placeholder*="share"]'
            ]
            
            filled = False
            for selector in editor_selectors:
                try:
                    editor = page.locator(selector).first
                    if editor.is_visible(timeout=5000):
                        editor.click()
                        time.sleep(1)
                        editor.fill(post_content)
                        print(f"✅ Content filled using: {selector}")
                        filled = True
                        break
                except:
                    continue
            
            if not filled:
                print("❌ Could not find post editor")
                print("📋 Content to post:")
                print("-"*70)
                print(post_content)
                print("-"*70)
                print("\n⚠️ Please paste manually and press Enter...")
                input()
            
            time.sleep(2)
            
            # Click Post button
            print("📤 Publishing post...")
            
            post_submit_selectors = [
                'button[aria-label*="Post"]',
                'button:has-text("Post")',
                '.share-actions__primary-action',
                '[data-control-name="share.post"]'
            ]
            
            posted = False
            for selector in post_submit_selectors:
                try:
                    page.click(selector, timeout=5000)
                    posted = True
                    print(f"✅ Clicked Post button: {selector}")
                    break
                except:
                    continue
            
            if not posted:
                print("⚠️ Could not find Post button automatically")
                print("Please click 'Post' button manually and press Enter...")
                input()
            
            # Wait for post to publish
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
{post_content}

## Metadata
- Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Method: Playwright Automation
- Session: {session_path}

## Engagement
- Views: (check later)
- Likes: (check later)
- Comments: (check later)
- Shares: (check later)

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
            
            # Keep browser open for 5 seconds to see result
            time.sleep(5)
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
{post_content}

## Error
{str(e)}

---
*Failed to post*
"""
            tracking_file.write_text(tracking_content, encoding='utf-8')
            
            browser.close()
            return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("="*70)
        print("LINKEDIN AUTO-POST")
        print("="*70)
        print()
        print("Usage: python linkedin_auto_post_playwright.py \"Your topic\"")
        print()
        print("Example:")
        print('   python linkedin_auto_post_playwright.py "AI automation success!"')
        print()
        print("="*70)
        sys.exit(1)
    
    topic = " ".join(sys.argv[1:])
    auto_post_linkedin(topic)
