# 📊 Dashboard Guide - Urdu/English

## 🚀 Dashboard Kaise Chalayein / How to Run

### Step 1: Dependencies Install Karein
```cmd
npm install
```

### Step 2: Dashboard Start Karein
```cmd
npm run dashboard
```

### Step 3: Browser Mein Kholein
Apne browser mein ye URL open karein:
```
http://localhost:3000
```

## ✨ Dashboard Features

### 1. Statistics (Upar)
- **Total Tasks**: Kitne emails hain
- **High Priority**: Urgent emails (🔴 Red)
- **Medium Priority**: Normal emails (🟡 Yellow)  
- **Low Priority**: Kam important emails (🔵 Blue)

### 2. Search & Filter
- **Search Box**: Email subject, sender ya content search karein
- **Priority Filter**: Sirf specific priority ke emails dekhein
- **Refresh Button**: Naye emails load karein

### 3. Email Cards
Har email card mein:
- Subject (heading)
- Sender ka naam
- Date/Time
- Priority badge
- Email ka preview (pehle 150 characters)

### 4. Email Kholna
Kisi bhi email card pe click karein, wo markdown file khul jayegi.

## 🎨 Dashboard Ka Look

```
┌─────────────────────────────────────────┐
│  🤖 AI Employee Dashboard               │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐          │
│  │ 24 │ │ 12 │ │  8 │ │  4 │          │
│  │Tot │ │High│ │Med │ │Low │          │
│  └────┘ └────┘ └────┘ └────┘          │
├─────────────────────────────────────────┤
│  🔍 Search...  [Priority ▼] [🔄 Refresh]│
├─────────────────────────────────────────┤
│  ┌───────────────────────────────────┐ │
│  │ 🔴 Associate Project Manager      │ │
│  │ 📧 Indeed  📅 Today               │ │
│  │ Hi Asifa, It looks like your...  │ │
│  └───────────────────────────────────┘ │
│  ┌───────────────────────────────────┐ │
│  │ 🟡 Social Media Manager           │ │
│  │ 📧 LinkedIn  📅 Yesterday         │ │
│  │ New opportunity for you...        │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## 🔄 Workflow

### Complete Process:

1. **Gmail Watcher Run Karein**
   ```cmd
   python Skills/gmail_watcher.py poll
   ```
   Ye emails ko Needs_Action folder mein save karega.

2. **Dashboard Open Karein**
   ```cmd
   npm run dashboard
   ```
   Browser mein http://localhost:3000 kholein.

3. **Emails Dekhein**
   - Dashboard mein saare emails dikhenge
   - Priority ke saath sorted
   - Search aur filter kar sakte hain

4. **Email Process Karein**
   - Email card pe click karein
   - Markdown file khulegi
   - Action lein (reply, apply, etc.)

5. **Done Folder Mein Move Karein**
   - Jab kaam ho jaye
   - File ko Done/ folder mein move karein
   - Dashboard refresh karein

## 🎯 Tips & Tricks

### Search Tips:
- Company name search karein: "Indeed", "LinkedIn"
- Job type search karein: "Manager", "Developer"
- Sender search karein: "donotreply@indeed.com"

### Filter Tips:
- Pehle High Priority emails dekhein
- Urgent kaam pehle complete karein
- Low priority baad mein

### Organization:
- Roz dashboard check karein
- Processed emails Done/ mein move karein
- Dashboard clean rakhein

## 🛠️ Customization

### Colors Change Karna:
`ui/styles.css` file edit karein:
```css
/* High priority color */
.priority-high {
    background: #fee;
    color: #e74c3c;
}

/* Background gradient */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Port Change Karna:
`server.js` file mein:
```javascript
const PORT = 3000; // Apna port number
```

### Preview Length Change Karna:
`server.js` mein:
```javascript
preview = body.substring(0, 150) // 150 ko change karein
```

## 🆘 Troubleshooting

### Problem: "Cannot GET /api/emails"
**Solution**: 
- Server running hai check karein
- `npm run dashboard` command run karein
- Port 3000 free hai check karein

### Problem: "No emails found"
**Solution**:
- Needs_Action folder check karein
- Gmail watcher run karein
- .md files hain ya nahi dekhein

### Problem: "Port already in use"
**Solution**:
- server.js mein PORT change karein
- Ya running process band karein:
  ```cmd
  netstat -ano | findstr :3000
  taskkill /PID <process_id> /F
  ```

### Problem: Dashboard slow hai
**Solution**:
- Zyada emails hain toh Done/ mein move karein
- Browser cache clear karein
- Server restart karein

## 📱 Mobile View

Dashboard mobile-friendly hai:
- Stats 2x2 grid mein
- Search aur filter vertical
- Email cards full width
- Touch-friendly buttons

## 🔐 Security Notes

- Dashboard sirf localhost pe chalti hai
- Bahar se access nahi ho sakti
- Production ke liye authentication add karein
- Sensitive data hide karein

## 🎓 Next Steps

Dashboard ready hai! Ab:

1. ✅ Gmail watcher setup karein
2. ✅ Dashboard chalayein
3. ✅ Emails process karein
4. ⬜ MCP server add karein (Silver Tier)
5. ⬜ Auto-reply feature (Gold Tier)
6. ⬜ Cloud deployment (Platinum Tier)

## 📞 Support

Agar koi problem ho toh:
1. Logs check karein: `Logs/gmail_watcher/`
2. Server output dekhein
3. Browser console check karein (F12)
4. README files padhein

---

**Happy Emailing! 📧✨**
