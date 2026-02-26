# Obsidian UI Setup Guide

Apne AI Employee ko beautiful UI mein dekho!

---

## 📥 Step 1: Download Obsidian

1. Visit: https://obsidian.md
2. Download for Windows
3. Install karo (simple installer hai)

---

## 📂 Step 2: Open Your Vault

1. Obsidian open karo
2. Click "Open folder as vault"
3. Select: `F:\hackthone_0`
4. Click "Open"

---

## 🎨 Step 3: Explore Your AI Employee

### Dashboard Dekho:
- Left sidebar mein `Dashboard.md` click karo
- Yahan tumhara AI Employee ka status dikhega

### Processed Emails Dekho:
- Left sidebar mein `Needs_Action` folder expand karo
- 23 processed emails dikhenge
- Kisi bhi email pe click karo to full content dikhega

### Company Rules Dekho:
- `Company_Handbook.md` open karo
- Yahan tumhare AI ke rules hain

---

## ✨ Obsidian Features

### Graph View:
- Ctrl+G press karo
- Tumhare saare files ka visual network dikhega
- Connections between files dekh sakte ho

### Search:
- Ctrl+Shift+F
- Kisi bhi email mein search kar sakte ho
- Example: "urgent" search karo to saare urgent emails milenge

### Tags:
- Emails mein priority tags hain: 🔴 🟡 🟢
- Tag pe click karo to similar emails milenge

### File Explorer:
- Left sidebar mein folder structure
- Drag & drop files between folders
- Example: Done folder mein move karo completed tasks

---

## 🎯 Recommended Obsidian Plugins

### Core Plugins (Already Enabled):
- File explorer
- Search
- Graph view
- Backlinks

### Community Plugins (Optional):
1. **Kanban** - Task board view
2. **Calendar** - Date-based view
3. **Dataview** - Query your emails like a database
4. **Excalidraw** - Draw diagrams

To install:
1. Settings > Community plugins
2. Turn off Safe mode
3. Browse and install

---

## 📊 Create Custom Views

### Email Dashboard Query (with Dataview plugin):

```dataview
TABLE 
  sender_name as "From",
  priority as "Priority",
  date as "Date"
FROM "Needs_Action"
WHERE type = "email_task"
SORT priority DESC, date DESC
```

Add this to Dashboard.md to see all emails in a table!

---

## 🎨 Themes

Make it beautiful:

1. Settings > Appearance
2. Click "Manage" under Themes
3. Try: "Minimal", "Things", or "California Coast"

---

## 🚀 Quick Tips

- **Ctrl+P**: Command palette (search any action)
- **Ctrl+O**: Quick file switcher
- **Ctrl+E**: Toggle edit/preview mode
- **Ctrl+,**: Settings

---

## 📱 Mobile App (Bonus)

Obsidian has mobile apps too!
- Download from Play Store / App Store
- Sync using Obsidian Sync (paid) or Git

---

## ✅ You're Ready!

Ab tumhara AI Employee ek beautiful UI mein hai! 🎉
