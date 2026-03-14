#!/usr/bin/env python3
"""
Test Facebook Silver Tier Integration

Comprehensive test script for Facebook posting functionality.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def check_credentials():
    """Check Facebook credentials in .env."""
    print_header("STEP 1: Checking Credentials")
    
    page_id = os.getenv('FACEBOOK_PAGE_ID')
    token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
    app_id = os.getenv('FACEBOOK_APP_ID')
    app_secret = os.getenv('FACEBOOK_APP_SECRET')
    
    print("📋 Credentials Check:\n")
    
    # Check Page ID
    if page_id:
        print(f"✅ FACEBOOK_PAGE_ID: {page_id[:20]}...")
    else:
        print("❌ FACEBOOK_PAGE_ID: Not set")
    
    # Check Token
    if token:
        print(f"✅ FACEBOOK_PAGE_ACCESS_TOKEN: {token[:20]}...")
    else:
        print("❌ FACEBOOK_PAGE_ACCESS_TOKEN: Not set")
    
    # Check App ID
    if app_id:
        print(f"✅ FACEBOOK_APP_ID: {app_id[:20]}...")
    else:
        print("⚠️  FACEBOOK_APP_ID: Not set (optional)")
    
    # Check App Secret
    if app_secret:
        print(f"✅ FACEBOOK_APP_SECRET: {app_secret[:20]}...")
    else:
        print("⚠️  FACEBOOK_APP_SECRET: Not set (optional)")
    
    print()
    
    if page_id and token:
        print("✅ All required credentials found!")
        return True
    else:
        print("❌ Missing required credentials.")
        print("\n💡 To fix:")
        print("   1. Open .env file")
        print("   2. Add FACEBOOK_PAGE_ID and FACEBOOK_PAGE_ACCESS_TOKEN")
        print("   3. Run this test again")
        print("\n   Or use browser automation:")
        print("   python facebook_post_now.py \"Your message\"")
        return False


def test_api_connection():
    """Test Facebook API connection."""
    print_header("STEP 2: Testing API Connection")
    
    page_id = os.getenv('FACEBOOK_PAGE_ID')
    token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
    
    if not page_id or not token:
        print("⚠️  Skipping API test (credentials missing)")
        return False
    
    try:
        import requests
        
        # Test token validity
        url = f"https://graph.facebook.com/v18.0/{page_id}"
        params = {'access_token': token}
        
        print("📡 Testing token validity...")
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'id' in data:
            print(f"✅ Token is valid!")
            print(f"   Page ID: {data['id']}")
            if 'name' in data:
                print(f"   Page Name: {data['name']}")
            return True
        else:
            error = data.get('error', {})
            print(f"❌ Token validation failed:")
            print(f"   Error: {error.get('message', 'Unknown error')}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_posting():
    """Test Facebook posting."""
    print_header("STEP 3: Testing Facebook Posting")
    
    page_id = os.getenv('FACEBOOK_PAGE_ID')
    token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
    
    if not page_id or not token:
        print("⚠️  Skipping posting test (credentials missing)")
        print("\n💡 You can still test with browser automation:")
        print("   python facebook_post_now.py \"Test message\"")
        return False
    
    try:
        import requests
        
        # Create test message
        test_message = f"🤖 Silver Tier Test - {Path.cwd().name}\n\nThis is an automated test post from Facebook Silver Tier integration.\n\n#AI #Automation #Test"
        
        print("📝 Test Message:")
        print(f"   {test_message[:100]}...\n")
        
        # Post to Facebook
        url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
        params = {
            'message': test_message,
            'access_token': token
        }
        
        print("📤 Posting to Facebook...")
        response = requests.post(url, params=params, timeout=30)
        data = response.json()
        
        if 'id' in data:
            post_id = data['id']
            print(f"✅ SUCCESS!")
            print(f"   Post ID: {post_id}")
            print(f"   URL: https://facebook.com/{post_id}")
            print("\n💡 Check your Facebook page to verify the post!")
            return True
        else:
            error = data.get('error', {})
            print(f"❌ Posting failed:")
            print(f"   Error: {error.get('message', 'Unknown error')}")
            
            # Provide troubleshooting
            error_msg = error.get('message', '').lower()
            if 'expired' in error_msg or 'invalid' in error_msg:
                print("\n💡 Token expired or invalid:")
                print("   1. Go to: https://developers.facebook.com/tools/explorer/")
                print("   2. Generate new token with pages_manage_posts")
                print("   3. Update .env with new token")
            elif 'permission' in error_msg:
                print("\n💡 Permission issue:")
                print("   1. Check you're admin of the page")
                print("   2. Token has pages_manage_posts permission")
                print("   3. App is in Live mode")
            
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def check_tracking():
    """Check tracking directory."""
    print_header("STEP 4: Checking Tracking System")
    
    tracking_dir = Path("Social_Media_Tracking")
    
    if tracking_dir.exists():
        print(f"✅ Tracking directory exists: {tracking_dir.absolute()}")
        
        # Count tracking files
        facebook_files = list(tracking_dir.glob("facebook_*.md"))
        if facebook_files:
            print(f"✅ Found {len(facebook_files)} Facebook tracking file(s)")
            print("\n   Recent files:")
            for f in sorted(facebook_files)[-3:]:
                print(f"   - {f.name}")
        else:
            print("ℹ️  No Facebook tracking files yet (will be created on first post)")
    else:
        print("ℹ️  Tracking directory will be created on first post")
    
    return True


def test_mcp_skill():
    """Test MCP skill integration."""
    print_header("STEP 5: Testing MCP Skill")
    
    try:
        from Skills.facebook_mcp_skill import FacebookMCPSkill
        
        print("✅ MCP Skill module loaded successfully")
        
        # Initialize skill
        skill = FacebookMCPSkill()
        print(f"✅ MCP Skill initialized")
        print(f"   Configured: {skill.is_configured}")
        
        # Test setup instructions
        instructions = skill.get_setup_instructions()
        if instructions:
            print("✅ Setup instructions available")
        
        return True
        
    except ImportError as e:
        print(f"⚠️  MCP Skill not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def show_summary(results):
    """Show test summary."""
    print_header("TEST SUMMARY")
    
    tests = [
        ("Credentials Check", results.get('credentials', False)),
        ("API Connection", results.get('api', False)),
        ("Facebook Posting", results.get('posting', False)),
        ("Tracking System", results.get('tracking', False)),
        ("MCP Skill", results.get('mcp', False))
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for name, result in tests:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\n{'=' * 70}")
    print(f"  Results: {passed}/{total} tests passed")
    print(f"{'=' * 70}")
    
    if passed == total:
        print("\n🎉 All tests passed! Silver Tier Facebook is ready!")
    elif passed >= 3:
        print("\n✅ Most tests passed. Facebook integration is mostly ready.")
    else:
        print("\n⚠️  Some tests failed. Review the errors above.")


def main():
    """Main test function."""
    print_header("FACEBOOK SILVER TIER - TEST SUITE")
    
    results = {}
    
    # Run tests
    results['credentials'] = check_credentials()
    results['api'] = test_api_connection()
    
    if results['credentials'] and results['api']:
        results['posting'] = test_posting()
    else:
        print("\n⚠️  Skipping posting test (credentials/API missing)")
        results['posting'] = False
    
    results['tracking'] = check_tracking()
    results['mcp'] = test_mcp_skill()
    
    # Show summary
    show_summary(results)
    
    # Final recommendations
    print_header("NEXT STEPS")
    
    if results['credentials'] and results['posting']:
        print("✅ Facebook Silver Tier is COMPLETE and WORKING!")
        print("\nYou can now:")
        print("   1. Post messages: python facebook_silver_poster.py \"Your message\"")
        print("   2. Use MCP skill: from Skills.facebook_mcp_skill import FacebookMCPSkill")
        print("   3. Integrate with AI agent")
    else:
        print("⚠️  Facebook Silver Tier needs attention:")
        if not results['credentials']:
            print("\n   1. Configure credentials in .env:")
            print("      - FACEBOOK_PAGE_ID")
            print("      - FACEBOOK_PAGE_ACCESS_TOKEN")
        if not results['posting']:
            print("\n   2. Fix posting issues (see errors above)")
            print("   3. Or use browser automation:")
            print("      python facebook_post_now.py \"Test message\"")
    
    print("\n📁 Documentation: SILVER_TIER_FACEBOOK_COMPLETE.md")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
