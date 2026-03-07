# Facebook & Instagram Auto-Posting Guide

## Overview

Your AI Employee can automatically:
- ✅ Post to Facebook Pages
- ✅ Post to Instagram Business accounts
- ✅ Read comments and engagement
- ✅ Generate analytics summaries
- ✅ Schedule posts for later

---

## Part 1: Facebook Graph API Setup

### Step 1: Create Facebook Developer Account

1. Go to https://developers.facebook.com
2. Click **Get Started** or **Log In**
3. Accept terms and conditions
4. Verify your account with phone number

### Step 2: Create Facebook App

1. Click **My Apps** → **Create App**
2. Select **Business** app type
3. Fill in details:
   - **App Name**: `AI Employee Auto Poster`
   - **App Contact Email**: your-email@example.com
   - Click **Create App**

4. Complete security check

### Step 3: Add Facebook Login Product

1. In App Dashboard, scroll to **Add Products**
2. Find **Facebook Login** → Click **Set Up**
3. Configure **Valid OAuth Redirect URIs**:
   ```
   https://localhost:8000/callback
   ```
4. Click **Save**

### Step 4: Get Page Access Token

#### Method A: Graph API Explorer (Easy - Manual Renewal)

1. Go to https://developers.facebook.com/tools/explorer/
2. Select your app from dropdown (top right)
3. Click **Get Token** → **Get Page Access Token**
4. Select your Facebook Page
5. Check permissions:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_read_user_content`
   - `publish_to_groups` (if posting to groups)
6. Click **Generate Token**
7. **Copy the token** - this is your `FACEBOOK_PAGE_ACCESS_TOKEN`

#### Method B: Long-Lived Token (Recommended)

Page tokens from Graph Explorer expire in 1 hour. For production:

1. Get user token with `pages_read_engagement` and `pages_manage_posts`
2. Exchange for long-lived token (60 days):

```python
import requests

# Step 1: Get short-lived user token from Graph Explorer
short_lived_token = "YOUR_SHORT_LIVED_TOKEN"

# Step 2: Exchange for long-lived user token
app_id = "YOUR_APP_ID"
app_secret = "YOUR_APP_SECRET"

url = "https://graph.facebook.com/v18.0/oauth/access_token"
params = {
    "grant_type": "fb_exchange_token",
    "client_id": app_id,
    "client_secret": app_secret,
    "fb_exchange_token": short_lived_token
}

response = requests.get(url, params=params)
long_lived_user_token = response.json()["access_token"]

# Step 3: Get page token (doesn't expire)
url = f"https://graph.facebook.com/v18.0/me/accounts"
params = {"access_token": long_lived_user_token}

response = requests.get(url, params=params)
pages = response.json()["data"]

for page in pages:
    if page["name"] == "Your Page Name":
        page_access_token = page["access_token"]
        print(f"Page Token: {page_access_token}")
        print(f"Page ID: {page['id']}")
```

### Step 5: Get Instagram Business Account ID

1. In Graph API Explorer, run:
   ```
   GET /me?fields=instagram_business_account
   ```

2. Copy the `instagram_business_account.id`

3. Or use Python:

```python
import requests

url = "https://graph.facebook.com/v18.0/me"
params = {
    "fields": "instagram_business_account",
    "access_token": "YOUR_PAGE_ACCESS_TOKEN"
}

response = requests.get(url, params=params)
ig_account_id = response.json()["instagram_business_account"]["id"]
print(f"Instagram Business Account ID: {ig_account_id}")
```

---

## Part 2: Configure Environment

Create `.env` file in project root:

```env
# Facebook Configuration
FACEBOOK_PAGE_ACCESS_TOKEN=EAA...your_long_token_here
FACEBOOK_PAGE_ID=1234567890

# Instagram Configuration
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000000

# Odoo (if using)
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_db
ODOO_USERNAME=admin
ODOO_PASSWORD=your_password
```

---

## Part 3: Practical Examples

### Example 1: Simple Facebook Post

```python
import asyncio
import os
from dotenv import load_dotenv
from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer

# Load environment
load_dotenv()

# Initialize server
server = FacebookInstagramMCPServer(
    page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN'),
    instagram_business_account_id=os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
)

async def post_to_facebook():
    """Post a simple text update"""
    
    result = await server.execute_tool(
        "post_to_facebook",
        {
            "message": """🚀 Exciting News!

We just launched our new AI Employee system! 
This automation will transform how we do business.

#AI #Automation #Innovation #Business"""
        }
    )
    
    print(result.text)

# Run
asyncio.run(post_to_facebook())
```

### Example 2: Facebook Post with Image

```python
async def post_with_image():
    """Post with image from URL"""
    
    result = await server.execute_tool(
        "post_to_facebook",
        {
            "message": "Check out our latest product! 🎉",
            "photo_url": "https://example.com/product-image.jpg"
        }
    )
    
    print(result.text)

asyncio.run(post_with_image())
```

### Example 3: Facebook Post with Link

```python
async def post_with_link():
    """Share a link with preview"""
    
    result = await server.execute_tool(
        "post_to_facebook",
        {
            "message": "Read our latest blog post about AI automation!",
            "link": "https://yourblog.com/ai-automation-guide"
        }
    )
    
    print(result.text)

asyncio.run(post_with_link())
```

### Example 4: Scheduled Facebook Post

```python
from datetime import datetime, timedelta

async def schedule_post():
    """Schedule post for later"""
    
    # Schedule for tomorrow at 9 AM
    tomorrow_9am = datetime.now() + timedelta(days=1)
    tomorrow_9am = tomorrow_9am.replace(hour=9, minute=0, second=0)
    
    result = await server.execute_tool(
        "post_to_facebook",
        {
            "message": "Good morning! Here's your daily motivation... 💪",
            "scheduled_time": tomorrow_9am.isoformat()
        }
    )
    
    print(result.text)

asyncio.run(schedule_post())
```

### Example 5: Instagram Post

```python
async def post_to_instagram():
    """Post to Instagram (requires image URL)"""
    
    result = await server.execute_tool(
        "post_to_instagram",
        {
            "caption": """New product launch! 🚀

Stay tuned for something amazing.

#NewProduct #Launch #Innovation #Tech""",
            "image_url": "https://example.com/instagram-post.jpg"
        }
    )
    
    print(result.text)

asyncio.run(post_to_instagram())
```

### Example 6: Instagram Video Post

```python
async def post_instagram_video():
    """Post video to Instagram"""
    
    result = await server.execute_tool(
        "post_to_instagram",
        {
            "caption": "Behind the scenes of our latest project! 🎬",
            "image_url": "https://example.com/video-thumbnail.jpg",
            "is_video": True,
            "video_url": "https://example.com/video.mp4"
        }
    )
    
    print(result.text)

asyncio.run(post_instagram_video())
```

### Example 7: Get Recent Posts

```python
async def get_recent_posts():
    """Get last 5 posts from Facebook"""
    
    result = await server.execute_tool(
        "get_facebook_posts",
        {
            "limit": 5,
            "include_insights": True
        }
    )
    
    print(result.text)

asyncio.run(get_recent_posts())
```

### Example 8: Get Facebook Insights

```python
async def get_insights():
    """Get page analytics"""
    
    # Get impressions
    impressions = await server.execute_tool(
        "get_facebook_insights",
        {
            "metric": "page_impressions",
            "period": "week",
            "days": 7
        }
    )
    print("Impressions:", impressions.text)
    
    # Get engagements
    engagement = await server.execute_tool(
        "get_facebook_insights",
        {
            "metric": "page_post_engagements",
            "period": "week",
            "days": 7
        }
    )
    print("\nEngagements:", engagement.text)

asyncio.run(get_insights())
```

### Example 9: Get Instagram Insights

```python
async def get_instagram_insights():
    """Get Instagram analytics"""
    
    # Get follower count
    followers = await server.execute_tool(
        "get_instagram_insights",
        {
            "metric": "follower_count",
            "period": "week"
        }
    )
    print(followers.text)
    
    # Get reach
    reach = await server.execute_tool(
        "get_instagram_insights",
        {
            "metric": "reach",
            "period": "week"
        }
    )
    print("\nReach:", reach.text)

