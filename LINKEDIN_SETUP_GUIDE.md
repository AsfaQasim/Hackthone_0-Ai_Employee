# LinkedIn Authentication Setup Guide (Urdu/English)

## LinkedIn Ko Authenticate Karne Ka Tareeqa

LinkedIn watcher ko authenticate karne ke liye aapko LinkedIn API access token chahiye. Yeh do tareeqon se mil sakta hai:

### Option 1: LinkedIn API (Official - Complex)

**Steps:**

1. **LinkedIn Developer Portal par jao**
   - https://www.linkedin.com/developers/ par jao
   - "Create app" par click karo

2. **App Create karo**
   - App name: "AI Employee Watcher"
   - LinkedIn Page: Apna company page select karo (ya create karo)
   - App logo upload karo
   - Terms accept karo

3. **OAuth 2.0 Settings**
   - "Auth" tab par jao
   - Redirect URLs add karo: `http://localhost:8000/callback`
   - Scopes select karo:
     - `r_liteprofile` (basic profile)
     - `r_emailaddress` (email)
     - `w_member_social` (post karne ke liye)

4. **Access Token Generate karo**
   - Client ID aur Client Secret copy karo
   - OAuth flow complete karo
   - Access token milega

**Problem**: Yeh process complex hai aur LinkedIn API access limited hai.

---

### Option 2: Playwright-based Automation (Recommended - Simple)

LinkedIn API ke bajaye, hum WhatsApp watcher ki tarah browser automation use kar sakte hain.

**Advantages:**
- ✅ No API token needed
- ✅ Works like WhatsApp watcher
- ✅ Can read messages, notifications
- ✅ Can post updates

**Implementation:**

```python
# linkedin_watcher_playwright.py
from playwright.sync_api import sync_playwright
from base_watcher import BaseWatcher
from pathlib import Path
from datetime import datetime

class LinkedInWatcherPlaywright(BaseWatcher):
    """LinkedIn Watcher using Playwright (browser automation)"""
    
    def __init__(self, vault_path: str, session_path: str):
        super().__init__(vault_path, check_interval=300)  # 5 minutes
        self.session_path = Path(session_path)
        self.keywords = ['message', 'connection', 'job', 'opportunity']
    
    def authenticate(self):
        """Open LinkedIn for manual login"""
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                self.session_path,
                headless=False  # Show browser for login
            )
            page = browser.pages[0]
            page.goto('https://www.linkedin.com/login')
            
            print("Please login to LinkedIn...")
            print("Press Enter when done...")
            input()
            
            browser.close()
    
    def check_for_updates(self) -> list:
        """Check LinkedIn for new notifications"""
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                self.session_path,
                headless=True
            )
            page = browser.pages[0]
            page.goto('https://www.linkedin.com/notifications/')
            page.wait_for_selector('[data-test-notification-list]')
            
            # Get unread notifications
            notifications = page.query_selector_all('.notification-card--unread')
            
            items = []
            for notif in notifications[:5]:  # Process top 5
                text = notif.inner_text()
                items.append({
                    'text': text,
                    'timestamp': datetime.now().isoformat()
                })
            
            browser.close()
            return items
```

---

## Quick Setup (Playwright Method)

### Step 1: Install Playwright

```bash
pip install playwright
playwright install chromium
```

### Step 2: Create Session Folder

```bash
mkdir .linkedin_session
```

### Step 3: Authenticate

```bash
python Skills/linkedin_watcher_playwright.py auth
```

Yeh browser khol dega, aap manually login kar sakte ho.

### Step 4: Test

```bash
python Skills/linkedin_watcher_playwright.py poll
```

---

## Current Status

**Aapke paas already hai:**
- ✅ LinkedIn watcher file (Skills/linkedin_watcher.py)
- ✅ Base watcher framework

**Missing:**
- ❌ LinkedIn API access token
- ❌ Playwright-based implementation

---

## Recommendation

**Bronze Tier ke liye:** LinkedIn authentication optional hai. Aap Gmail watcher se Bronze Tier complete kar sakte ho.

**Silver Tier ke liye:** LinkedIn watcher implement karna hai. Main recommend karta hoon:

1. **Abhi ke liye:** Gmail watcher use karo (already working)
2. **Baad mein:** Playwright-based LinkedIn watcher implement karo (WhatsApp jaise)

---

## Alternative: Manual LinkedIn Monitoring

Agar API ya automation nahi chahiye, toh aap manually LinkedIn check kar sakte ho aur important messages ko Inbox folder mein copy kar sakte ho:

```bash
# Manually create LinkedIn notification file
echo "---
type: linkedin_message
from: John Doe
subject: Job Opportunity
priority: high
---

# LinkedIn Message

John Doe sent you a message about a job opportunity...
" > Inbox/linkedin_message_$(date +%Y%m%d_%H%M%S).md
```

---

## Next Steps

**For Bronze Tier (Current):**
1. ✅ Use Gmail watcher (already working)
2. ✅ Skip LinkedIn for now
3. ✅ Complete Bronze Tier

**For Silver Tier (Later):**
1. Implement Playwright-based LinkedIn watcher
2. Or use LinkedIn API if you get access
3. Or manually monitor LinkedIn

---

## Questions?

- **Q: Kya LinkedIn authentication zaroori hai Bronze Tier ke liye?**
  - A: Nahi, Bronze Tier ke liye sirf ek watcher chahiye (Gmail already hai)

- **Q: LinkedIn API kaise milega?**
  - A: LinkedIn Developer Portal se app create karke

- **Q: Kya Playwright method safe hai?**
  - A: Haan, lekin LinkedIn ke terms of service check karo

- **Q: Kya main LinkedIn skip kar sakta hoon?**
  - A: Haan, Bronze Tier ke liye Gmail watcher kaafi hai

---

**Recommendation:** Abhi Bronze Tier complete karo Gmail watcher se. LinkedIn baad mein add kar sakte ho Silver Tier mein.
