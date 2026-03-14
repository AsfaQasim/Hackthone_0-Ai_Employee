# 🔧 Fix Facebook Permission Error

## Your Error

```
(#200) If posting to a group, requires app being installed in the group...
If posting to a page, requires both pages_read_engagement and pages_manage_posts 
as an admin with sufficient administrative permission
```

## ✅ Solution: Get New Token with Correct Permissions

### Quick Steps

#### 1. Open Graph API Explorer
Click this link: **https://developers.facebook.com/tools/explorer/**

#### 2. Select Your App
- Choose your app from dropdown at top
- App ID: `1423095195415885`

#### 3. Get User Token First
1. Click **"Get Token"** button
2. Select **"Get User Token"**
3. Check these permissions:
   - ☑️ `pages_manage_posts`
   - ☑️ `pages_read_engagement`
   - ☑️ `pages_show_list`
4. Click **"Generate Access Token"**
5. Login and grant permissions if prompted

#### 4. Get PAGE Access Token (Important!)
1. Click **"Get Token"** again
2. Select **"Get Page Access Token"** (NOT User Token!)
3. Select your page from the list
4. This generates a **PAGE access token** ← This is what you need!

#### 5. Copy the Token
- Copy the FULL token string (starts with `EAA...`)
- It's long, make sure to copy all of it

#### 6. Update .env File

Open `.env` and update this line:
```env
FACEBOOK_PAGE_ACCESS_TOKEN=EAA...your_new_token_here
```

#### 7. Test
```cmd
python verify_facebook_token.py
python facebook_silver_poster.py "Test post"
```

---

## ⚠️ Common Issues

### Issue: "Pages you manage" list is empty
**Fix:** Make sure you're admin of the Facebook Page

### Issue: Token expires in 1 hour
**Fix:** Get a long-lived token:
1. Go to: https://developers.facebook.com/tools/debug/access_token/
2. Paste your token
3. Click "Debug"
4. Click "Extend Access Token"
5. Copy new 60-day token to `.env`

### Issue: Still getting permission error
**Fix:** You're probably using USER token instead of PAGE token
- USER token: Short, for personal actions
- PAGE token: Long, for posting to pages ← You need this one!

---

## 🔍 Verify Token Type

**PAGE Token** (what you need):
- Long string (200+ characters)
- Starts with `EAA...`
- Generated via "Get Page Access Token"

**USER Token** (won't work):
- Shorter string
- Also starts with `EAA...`
- Generated via "Get User Token"

---

## 📝 After Updating Token

Run these commands:

```cmd
# 1. Verify token is valid
python verify_facebook_token.py

# Expected output: ✅ TOKEN IS VALID!

# 2. Test posting
python facebook_silver_poster.py "Testing Silver Tier!"

# Expected output: ✅ SUCCESS!
```

---

## 🎯 Direct Links

- **Graph API Explorer:** https://developers.facebook.com/tools/explorer/
- **Token Debugger:** https://developers.facebook.com/tools/debug/access_token/
- **Your Page:** https://www.facebook.com/profile.php?id=967740493097470

---

## Need Help?

1. Check `SILVER_TIER_FACEBOOK_QUICKSTART.md` for complete guide
2. Check `SILVER_TIER_FACEBOOK_COMPLETE.md` for full documentation
3. Run `python test_facebook_silver_tier.py` for full diagnostic

---

*Silver Tier Facebook - Permission Fix Guide*
