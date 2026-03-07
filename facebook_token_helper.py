#!/usr/bin/env python3
"""
Facebook Token Helper

This script helps you:
1. Get your Facebook Page ID
2. Exchange short-lived token for long-lived token
3. Test if your token works
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def get_page_info(user_token):
    """
    Get list of pages you manage and their tokens.
    
    Args:
        user_token: Your user access token from Graph API Explorer
    """
    print_header("GETTING YOUR FACEBOOK PAGES")
    
    url = "https://graph.facebook.com/v18.0/me/accounts"
    params = {
        'access_token': user_token
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and len(data['data']) > 0:
            print("\n✅ Found your Facebook Pages:\n")
            
            for i, page in enumerate(data['data'], 1):
                print(f"{i}. Page Name: {page['name']}")
                print(f"   Page ID: {page['id']}")
                print(f"   Category: {page.get('category', 'N/A')}")
                print(f"   Access Token: {page['access_token'][:20]}...")
                print(f"   Tasks: {', '.join(page.get('tasks', []))}")
                print()
            
            print("\n📝 To use a page:")
            print("1. Copy the Page ID")
            print("2. Copy the Access Token")
            print("3. Update your .env file:")
            print("   FACEBOOK_PAGE_ID=<Page ID>")
            print("   FACEBOOK_PAGE_ACCESS_TOKEN=<Access Token>")
            
            return data['data']
        else:
            print("\n❌ No pages found. Make sure:")
            print("   1. You're an admin of at least one Facebook Page")
            print("   2. Your token has 'pages_show_list' permission")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error getting pages: {e}")
        if hasattr(e.response, 'json'):
            error_data = e.response.json()
            print(f"   Error details: {error_data.get('error', {}).get('message', 'Unknown error')}")
        return []

def exchange_token(short_lived_token, app_id, app_secret):
    """
    Exchange short-lived token for long-lived token (60 days).
    
    Args:
        short_lived_token: Your short-lived user token
        app_id: Your Facebook App ID
        app_secret: Your Facebook App Secret
    """
    print_header("EXCHANGING FOR LONG-LIVED TOKEN")
    
    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_lived_token
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'access_token' in data:
            print("\n✅ Successfully exchanged token!")
            print(f"\n📝 Long-lived token (60 days):")
            print(f"   {data['access_token']}")
            print(f"\n⏰ Expires in: {data.get('expires_in', 'Unknown')} seconds")
            print(f"   (approximately {data.get('expires_in', 0) // 86400} days)")
            
            return data['access_token']
        else:
            print("\n❌ Failed to exchange token")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error exchanging token: {e}")
        if hasattr(e.response, 'json'):
            error_data = e.response.json()
            print(f"   Error details: {error_data.get('error', {}).get('message', 'Unknown error')}")
        return None

def test_page_token(page_id, page_token):
    """
    Test if page token works by trying to get page info.
    
    Args:
        page_id: Facebook Page ID
        page_token: Page access token
    """
    print_header("TESTING PAGE TOKEN")
    
    url = f"https://graph.facebook.com/v18.0/{page_id}"
    params = {
        'fields': 'id,name,category,access_token',
        'access_token': page_token
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        print("\n✅ Token is valid!")
        print(f"\n📄 Page Info:")
        print(f"   Name: {data.get('name', 'N/A')}")
        print(f"   ID: {data.get('id', 'N/A')}")
        print(f"   Category: {data.get('category', 'N/A')}")
        
        # Test posting permission
        print("\n🔐 Testing posting permission...")
        test_url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
        test_params = {
            'message': 'Test post - please ignore',
            'access_token': page_token,
            'published': 'false'  # Don't actually publish
        }
        
        test_response = requests.post(test_url, params=test_params)
        if test_response.status_code == 200:
            print("   ✅ Posting permission: OK")
        else:
            print("   ❌ Posting permission: FAILED")
            print(f"   Error: {test_response.json().get('error', {}).get('message', 'Unknown')}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Token is invalid or expired: {e}")
        if hasattr(e.response, 'json'):
            error_data = e.response.json()
            print(f"   Error details: {error_data.get('error', {}).get('message', 'Unknown error')}")
        return False

def main():
    """Main function with interactive menu."""
    print("\n" + "=" * 70)
    print("  FACEBOOK TOKEN HELPER")
    print("=" * 70)
    
    print("\nWhat would you like to do?\n")
    print("1. Get my Facebook Pages and their tokens")
    print("2. Exchange short-lived token for long-lived token")
    print("3. Test my current token from .env")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        print("\n📝 Instructions:")
        print("1. Go to: https://developers.facebook.com/tools/explorer/")
        print("2. Select your app")
        print("3. Click 'Generate Access Token'")
        print("4. Select permissions: pages_show_list, pages_manage_posts")
        print("5. Copy the token and paste below")
        
        user_token = input("\n🔑 Paste your USER access token: ").strip()
        
        if user_token:
            pages = get_page_info(user_token)
            
            if pages:
                print("\n💡 Tip: Copy the Page ID and Access Token to your .env file")
        else:
            print("\n❌ No token provided")
    
    elif choice == "2":
        print("\n📝 You need:")
        print("1. Your short-lived token")
        print("2. Your App ID (from Facebook App Dashboard)")
        print("3. Your App Secret (from Facebook App Dashboard)")
        
        token = input("\n🔑 Short-lived token: ").strip()
        app_id = input("📱 App ID: ").strip()
        app_secret = input("🔐 App Secret: ").strip()
        
        if token and app_id and app_secret:
            long_token = exchange_token(token, app_id, app_secret)
            
            if long_token:
                print("\n💡 Now get the page token:")
                print("   Run option 1 with this long-lived token")
        else:
            print("\n❌ Missing required information")
    
    elif choice == "3":
        page_id = os.getenv('FACEBOOK_PAGE_ID')
        page_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
        
        if page_id and page_token:
            test_page_token(page_id, page_token)
        else:
            print("\n❌ FACEBOOK_PAGE_ID or FACEBOOK_PAGE_ACCESS_TOKEN not found in .env")
            print("   Please set them first")
    
    elif choice == "4":
        print("\n👋 Goodbye!")
        return
    
    else:
        print("\n❌ Invalid choice")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
