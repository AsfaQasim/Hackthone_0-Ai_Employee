# Bronze Tier Setup Guide

**Estimated Time**: 8-12 hours  
**Difficulty**: Beginner-Friendly

---

## ✅ What You're Building

A basic AI Employee that:
1. Monitors your Gmail inbox
2. Creates markdown files for important emails
3. Uses Claude Code (me!) to read and process tasks
4. Maintains an Obsidian vault as its "brain"

---

## 📁 Folder Structure

```
your-workspace/
├── Dashboard.md              # Real-time status overview
├── Company_Handbook.md       # Rules and guidelines
├── Inbox/                    # Incoming items (optional)
├── Needs_Action/            # Tasks requiring attention
├── Pending_Approval/        # Actions awaiting approval
├── Approved/                # Approved actions
├── Done/                    # Completed tasks
├── Logs/                    # Activity logs
├── Plans/                   # Multi-step task plans
├── Skills/                  # Agent capabilities
│   ├── gmail_watcher.py     # Gmail monitoring script
│   └── config/              # Configuration files
└── .env                     # Secrets (NEVER commit!)
```

---

## 🚀 Step-by-Step Setup

### Step 1: Install Prerequisites

**Python 3.8+**:
```bash
python --version
```

**Required Python packages**:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pyyaml html2text
```

**Obsidian** (optional but recommended):
- Download from: https://obsidian.md
- Open this folder as a vault

---

### Step 2: Gmail API Setup

1. **Go to Google Cloud Console**: https://console.cloud.google.com
2. **Create a new project** (or use existing)
3. **Enable Gmail API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"
4. **Create OAuth 2.0 Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app"
   - Download the JSON file
5. **Save credentials**:
   - Create folder: `config/`
   - Save downloaded file as: `config/gmail-credentials.json`

---

### Step 3: Configure Gmail Watcher

Edit `Skills/config/gmail_watcher_config.yaml`:

```yaml
# Add your VIP senders
importanceCriteria:
  senderWhitelist:
    - "your-boss@company.com"
    - "important-client@example.com"
  
  keywordPatterns:
    - "urgent"
    - "invoice"
    - "payment"
```

---

### Step 4: Authenticate Gmail

Run the authentication flow:

```bash
python Skills/gmail_watcher.py auth --config Skills/config/gmail_watcher_config.yaml
```

This will:
1. Open your browser
2. Ask you to log in to Gmail
3. Request permissions
4. Save a token to `config/gmail-token.json`

---

### Step 5: Test the Watcher (Dry Run)

Test without making changes:

```bash
python Skills/gmail_watcher.py poll --config Skills/config/gmail_watcher_config.yaml --dry-run
```

You should see:
- Number of unread emails retrieved
- Which emails would be processed
- Where files would be created

---

### Step 6: Run First Real Poll

Process emails for real:

```bash
python Skills/gmail_watcher.py poll --config Skills/config/gmail_watcher_config.yaml
```

Check `Needs_Action/` folder for new markdown files!

---

### Step 7: Start Continuous Monitoring

Run the watcher continuously (polls every 5 minutes):

```bash
python Skills/gmail_watcher.py start --config Skills/config/gmail_watcher_config.yaml
```

**To stop**: Press `Ctrl+C`

---

### Step 8: Use Claude Code to Process Tasks

Now I (Claude Code) can help you process the tasks!

**In your terminal**:
```bash
# Point me at your vault
cd /path/to/your-workspace

# Ask me to check for tasks
# (Just chat with me in Kiro!)
```

**Example prompts**:
- "Check the Needs_Action folder and summarize what needs attention"
- "Read the email task files and draft responses"
- "Update the Dashboard with current status"
- "Create a Plan.md for handling today's emails"

---

## 🎯 Bronze Tier Checklist

- [ ] Obsidian vault created with Dashboard.md and Company_Handbook.md
- [ ] Gmail Watcher installed and configured
- [ ] Gmail API credentials set up
- [ ] Successfully authenticated with Gmail
- [ ] Ran test poll (dry-run)
- [ ] Processed at least one real email
- [ ] Created markdown file in Needs_Action/
- [ ] Used Claude Code to read and process a task
- [ ] Folder structure complete: /Inbox, /Needs_Action, /Done

---

## 🔧 Troubleshooting

### "Module not found" error
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pyyaml html2text
```

### "Credentials file not found"
- Make sure `config/gmail-credentials.json` exists
- Check the path in `gmail_watcher_config.yaml`

### "Authentication failed"
- Delete `config/gmail-token.json`
- Run `python Skills/gmail_watcher.py auth` again

### No emails being processed
- Check your `importanceCriteria` in config
- Make sure you have unread emails matching the criteria
- Try with `--dry-run` to see what's being filtered

---

## 🎓 What You've Learned

✅ How to set up Gmail API access  
✅ How to run a Python watcher script  
✅ How to structure an Obsidian vault for AI  
✅ How to use Claude Code to process tasks  
✅ Basic file-based workflow automation

---

## 🚀 Next Steps (Silver Tier)

Ready to level up? Silver Tier adds:
- Multiple watchers (WhatsApp, LinkedIn)
- Automated reasoning loop (Ralph Loop)
- MCP server for sending emails
- Human-in-the-loop approval workflow
- Scheduled tasks (cron/Task Scheduler)

---

## 📚 Resources

- Gmail API Docs: https://developers.google.com/gmail/api
- Obsidian Help: https://help.obsidian.md
- Python Docs: https://docs.python.org
- Claude Code Guide: https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows

---

**Congratulations on completing Bronze Tier! 🎉**

*You now have a working AI Employee foundation.*
