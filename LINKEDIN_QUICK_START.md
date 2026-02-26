# LinkedIn Watcher - Quick Start Guide

## Aasan Tareeqa (Simple Method)

### Step 1: Playwright Install karo

```bash
pip install playwright
playwright install chromium
```

### Step 2: LinkedIn Login karo

```bash
python Skills/linkedin_watcher_simple.py auth --vault . --session .linkedin_session
```

Yeh browser khol dega. Aap manually LinkedIn login karo, phir Enter press karo.

### Step 3: Test karo

```bash
python Skills/linkedin_watcher_simple.py poll --vault . --session .linkedin_session
```

Yeh aapke LinkedIn notifications check karega aur Inbox folder mein files bana dega.

---

## Important Notes

### Bronze Tier ke liye

**LinkedIn authentication OPTIONAL hai!**

Bronze Tier requirements:
- ✅ Obsidian vault (Done)
- ✅ Dashboard.md (Done)
- ✅ Company_Handbook.md (Done)
- ✅ **ONE working watcher** (Gmail already working ✅)
- ✅ Claude integration (Done)
- ✅ Agent Skills (Done)

**Aapka Bronze Tier already complete hai!** LinkedIn optional hai.

### Silver Tier ke liye

Silver Tier mein **TWO or more watchers** chahiye:
- ✅ Gmail Watcher (already done)
- ⏳ LinkedIn Watcher (optional - can use simple version)
- ✅ WhatsApp Watcher (already done)

---

## Current Status

**Aapke paas hai:**
1. ✅ Gmail Watcher (fully working)
2. ✅ WhatsApp Watcher (fully working)
3. ✅ LinkedIn Watcher (2 versions available)
   - `Skills/linkedin_watcher.py` (API-based - needs token)
   - `Skills/linkedin_watcher_simple.py` (Playwright-based - easy)

**Recommendation:**
- **Bronze Tier**: Use Gmail watcher only (already complete ✅)
- **Silver Tier**: Add LinkedIn simple watcher later

---

## Troubleshooting

### "playwright not found"
```bash
pip install playwright
playwright install chromium
```

### "Session not working"
Delete session folder and re-authenticate:
```bash
rmdir /s .linkedin_session
python Skills/linkedin_watcher_simple.py auth
```

### "LinkedIn blocking automation"
LinkedIn may detect automation. Use carefully and don't poll too frequently.

---

## Summary

**Aapko abhi kuch nahi karna hai!**

Your Bronze Tier is 100% complete with Gmail watcher. LinkedIn is optional for Silver Tier.

**Next steps:**
1. ✅ Bronze Tier complete - Submit it!
2. Test Gmail watcher end-to-end
3. Later: Add LinkedIn if needed for Silver Tier

---

**Bronze Tier Status**: ✅ COMPLETE  
**LinkedIn**: Optional (can add later)
