#!/usr/bin/env python3
"""
Facebook Manual-Assisted Posting

Opens Facebook page, you post manually, script tracks it.
Simplest and most reliable method!
"""

import os
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

def facebook_manual_post(message):
    """
    Open Facebook page, let user post manually, track it.
    """
    
    print("\n" + "=" * 70)
    print("  FACEBOOK MANUAL-ASSISTED POSTING")
    print("=" * 70)
    
    print(f"\n📝 Message to post:")
    print(f"\n{message}\n")
    print("=" * 70)
    
    try:
        with sync_playwright() as p:
            # Use saved session
            session_path = Path('.facebook_session')
            session_path.mkdir(exist_ok=True)
            
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False
            )
            
            if len(browser.pages) > 0:
                page = browser.pages[0]
            else:
                page = browser.new_page()
            
            # Go to your Facebook page
            print("\n📄 Opening your Facebook page...")
            page.goto('https://www.facebook.com/profile.php?id=967740493097470')
            
            time.sleep(3)
            
            print("\n" + "=" * 70)
            print("  MANUAL STEPS")
            print("=" * 70)
            print("\n1. Browser me apna Facebook page khul gaya hai")
            print("2. 'What's on your mind?' ya 'Create post' click karo")
            print("3. Ye message copy-paste karo:")
            print(f"\n   {message}\n")
            print("4. 'Post' button click karo")
            print("5. Post publish hone ka wait karo")
            print("6. Wapas yahan aao aur Enter press karo")
            print("\n" + "=" * 70)
            
            input("\n✅ Press Enter after posting...")
            
            print("\n✅ Post tracked!")
            
            # Track the post
            track_post(message, True)
            
            # Keep browser open for a bit
            print("\n💡 Browser 5 seconds me band ho jayega...")
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
    filename = f"facebook_{timestamp}_manual.md"
    filepath = tracking_dir / filename
    
    status = "✅ Published" if success else "❌ Failed"
    
    content = f"""---
type: facebook_manual_post
timestamp: "{datetime.now().isoformat()}"
status: "{status}"
---

# Facebook Post (Manual)

**Status**: {status}  
**Posted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Method**: Manual-Assisted

## Message
{message}

"""
    
    if error:
        content += f"\n## Error\n{error}\n"
    
    content += "\n---\n\n*Posted via Manual-Assisted Method*\n"
    
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
    
    facebook_manual_post(message)
    
    print("\n" + "=" * 70)
    print("  ✅ DONE!")
    print("=" * 70)
    print("\n💡 Next time:")
    print("   python facebook_manual_post.py \"Your message\"")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