asyncio.run(get_instagram_insights())
```

### Example 10: Generate Social Media Summary

```python
async def generate_summary():
    """Generate combined Facebook + Instagram report"""
    
    result = await server.execute_tool(
        "generate_social_media_summary",
        {
            "platform": "both",
            "period_days": 7
        }
    )
    
    print(result.text)

asyncio.run(generate_summary())
```

---

## Part 4: Auto-Posting Automation

### Auto-Post from AI Employee (Real Workflow)

Here's how to integrate with your AI Employee for automatic posting:

```python
# ai_social_poster.py
import asyncio
import os
from dotenv import load_dotenv
from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer
from pathlib import Path
from datetime import datetime

class AutoSocialPoster:
    """Automatically post to social media based on AI decisions"""
    
    def __init__(self):
        load_dotenv()
        self.server = FacebookInstagramMCPServer(
            page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN'),
            instagram_business_account_id=os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        )
        self.vault_path = Path(".")
        
    async def post_business_update(self, revenue: float, tasks_completed: int):
        """Post weekly business update"""
        
        message = f"""📊 Weekly Business Update

✅ Tasks Completed: {tasks_completed}
💰 Revenue: ${revenue:,.2f}

Our AI Employee is crushing it! 

#BusinessGrowth #AI #Automation #Success"""
        
        # Post to Facebook
        fb_result = await self.server.execute_tool(
            "post_to_facebook",
            {"message": message}
        )
        print(f"Facebook: {fb_result.text}")
        
        # Post to Instagram
        ig_result = await self.server.execute_tool(
            "post_to_instagram",
            {
                "caption": f"Weekly wins! 🎉 {tasks_completed} tasks, ${revenue:,.2f} revenue!",
                "image_url": "https://via.placeholder.com/1080x1080/4267B2/ffffff?text=Weekly+Update"
            }
        )
        print(f"Instagram: {ig_result.text}")
    
    async def post_invoice_created(self, customer_name: str, amount: float):
        """Post when invoice is created (optional - for marketing)"""
        
        message = f"""🎉 Welcome aboard, {customer_name}!

Excited to partner with you on this journey.

#NewClient #Business #Partnership"""
        
        await self.server.execute_tool(
            "post_to_facebook",
            {"message": message}
        )

# Usage
async def main():
    poster = AutoSocialPoster()
    
    # Post business update
    await poster.post_business_update(revenue=5000, tasks_completed=25)

asyncio.run(main())
```

### Scheduled Auto-Posting (Daily Motivation)

```python
# scheduled_posts.py
import asyncio
import schedule
import time
from datetime import datetime

class ScheduledPosts:
    """Schedule regular social media posts"""
    
    def __init__(self):
        from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        self.server = FacebookInstagramMCPServer(
            page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
        )
    
    async def post_morning_motivation(self):
        """Post daily motivation at 8 AM"""
        
        quotes = [
            "The best way to predict the future is to create it! 💪 #MondayMotivation",
            "Success is not final, failure is not fatal: It is the courage to continue that counts. ✨ #Inspiration",
            "Believe you can and you're halfway there. 🚀 #Motivation",
            "Your limitation—it's only your imagination. 💡 #GrowthMindset",
            "Push yourself, because no one else is going to do it for you. 🔥 #Fitness"
        ]
        
        import random
        message = random.choice(quotes)
        
        result = await self.server.execute_tool(
            "post_to_facebook",
            {"message": message}
        )
        
        print(f"Posted: {result.text}")
    
    def schedule_posts(self):
        """Schedule all posts"""
        
        # Daily motivation at 8 AM
        schedule.every().day.at("08:00").do(
            lambda: asyncio.run(self.post_morning_motivation())
        )
        
        print("Scheduled posts configured!")
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)

# Run scheduler
if __name__ == "__main__":
    scheduler = ScheduledPosts()
    scheduler.schedule_posts()
```

---

## Part 5: Auto-Comment Response

```python
# comment_responder.py
import asyncio
import requests
import os
from dotenv import load_dotenv

