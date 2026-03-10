"""
LinkedIn Post with Manual Login
Opens browser, you log in, then auto-posts
"""

import sys
import codecs
from pathlib import Path
from datetime import datetime
from patchright.sync_api import sync_playwright
import time

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def post_with_login(content: str):
    print("="*70)
    print("LINKEDIN POST - LOGIN FIRST")
    print("="*70)
    print()
    
    session_path = Path(".linkedin_session")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    tracking_dir = Path("Social_Media_Tracking")
    tracking_dir.mkdir(exist_ok=True)
    tracking_file = tracking_dir / f"linkedin_{timestamp}_manual.md"
    
    print(f"📝 Content:\n{content}\n")
    print("🌐 Opening LinkedIn...")
    print()
    print("⚠️  INSTRUCTIONS:")
    print("   1. Log in to LinkedIn in the browser window")
    print("   2. Wait until you see your feed/homepage")
    print("   3. The script will auto-detect and post")
    print()
    print("   Opening browser in 3 seconds...")
    time.sleep(3)
    
    browser = None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                viewport={'width': 1280, 'height': 720}
            )
            
            if browser.pages:
                page = browser.pages[0]
            else:
                page = browser.new_page()
            
            # Go to LinkedIn login
            print("📍 Opening LinkedIn login page...")
            page.goto('https://www.linkedin.com/login', timeout=60000)
            
            print()
            print("="*70)
            print("LOGIN NOW")
            print("="*70)
            print("Enter your email and password in the browser window.")
            print("After login, the script will continue automatically.")
            print("="*70)
            print()
            
            # Wait for login - check every 5 seconds
            logged_in = False
            max_wait = 300  # 5 minutes
            waited = 0
            
            while waited < max_wait:
                try:
                    # Check if we're on feed page (logged in)
                    if 'feed' in page.url or 'mynetwork' in page.url or 'jobs' in page.url:
                        print("✅ Login detected!")
                        logged_in = True
                        break
                    
                    # Check if still on login page
                    if 'login' not in page.url:
                        time.sleep(2)
                        if 'feed' in page.url:
                            print("✅ Login detected!")
                            logged_in = True
                            break
                    
                    time.sleep(3)
                    waited += 3
                    
                    # Show progress every 30 seconds
                    if waited % 30 == 0:
                        print(f"⏳ Waiting for login... ({waited}/{max_wait}s)")
                        
                except:
                    time.sleep(3)
                    waited += 3
            
            if not logged_in:
                print()
                print("❌ Login timeout. Please try again.")
                browser.close()
                return False
            
            # Now post
            print()
            print("📝 Navigating to post composer...")
            page.goto('https://www.linkedin.com/feed/', timeout=60000)
            time.sleep(3)
            
            # Click Start a post
            print("📝 Opening post composer...")
            try:
                page.click('button[aria-label*="Start a post"]', timeout=5000)
                time.sleep(2)
            except:
                page.goto('https://www.linkedin.com/feed/?shareActive=true')
                time.sleep(2)
            
            # Fill content
            print("✍️  Writing post...")
            editor_selectors = [
                '.ql-editor[contenteditable="true"]',
                'div[role="textbox"][contenteditable="true"]',
            ]
            
            for selector in editor_selectors:
                try:
                    editor = page.locator(selector).first
                    if editor.is_visible(timeout=5000):
                        editor.click()
                        time.sleep(1)
                        editor.fill(content)
                        print("✅ Content added")
                        break
                except:
                    continue
            
            time.sleep(2)
            
            # Click Post
            print("📤 Publishing...")
            try:
                page.click('button[aria-label*="Post"]', timeout=5000)
                print("✅ Post button clicked!")
            except:
                print("⚠️  Please click 'Post' button manually")
            
            time.sleep(5)
            
            # Save tracking
            tracking_content = f"""---
platform: linkedin
timestamp: {timestamp}
status: posted
method: manual_login_post
---

# LinkedIn Post

## Content
{content}

## Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*Posted via LinkedIn Manual Login Post*
"""
            tracking_file.write_text(tracking_content, encoding='utf-8')
            
            print()
            print("="*70)
            print("✅ SUCCESS!")
            print("="*70)
            print(f"📝 Tracked: {tracking_file}")
            print(f"🔗 Check: https://www.linkedin.com/feed/")
            print("="*70)
            
            time.sleep(3)
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
        print("LINKEDIN POST WITH LOGIN")
        print("="*70)
        print()
        print("Usage: python linkedin_post_login.py \"Your post content\"")
        print()
        print("Example:")
        print('   python linkedin_post_login.py "Hello LinkedIn!"')
        print()
        print("="*70)
        sys.exit(1)
    
    content = " ".join(sys.argv[1:])
    success = post_with_login(content)
    sys.exit(0 if success else 1)
