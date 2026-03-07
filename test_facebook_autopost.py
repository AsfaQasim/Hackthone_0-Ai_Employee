#!/usr/bin/env python3
"""
Facebook Auto-Posting Test Script

Test your Facebook/Instagram integration with practical examples.
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

# Add Skills to path
sys.path.insert(0, str(Path(__file__).parent / "Skills"))

from mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer


def load_env():
    """Load environment variables from .env file"""
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


async def test_1_simple_post():
    """Test 1: Simple text post"""
    print("\n" + "="*60)
    print("TEST 1: Simple Facebook Post")
    print("="*60)
    
    server = FacebookInstagramMCPServer(
        page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', '')
    )
    
    message = f"""[AI Employee Test] Auto-Post Test

Testing automatic Facebook posting!
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#AITest #Automation #GoldTier"""
    
    try:
        result = await server.execute_tool(
            "post_to_facebook",
            {"message": message}
        )
        print(f"\n[OK] SUCCESS!")
        print(result.text)
        return True
    except Exception as e:
        print(f"\n[FAIL] FAILED: {e}")
        return False


async def test_2_post_with_image():
    """Test 2: Post with image"""
    print("\n" + "="*60)
    print("TEST 2: Facebook Post with Image")
    print("="*60)
    
    server = FacebookInstagramMCPServer(
        page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', '')
    )
    
    try:
        result = await server.execute_tool(
            "post_to_facebook",
            {
                "message": "Check out our AI Employee in action!",
                "photo_url": "https://via.placeholder.com/1200x630/4267B2/ffffff?text=AI+Employee+Test"
            }
        )
        print(f"\n[OK] SUCCESS!")
        print(result.text)
        return True
    except Exception as e:
        print(f"\n[FAIL] FAILED: {e}")
        return False


async def test_3_get_posts():
    """Test 3: Get recent posts"""
    print("\n" + "="*60)
    print("TEST 3: Get Recent Facebook Posts")
    print("="*60)
    
    server = FacebookInstagramMCPServer(
        page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', '')
    )
    
    try:
        result = await server.execute_tool(
            "get_facebook_posts",
            {"limit": 3, "include_insights": False}
        )
        print(f"\n[OK] SUCCESS!")
        print(result.text)
        return True
    except Exception as e:
        print(f"\n[FAIL] FAILED: {e}")
        return False


async def test_4_get_insights():
    """Test 4: Get page insights"""
    print("\n" + "="*60)
    print("TEST 4: Get Facebook Insights")
    print("="*60)
    
    server = FacebookInstagramMCPServer(
        page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', '')
    )
    
    try:
        result = await server.execute_tool(
            "get_facebook_insights",
            {
                "metric": "page_impressions",
                "period": "week",
                "days": 7
            }
        )
        print(f"\n[OK] SUCCESS!")
        print(result.text)
        return True
    except Exception as e:
        print(f"\n[FAIL] FAILED: {e}")
        return False


async def test_5_instagram_post():
    """Test 5: Instagram post"""
    print("\n" + "="*60)
    print("TEST 5: Instagram Post")
    print("="*60)
    
    server = FacebookInstagramMCPServer(
        page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', ''),
        instagram_business_account_id=os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', '')
    )
    
    if not os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID'):
        print("\n[WARN] SKIPPED: INSTAGRAM_BUSINESS_ACCOUNT_ID not set in .env")
        return True
    
    try:
        result = await server.execute_tool(
            "post_to_instagram",
            {
                "caption": f"""AI Employee Test Post!

Testing Instagram auto-posting.
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#AITest #Automation #GoldTier""",
                "image_url": "https://via.placeholder.com/1080x1080/E1306C/ffffff?text=AI+Employee+Test"
            }
        )
        print(f"\n[OK] SUCCESS!")
        print(result.text)
        return True
    except Exception as e:
        print(f"\n[FAIL] FAILED: {e}")
        return False


async def test_6_instagram_insights():
    """Test 6: Instagram insights"""
    print("\n" + "="*60)
    print("TEST 6: Instagram Insights")
    print("="*60)
    
    server = FacebookInstagramMCPServer(
        page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', ''),
        instagram_business_account_id=os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', '')
    )
    
    if not os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID'):
        print("\n[WARN] SKIPPED: INSTAGRAM_BUSINESS_ACCOUNT_ID not set in .env")
        return True
    
    try:
        result = await server.execute_tool(
            "get_instagram_insights",
            {
                "metric": "follower_count",
                "period": "week"
            }
        )
        print(f"\n[OK] SUCCESS!")
        print(result.text)
        return True
    except Exception as e:
        print(f"\n[FAIL] FAILED: {e}")
        return False


async def test_7_generate_summary():
    """Test 7: Generate social media summary"""
    print("\n" + "="*60)
    print("TEST 7: Generate Social Media Summary")
    print("="*60)
    
    server = FacebookInstagramMCPServer(
        page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', ''),
        instagram_business_account_id=os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', '')
    )
    
    try:
        result = await server.execute_tool(
            "generate_social_media_summary",
            {
                "platform": "both",
                "period_days": 7
            }
        )
        print(f"\n[OK] SUCCESS!")
        print(result.text)
        return True
    except Exception as e:
        print(f"\n[FAIL] FAILED: {e}")
        return False


async def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  FACEBOOK/INSTAGRAM AUTO-POSTING TESTS")
    print("="*60)
    
    # Load environment
    load_env()
    
    # Check credentials
    if not os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN'):
        print("\n[ERROR] FACEBOOK_PAGE_ACCESS_TOKEN not set in .env file!")
        print("\nPlease create .env file with:")
        print("FACEBOOK_PAGE_ACCESS_TOKEN=your_token_here")
        print("INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id_here")
        return
    
    print("\n[OK] Environment loaded")
    print(f"   Facebook Token: {'Set' if os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN') else 'Missing'}")
    print(f"   Instagram ID: {'Set' if os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID') else 'Missing'}")
    
    # Run tests
    results = []
    
    results.append(("Simple Facebook Post", await test_1_simple_post()))
    results.append(("Facebook Post with Image", await test_2_post_with_image()))
    results.append(("Get Recent Posts", await test_3_get_posts()))
    results.append(("Get Facebook Insights", await test_4_get_insights()))
    
    if os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID'):
        results.append(("Instagram Post", await test_5_instagram_post()))
        results.append(("Instagram Insights", await test_6_instagram_insights()))
    
    results.append(("Generate Summary", await test_7_generate_summary()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[OK] PASS" if result else "[FAIL] FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n[SUCCESS] ALL TESTS PASSED! Your Facebook/Instagram integration is working!")
    else:
        print(f"\n[WARN] {total - passed} tests failed. Check errors above.")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
