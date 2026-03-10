"""
LinkedIn Auto Poster with Playwright
Automatically posts content to LinkedIn using browser automation
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LinkedInAutoPoster:
    """LinkedIn auto-poster using Playwright for browser automation"""
    
    def __init__(self, session_path: str = ".linkedin_session", headless: bool = True):
        """
        Initialize LinkedIn auto-poster
        
        Args:
            session_path: Path to store browser session data
            headless: Run browser in headless mode
        """
        self.session_path = Path(session_path)
        self.session_path.mkdir(exist_ok=True)
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
    def __enter__(self):
        """Context manager entry"""
        self.start_browser()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
        
    def start_browser(self):
        """Start browser with persistent session"""
        try:
            self.playwright = sync_playwright().start()
            
            # Launch browser with persistent context
            self.context = self.playwright.chromium.launch_persistent_context(
                user_data_dir=str(self.session_path),
                headless=self.headless,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled'
                ],
                viewport={'width': 1280, 'height': 720}
            )
            
            # Create new page
            self.page = self.context.new_page()
            logger.info("Browser started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise
            
    def is_logged_in(self) -> bool:
        """Check if user is logged into LinkedIn"""
        try:
            self.page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=10000)
            self.page.wait_for_timeout(2000)
            
            # Check if we're on the feed page (logged in) or login page
            current_url = self.page.url
            return "feed" in current_url or "mynetwork" in current_url
            
        except Exception as e:
            logger.error(f"Error checking login status: {e}")
            return False
            
    def login(self, email: Optional[str] = None, password: Optional[str] = None, timeout: int = 300000):
        """
        Login to LinkedIn (manual or automated)
        
        Args:
            email: LinkedIn email (optional for manual login)
            password: LinkedIn password (optional for manual login)
            timeout: Timeout for manual login in milliseconds (default: 5 minutes)
        """
        try:
            # Check if already logged in
            if self.is_logged_in():
                logger.info("Already logged in to LinkedIn")
                return True
                
            logger.info("Navigating to LinkedIn login page...")
            self.page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
            self.page.wait_for_timeout(2000)
            
            if email and password:
                # Automated login
                logger.info("Attempting automated login...")
                self.page.fill('input[name="session_key"]', email)
                self.page.fill('input[name="session_password"]', password)
                self.page.click('button[type="submit"]')
                self.page.wait_for_timeout(5000)
                
                # Check if login was successful
                if self.is_logged_in():
                    logger.info("Automated login successful")
                    return True
                else:
                    logger.warning("Automated login may have failed, check for 2FA or captcha")
                    
            else:
                # Manual login
                logger.info(f"Please log in manually in the browser window (timeout: {timeout/1000}s)...")
                print("\n" + "="*60)
                print("MANUAL LOGIN REQUIRED")
                print("="*60)
                print("1. A browser window should open")
                print("2. Log in to LinkedIn manually")
                print("3. Complete any 2FA or captcha challenges")
                print(f"4. You have {timeout/1000} seconds to complete login")
                print("="*60 + "\n")
                
                # Wait for user to login manually
                try:
                    self.page.wait_for_url("**/feed/**", timeout=timeout)
                    logger.info("Manual login successful")
                    return True
                except Exception as e:
                    logger.error(f"Manual login timeout or failed: {e}")
                    return False
                    
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
            
    def post_text(self, content: str) -> Dict[str, Any]:
        """
        Post text content to LinkedIn
        
        Args:
            content: Text content to post
            
        Returns:
            Dict with status and details
        """
        try:
            if not self.is_logged_in():
                return {
                    "success": False,
                    "error": "Not logged in to LinkedIn"
                }
                
            logger.info("Navigating to LinkedIn feed...")
            self.page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
            self.page.wait_for_timeout(3000)
            
            # Click on "Start a post" button
            logger.info("Opening post composer...")
            start_post_selectors = [
                'button[aria-label*="Start a post"]',
                'button.share-box-feed-entry__trigger',
                'button[data-test-share-box-trigger]',
                '.share-box-feed-entry__trigger'
            ]
            
            clicked = False
            for selector in start_post_selectors:
                try:
                    self.page.click(selector, timeout=5000)
                    clicked = True
                    break
                except:
                    continue
                    
            if not clicked:
                return {
                    "success": False,
                    "error": "Could not find 'Start a post' button"
                }
                
            self.page.wait_for_timeout(2000)
            
            # Fill in the post content
            logger.info("Filling in post content...")
            editor_selectors = [
                'div[role="textbox"][contenteditable="true"]',
                '.ql-editor[contenteditable="true"]',
                'div.ql-editor'
            ]
            
            filled = False
            for selector in editor_selectors:
                try:
                    self.page.fill(selector, content)
                    filled = True
                    break
                except:
                    continue
                    
            if not filled:
                return {
                    "success": False,
                    "error": "Could not find post editor"
                }
                
            self.page.wait_for_timeout(2000)
            
            # Click the Post button
            logger.info("Clicking Post button...")
            post_button_selectors = [
                'button[aria-label*="Post"]',
                'button.share-actions__primary-action',
                'button[data-test-share-actions-primary-action]'
            ]
            
            posted = False
            for selector in post_button_selectors:
                try:
                    self.page.click(selector, timeout=5000)
                    posted = True
                    break
                except:
                    continue
                    
            if not posted:
                return {
                    "success": False,
                    "error": "Could not find Post button"
                }
                
            # Wait for post to be published
            self.page.wait_for_timeout(5000)
            
            logger.info("Post published successfully")
            return {
                "success": True,
                "message": "Post published successfully",
                "timestamp": datetime.now().isoformat(),
                "content": content
            }
            
        except Exception as e:
            logger.error(f"Failed to post: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def post_with_image(self, content: str, image_path: str) -> Dict[str, Any]:
        """
        Post content with an image to LinkedIn
        
        Args:
            content: Text content to post
            image_path: Path to image file
            
        Returns:
            Dict with status and details
        """
        try:
            if not self.is_logged_in():
                return {
                    "success": False,
                    "error": "Not logged in to LinkedIn"
                }
                
            if not Path(image_path).exists():
                return {
                    "success": False,
                    "error": f"Image file not found: {image_path}"
                }
                
            logger.info("Navigating to LinkedIn feed...")
            self.page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
            self.page.wait_for_timeout(3000)
            
            # Click on "Start a post" button
            logger.info("Opening post composer...")
            self.page.click('button[aria-label*="Start a post"]', timeout=10000)
            self.page.wait_for_timeout(2000)
            
            # Fill in the post content
            logger.info("Filling in post content...")
            self.page.fill('div[role="textbox"][contenteditable="true"]', content)
            self.page.wait_for_timeout(1000)
            
            # Click on media upload button
            logger.info("Uploading image...")
            media_button_selectors = [
                'button[aria-label*="Add a photo"]',
                'button[aria-label*="Add media"]',
                'input[type="file"][accept*="image"]'
            ]
            
            for selector in media_button_selectors:
                try:
                    if 'input' in selector:
                        self.page.set_input_files(selector, image_path)
                    else:
                        self.page.click(selector)
                        self.page.wait_for_timeout(1000)
                        self.page.set_input_files('input[type="file"]', image_path)
                    break
                except:
                    continue
                    
            self.page.wait_for_timeout(3000)
            
            # Click the Post button
            logger.info("Clicking Post button...")
            self.page.click('button[aria-label*="Post"]', timeout=10000)
            
            # Wait for post to be published
            self.page.wait_for_timeout(5000)
            
            logger.info("Post with image published successfully")
            return {
                "success": True,
                "message": "Post with image published successfully",
                "timestamp": datetime.now().isoformat(),
                "content": content,
                "image": image_path
            }
            
        except Exception as e:
            logger.error(f"Failed to post with image: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def close(self):
        """Close browser and cleanup"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if hasattr(self, 'playwright'):
                self.playwright.stop()
            logger.info("Browser closed")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")


def main():
    """Main function for CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="LinkedIn Auto Poster")
    parser.add_argument("--login", action="store_true", help="Login to LinkedIn")
    parser.add_argument("--email", help="LinkedIn email")
    parser.add_argument("--password", help="LinkedIn password")
    parser.add_argument("--post", help="Post text content")
    parser.add_argument("--image", help="Path to image file")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--session-path", default=".linkedin_session", help="Session storage path")
    
    args = parser.parse_args()
    
    # Create poster instance
    with LinkedInAutoPoster(session_path=args.session_path, headless=args.headless) as poster:
        
        # Login if requested
        if args.login:
            poster.login(email=args.email, password=args.password)
            
        # Post content if provided
        elif args.post:
            if args.image:
                result = poster.post_with_image(args.post, args.image)
            else:
                result = poster.post_text(args.post)
                
            print(json.dumps(result, indent=2))
            
        else:
            print("No action specified. Use --login or --post")


if __name__ == "__main__":
    main()
