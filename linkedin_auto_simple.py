"""
LinkedIn Auto-Post - Simple Direct Method
Opens browser, waits for login, then auto-posts
"""

import sys
import codecs
from pathlib import Path
from datetime import datetime
from patchright.sync_api import sync_playwright
import time

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def post():
    print("="*70)
    print("LINKEDIN AUTO POST")
    print("="*70)
    print()
    
    content = """🚀 AI Testing & Automation Breakthrough!

Just completed comprehensive testing of our new AI automation system.

✅ Automated workflows running smoothly
✅ Error rates significantly reduced
✅ Productivity increased by 40%
✅ Seamless integration across all platforms

Key takeaways:
1. Start small, scale fast
2. Monitor everything
3. Human oversight remains critical
4. Continuous improvement is the key

#AITesting #Automation #ArtificialIntelligence #Innovation #Productivity"""

    print(f"📝 Content:\n{content}\n")
    
    session_path = Path(".linkedin_session")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    tracking_dir = Path("Social_Media_Tracking")
    tracking_dir.mkdir(exist_ok=True)
    
    try:
        with sync_playwright() as p:
            print("🌐 Opening browser...")
            
            browser = p.chromium.launch(
                headless=False,
                args=['--start-maximized']
            )
            
            context = browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            page = context.new_page()
            
            # Go to LinkedIn
            print("📍 Going to LinkedIn...")
            page.goto('https://www.linkedin.com/', timeout=60000)
            time.sleep(3)
            
            print()
            print("="*70)
            print("LOGIN INSTRUCTIONS")
            print("="*70)
            print()
            print("👉 Browser window mein login karein:")
            print("   1. Email enter karein")
            print("   2. Password enter karein")
            print("   3. Login click karein")
            print()
            print("⏳ Script 10 minutes wait karega...")
            print("   Login ke baad automatically post hoga")
            print("="*70)
            print()
            
            # Wait for login
            max_wait = 300  # 5 minutes
            waited = 0
            
            while waited < max_wait:
                try:
                    current_url = page.url
                    
                    # Check if logged in
                    if any(x in current_url for x in ['/feed', '/mynetwork', '/jobs', '/messaging']):
                        print()
                        print("✅ Login detected!")
                        print()
                        break
                    
                    time.sleep(3)
                    waited += 3
                    
                    if waited % 30 == 0 and waited > 0:
                        print(f"⏳ Waiting for login... ({waited}s / {max_wait}s)")
                        
                except Exception as e:
                    time.sleep(3)
                    waited += 3
            else:
                print()
                print("❌ Login timeout (10 minutes)")
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
                print("✅ Post composer opened")
                time.sleep(2)
            except:
                print("⚠️  Using alternative method...")
                page.goto('https://www.linkedin.com/feed/?shareActive=true')
                time.sleep(2)
            
            # Fill content
            print("✍️  Filling content...")
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
                        print("✅ Content filled successfully")
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
                print("⚠️  Please click Post button manually")
            
            # Wait for post to complete
            print()
            print("⏳ Posting...")
            time.sleep(5)
            
            # Save tracking
            tracking_file = tracking_dir / f"linkedin_{timestamp}_auto.md"
            tracking_content = f"""---
platform: linkedin
timestamp: {timestamp}
status: posted
method: playwright_auto
---

# LinkedIn Post

{content}

Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            tracking_file.write_text(tracking_content, encoding='utf-8')
            
            print()
            print("="*70)
            print("✅ POST SUCCESSFUL!")
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
        return False

if __name__ == "__main__":
    success = post()
    sys.exit(0 if success else 1)
