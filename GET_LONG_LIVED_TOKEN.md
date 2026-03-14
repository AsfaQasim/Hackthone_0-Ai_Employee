# 🔄 Get Long-Lived Facebook Token (60 Days)

## Problem
Aapka token 1 hour mein expire ho raha hai. Solution: **60-day long-lived token** lein.

---

## ✅ Step-by-Step Solution

### Step 1: Get Short-Lived Token (1 hour)

1. **Open Graph API Explorer:**
   https://developers.facebook.com/tools/explorer/

2. **Select your app:**
   - App ID: `1423095195415885`

3. **Get User Token:**
   - Click "Get Token" → "Get User Token"
   - Check permissions:
     - ✅ `pages_manage_posts`
     - ✅ `pages_read_engagement`
     - ✅ `pages_show_list`
   - Click "Generate Access Token"
   - Login and approve

4. **Get Page Token:**
   - Click "Get Token" → "Get Page Access Token"
   - Select your page: "AI posting"
   - Copy this token (short-lived, 1 hour)

---

### Step 2: Extend to Long-Lived Token (60 days)

1. **Open Access Token Debugger:**
   https://developers.facebook.com/tools/debug/access_token/

2. **Paste your short-lived token**
   - Paste the token you copied in Step 1

3. **Click "Debug"**
   - Shows token info and expiry

4. **Click "Extend Access Token"**
   - Facebook generates 60-day token

5. **Copy the NEW token**
   - This is your long-lived token (60 days)

---

### Step 3: Update .env File

Open `.env` and replace:

```env
FACEBOOK_PAGE_ACCESS_TOKEN=EAA...<your_60_day_token_here>
```

**Save the file.**

---

### Step 4: Verify

```cmd
python verify_facebook_token.py
```

Should show:
```
✅ TOKEN IS VALID!
   Page ID: 967740493097470
   Page Name: AI posting
```

---

### Step 5: Test Posting

```cmd
python facebook_silver_poster.py "Testing long-lived token!"
```

Should show:
```
✅ SUCCESS!
   Post ID: 967740493097470_xxxxx
   URL: https://facebook.com/xxxxx
```

---

## 🔍 Token Comparison

| Token Type | Validity | Length | Use |
|------------|----------|--------|-----|
| Short-Lived | 1 hour | ~150 chars | Testing |
| Long-Lived | 60 days | ~200 chars | Production ✅ |

---

## 📝 Important Notes

1. **Page Token, not User Token**
   - Page token is longer
   - Has page posting permissions
   - Required for posting to pages

2. **Token Expiry**
   - Short-lived: 1 hour
   - Long-lived: 60 days
   - After 60 days, extend again

3. **Store Safely**
   - Never commit `.env` to git
   - Keep token private
   - Rotate monthly

---

## 🚀 Quick Links

- **Graph API Explorer:** https://developers.facebook.com/tools/explorer/
- **Token Debugger:** https://developers.facebook.com/tools/debug/access_token/
- **Extend Token:** https://developers.facebook.com/tools/debug/access_token/ (click "Extend")

---

## ❓ Troubleshooting

### "Extend" button not showing
- Make sure token is valid (not already expired)
- Make sure you're using Page Token, not User Token

### Token still expires quickly
- Make sure you clicked "Extend Access Token"
- Copy the NEW token from the extend dialog

### Still getting permission error
- Check token has `pages_manage_posts` permission
- Check you're admin of the page

---

*Silver Tier Facebook - Long-Lived Token Guide*
