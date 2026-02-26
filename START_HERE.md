# 👋 START HERE - Your AI Employee Journey

Welcome! You're about to build your own AI Employee. This guide will get you started in the right order.

---

## 🎯 Your Goal: Bronze Tier

Build a basic AI assistant that:
- Monitors your Gmail inbox
- Creates task files for important emails
- Uses Claude Code (AI) to help you process them
- Maintains an organized workspace

**Time**: 8-12 hours  
**Difficulty**: Beginner-friendly

---

## 📚 Read These Files In Order

### 1. **QUICK_START.md** (Start here!)
   - 30-minute quick setup guide
   - Get running fast
   - Minimal explanation, maximum action

### 2. **BRONZE_TIER_SETUP.md** (Detailed guide)
   - Complete step-by-step instructions
   - Troubleshooting tips
   - Full explanations

### 3. **ARCHITECTURE_BRONZE.md** (Understanding)
   - How the system works
   - Visual diagrams
   - Component responsibilities

### 4. **Company_Handbook.md** (Customize)
   - Your AI's rules and guidelines
   - Edit this to match your needs
   - Add your VIP contacts

### 5. **BRONZE_CHECKLIST.md** (Track progress)
   - 60-item checklist
   - Track what's done
   - Ensure nothing is missed

---

## ⚡ Super Quick Start (5 minutes)

If you just want to dive in:

```bash
# 1. Install dependencies
pip install -r Skills/requirements.txt

# 2. Get Gmail credentials
# → Go to: https://console.cloud.google.com
# → Create project → Enable Gmail API → Download credentials
# → Save as: config/gmail-credentials.json

# 3. Authenticate
python Skills/gmail_watcher.py auth

# 4. Test it
python Skills/gmail_watcher.py poll --dry-run

# 5. Run it for real
python Skills/gmail_watcher.py poll
```

Check `Needs_Action/` folder for your first task file!

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `Dashboard.md` | Your AI's status overview |
| `Company_Handbook.md` | Rules and guidelines |
| `Needs_Action/` | Tasks waiting for you |
| `Done/` | Completed tasks |
| `Skills/gmail_watcher.py` | The email monitoring script |
| `config/gmail_watcher_config.yaml` | Customize what emails to watch |

---

## 🎓 Learning Path

### Phase 1: Setup (2-3 hours)
- Install Python dependencies
- Set up Gmail API access
- Authenticate and test

### Phase 2: Configuration (1-2 hours)
- Customize importance criteria
- Add your VIP senders
- Adjust priority rules

### Phase 3: Testing (1-2 hours)
- Run dry-run tests
- Process real emails
- Verify markdown files

### Phase 4: Integration (2-3 hours)
- Use Claude Code to process tasks
- Update Dashboard
- Create workflows

### Phase 5: Refinement (2-4 hours)
- Fine-tune filtering rules
- Optimize polling interval
- Document your setup

---

## 🆘 Need Help?

### Common Issues

**"Module not found"**
```bash
pip install -r Skills/requirements.txt
```

**"Credentials not found"**
- Check `config/gmail-credentials.json` exists
- Download from Google Cloud Console

**"No emails processed"**
- Check `importanceCriteria` in config
- Make sure you have unread emails
- Try `--dry-run` to see filtering

### Where to Look

- **Setup issues**: `BRONZE_TIER_SETUP.md` → Troubleshooting section
- **How it works**: `ARCHITECTURE_BRONZE.md`
- **Configuration**: `Skills/config/gmail_watcher_config.yaml`
- **Logs**: `Logs/gmail_watcher/gmail-watcher.log`

---

## ✅ Success Criteria

You've completed Bronze Tier when:

- ✅ Gmail Watcher is running
- ✅ At least 1 email processed into markdown
- ✅ Dashboard.md and Company_Handbook.md exist
- ✅ Claude Code can read and process tasks
- ✅ Folder structure is complete

---

## 🚀 Next Steps After Bronze

### Silver Tier (20-30 hours)
- Add WhatsApp watcher
- Build MCP server for sending emails
- Implement approval workflow
- Add scheduling

### Gold Tier (40+ hours)
- Integrate accounting (Odoo)
- Add social media watchers
- Weekly CEO briefing
- Multi-step task automation

### Platinum Tier (60+ hours)
- Deploy to cloud (24/7)
- Agent-to-agent communication
- Production monitoring
- Full autonomous operation

---

## 📖 Additional Resources

- **Gmail API Docs**: https://developers.google.com/gmail/api
- **Obsidian**: https://obsidian.md
- **Claude Code Guide**: https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows
- **Python Tutorial**: https://docs.python.org/3/tutorial/

---

## 🎬 Ready to Start?

1. **Read**: `QUICK_START.md`
2. **Run**: `pip install -r Skills/requirements.txt`
3. **Setup**: Gmail API credentials
4. **Test**: `python Skills/gmail_watcher.py poll --dry-run`
5. **Go**: `python Skills/gmail_watcher.py start`

---

**Let's build your AI Employee! 🚀**

*Questions? Ask Claude Code (me!) for help anytime.*
