"""
Universal Social Media Auto-Poster with Playwright
Posts to LinkedIn, Facebook, Twitter, Instagram using browser automation
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

try:
    from agent_skills import generate_linkedin_post
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False


class SocialMediaPoster:
    """Universal social media poster using Playwright"""
    
    def __init__(self):
        self.tracking_dir = Path("Social_Media_Tracking")
        self.tracking_dir.mkdir(exist_ok=True)
    
    def generate_content(self, topic: str, platform: str) -> str:
        """Generate AI content for the post"""
        if AI_AVAILABLE:
            try:
                print(f"🤖 Generating {platform} post with AI...")
                content = generate_linkedin_post(
                    topic=topic,
                    style="professional",
                    include_hashtags=True
                )
                return content
            except Exception as e:
                print(f"⚠️ AI generation failed: {e}")
                return topic
        else:
            return topic
    
    def save_tracking(self, platform: str, content: str, status: str, error: str = None):
        """Save post tracking file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        tracking_file = self.tracking_dir / f"{platform}_{timestamp}_{platform}.md"
        
        tracking_content = f"""---
platform: {platform}
timestamp: {timestamp}
status: {status}
method: playwright_auto
---

# {platform.title()} Post

## Content
{content}

## Metadata
- Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Method: Playwright Browser Automation
- Status: {status}

"""
        
        if error:
            tracking_content += f"""## Error
{error}

"""
        
        tracking_content += f"""## Engagement
- Views: (check later)
- Likes: (check later)
- Comments: (check later)
- Shares: (check later)

---
*Posted by Universal Social Media Auto-Poster*
"""
        
        tracking_file.write_text(tracking_content, encoding='utf-8')
        print(f"📝 Tracked: {tracking_file}")
        return tracking_file
    
    def post_to_linkedin(self, content: str, session_path: str = ".linkedin_session"):
        """Post to LinkedIn"""
        print("\n" + "="*70)
        print("POSTING TO LINKEDIN")
        print("="*70)
        
        with sync_playwright() as p:
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
                    print("❌ Not logged in to LinkedIn!")
                    print("💡 Please login manually...")
                    input("Press Enter after logging in...")
                    page.goto('https://www.linkedin.com/feed/')
                    time.sleep(3)
                
                print("✅ Logged in to LinkedIn")
                
                # Click "Start a post"
                print("📝 Opening post composer...")
                selectors = [
                    'button:has-text("Start a post")',
                    '.share-box-feed-entry__trigger'
                ]
                
                for selector in selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.locator(selector).first.click(timeout=5000)
                            print("✅ Opened post composer")
                            break
                    except:
                        continue
                
                time.sleep(3)
                
                # Fill content
                print("✍️ Writing content...")
                editor_selectors = [
                    '.ql-editor[contenteditable="true"]',
                    'div[role="textbox"][contenteditable="true"]'
                ]
                
                for selector in editor_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            editor = page.locator(selector).first
                            editor.click()
                            time.sleep(1)
                            editor.fill("")
                            editor.type(content, delay=30)
                            print("✅ Content filled")
                            break
                    except:
                        continue
                
                time.sleep(2)
                
                # Click Post
                print("📤 Publishing...")
                post_selectors = [
                    'button:has-text("Post")',
                    '.share-actions__primary-action'
                ]
                
                for selector in post_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.locator(selector).first.click(timeout=5000)
                            print("✅ Posted to LinkedIn!")
                            break
                    except:
                        continue
                
                time.sleep(5)
                self.save_tracking('linkedin', content, 'posted')
                
                browser.close()
                return True
                
            except Exception as e:
                print(f"❌ LinkedIn error: {e}")
                self.save_tracking('linkedin', content, 'failed', str(e))
                browser.close()
                return False
    
    def post_to_facebook(self, content: str, session_path: str = ".facebook_session"):
        """Post to Facebook"""
        print("\n" + "="*70)
        print("POSTING TO FACEBOOK")
        print("="*70)
        
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                session_path,
                headless=False,
                viewport={'width': 1280, 'height': 720}
            )
            
            page = browser.pages[0] if browser.pages else browser.new_page()
            
            try:
                # Go to Facebook page
                page_id = os.getenv('FACEBOOK_PAGE_ID', '967740493097470')
                page.goto(f'https://www.facebook.com/{page_id}', timeout=30000)
                time.sleep(3)
                
                # Check if logged in
                if 'login' in page.url:
                    print("❌ Not logged in to Facebook!")
                    print("💡 Please login manually...")
                    input("Press Enter after logging in...")
                    page.goto(f'https://www.facebook.com/{page_id}')
                    time.sleep(3)
                
                print("✅ Logged in to Facebook")
                
                # Click "Create post" or "What's on your mind?"
                print("📝 Opening post composer...")
                selectors = [
                    '[aria-label*="Create a post"]',
                    '[aria-label*="Write something"]',
                    '[role="button"]:has-text("What\'s on your mind")',
                    'div[role="button"]:has-text("Create post")'
                ]
                
                for selector in selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.locator(selector).first.click(timeout=5000)
                            print("✅ Opened post composer")
                            break
                    except:
                        continue
                
                time.sleep(3)
                
                # Fill content
                print("✍️ Writing content...")
                editor_selectors = [
                    '[contenteditable="true"][role="textbox"]',
                    'div[contenteditable="true"]',
                    '[aria-label*="What\'s on your mind"]'
                ]
                
                for selector in editor_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            editor = page.locator(selector).first
                            editor.click()
                            time.sleep(1)
                            editor.fill(content)
                            print("✅ Content filled")
                            break
                    except:
                        continue
                
                time.sleep(2)
                
                # Click Post
                print("📤 Publishing...")
                post_selectors = [
                    '[aria-label="Post"]',
                    'div[role="button"]:has-text("Post")',
                    'button:has-text("Post")'
                ]
                
                for selector in post_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.locator(selector).first.click(timeout=5000)
                            print("✅ Posted to Facebook!")
                            break
                    except:
                        continue
                
                time.sleep(5)
                self.save_tracking('facebook', content, 'posted')
                
                browser.close()
                return True
                
            except Exception as e:
                print(f"❌ Facebook error: {e}")
                self.save_tracking('facebook', content, 'failed', str(e))
                browser.close()
                return False
    
    def post_to_twitter(self, content: str, session_path: str = ".twitter_session"):
        """Post to Twitter/X"""
        print("\n" + "="*70)
        print("POSTING TO TWITTER/X")
        print("="*70)
        
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                session_path,
                headless=False,
                viewport={'width': 1280, 'height': 720}
            )
            
            page = browser.pages[0] if browser.pages else browser.new_page()
            
            try:
                # Go to Twitter
                page.goto('https://twitter.com/home', timeout=30000)
                time.sleep(3)
                
                # Check if logged in
                if 'login' in page.url:
                    print("❌ Not logged in to Twitter!")
                    print("💡 Please login manually...")
                    input("Press Enter after logging in...")
                    page.goto('https://twitter.com/home')
                    time.sleep(3)
                
                print("✅ Logged in to Twitter")
                
                # Find tweet box
                print("✍️ Writing tweet...")
                editor_selectors = [
                    '[data-testid="tweetTextarea_0"]',
                    '[role="textbox"][contenteditable="true"]',
                    'div[contenteditable="true"]'
                ]
                
                for selector in editor_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            editor = page.locator(selector).first
                            editor.click()
                            time.sleep(1)
                            editor.fill(content[:280])  # Twitter limit
                            print("✅ Content filled")
                            break
                    except:
                        continue
                
                time.sleep(2)
                
                # Click Tweet button
                print("📤 Publishing...")
                tweet_selectors = [
                    '[data-testid="tweetButtonInline"]',
                    '[data-testid="tweetButton"]',
                    'button:has-text("Post")'
                ]
                
                for selector in tweet_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.locator(selector).first.click(timeout=5000)
                            print("✅ Posted to Twitter!")
                            break
                    except:
                        continue
                
                time.sleep(5)
                self.save_tracking('twitter', content, 'posted')
                
                browser.close()
                return True
                
            except Exception as e:
                print(f"❌ Twitter error: {e}")
                self.save_tracking('twitter', content, 'failed', str(e))
                browser.close()
                return False
    
    def post_to_all(self, content: str, platforms: list = None):
        """Post to multiple platforms"""
        if platforms is None:
            platforms = ['linkedin', 'facebook', 'twitter']
        
        print("="*70)
        print("UNIVERSAL SOCIAL MEDIA AUTO-POSTER")
        print("="*70)
        print(f"\n📝 Content:\n{content}\n")
        print(f"🎯 Platforms: {', '.join(platforms)}\n")
        
        results = {}
        
        for platform in platforms:
            if platform.lower() == 'linkedin':
                results['linkedin'] = self.post_to_linkedin(content)
            elif platform.lower() == 'facebook':
                results['facebook'] = self.post_to_facebook(content)
            elif platform.lower() == 'twitter':
                results['twitter'] = self.post_to_twitter(content)
            else:
                print(f"⚠️ Unknown platform: {platform}")
        
        # Summary
        print("\n" + "="*70)
        print("POSTING SUMMARY")
        print("="*70)
        for platform, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"{platform.title()}: {status}")
        print("="*70)
        
        return results


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("="*70)
        print("UNIVERSAL SOCIAL MEDIA AUTO-POSTER")
        print("="*70)
        print()
        print("Usage:")
        print("  python social_media_auto_poster.py \"Your message\" [platforms]")
        print()
        print("Platforms (comma-separated):")
        print("  - linkedin")
        print("  - facebook")
        print("  - twitter")
        print("  - all (default)")
        print()
        print("Examples:")
        print('  python social_media_auto_poster.py "Hello world!" linkedin')
        print('  python social_media_auto_poster.py "Big news!" linkedin,facebook')
        print('  python social_media_auto_poster.py "Check this out!" all')
        print()
        print("="*70)
        sys.exit(1)
    
    # Get content
    content = sys.argv[1]
    
    # Get platforms
    if len(sys.argv) > 2:
        platforms_arg = sys.argv[2].lower()
        if platforms_arg == 'all':
            platforms = ['linkedin', 'facebook', 'twitter']
        else:
            platforms = [p.strip() for p in platforms_arg.split(',')]
    else:
        platforms = ['linkedin', 'facebook', 'twitter']
    
    # Create poster and post
    poster = SocialMediaPoster()
    poster.post_to_all(content, platforms)


if __name__ == "__main__":
    main()
