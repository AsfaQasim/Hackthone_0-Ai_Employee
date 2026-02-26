# WhatsApp Kaise Connect Karein - Urdu Guide

## Masla Kya Hai?

WhatsApp ka session expire ho gaya hai. Messages aa rahe hain (inbox mein 3 messages hain) lekin send nahi ho rahe.

## Hal - QR Code Dobara Scan Karo

### Step 1: Command Run Karo

```cmd
python Skills/whatsapp_watcher.py auth
```

Ya yeh file double-click karo:
```
reconnect_whatsapp.bat
```

### Step 2: Browser Khulega

- Chrome browser automatically khulega
- WhatsApp Web load hoga
- QR code dikhega (black and white square)

### Step 3: Phone Se Scan Karo

**Apne phone mein:**

1. WhatsApp app kholo
2. Upar right corner mein 3 dots (⋮) tap karo
3. "Linked Devices" select karo
4. Neeche "Link a Device" ka button tap karo
5. Camera khulega
6. Computer screen pe jo QR code hai usko scan karo

### Step 4: Connected!

- Scan hone ke baad "WhatsApp Web is ready" dikhega
- Browser automatically band ho jayega
- Ab send bhi kaam karega!

### Step 5: Test Karo

```cmd
python simple_send_test.py
```

Yeh Anisa ko automated message bhej dega.

## Kyun Disconnect Hua?

WhatsApp Web sessions temporary hote hain:
- Computer restart hua
- Browser band kar diya
- Long time se use nahi kiya
- Phone pe WhatsApp logout kiya

## Bar Bar Disconnect Ho Raha Hai?

**Solution**: Watcher running rakho

```cmd
python Skills/whatsapp_watcher.py start
```

Yeh background mein chalega aur connection alive rakhega.

## Quick Commands - Yaad Rakho

| Kaam | Command |
|------|---------|
| Reconnect karo | `reconnect_whatsapp.bat` |
| Status check karo | `python check_silver_status.py` |
| Message bhejo | `python simple_send_test.py` |
| Watcher start karo | `python Skills/whatsapp_watcher.py start` |

## Important!

- **Token ki zaroorat NAHI hai** - Yeh WhatsApp Web hai, free hai
- **Facebook account ki zaroorat NAHI hai** - Bas QR code scan karo
- **Session files** `.whatsapp_session` folder mein save hote hain
- **Agar problem ho** toh session delete karo: `rmdir /s .whatsapp_session`

## Abhi Kya Karna Hai?

1. ✅ Browser khula hai? QR code dikha?
2. ✅ Phone se scan karo
3. ✅ "Connected" dikhne ka wait karo
4. ✅ Test message bhejo

---

**Yaad Rakho**: Yeh normal hai! WhatsApp Web ko regular reconnect karna padta hai. Ek baar connect ho gaya toh kaam karega! 🚀
