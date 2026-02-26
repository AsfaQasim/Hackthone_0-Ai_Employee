# 🚀 Quick Start - Bronze Tier

Get your AI Employee running in 30 minutes!

---

## ⚡ Super Quick Setup

### 1. Run Setup Script

**Windows**:
```cmd
setup-bronze.bat
```

**Mac/Linux**:
```bash
chmod +x setup-bronze.sh
./setup-bronze.sh
```

### 2. Get Gmail Credentials

1. Go to: https://console.cloud.google.com
2. Create project → Enable Gmail API
3. Create OAuth credentials (Desktop app)
4. Download JSON → Save as `config/gmail-credentials.json`

### 3. Authenticate

```bash
python Skills/gmail_watcher.py auth
```

### 4. Test It

```bash
# Dry run (safe test)
python Skills/gmail_watcher.py poll --dry-run

# Real run (creates files)
python Skills/gmail_watcher.py poll
```

### 5. Start Monitoring

```bash
# Continuous monitoring (every 5 min)
python Skills/gmail_watcher.py start
```

---

## 🎯 What Happens?

1. **Watcher checks Gmail** every 5 minutes
2. **Finds important emails** (based on your rules)
3. **Creates markdown files** in `Needs_Action/`
4. **You (or Claude Code) process them**
5. **Move to Done/** when complete

---

## 💬 Using Claude Code (Me!)

Once emails are in `Needs_Action/`, ask me:

```
"Check Needs_Action folder and summarize tasks"
"Draft a reply to the email from [sender]"
"Update Dashboard.md with current status"
"Create a plan for handling today's emails"
```

---

## 📝 Customize Your Rules

Edit `Skills/config/gmail_watcher_config.yaml`:

```yaml
importanceCriteria:
  senderWhitelist:
    - "your-boss@company.com"  # Add VIP emails
  
  keywordPatterns:
    - "urgent"
    - "invoice"  # Add keywords to watch
```

---

## 🎉 Bronze Tier Complete When:

- ✅ Gmail Watcher running
- ✅ At least 1 email processed
- ✅ Markdown file created in Needs_Action/
- ✅ Dashboard.md and Company_Handbook.md exist
- ✅ Folder structure complete

---

## 🆘 Quick Troubleshooting

**"Module not found"**:
```bash
pip install google-auth google-auth-oauthlib google-api-python-client pyyaml html2text
```

**"No credentials"**:
- Check `config/gmail-credentials.json` exists
- Re-download from Google Cloud Console

**"No emails processed"**:
- Check you have unread emails
- Adjust `importanceCriteria` in config
- Try `--dry-run` to see what's filtered

---

## 📚 Full Documentation

- **Complete Guide**: `BRONZE_TIER_SETUP.md`
- **Rules & Guidelines**: `Company_Handbook.md`
- **Status Overview**: `Dashboard.md`

---

**Ready? Run the setup script and let's go! 🚀**
