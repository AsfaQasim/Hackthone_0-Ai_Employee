# WhatsApp Access Token - Step by Step Guide

## Access Token Kahan Se Milega? 🔑

---

## Method 1: Quick Test Token (5 Minutes) - RECOMMENDED

### Step 1: Meta Developers Par Jao
```
https://developers.facebook.com/
```

1. **Login** karo Facebook account se
2. Agar pehli baar hai to **"Get Started"** click karo

### Step 2: App Banao

1. **"My Apps"** par click karo (top right)
2. **"Create App"** button click karo
3. **"Business"** type select karo
4. **Next** click karo
5. App details bharo:
   - App Name: "My WhatsApp Bot" (kuch bhi naam)
   - App Contact Email: Apna email
6. **"Create App"** click karo

### Step 3: WhatsApp Product Add Karo

1. App dashboard mein **"Add Product"** section dekho
2. **"WhatsApp"** dhundo
3. **"Set Up"** button click karo

### Step 4: Access Token Milega! ✅

1. Left sidebar mein **"WhatsApp"** > **"Getting Started"** par jao
2. Page scroll karo
3. **"Temporary access token"** section dekho
4. Yahan **ACCESS TOKEN** dikhega! 
5. **Copy** button click karo

**Example:**
```
EAABsbCS1iHgBO4rqDwFZC8ZAn7ZBqBAZCZCqhZBqhZBqhZBqhZBqh...
```

### Step 5: Phone Number ID Bhi Milega

Same page par:
1. **"Phone number ID"** section dekho
2. Number copy karo

**Example:**
```
123456789012345
```

### Step 6: Test Number Add Karo

1. **"To"** field mein apna WhatsApp number add karo
   - Format: Country code + number (no spaces, no +)
   - Pakistan: 923001234567
   - India: 919876543210

2. **"Send Message"** button se test karo
3. Apne WhatsApp par message aayega! ✅

---

## Method 2: Permanent Token (Production Use)

Temporary token 24 hours mein expire ho jata hai.
Permanent token ke liye:

### Step 1: System User Banao

1. **Meta Business Suite** par jao:
   ```
   https://business.facebook.com/
   ```

2. **Business Settings** > **Users** > **System Users**

3. **"Add"** button click karo

4. System user banao:
   - Name: "WhatsApp Bot"
   - Role: Admin

### Step 2: Token Generate Karo

1. System user par click karo
2. **"Generate New Token"** button
3. **App** select karo (jo aapne banaya)
4. **Permissions** select karo:
   - `whatsapp_business_messaging`
   - `whatsapp_business_management`
5. **"Generate Token"** click karo
6. Token copy karo aur safe rakho! ⚠️

---

## Screenshots Guide (Visual Steps)

### 1. Meta Developers Homepage
```
https://developers.facebook.com/
```
- Top right: "My Apps" button
- Click karke "Create App"

### 2. Create App Screen
- Select: "Business" type
- Fill: App name
- Click: "Create App"

### 3. Add WhatsApp Product
- Dashboard mein "Add Product" section
- WhatsApp dhundo
- "Set Up" click karo

### 4. Getting Started Page
```
Left Sidebar:
├── WhatsApp
│   ├── Getting Started  ← Yahan jao
│   ├── API Setup
│   └── Configuration
```

### 5. Access Token Section
```
┌─────────────────────────────────────────┐
│ Temporary access token                  │
├─────────────────────────────────────────┤
│ EAABsbCS1iHgBO4rqDwFZC8ZAn7ZBqBAZC...  │
│ [Copy] button                           │
│                                         │
│ ⚠️ Expires in 23 hours                  │
└─────────────────────────────────────────┘
```

### 6. Phone Number ID Section
```
┌─────────────────────────────────────────┐
│ Phone number ID                         │
├─────────────────────────────────────────┤
│ 123456789012345                         │
│ [Copy] button                           │
└─────────────────────────────────────────┘
```

---

## Quick Copy-Paste Setup

### Step 1: Get Token (5 minutes)
1. Go to: https://developers.facebook.com/
2. Create App > Business type
3. Add WhatsApp product
4. Copy token from "Getting Started"

### Step 2: Configure
Create `.env` file:
```env
WHATSAPP_PHONE_ID=123456789012345
WHATSAPP_ACCESS_TOKEN=EAABsbCS1iHgBO4rqDwFZC8ZAn7ZBqBAZC...
```

### Step 3: Test
```cmd
python whatsapp_business_api.py check
```

Should show:
```
✅ Phone ID: 123456789...
✅ Access Token: EAABsbCS1iHg...
✅ API is configured!
```

---

## Troubleshooting

### Problem: "Token not found"
**Solution:** 
- Make sure you're on "Getting Started" page
- Scroll down to find "Temporary access token"
- If not visible, refresh page

### Problem: "Token expired"
**Solution:**
- Temporary token expires in 24 hours
- Generate new token from same page
- Or create permanent token (Method 2)

### Problem: "Invalid token"
**Solution:**
- Copy complete token (very long string)
- No spaces before/after
- Check .env file format

### Problem: "Phone number not found"
**Solution:**
- Look for "Phone number ID" (not phone number)
- It's a long number like: 123456789012345
- Copy from "Getting Started" page

---

## Video Tutorial Links

### Official Meta Tutorial:
```
https://developers.facebook.com/docs/whatsapp/cloud-api/get-started
```

### YouTube Tutorials:
Search for: "WhatsApp Business API setup"

---

## Important Notes

### ⚠️ Temporary Token:
- Expires in 24 hours
- Good for testing
- Need to regenerate daily

### ✅ Permanent Token:
- Never expires
- Good for production
- Requires System User setup

### 🔒 Security:
- Never share token publicly
- Don't commit to GitHub
- Keep in .env file only

---

## Test Karne Ke Liye

### 1. Token Copy Karo
From: https://developers.facebook.com/ > Your App > WhatsApp > Getting Started

### 2. .env File Banao
```env
WHATSAPP_PHONE_ID=your_phone_id_here
WHATSAPP_ACCESS_TOKEN=your_token_here
```

### 3. Check Karo
```cmd
python whatsapp_business_api.py check
```

### 4. Test Message Bhejo
```cmd
python whatsapp_business_api.py test
```

---

## Summary

**Access Token Kahan Se Milega:**

1. ✅ https://developers.facebook.com/
2. ✅ Create App (Business type)
3. ✅ Add WhatsApp product
4. ✅ Go to "Getting Started"
5. ✅ Copy "Temporary access token"
6. ✅ Copy "Phone number ID"
7. ✅ Add to .env file
8. ✅ Test!

**Time Required:** 5 minutes

**Cost:** FREE (1000 messages/month)

---

## Next Steps

```cmd
# 1. Get token from Meta Developers
# 2. Add to .env file
# 3. Test

python whatsapp_business_api.py check
python whatsapp_business_api.py test
```

**Messages will go directly to WhatsApp!** ✅

---

## Need Help?

### Official Documentation:
https://developers.facebook.com/docs/whatsapp/cloud-api/get-started

### Support:
https://developers.facebook.com/support/

### Community:
https://stackoverflow.com/questions/tagged/whatsapp-business-api

---

**Ready to get your token?**

Go to: https://developers.facebook.com/

Follow steps above, and in 5 minutes you'll have your Access Token! 🚀
