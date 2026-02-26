# 📊 AI Employee Dashboard

Aapke Bronze Tier emails ko UI mein dekhne ke liye dashboard.

## 🚀 Kaise Chalayein

### 1. Dependencies Install Karein
```cmd
npm install
```

### 2. Dashboard Server Start Karein
```cmd
npm run dashboard
```

### 3. Browser Mein Kholein
```
http://localhost:3000
```

## ✨ Features

- ✅ Saare Needs_Action emails ek jagah
- ✅ Priority ke saath color coding (High/Medium/Low)
- ✅ Search functionality
- ✅ Priority filter
- ✅ Real-time stats
- ✅ Responsive design (mobile friendly)
- ✅ Auto-refresh button

## 📱 Screenshot

Dashboard mein aapko dikhega:
- Total tasks count
- Priority-wise breakdown
- Search box
- Filter dropdown
- Email cards with:
  - Subject
  - Sender
  - Date
  - Priority badge
  - Preview text

## 🎨 Customization

### Colors Change Karna
`ui/styles.css` file edit karein:
```css
.priority-high {
    background: #fee;
    color: #e74c3c;
}
```

### Port Change Karna
`server.js` file mein:
```javascript
const PORT = 3000; // Yahan apna port number daalein
```

## 🔄 Auto-Refresh

Dashboard automatically refresh nahi hota. Refresh button click karein ya page reload karein.

## 📝 Notes

- Server ko running rehna chahiye dashboard dekhne ke liye
- Needs_Action folder mein jo bhi .md files hongi wo show hongi
- Email click karne se wo file open hogi

## 🆘 Troubleshooting

**"Cannot GET /api/emails"**
- Server running hai ya nahi check karein
- `npm run dashboard` command run karein

**"No emails found"**
- Needs_Action folder mein emails hain ya nahi check karein
- Gmail watcher run karein: `python Skills/gmail_watcher.py poll`

**Port already in use**
- server.js mein PORT number change karein
- Ya running process ko band karein

## 🎯 Next Steps

Dashboard ready hai! Ab aap:
1. Gmail watcher chalayein
2. Dashboard refresh karein
3. Emails process karein
4. Done folder mein move karein