class AutoCommentResponder:
    """Automatically respond to comments"""
    
    def __init__(self):
        load_dotenv()
        self.access_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
        self.page_id = os.getenv('FACEBOOK_PAGE_ID')
        self.graph_url = "https://graph.facebook.com/v18.0"
    
    async def get_post_comments(self, post_id: str):
        """Get comments on a post"""
        
        url = f"{self.graph_url}/{post_id}/comments"
        params = {
            "access_token": self.access_token,
            "fields": "id,from,message,created_time,comment_count"
        }
        
        response = requests.get(url, params=params)
        return response.json().get("data", [])
    
    async def reply_to_comment(self, comment_id: str, message: str):
        """Reply to a comment"""
        
        url = f"{self.graph_url}/{comment_id}/comments"
        params = {
            "message": message,
            "access_token": self.access_token
        }
        
        response = requests.post(url, params=params)
        return response.json()
    
    async def check_and_respond(self, post_id: str):
        """Check for new comments and respond"""
        
        comments = await self.get_post_comments(post_id)
        
        for comment in comments:
            # Check if comment needs response
            message = comment.get("message", "").lower()
            
            # Auto-respond to questions
            if "?" in message or "how" in message or "what" in message:
                response_message = "Thanks for your question! We'll get back to you shortly. 😊"
                
                result = await self.reply_to_comment(
                    comment["id"],
                    response_message
                )
                
                print(f"Replied to comment {comment['id']}: {result}")
            
            # Auto-respond to positive comments
            elif any(word in message for word in ["great", "awesome", "love", "amazing"]):
                response_message = "Thank you so much! We appreciate your support! ❤️"
                
                result = await self.reply_to_comment(
                    comment["id"],
                    response_message
                )
                
                print(f"Replied to comment {comment['id']}: {result}")

# Usage
async def main():
    responder = AutoCommentResponder()
    
    # Replace with actual post ID
    post_id = "YOUR_POST_ID"
    
    await responder.check_and_respond(post_id)

asyncio.run(main())
```

---

## Part 6: Complete Auto-Posting System

Here's a complete system that monitors your business and auto-posts:

```python
# complete_auto_poster.py
"""
Complete Auto-Posting System for AI Employee

Monitors business activities and automatically posts updates to social media.
"""

import asyncio
import os
from dotenv import load_dotenv
from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer
from Skills.mcp_servers.odoo_mcp_server import OdooMCPServer
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

class CompleteAutoPoster:
    """Complete auto-posting system"""
    
    def __init__(self):
        load_dotenv()
        
        # Initialize servers
        self.social_server = FacebookInstagramMCPServer(
            page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN'),
            instagram_business_account_id=os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        )
        
        self.odoo_server = OdooMCPServer(
            odoo_url=os.getenv('ODOO_URL', 'http://localhost:8069'),
            db_name=os.getenv('ODOO_DB', 'odoo_db'),
            username=os.getenv('ODOO_USERNAME', 'admin'),
            password=os.getenv('ODOO_PASSWORD', '')
        )
        
        self.posted_invoices = set()
    
    async def post_new_invoice(self, invoice_id: int, customer: str, amount: float):
        """Post when new invoice is created"""
        
        if invoice_id in self.posted_invoices:
            return  # Already posted
        
        message = f"""🎉 New Invoice Created!

Customer: {customer}
Amount: ${amount:,.2f}

Thank you for your business! 

#NewBusiness #Invoice #Growth"""
        
        result = await self.social_server.execute_tool(
            "post_to_facebook",
            {"message": message}
        )
        
        self.posted_invoices.add(invoice_id)
        print(f"Posted invoice {invoice_id}: {result.text}")
    
    async def post_weekly_summary(self):
        """Post weekly business summary"""
        
        # Get Odoo summary
        summary = await self.odoo_server.execute_tool(
            "odoo_get_account_summary",
            {"period": "week"}
        )
        
        # Parse summary (simplified)
        revenue = 5000  # Replace with actual parsing
        expenses = 2000
        
        message = f"""📊 Weekly Business Summary

💰 Revenue: ${revenue:,.2f}
💸 Expenses: ${expenses:,.2f}
📈 Profit: ${revenue - expenses:,.2f}

Powered by our AI Employee! 🤖

#BusinessSummary #WeeklyReport #AI"""
        
        # Post to Facebook
        fb_result = await self.social_server.execute_tool(
            "post_to_facebook",
            {"message": message}
        )
        print(f"Facebook summary: {fb_result.text}")
        
        # Post to Instagram
        ig_result = await self.social_server.execute_tool(
            "post_to_instagram",
            {
                "caption": f"Weekly wins! 💪 ${revenue - expenses:,.2f} profit!",
                "image_url": "https://via.placeholder.com/1080x1080/4CAF50/ffffff?text=Weekly+Profit"
            }
        )
        print(f"Instagram summary: {ig_result.text}")
    
    async def monitor_and_post(self):
        """Continuously monitor and auto-post"""
        
        print("Starting auto-posting monitor...")
        
        while True:
            try:
                # Check for new invoices every hour
                invoices = await self.odoo_server.execute_tool(
                    "odoo_get_invoices",
                    {"state": "posted", "limit": 10}
                )
                
                # Process new invoices
                # (Parse and call post_new_invoice for each)
                
                # Post weekly summary every Monday at 9 AM
                if datetime.now().weekday() == 0 and datetime.now().hour == 9:
                    await self.post_weekly_summary()
                
            except Exception as e:
                print(f"Error in monitor: {e}")
            
            # Check every hour
            await asyncio.sleep(3600)

