# Bronze Tier - Live Testing Guide

Yeh simple steps follow karo to verify karo ke sab kuch working hai:

---

## ✅ Step 1: Check Python Installation

```bash
python --version
```

**Expected**: Python 3.8 ya usse upar  
**Your System**: Python 3.12.0 ✅

---

## ✅ Step 2: Check Gmail Watcher Dependencies

```bash
pip list | findstr google
```

**Expected**: Yeh packages dikhne chahiye:
- google-auth
- google-auth-oauthlib
- google-api-python-client

---

## ✅ Step 3: Verify Gmail Authentication

```bash
dir config\gmail-token.json
```

**Expected**: File exist karni chahiye (782 bytes)  
**Your System**: ✅ File exists!

---

## ✅ Step 4: Test Gmail Watcher (Dry Run)

```bash
python Skills/gmail_watcher.py poll --dry-run
```

**Expected Output**:
```
[INFO] Loaded processed index with X entries
[INFO] Successfully authenticated with Gmail API
[INFO] Retrieved X unread emails
[INFO] Polling cycle completed
```

**Kya hoga**: Yeh tumhare Gmail ko check karega WITHOUT koi file banaye

---

## ✅ Step 5: Check Processed Emails

```bash
dir Needs_Action\*.md
```

**Expected**: Markdown files dikhni chahiye  
**Your System**: ✅ 23 files already processed!

---

## ✅ Step 6: Read One Email Task

```bash
type Needs_Action\20260217_181027_update-on-the-frontend-software-e*.md
```

**Expected**: Email content markdown format mein dikhe with:
- Frontmatter (metadata)
- Email subject
- Sender info
- Body content
- Action items

---

## ✅ Step 7: Check Processing Index

```bash
type .index\gmail-watcher-processed.json
```

**Expected**: JSON file with processed email IDs  
**Your System**: ✅ 4,425 bytes of tracking data

---

## ✅ Step 8: Run TypeScript Tests

```bash
npm test
```

**Expected**: Tests pass honi chahiye  
**Your System**: ✅ 227 tests passing!

---

## ✅ Step 9: Start Live Monitoring (Optional)

```bash
python Skills/gmail_watcher.py start
```

**Kya hoga**:
- Har 5 minutes mein Gmail check karega
- Naye important emails ke liye markdown files banayega
- Logs mein activity record karega
- Press Ctrl+C to stop

**Warning**: Yeh continuously run hoga, testing ke liye mat chalaao!

---

## ✅ Step 10: Process One Real Email

```bash
python Skills/gmail_watcher.py poll
```

**Kya hoga**:
- Gmail check karega
- Agar koi naya important email hai to markdown file banayega
- Results show karega

**Expected Output**:
```
Poll Results:
  Retrieved: X
  Processed: X
  Filtered: X
  Created: X
  Errors: 0
```

---

## 🎯 Quick Verification Checklist

Run these commands one by one:

```bash
# 1. Python check
python --version

# 2. Files exist check
dir config\gmail-credentials.json
dir config\gmail-token.json

# 3. Processed emails check
dir Needs_Action | find /c ".md"

# 4. Dry run test
python Skills/gmail_watcher.py poll --dry-run

# 5. TypeScript tests
npm test
```

---

## 🚨 Troubleshooting

### Agar "Module not found" error aaye:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pyyaml html2text
```

### Agar "Authentication failed" aaye:
```bash
# Token delete karo aur phir se authenticate karo
del config\gmail-token.json
python Skills/gmail_watcher.py auth
```

### Agar koi email process nahi ho rahi:
```bash
# Config check karo
type Skills\config\gmail_watcher_config.yaml
```

---

## ✅ Success Indicators

Tumhara Bronze Tier ready hai agar:

1. ✅ Python 3.8+ installed
2. ✅ Gmail credentials file exists
3. ✅ Gmail token file exists  
4. ✅ At least 1 email processed in Needs_Action/
5. ✅ Dry run works without errors
6. ✅ TypeScript tests passing
7. ✅ Dashboard.md exists
8. ✅ Company_Handbook.md exists

**Your Status**: ALL ✅ COMPLETE!

---

## 🎬 Demo Video Steps

Agar demo banana hai to yeh record karo:

1. Terminal open karo
2. Run: `python Skills/gmail_watcher.py poll --dry-run`
3. Show: Needs_Action folder with files
4. Open: One markdown file to show email content
5. Run: `npm test` to show tests passing
6. Show: Dashboard.md in Obsidian/editor

---

## 🚀 Next: Use Your AI Employee!

Ab tum mujhse (Claude Code) keh sakte ho:

- "Needs_Action folder ke emails summarize karo"
- "Dashboard update karo with current status"
- "Sabse important email konsi hai?"
- "Draft a response for the urgent email"

Try it now! 🎉
