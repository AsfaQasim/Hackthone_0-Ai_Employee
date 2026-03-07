# 🔧 Fix Facebook Permissions

## The Problem

Your token needs TWO permissions:
1. ✅ `pages_manage_posts` (you have this)
2. ❌ `pages_read_engagement` (missing)

## Quick Fix (5 Minutes)

### Step 1: Go to Graph API Explorer

https://developers.facebook.com/tools/explorer/

### Step 2: Add Missing Permission

1. Look at the right side "Permissions" section
2. Click "Add a Permission" or search box
3. Type: `pages_read_engagement`
4. Click to add it
5. You should now have BOTH:
   - `pages_manage_posts` ✅
   - `pages_read_engagement` ✅

### Step 3: Generate New Token

1. Click "Generate Access Token" button (blue button)
2. Facebook will ask you to confirm
3. Click "Continue" and "Done"

### Step 4: Get Page Token

1. Change the endpoint to: `me/accounts`
2. Click "Submit"
3. Copy the `access_token` from the response

### Step 5: Update .env

Open `.env` and replace the old token:

```env
FACEBOOK_PAGE_ACCESS_TOKEN=EAA...paste_NEW_token_here
```

### Step 6: Test Again

```bash
python facebook_auto_post.py "Test post after fixing permissions"
```

## Visual Checklist

Before generating token:
- [ ] I'm in Graph API Explorer
- [ ] I've selected my app
- [ ] I see `pages_manage_posts` permission
- [ ] I see `pages_read_engagement` permission
- [ ] Both are checked/enabled

After generating:
- [ ] Changed endpoint to `me/accounts`
- [ ] Clicked Submit
- [ ] Copied the `access_token` from response
- [ ] Updated `FACEBOOK_PAGE_ACCESS_TOKEN` in `.env`
- [ ] Saved `.env` file

## Alternative: Use Helper Script

```bash
python facebook_token_helper.py
```

Choose option 1, paste your NEW token (with both permissions), and it will show you the page token to use.

## Why This Happens

Facebook requires BOTH permissions to post to pages:
- `pages_manage_posts` - Permission to create posts
- `pages_read_engagement` - Permission to read page data

Without both, posting will fail.

## After Fixing

Once you have both permissions, you can:
- ✅ Post to Facebook automatically
- ✅ Schedule posts
- ✅ Use the auto-poster
- ✅ Integrate with AI Employee

---

**Quick Summary**:
1. Add `pages_read_engagement` permission
2. Generate new token
3. Get page token from `/me/accounts`
4. Update `.env`
5. Test again!
