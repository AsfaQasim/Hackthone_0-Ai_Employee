# 📸 Facebook Token - Step by Step (With Screenshots Guide)

## What You See vs What You Need

### ❌ Current Problem (From Your Screenshot)

You have:
- Permission: `manage_fundraisers` ← Wrong permission
- Token type: User Token ← Need Page Token

### ✅ What You Need

You need:
- Permission: `pages_manage_posts` ← Correct permission
- Token type: Page Token ← From /me/accounts

---

## Step-by-Step Instructions

### Step 1: Fix Permissions

**In Graph API Explorer (where you are now):**

1. Look at the right side where it says "Permissions"
2. You'll see `manage_fundraisers` with an X
3. **Click the X** to remove it

4. Now click **"Add a Permission"** or search box
5. Type: `pages_manage_posts`
6. Click to add it

7. Also add:
   - `pages_show_list`
   - `pages_read_engagement`

### Step 2: Generate Token

1. Click the blue **"Generate Access Token"** button (top right)
2. A popup appears
3. Click **"Continue as [Your Name]"**
4. Select your Facebook Page
5. Click **"Done"**

### Step 3: Get Page Token (MOST IMPORTANT!)

**Now you have a USER token, but you need a PAGE token:**

1. Look at the top where it says:
   ```
   GET  graph  facebook.com  v25.0  /me?fields=id,name
   ```

2. **Change** `/me?fields=id,name` to just:
   ```
   me/accounts
   ```

3. Click the **"Submit"** button (blue button on right)

4. You'll see a response like:
   ```json
   {
     "data": [
       {
         "access_token": "EAABsbCS1iHgBO7ZC1iHgBO7ZC...",
         "category": "Community",
         "name": "My Awesome Page",
         "id": "123456789012345",
         "tasks": ["ANALYZE", "ADVERTISE", "CREATE_CONTENT", "MODERATE"]
       }
     ]
   }
   ```

5. **Copy TWO things from this response:**
   - `id`: This is your **FACEBOOK_PAGE_ID**
   - `access_token`: This is your **FACEBOOK_PAGE_ACCESS_TOKEN**

### Step 4: Update .env File

Open your `.env` file in the project folder and add:

```env
# Facebook Configuration
FACEBOOK_PAGE_ID=123456789012345
FACEBOOK_PAGE_ACCESS_TOKEN=EAABsbCS1iHgBO7ZC1iHgBO7ZC...
```

**Important Notes:**
- Replace `123456789012345` with YOUR page ID
- Replace `EAABsbCS1iHgBO7ZC...` with YOUR page token
- The token is LONG (200+ characters) - copy ALL of it
- No spaces around the `=` sign

### Step 5: Save and Test

1. Save the `.env` file

2. Open terminal/command prompt

3. Run:
   ```bash
   python facebook_token_helper.py
   ```

4. Choose option 3 to test

5. If it says "✅ Token is valid!" - you're done!

---

## Visual Checklist

Before you start:
- [ ] I'm in Graph API Explorer (https://developers.facebook.com/tools/explorer/)
- [ ] I've selected my app "Hackthone_0" in the dropdown
- [ ] I can see the "Generate Access Token" button

Step 1 - Permissions:
- [ ] Removed `manage_fundraisers`
- [ ] Added `pages_manage_posts`
- [ ] Added `pages_show_list`
- [ ] Added `pages_read_engagement`

Step 2 - Generate:
- [ ] Clicked "Generate Access Token"
- [ ] Selected my Facebook Page
- [ ] Clicked "Done"

Step 3 - Get Page Token:
- [ ] Changed endpoint to `me/accounts`
- [ ] Clicked "Submit"
- [ ] Copied the `id` from response
- [ ] Copied the `access_token` from response

Step 4 - Update .env:
- [ ] Opened `.env` file
- [ ] Added `FACEBOOK_PAGE_ID=...`
- [ ] Added `FACEBOOK_PAGE_ACCESS_TOKEN=...`
- [ ] Saved the file

Step 5 - Test:
- [ ] Ran `python facebook_token_helper.py`
- [ ] Chose option 3
- [ ] Saw "✅ Token is valid!"

---

## Common Issues

### Issue: "Invalid OAuth access token"

**Cause**: Token expired or wrong token type

**Fix**: 
1. Make sure you're using the PAGE token from `/me/accounts`
2. Not the USER token from the top field

### Issue: "Permissions error"

**Cause**: Missing `pages_manage_posts` permission

**Fix**:
1. Go back to Step 1
2. Make sure you added `pages_manage_posts`
3. Generate token again

### Issue: "Page not found"

**Cause**: Wrong Page ID or not admin of page

**Fix**:
1. Make sure you copied the correct `id` from `/me/accounts`
2. Make sure you're an admin of the Facebook Page

### Issue: Token expires quickly

**Cause**: Using short-lived token

**Fix**:
1. Page tokens from `/me/accounts` last longer
2. For 60-day token, use the helper script option 2

---

## Quick Test Command

After updating `.env`, test immediately:

```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Page ID:', os.getenv('FACEBOOK_PAGE_ID')); print('Token:', os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')[:20] + '...')"
```

This will show you if the values are loaded correctly.

---

## Need More Help?

If you're stuck on any step, run:

```bash
python facebook_token_helper.py
```

Choose option 1 and follow the prompts. The script will guide you through getting the correct token.

---

**Remember**: The key is getting the PAGE token from `/me/accounts`, not the USER token from the top field!
