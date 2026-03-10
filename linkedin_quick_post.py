"""
LinkedIn Quick Post - Uses existing session
No re-authentication needed - uses .linkedin_session directory
"""

import sys
import codecs
from pathlib import Path
from datetime import datetime
from patchright.sync_api import sync_playwright
import time

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def quick_post_linkedin(content: str):
    """
    Post to LinkedIn using existing session in .linkedin_session
    """
    print("="*70)
    print("LINKEDIN QUICK POST")
    print("="*70)
    print()
    
    session_path = Path(".linkedin_session")
    
    if not session_path.exists():
        print("❌ No LinkedIn session found!")
        print("Please make sure you're logged in to LinkedIn.")
        return False
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    tracking_dir = Path("Social_Media_Tracking")
    tracking_dir.mkdir(exist_ok=True)
    tracking_file = tracking_dir / f"linkedin_{timestamp}_quick.md"
    
    print(f"📝 Content:\n{content}\n")
    print("🌐 Opening LinkedIn with existing session...")
    print()
    
    browser = None
    try:
        with sync_playwright() as p:
            # Launch browser with existing session
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                viewport={'width': 1280, 'height': 720},
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox'
                ]
            )
            
            # Get or create page
            if browser.pages:
                page = browser.pages[0]
            else:
                page = browser.new_page()
            
            # Navigate to LinkedIn
            print("📍 Going to LinkedIn...")
            page.goto('https://www.linkedin.com/feed/', timeout=60000)
            time.sleep(3)
            
            # Check if logged in
            if 'login' in page.url or 'authwall' in page.url:
                print("❌ Not logged in!")
                print("Please log in to LinkedIn in your browser.")
                browser.close()
                return False
            
            print("✅ Logged in")
            print()
            
            # Click "Start a post" button
            print("📝 Opening post composer...")
            
            post_button_selectors = [
                'button[aria-label*="Start a post"]',
                'button:has-text("Start a post")',
                '.share-box-feed-entry__trigger',
            ]
            
            clicked = False
            for selector in post_button_selectors:
                try:
                    if page.is_visible(selector, timeout=5000):
                        page.click(selector)
                        clicked = True
                        print(f"✅ Post composer opened")
                        break
                except:
                    continue
            
            if not clicked:
                page.goto('https://www.linkedin.com/feed/?shareActive=true')
                time.sleep(2)
            
            time.sleep(2)
            
            # Fill content
            print("✍️  Writing post...")
            
            editor_selectors = [
                '.ql-editor[contenteditable="true"]',
                'div[role="textbox"][contenteditable="true"]',
            ]
            
            filled = False
            for selector in editor_selectors:
                try:
                    editor = page.locator(selector).first
                    if editor.is_visible(timeout=5000):
                        editor.click()
                        time.sleep(1)
                        editor.fill(content)
                        filled = True
                        print(f"✅ Content added")
                        break
                except:
                    continue
            
            if not filled:
                print("❌ Could not fill content")
                browser.close()
                return False
            
            time.sleep(2)
            
            # Click Post button
            print("📤 Publishing...")
            
            post_submit_selectors = [
                'button[aria-label*="Post"]',
                'button:has-text("Post")',
            ]
            
            posted = False
            for selector in post_submit_selectors:
                try:
                    if page.is_visible(selector, timeout=5000):
                        page.click(selector)
                        posted = True
                        print(f"✅ Post published!")
                        break
                except:
                    continue
            
            if not posted:
                print("⚠️  Please click 'Post' button manually")
                input("Press Enter when done...")
            
            time.sleep(3)
            
            # Save tracking
            tracking_content = f"""---
platform: linkedin
timestamp: {timestamp}
status: posted
method: quick_post
---

# LinkedIn Post

## Content
{content}

## Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*Posted via LinkedIn Quick Post*
"""
            tracking_file.write_text(tracking_content, encoding='utf-8')
            
            print()
            print("="*70)
            print("✅ SUCCESS!")
            print("="*70)
            print(f"📝 Tracked: {tracking_file}")
            print(f"🔗 Check: https://www.linkedin.com/feed/")
            print("="*70)
            
            time.sleep(2)
            browser.close()
            
            return True
            
    except Exception as e:
        print()
        print("="*70)
        print("❌ FAILED")
        print("="*70)
        print(f"Error: {str(e)}")
        
        if browser:
            try:
                browser.close()
            except:
                pass
        
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("="*70)
        print("LINKEDIN QUICK POST")
        print("="*70)
        print()
        print("Usage: python linkedin_quick_post.py \"Your post content\"")
        print()
        print("Example:")
        print('   python linkedin_quick_post.py "Hello LinkedIn!"')
        print()
        print("="*70)
        sys.exit(1)
    
    content = " ".join(sys.argv[1:])
    success = quick_post_linkedin(content)
    sys.exit(0 if success else 1)
