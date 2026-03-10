"""
Quick LinkedIn Post - Opens LinkedIn, you paste and post
Fastest method
"""

import sys
import codecs
import webbrowser
import subprocess
from pathlib import Path
from datetime import datetime
import time

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def quick_post():
    print("="*70)
    print("LINKEDIN QUICK POST")
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

    print("📝 Content ready to post:\n")
    print("-"*70)
    print(content)
    print("-"*70)
    print()
    
    # Copy to clipboard
    import subprocess
    subprocess.run(['clip'], input=content.encode('utf-8'), check=True)
    
    print("✅ Content copied to clipboard!")
    print()
    print("Opening LinkedIn in 3 seconds...")
    time.sleep(3)
    
    # Open LinkedIn
    webbrowser.open('https://www.linkedin.com/feed/')
    
    print()
    print("="*70)
    print("📌 NEXT STEPS:")
    print("="*70)
    print()
    print("1. LinkedIn will open in your browser")
    print("2. Click 'Start a post'")
    print("3. Press Ctrl+V to paste (content already copied)")
    print("4. Click 'Post'")
    print()
    print("="*70)
    
    # Save tracking
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    tracking_dir = Path("Social_Media_Tracking")
    tracking_dir.mkdir(exist_ok=True)
    tracking_file = tracking_dir / f"linkedin_{timestamp}_quick.md"
    
    tracking_content = f"""---
platform: linkedin
timestamp: {timestamp}
status: manual_post
method: quick_copy_paste
---

# LinkedIn Post

{content}

Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    tracking_file.write_text(tracking_content, encoding='utf-8')
    
    print("✅ Tracking saved")
    print("="*70)

if __name__ == "__main__":
    quick_post()
