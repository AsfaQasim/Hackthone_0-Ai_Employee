"""
LinkedIn MCP Auto-Poster with Playwright
Automatically post to LinkedIn using the MCP server and Playwright browser automation
"""

import sys
import codecs
from pathlib import Path
from datetime import datetime
from patchright.sync_api import sync_playwright
import time
import os
import json

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Add Skills to path
sys.path.insert(0, str(Path(__file__).parent / "Skills"))


class LinkedInMCPAutoPoster:
    """
    LinkedIn Auto-Poster using MCP Server and Playwright
    """
    
    def __init__(self, profile_path: str = None):
        """
        Initialize the LinkedIn MCP Auto-Poster
        
        Args:
            profile_path: Path to LinkedIn browser profile (default: ~/.linkedin-mcp/profile)
        """
        if profile_path is None:
            self.profile_path = Path.home() / ".linkedin-mcp" / "profile"
        else:
            self.profile_path = Path(profile_path)
        
        self.tracking_dir = Path("Social_Media_Tracking")
        self.tracking_dir.mkdir(exist_ok=True)
        
    def generate_post_content(self, topic: str, style: str = "professional") -> str:
        """
        Generate AI-powered LinkedIn post content
        
        Args:
            topic: Topic or content to post
            style: Post style (professional, casual, enthusiastic)
            
        Returns:
            Generated post content
        """
        try:
            from agent_skills import generate_linkedin_post
            return generate_linkedin_post(
                topic=topic,
                style=style,
                include_hashtags=True
            )
        except ImportError:
            # Fallback if agent_skills not available
            return f"""🚀 {topic}

#ProfessionalDevelopment #CareerGrowth #Innovation

---
Posted via LinkedIn MCP Auto-Poster
"""
    
    def post(self, content: str, headless: bool = False, slow_mo: int = 0) -> bool:
        """
        Post content to LinkedIn
        
        Args:
            content: Content to post
            headless: Run browser in headless mode
            slow_mo: Slow motion delay in ms for debugging
            
        Returns:
            True if successful, False otherwise
        """
        print("="*70)
        print("LINKEDIN MCP AUTO-POST")
        print("="*70)
        print()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        tracking_file = self.tracking_dir / f"linkedin_{timestamp}_mcp.md"
        
        print(f"📝 Content to post:\n{content}\n")
        print("🌐 Opening LinkedIn with persistent profile...")
        print()
        
        browser = None
        try:
            with sync_playwright() as p:
                # Launch browser with persistent profile
                browser = p.chromium.launch_persistent_context(
                    str(self.profile_path),
                    headless=headless,
                    viewport={'width': 1280, 'height': 720},
                    slow_mo=slow_mo,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox'
                    ]
                )
                
                # Create or get page
                if browser.pages:
                    page = browser.pages[0]
                else:
                    page = browser.new_page()
                
                # Navigate to LinkedIn
                print("📍 Navigating to LinkedIn...")
                page.goto('https://www.linkedin.com/feed/', timeout=60000)
                time.sleep(3)
                
                # Check if logged in
                if 'login' in page.url or 'authwall' in page.url:
                    print("❌ Not logged in to LinkedIn!")
                    print()
                    print("Please authenticate first:")
                    print("   python linkedin_mcp_auth.py")
                    self._save_tracking_file(tracking_file, timestamp, content, "failed", "Not logged in")
                    browser.close()
                    return False
                
                print("✅ Logged in successfully")
                print()
                
                # Click "Start a post" button
                print("📝 Opening post composer...")
                
                post_button_selectors = [
                    'button[aria-label*="Start a post"]',
                    'button:has-text("Start a post")',
                    '.share-box-feed-entry__trigger',
                    '[data-control-name="share_box_trigger"]'
                ]
                
                clicked = False
                for selector in post_button_selectors:
                    try:
                        if page.is_visible(selector, timeout=5000):
                            page.click(selector)
                            clicked = True
                            print(f"✅ Clicked post button")
                            break
                    except:
                        continue
                
                if not clicked:
                    print("⚠️  Trying alternative method...")
                    page.goto('https://www.linkedin.com/feed/?shareActive=true')
                    time.sleep(2)
                
                time.sleep(2)
                
                # Fill the post editor
                print("✍️  Writing post content...")
                
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
                            editor.fill(content)
                            filled = True
                            print(f"✅ Content filled")
                            break
                    except:
                        continue
                
                if not filled:
                    print("❌ Could not find post editor")
                    self._save_tracking_file(tracking_file, timestamp, content, "failed", "Editor not found")
                    browser.close()
                    return False
                
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
                        if page.is_visible(selector, timeout=5000):
                            page.click(selector)
                            posted = True
                            print(f"✅ Post published")
                            break
                    except:
                        continue
                
                if not posted:
                    print("⚠️  Could not click Post button automatically")
                    print("Please click 'Post' button manually")
                    input("Press Enter when done...")
                
                # Wait for post to publish
                time.sleep(5)
                
                # Save tracking file
                self._save_tracking_file(tracking_file, timestamp, content, "posted")
                
                print()
                print("="*70)
                print("✅ POST SUCCESSFUL!")
                print("="*70)
                print(f"📝 Tracked: {tracking_file}")
                print(f"🔗 Check your post: https://www.linkedin.com/feed/")
                print("="*70)
                
                # Keep browser open briefly
                time.sleep(3)
                browser.close()
                
                return True
                
        except Exception as e:
            print()
            print("="*70)
            print("❌ POST FAILED")
            print("="*70)
            print(f"Error: {str(e)}")
            print()
            
            self._save_tracking_file(tracking_file, timestamp, content, "failed", str(e))
            
            if browser:
                try:
                    browser.close()
                except:
                    pass
            
            return False
    
    def _save_tracking_file(self, tracking_file: Path, timestamp: str, content: str, 
                          status: str, error: str = None):
        """Save post tracking information"""
        tracking_content = f"""---
platform: linkedin
timestamp: {timestamp}
status: {status}
method: linkedin_mcp_playwright
profile: {self.profile_path}
"""
        if error:
            tracking_content += f"""error: {error}
"""
        
        tracking_content += f"""---

# LinkedIn Post

## Content
{content}

## Metadata
- Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Method: LinkedIn MCP with Playwright
- Profile: {self.profile_path}

## Engagement
- Views: (check later)
- Likes: (check later)
- Comments: (check later)
- Shares: (check later)

---
*Posted by LinkedIn MCP Auto-Poster*
"""
        
        tracking_file.write_text(tracking_content, encoding='utf-8')


