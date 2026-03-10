# LinkedIn MCP Auto-Poster - Quick Start Guide

## 🚀 Setup Complete!

The LinkedIn MCP Server with Playwright automation has been successfully integrated into your project.

## 📋 What Was Installed

### Packages
- ✅ `linkedin-scraper-mcp` (4.3.0) - LinkedIn MCP Server
- ✅ `patchright` (1.58.2) - Playwright fork for browser automation
- ✅ `playwright` (1.58.0) - Browser automation

### Scripts Created
- ✅ `linkedin_mcp_auth.py` - Authentication manager
- ✅ `linkedin_mcp_auto_post.py` - Auto-posting with AI content
- ✅ `linkedin_mcp_auth.bat` - Windows authentication shortcut
- ✅ `linkedin_mcp_auto_post.bat` - Windows posting shortcut
- ✅ `test_linkedin_mcp_integration.py` - Installation tester

### Documentation
- ✅ `LINKEDIN_MCP_INTEGRATION.md` - Complete integration guide

## ⚡ Quick Start (3 Steps)

### Step 1: Authenticate with LinkedIn (First Time Only)

Run the authentication script to create a persistent browser session:

```bash
# Option A: Using Python
python linkedin_mcp_auth.py

# Option B: Using batch file
linkedin_mcp_auth.bat
```

**What happens:**
- A browser window will open
- Log in to LinkedIn (complete 2FA/captcha if needed)
- Your session is saved to `~/.linkedin-mcp/profile/`
- You have 5 minutes to complete login

### Step 2: Post to LinkedIn

```bash
# Option A: Using Python
python linkedin_mcp_auto_post.py "Your post topic"

# Option B: Using batch file
linkedin_mcp_auto_post.bat "Your post topic"
```

**Examples:**

```bash
# Professional post
python linkedin_mcp_auto_post.py "Excited to announce our new AI automation project!"

# Casual post
python linkedin_mcp_auto_post.py "Team lunch celebration! 🎉" --style casual

# Enthusiastic post
python linkedin_mcp_auto_post.py "We hit 10K users! Thank you all!" --style enthusiastic

# Headless mode (no browser GUI)
python linkedin_mcp_auto_post.py "Industry insights" --headless
```

### Step 3: Check Your Post

- View on LinkedIn: https://www.linkedin.com/feed/
- Check tracking files: `Social_Media_Tracking/linkedin_*.md`

## 🔧 Common Commands

### Authentication
```bash
# Authenticate
python linkedin_mcp_auth.py

# Check session status
python linkedin_mcp_auth.py --status

# Logout (clear profile)
python linkedin_mcp_auth.py --logout
```

### Posting
```bash
# Post with different styles
python linkedin_mcp_auto_post.py "Topic" --style professional
python linkedin_mcp_auto_post.py "Topic" --style casual
python linkedin_mcp_auto_post.py "Topic" --style enthusiastic

# Debug mode (slow, visible browser)
python linkedin_mcp_auto_post.py "Topic" --slow-mo 1000

# Headless mode (automated, no GUI)
python linkedin_mcp_auto_post.py "Topic" --headless
```

### Testing
```bash
# Check installation
python test_linkedin_mcp_integration.py

# Check session status
python test_linkedin_mcp_integration.py --session
```

## 📁 File Locations

### Profile Storage
- **Windows**: `C:\Users\<YourUsername>\.linkedin-mcp\profile\`
- **Linux/Mac**: `~/.linkedin-mcp/profile/`

### Post Tracking
- **Location**: `F:\hackthone_0\Social_Media_Tracking\`
- **Format**: `linkedin_YYYYMMDD_HHMMSS_mcp.md`

## 🐛 Troubleshooting

### "Not logged in" Error
```bash
# Solution: Re-authenticate
python linkedin_mcp_auth.py
```

### Session Expired
```bash
# Check status
python linkedin_mcp_auth.py --status

# Re-authenticate if needed
python linkedin_mcp_auth.py
```

### Browser Timeout
```bash
# Increase timeout (in script or environment)
set LINKEDIN_BROWSER_TIMEOUT=120000
```

### Captcha Challenges
1. Run authentication again
2. Complete the captcha manually in the browser
3. Session will be saved for future use

## 🔐 Security Notes

⚠️ **Important:**
- Your browser profile contains your LinkedIn session - keep it secure!
- Never share your `~/.linkedin-mcp/profile/` directory
- Automation may violate LinkedIn's Terms of Service - use at your own risk
- Use responsibly (1-3 posts per day maximum)

## 📖 Full Documentation

For complete documentation, see:
- **Integration Guide**: `LINKEDIN_MCP_INTEGRATION.md`
- **MCP Server Docs**: https://github.com/stickerdaniel/linkedin-mcp-server

## 💡 Usage in Python Code

```python
from linkedin_mcp_auto_post import LinkedInMCPAutoPoster

# Initialize
poster = LinkedInMCPAutoPoster()

# Generate content
content = poster.generate_post_content("AI automation", style="professional")

# Post
success = poster.post(content)

if success:
    print("✅ Post published!")
else:
    print("❌ Posting failed")
```

## ✅ Verification Checklist

- [ ] Packages installed (`pip list | findstr linkedin`)
- [ ] Authentication completed (`python linkedin_mcp_auth.py`)
- [ ] Session valid (`python linkedin_mcp_auth.py --status`)
- [ ] Test post successful
- [ ] Post visible on LinkedIn
- [ ] Tracking file created

## 🎯 Next Steps

1. **Authenticate**: Run `linkedin_mcp_auth.bat`
2. **Test Post**: Try a simple test post
3. **Integrate**: Add to your automation workflows
4. **Schedule**: Set up automated posting (Windows Task Scheduler)

---

**Need Help?**
- Run: `python test_linkedin_mcp_integration.py`
- Check: `LINKEDIN_MCP_INTEGRATION.md`
- Review error messages in console

**Last Updated**: March 10, 2026
**Version**: 1.0.0