# Run
async def main():
    poster = CompleteAutoPoster()
    await poster.monitor_and_post()

asyncio.run(main())
```

---

## Part 7: Testing Your Setup

### Test Script

```python
# test_facebook_setup.py
import asyncio
import os
from dotenv import load_dotenv
from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer

async def test_setup():
    """Test Facebook/Instagram setup"""
    
    load_dotenv()
    
    print("="*60)
    print("FACEBOOK/INSTAGRAM SETUP TEST")
    print("="*60)
    
    # Initialize
    server = FacebookInstagramMCPServer(
        page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN'),
        instagram_business_account_id=os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
    )
    
    # Test 1: Get recent posts
    print("\n[Test 1] Getting recent Facebook posts...")
    try:
        result = await server.execute_tool(
            "get_facebook_posts",
            {"limit": 1}
        )
        print(f"✅ Success: {result.text[:100]}...")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test 2: Post to Facebook
    print("\n[Test 2] Posting test message to Facebook...")
    try:
        result = await server.execute_tool(
            "post_to_facebook",
            {"message": "Test post from AI Employee! 🤖 #Automation"}
        )
        print(f"✅ Success: {result.text}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test 3: Get insights
    print("\n[Test 3] Getting Facebook insights...")
    try:
        result = await server.execute_tool(
            "get_facebook_insights",
            {"metric": "page_impressions", "days": 7}
        )
        print(f"✅ Success: {result.text[:100]}...")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test 4: Instagram insights
    print("\n[Test 4] Getting Instagram insights...")
    try:
        result = await server.execute_tool(
            "get_instagram_insights",
            {"metric": "follower_count"}
        )
        print(f"✅ Success: {result.text}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

asyncio.run(test_setup())
```

Run test:
```bash
python test_facebook_setup.py
```

---

## Part 8: Common Issues & Solutions

### Issue 1: "Invalid Access Token"
**Solution**: Token expired. Generate new one from Graph Explorer.

### Issue 2: "Permissions Error"
**Solution**: Make sure app has these permissions:
- `pages_manage_posts`
- `pages_read_engagement`
- `instagram_basic`
- `instagram_content_publish`

### Issue 3: "Instagram Account Not Found"
**Solution**: 
- Ensure Instagram is Business account
- Connected to Facebook Page
- Account is public (not private)

### Issue 4: "Image URL Not Accessible"
**Solution**: Image must be publicly accessible URL (not localhost).

---

## Quick Reference

### Post to Facebook
```bash
python -c "from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer; import asyncio; import os; from dotenv import load_dotenv; load_dotenv(); server = FacebookInstagramMCPServer(page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')); result = asyncio.run(server.execute_tool('post_to_facebook', {'message': 'Test!'})); print(result.text)"
```

### Get Insights
```bash
python -c "from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer; import asyncio; import os; from dotenv import load_dotenv; load_dotenv(); server = FacebookInstagramMCPServer(page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')); result = asyncio.run(server.execute_tool('get_facebook_insights', {'metric': 'page_impressions', 'days': 7})); print(result.text)"
```

---

**Your AI Employee can now auto-post to Facebook and Instagram!** 🚀
