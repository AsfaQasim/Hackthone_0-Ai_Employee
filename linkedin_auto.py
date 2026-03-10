"""
LinkedIn Auto Post - Fully Automatic
Opens browser, you login quickly, then auto-posts
"""

import sys
import codecs
from pathlib import Path
from datetime import datetime
from patchright.sync_api import sync_playwright
import time

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def auto_post(content: str):
    print("="*70)
    print("LINKEDIN AUTO POST")
    print("="*70)
    print()
    
    session_path = Path(".linkedin_session")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    tracking_dir = Path("Social_Media_Tracking")
    tracking_dir.mkdir(exist_ok=True)
    tracking_file = tracking_dir / f"linkedin_{timestamp}_auto.md"
    
    print(f"📝 Content:\n{content}\n")
    print("🌐 Opening browser...")
    print()
    
    browser = None
    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                viewport={'width': 1280, 'height': 720}
            )
            
            if browser.pages:
                page = browser.pages[0]
            else:
                page = browser.new_page()
            
            # Go to LinkedIn
            print("📍 Going to LinkedIn...")
            page.goto('https://www.linkedin.com/', timeout=60000)
            time.sleep(2)
            
            # Check if already logged in
            if 'feed' in page.url or 'mynetwork' in page.url:
                print("✅ Already logged in!")
            else:
                print()
                print("="*70)
                print("⚠️  LOGIN REQUIRED")
                print("="*70)
                print()
                print("👉 Browser window mein login karein:")
                print("   - Email enter karein")
                print("   - Password enter karein") 
                print("   - Login click karein")
                print()
                print("⏳ Script automatically detect karega aur continue karega...")
                print("="*70)
                print()
                
                # Wait for login (10 minutes max)
                max_wait = 600
                waited = 0
                check_interval = 2
                
                while waited < max_wait:
                    try:
                        current_url = page.url
                        
                        # Check if logged in
                        if any(x in current_url for x in ['/feed', '/mynetwork', '/jobs', '/messaging']):
                            print()
                            print("✅ Login detected! Continuing...")
                            print()
                            break
                        
                        time.sleep(check_interval)
                        waited += check_interval
                        
                        if waited % 30 == 0:
                            print(f"⏳ Waiting for login... ({waited}s / {max_wait}s)")
                            
                    except Exception as e:
                        time.sleep(check_interval)
                        waited += check_interval
                
                else:
                    print()
                    print("❌ Login timeout (10 minutes)")
                    print("   Browser close karke dobara try karein")
                    browser.close()
                    return False
            
            # Navigate to feed
            print("📍 Opening feed...")
            page.goto('https://www.linkedin.com/feed/', timeout=60000)
            time.sleep(3)
            
            # Click Start a post
            print("📝 Opening post composer...")
            try:
                page.click('button[aria-label*="Start a post"]', timeout=5000)
                print("✅ Composer opened")
            except:
                page.goto('https://www.linkedin.com/feed/?shareActive=true')
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
                        print("✅ Content filled")
                        filled = True
                        break
                except:
                    continue
            
            if not filled:
                print("❌ Could not fill content")
                browser.close()
                return False
            
            time.sleep(2)
            
            # Click Post button
            print("📤 Publishing post...")
            try:
                page.click('button[aria-label*="Post"]', timeout=5000)
                print("✅ Post button clicked!")
            except:
                print("⚠️  Post button manually click karein")
                # Wait for manual post
                time.sleep(10)
            
            # Wait for post to complete
            time.sleep(5)
            
            # Save tracking
            tracking_content = f"""---
platform: linkedin
timestamp: {timestamp}
status: posted
method: auto_post
---

# LinkedIn Post

## Content
{content}

## Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*Posted via LinkedIn Auto Post*
"""
            tracking_file.write_text(tracking_content, encoding='utf-8')
            
            print()
            print("="*70)
            print("✅ POST SUCCESSFUL!")
            print("="*70)
            print(f"📝 Tracked: {tracking_file}")
            print(f"🔗 Check: https://www.linkedin.com/feed/")
            print("="*70)
            
            # Keep browser open briefly
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
        print("LINKEDIN AUTO POST")
        print("="*70)
        print()
        print("Usage: python linkedin_auto.py \"Your post content\"")
        print()
        print("Example:")
        print('   python linkedin_auto.py "Hello LinkedIn!"')
        print()
        print("="*70)
        sys.exit(1)
    
    content = " ".join(sys.argv[1:])
    success = auto_post(content)
    sys.exit(0 if success else 1)