def auto_post_linkedin(topic: str, style: str = "professional", 
                       headless: bool = False, profile_path: str = None):
    """
    Convenience function to auto-post to LinkedIn
    
    Args:
        topic: Topic to post about
        style: Post style (professional, casual, enthusiastic)
        headless: Run browser in headless mode
        profile_path: Custom profile path
    """
    poster = LinkedInMCPAutoPoster(profile_path)
    
    # Generate content
    print("🤖 Generating LinkedIn post with AI...")
    content = poster.generate_post_content(topic, style)
    print()
    
    # Post
    success = poster.post(content, headless=headless)
    return success


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="LinkedIn MCP Auto-Poster with Playwright",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python linkedin_mcp_auto_post.py "AI automation success!"
  python linkedin_mcp_auto_post.py "New project launch" --style enthusiastic
  python linkedin_mcp_auto_post.py "Industry insights" --headless
        """
    )
    
    parser.add_argument(
        'topic',
        nargs='?',
        default=None,
        help='Topic or content to post'
    )
    
    parser.add_argument(
        '--style',
        choices=['professional', 'casual', 'enthusiastic'],
        default='professional',
        help='Post style (default: professional)'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode (no GUI)'
    )
    
    parser.add_argument(
        '--profile',
        type=str,
        default=None,
        help='Custom LinkedIn profile path'
    )
    
    parser.add_argument(
        '--slow-mo',
        type=int,
        default=0,
        help='Slow motion delay in ms for debugging'
    )
    
    args = parser.parse_args()
    
    if args.topic is None:
        print("="*70)
        print("LINKEDIN MCP AUTO-POST")
        print("="*70)
        print()
        print("Usage: python linkedin_mcp_auto_post.py \"Your topic\"")
        print()
        print("Examples:")
        print('   python linkedin_mcp_auto_post.py "AI automation success!"')
        print('   python linkedin_mcp_auto_post.py "New project launch" --style enthusiastic')
        print()
        print("To authenticate first:")
        print("   python linkedin_mcp_auth.py")
        print()
        print("="*70)
        sys.exit(1)
    
    success = auto_post_linkedin(
        args.topic,
        style=args.style,
        headless=args.headless,
        profile_path=args.profile
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
