# 📘 Facebook Access Token Setup Guide

## Current Issue

Your token needs the correct permissions to post to Facebook pages.

## Step-by-Step Instructions

### Step 1: Go to Graph API Explorer

URL: https://developers.facebook.com/tools/explorer/

### Step 2: Select Your App

In the top dropdown, select: **Hackthone_0** (your app)

### Step 3: Get Page Access Token

1. Click the **"Generate Access Token"** button (blue button on right)
2. A popup will appear asking for permissions

### Step 4: Select Required Permissions

In the permissions popup, search for and enable these:

**Required Permissions**:
- ✅ `pages_manage_posts` - Allows posting to your page
- ✅ `pages_read_engagement` - Read page engagement data
- ✅ `pages_show_list` - List your pages

**Optional but Recommended**:
- ✅ `pages_read_user_content` - Read page content
- ✅ `publish_to_groups` - Post to groups (if needed)

### Step 5: Remove Unwanted Permissions

- ❌ Remove `manage_fundraisers` (not needed for posting)

### Step 6: Generate Token

1. Click **"Generate Token"** in the popup
2. Facebook will ask you to log in and confirm
3. Select which Facebook Page you want to post to
4. Click **"Continue"** and **"Done"**

### Step 7: Copy the Token

1. The token will appear in the "Access Token" field (starts with `EAA...`)
2. Click the copy icon next to it
3. This is your **User Access Token** (short-lived, 1-2 hours)

### Step 8: Get Page Access Token (Important!)

The token you just got is a USER token. You need a PAGE token:

1. In Graph API Explorer, change the endpoint to:
   ```
   GET /me/accounts
   ```

2. Click **"Submit"**

3. You'll see a list of your pages with their tokens:
   ```json
   {
     "data": [
       {
         "access_token": "EAAxxxx...",  // This is your PAGE token
         "category": "...",
         "name": "Your Page Name",
         "id": "123456789",
         "tasks": ["ANALYZE", "ADVERTISE", "MODERATE", "CREATE_CONTENT"]
       }
     ]
   }
   ```

4. Copy the `access_token` from YOUR page (the one you want to post to)

### Step 9: Update .env File

Open your `.env` file and add/update:

```env
# Facebook Configuration
FACEBOOK_PAGE_ID=123456789
FACEBOOK_PAGE_ACCESS_TOKEN=EAAxxxx...paste_PAGE_token_here
```

**Important**: Use the PAGE token from Step 8, NOT the user token!

## Getting Long-Lived Token (60 Days)

Short-lived tokens expire in 1-2 hours. To get a long-lived token:

### Method 1: Using Graph API Explorer

1. Go to: https://developers.facebook.com/tools/explorer/

2. Change endpoint to:
   ```
   GET /oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_LIVED_TOKEN
   ```

3. Replace:
   - `YOUR_APP_ID` - Your app ID (from Facebook App Dashboard)
   - `YOUR_APP_SECRET` - Your app secret (from Facebook App Dashboard)
   - `YOUR_SHORT_LIVED_TOKEN` - The page token from Step 8

4. Click Submit

5. Copy the new long-lived token

### Method 2: Using Python Script

I'll create a script for you to exchange tokens automatically.

## Verification

After updating `.env`, test the token:

```bash
python test_facebook_token.py
```

## Common Issues

### Issue 1: "Invalid OAuth access token"
**Solution**: Token expired. Get a new one following steps above.

### Issue 2: "Permissions error"
**Solution**: Make sure you selected `pages_manage_posts` permission.

### Issue 3: "Page not found"
**Solution**: 
- Verify `FACEBOOK_PAGE_ID` is correct
- Make sure you're using PAGE token, not USER token

### Issue 4: Token expires too quickly
**Solution**: Get long-lived token (60 days) using Method 1 or 2 above.

## Important Notes

1. **User Token vs Page Token**:
   - User Token: Expires in 1-2 hours
   - Page Token: Can be long-lived (60 days)
   - Always use PAGE token for posting

2. **Token Security**:
   - Never commit tokens to git
   - Keep `.env` in `.gitignore`
   - Rotate tokens regularly

3. **Permissions**:
   - You need to be admin of the Facebook Page
   - App must be in Development or Live mode
   - Some permissions require app review

## Next Steps

1. Follow steps above to get PAGE access token
2. Update `.env` file
3. Run test script to verify
4. If successful, you can start posting!

---

**Need Help?** If you're still having issues, let me know which step is failing.
