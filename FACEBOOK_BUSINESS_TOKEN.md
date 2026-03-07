# 🔑 Facebook Token - Business Settings Se (Alternative Method)

## Problem
Graph API Explorer me `pages_manage_posts` permission nahi dikh raha.

## Solution: Facebook Business Settings Use Karo

### Method 1: Access Token Tool (Easiest)

1. **Is link par jao**: 
   https://developers.facebook.com/tools/accesstoken/

2. **Apni app select karo**: "Hackthone_0"

3. **Page Access Tokens** section me:
   - Apna page "AI posting" dikhega
   - "Generate Token" button click karo
   - Token copy karo

4. **Token update karo**:
   ```bash
   python update_facebook_token.py
   ```

### Method 2: App Settings Se

1. **Facebook Developers** par jao:
   https://developers.facebook.com/apps/

2. **Apni app select karo**: "Hackthone_0"

3. **Left sidebar** me:
   - "Add Product" click karo
   - "Facebook Login" select karo
   - "Set Up" click karo

4. **Settings** → **Basic**:
   - App ID copy karo
   - App Secret copy karo

5. **Token generate karo manually**:
   ```bash
   python generate_long_lived_token.py
   ```

### Method 3: Direct Page Token (Recommended)

1. **Facebook Page Settings** me jao:
   - Apna page "AI posting" kholo
   - Settings → Page Access
   - "Generate Token" option dhundo

2. Ya ye link try karo:
   https://www.facebook.com/v18.0/dialog/oauth?client_id=YOUR_APP_ID&redirect_uri=https://localhost&scope=pages_manage_posts,pages_read_engagement

   Replace `YOUR_APP_ID` with: `1423095195415885`

---

## Quick Fix Script

Main ek script bana deta hoon jo automatically sahi permissions ke saath token generate karega:
