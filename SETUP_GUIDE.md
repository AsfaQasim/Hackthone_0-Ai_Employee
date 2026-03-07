# 🚀 Setup Guide: Personal AI Employee (Gold Tier)

## Prerequisites

Before starting, ensure you have:

- Windows 10/11, macOS 10.15+, or Linux
- 8GB RAM minimum (16GB recommended)
- 20GB free disk space
- Stable internet connection (10+ Mbps)
- Admin/sudo access for installations

## Required Software

### 1. Python 3.13+

**Windows**:
```cmd
# Download from python.org and install
# Or use winget:
winget install Python.Python.3.13
```

**macOS**:
```bash
brew install python@3.13
```

**Linux**:
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3-pip
```

### 2. Node.js 24+ LTS

**Windows**:
```cmd
# Download from nodejs.org and install
# Or use winget:
winget install OpenJS.NodeJS.LTS
```

**macOS**:
```bash
brew install node@24
```

**Linux**:
```bash
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt install -y nodejs
```

### 3. Git

**Windows**:
```cmd
winget install Git.Git
```

**macOS**:
```bash
brew install git
```

**Linux**:
```bash
sudo apt install git
```


### 4. Obsidian

Download from [obsidian.md](https://obsidian.md/download) and install.

### 5. Claude Code

Sign up at [claude.com](https://claude.com/product/claude-code) and install.

## Installation Steps

### Step 1: Clone Repository

```bash
git clone https://github.com/AsfaQasim/Hackthone_0-AI_Employee.git
cd Hackthone_0-AI_Employee
```

### Step 2: Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Install Node.js Dependencies

```bash
npm install
```

### Step 4: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
# Windows: notepad .env
# macOS/Linux: nano .env
```

Required environment variables:
```
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret
WHATSAPP_SESSION_PATH=.whatsapp_session
LINKEDIN_ACCESS_TOKEN=your_linkedin_token (optional)
```


### Step 5: Gmail Authentication

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download credentials as `config/gmail-credentials.json`
6. Run authentication:

```bash
python Skills/gmail_watcher.py auth
```

7. Click the URL, sign in to Google
8. Click "Advanced" → "Go to [App] (unsafe)" → "Allow"
9. Token saved to `config/gmail-token.json`

### Step 6: WhatsApp Authentication

```bash
python authenticate_whatsapp.py
```

1. Browser window opens with WhatsApp Web
2. Scan QR code with your phone
3. Session saved to `.whatsapp_session/`
4. Close browser when done

### Step 7: LinkedIn Authentication (Optional)

**Option A: API-based** (requires company page):
1. Create LinkedIn app at [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Get access token
3. Add to `.env` file

**Option B: Playwright-based** (recommended):
```bash
python Skills/linkedin_watcher_simple.py auth
```

### Step 8: Open Obsidian Vault

1. Open Obsidian
2. Click "Open folder as vault"
3. Select the project directory
4. Vault opens with Dashboard.md


## Running the System

### Start Watchers

**Gmail Watcher**:
```bash
python Skills/gmail_watcher.py poll
```

**WhatsApp Watcher**:
```bash
python Skills/whatsapp_watcher.py
```

**LinkedIn Watcher**:
```bash
python Skills/linkedin_watcher_simple.py
```

### Start Scheduler (Optional)

For automated daily/weekly tasks:

**Windows**:
```cmd
python setup_scheduler.py
```

**macOS/Linux**:
```bash
# Add to crontab
crontab -e

# Add these lines:
0 8 * * * cd /path/to/project && python Skills/ceo_briefing_generator.py
0 */2 * * * cd /path/to/project && python Skills/gmail_watcher.py poll
```

### Test the System

```bash
# Run verification script
python verify_gold_tier_complete.py

# Run tests
python test_gold_tier.py
```

## Verification

After setup, verify everything works:

1. **Check watchers**: New emails/messages create files in `/Needs_Action/`
2. **Check Obsidian**: Dashboard.md shows current status
3. **Check logs**: `/Logs/` folder contains audit logs
4. **Check MCP servers**: Test email sending with dry-run mode


## Troubleshooting

### Gmail Authentication Issues

**Problem**: "Google hasn't verified this app" warning

**Solution**:
1. Click "Advanced" at bottom of warning
2. Click "Go to [App Name] (unsafe)"
3. Click "Allow" to grant permissions

### WhatsApp Session Expired

**Problem**: WhatsApp watcher fails with "Not logged in"

**Solution**:
```bash
python reconnect_whatsapp.bat
```
Scan QR code again to restore session.

### LinkedIn Authentication Failed

**Problem**: LinkedIn API returns 401 Unauthorized

**Solution**:
Use Playwright-based watcher instead:
```bash
python Skills/linkedin_watcher_simple.py auth
```

### Port Already in Use

**Problem**: MCP server fails to start

**Solution**:
```bash
# Find process using port
# Windows:
netstat -ano | findstr :3000
taskkill /PID <process_id> /F

# macOS/Linux:
lsof -i :3000
kill -9 <process_id>
```

### Disk Space Issues

**Problem**: System runs out of disk space

**Solution**:
1. Clean old logs: `rm -rf Logs/2025-*`
2. Clean browser cache: `rm -rf .whatsapp_session/Cache`
3. Clean Python cache: `find . -type d -name __pycache__ -exec rm -rf {} +`


## Configuration

### Watcher Settings

Edit `Skills/base_watcher.py` to adjust:
- `check_interval`: Polling frequency (default: 60 seconds)
- `max_retries`: Retry attempts on failure (default: 3)
- `timeout`: Request timeout (default: 30 seconds)

### Approval Thresholds

Edit `Skills/approval_workflow.py` to adjust:
- Email auto-approve: Known contacts only
- Payment auto-approve: < $50 recurring
- Social media auto-approve: Scheduled posts only

### Logging Settings

Edit `Skills/audit_logger.py` to adjust:
- `retention_days`: Log retention (default: 90 days)
- `log_level`: DEBUG, INFO, WARNING, ERROR
- `max_log_size`: Maximum log file size (default: 10MB)

## Security Best Practices

1. **Never commit sensitive files**:
   - `.env`
   - `config/gmail-token.json`
   - `config/gmail-credentials.json`
   - `.whatsapp_session/`

2. **Use environment variables** for all credentials

3. **Enable dry-run mode** during testing:
   ```bash
   export DRY_RUN=true
   python Skills/gmail_watcher.py poll
   ```

4. **Rotate credentials monthly**

5. **Review audit logs regularly**

## Next Steps

1. Read `ARCHITECTURE.md` to understand system design
2. Read `LESSONS_LEARNED.md` for insights
3. Customize `Company_Handbook.md` with your rules
4. Test with real data
5. Monitor logs for issues
6. Create CEO briefing schedule

## Support

For issues or questions:
- Check `LESSONS_LEARNED.md` for common problems
- Review logs in `/Logs/` folder
- Check GitHub issues
- Contact: asfaqasim145@gmail.com

## License

MIT License - See LICENSE file for details

---

**Last Updated**: March 4, 2026  
**Version**: Gold Tier v1.0  
**Author**: Asfa Qasim
