# Facebook Auto-Posting - Quick Start

## 5-Minute Setup Guide

### Step 1: Get Facebook Page Access Token (2 minutes)

1. Go to: https://developers.facebook.com/tools/explorer/
2. Select your app (or create one)
3. Click **Get Token** → **Get Page Access Token**
4. Select your Facebook Page
5. Copy the token (starts with `EAA...`)

### Step 2: Configure .env File (1 minute)

Create/edit `.env` file in project root:

```env
FACEBOOK_PAGE_ACCESS_TOKEN=EAA...your_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000000
```

### Step 3: Test Posting (2 minutes)

```bash
# Run test script
test_facebook_autopost.bat

# Or manually
python test_facebook_autopost.py
```

**That's it!** Your AI Employee can now post to Facebook automatically!

---

## Practical Examples

### Example 1: Post Business Update

```python
import asyncio
from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer
import os
from dotenv import load_dotenv

load_dotenv()

server = FacebookInstagramMCPServer(
    page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
)

async def post_update():
    result = await server.execute_tool(
        "post_to_facebook",
        {
            "message": """🎉 Business Update!

Just closed a new deal worth $5,000!
Our AI Employee is crushing it!

#Business #Success #AI"""
        }
    )
    print(result.text)

asyncio.run(post_update())
```

### Example 2: Auto-Post from Odoo Invoice

```python
# When invoice is created in Odoo, auto-post to Facebook
async def post_invoice(invoice_id, customer, amount):
    message = f"""🎉 New Invoice!

Customer: {customer}
Amount: ${amount:,.2f}

Thank you for your business!"""
    
    await server.execute_tool(
        "post_to_facebook",
        {"message": message}
    )

# Usage
await post_invoice(123, "Acme Corp", 1500)
```

### Example 3: Daily Motivation Post

```python
import schedule
import time
from datetime import datetime

async def post_daily_motivation():
    quotes = [
        "The best way to predict the future is to create it! 💪",
        "Success is not final, failure is not fatal! ✨",
        "Believe you can and you're halfway there. 🚀"
    ]
    
    import random
    await server.execute_tool(
        "post_to_facebook",
        {"message": random.choice(quotes)}
    )

# Schedule daily at 8 AM
schedule.every().day.at("08:00").do(
    lambda: asyncio.run(post_daily_motivation())
)

# Keep running
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Commands Reference

### Post to Facebook
```bash
python -c "from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer; import asyncio; import os; from dotenv import load_dotenv; load_dotenv(); server = FacebookInstagramMCPServer(page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')); result = asyncio.run(server.execute_tool('post_to_facebook', {'message': 'Test!'})); print(result.text)"
```

### Get Recent Posts
```bash
python -c "from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer; import asyncio; import os; from dotenv import load_dotenv; load_dotenv(); server = FacebookInstagramMCPServer(page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')); result = asyncio.run(server.execute_tool('get_facebook_posts', {'limit': 5})); print(result.text)"
```

### Get Insights
```bash
python -c "from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer; import asyncio; import os; from dotenv import load_dotenv; load_dotenv(); server = FacebookInstagramMCPServer(page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')); result = asyncio.run(server.execute_tool('get_facebook_insights', {'metric': 'page_impressions', 'days': 7})); print(result.text)"
```

---

## Full Documentation

- **Complete Guide**: `FACEBOOK_INSTAGRAM_AUTOPOST_GUIDE.md`
- **Test Script**: `test_facebook_autopost.py`
- **Batch Test**: `test_facebook_autopost.bat`

---

## Troubleshooting

### "Invalid Token"
→ Token expired. Get new one from Graph Explorer.

### "Permissions Error"
→ Make sure app has `pages_manage_posts` permission.

### "Page Not Found"
→ Ensure you're admin of the Facebook Page.

---

**Ready to auto-post!** 🚀
