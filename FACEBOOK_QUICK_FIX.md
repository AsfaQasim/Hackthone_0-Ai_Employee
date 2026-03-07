# 🚀 Facebook Token - Quick Fix

## What You Need to Do (5 Minutes)

Looking at your screenshot, you're almost there! Just need to fix the permissions.

### Step 1: Fix Permissions in Graph API Explorer

You're already in the right place! Now:

1. **Remove** the `manage_fundraisers` permission (click the X next to it)

2. **Add** these permissions instead:
   - Type `pages_manage_posts` in the search box → Click to add
   - Type `pages_show_list` in the search box → Click to add
   - Type `pages_read_engagement` in the search box → Click to add

3. Click **"Generate Access Token"** button (blue button)

4. Facebook will ask you to:
   - Log in (if not already)
   - Select which Facebook Page to use
   - Confirm permissions

5. Click **"Continue"** and **"Done"**

### Step 2: Get Your PAGE Token (Important!)

The token you just got is a USER token. You need a PAGE token:

1. In the Graph API Explorer, change the GET request to:
   ```
   me/accounts
   ```

2. Click the **"Submit"** button

3. You'll see JSON response like this:
   ```json
   {
     "data": [
       {
         "access_token": "EAABsbCS1iHgBO7ZC...",  ← Copy THIS token
         "category": "Community",
         "name": "Your Page Name",
         "id": "123456789012345",  ← Copy this ID too
         "tasks": ["ANALYZE", "ADVERTISE", "CREATE_CONTENT"]
       }
     ]
   }
   ```

4. Copy TWO things:
   - The `id` (your Page ID)
   - The `access_token` (your Page token)

### Step 3: Update Your .env File

Open your `.env` file and add/update these lines:

```env
# Facebook Configuration
FACEBOOK_PAGE_ID=123456789012345
FACEBOOK_PAGE_ACCESS_TOKEN=EAABsbCS1iHgBO7ZC...paste_full_token_here
```

**Important**: 
- Use the PAGE token from Step 2, NOT the user token!
- Make sure there are no spaces around the `=` sign
- The token should start with `EAA`

### Step 4: Test It

Run this command:

```bash
python facebook_token_helper.py
```

Choose option 3 to test your token.

Or run:

```bash
python test_facebook_autopost.py
```

## Alternative: Use the Helper Script

If you want an easier way:

```bash
python facebook_token_helper.py
```

Choose option 1, paste your USER token, and it will show you all your pages with their tokens.

## Why This Matters

- **User Token**: Represents YOU, expires in 1-2 hours
- **Page Token**: Represents your PAGE, can last 60 days
- You need the PAGE token to post to your page

## Common Mistakes

❌ **Wrong**: Using the token from the "Access Token" field at the top  
✅ **Right**: Using the token from `/me/accounts` response

❌ **Wrong**: Using `manage_fundraisers` permission  
✅ **Right**: Using `pages_manage_posts` permission

❌ **Wrong**: Copying only part of the token  
✅ **Right**: Copying the ENTIRE token (usually 200+ characters)

## Still Not Working?

If you're still having issues, run:

```bash
python facebook_token_helper.py
```

And choose option 1. Paste your token and I'll help you get the right page token.

---

**Quick Summary**:
1. Remove `manage_fundraisers` permission
2. Add `pages_manage_posts` permission
3. Generate token
4. Get page token from `/me/accounts`
5. Update `.env` file
6. Test it!
