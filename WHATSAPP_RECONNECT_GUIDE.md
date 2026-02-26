# WhatsApp Reconnect Guide

## Problem
WhatsApp session expire ho gaya hai. Messages aa rahe hain but send nahi ho rahe.

## Solution - Dobara QR Code Scan Karo

### Step 1: Reconnect Command
```cmd
reconnect_whatsapp.bat
```

Ya directly:
```cmd
python Skills/whatsapp_watcher.py auth
```

### Step 2: QR Code Scan Karo

1. **Browser khulega** - Chrome window dikhegi
2. **WhatsApp Web load hoga** - QR code dikhega
3. **Apne phone mein:**
   - WhatsApp open karo
   - Settings (⚙️) > Linked Devices
   - "Link a Device" tap karo
   - QR code scan karo

### Step 3: Wait for Connection
- QR code scan hone ke baad
- "WhatsApp Web is ready" dikhega
- Browser automatically band ho jayega
- Session save ho jayega

### Step 4: Test Send Again
```cmd
python simple_send_test.py
```

## Why Session Expire Hota Hai?

WhatsApp Web sessions expire ho jate hain agar:
- Browser band kar do
- Long time se use nahi kiya
- WhatsApp phone pe logout kiya
- Computer restart hua

## Solution: Auto-Reconnect

Agar bar bar reconnect karna pad raha hai, toh:

1. **Keep browser open** - Headless mode off rakho
2. **Regular polling** - Watcher running rakho
3. **Session refresh** - Har 24 hours mein ek baar reconnect

## Quick Commands

### Check Status
```cmd
python check_silver_status.py
```

### Reconnect
```cmd
reconnect_whatsapp.bat
```

### Test Send
```cmd
python simple_send_test.py
```

### Start Watcher (keeps connection alive)
```cmd
python Skills/whatsapp_watcher.py start
```

## Important Notes

- **Session files** `.whatsapp_session` folder mein hain
- **Delete session** agar corrupt ho gaya: `rmdir /s .whatsapp_session`
- **Fresh start** ke liye session delete karo aur dobara auth karo

## Troubleshooting

### "WhatsApp Web not loaded"
→ Session expire hai, reconnect karo

### "QR code timeout"
→ 5 minutes ke andar scan karo

### "Browser not opening"
→ Chrome installed hai? System Chrome use kar rahe hain

### "Messages receive ho rahe but send nahi"
→ Session read-only mode mein hai, reconnect karo

---

**Remember**: WhatsApp Web sessions temporary hote hain. Regular use se active rehte hain!
