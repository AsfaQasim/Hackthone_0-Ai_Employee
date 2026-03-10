# LinkedIn MCP Server Integration Guide

Complete guide for integrating the LinkedIn MCP Server with Playwright for automated posting.

## Overview

This integration uses the [LinkedIn MCP Server](https://github.com/stickerdaniel/linkedin-mcp-server) with Playwright browser automation to enable automated LinkedIn posting. The system uses persistent browser profiles to maintain authenticated sessions.

## Features

- ✅ **Automated Posting**: Post to LinkedIn automatically using AI-generated content
- ✅ **Persistent Sessions**: Browser profiles saved for reuse (no repeated logins)
- ✅ **Playwright Automation**: Uses Patchright (Playwright fork) for reliable browser automation
- ✅ **AI Content Generation**: Integrates with agent_skills for post generation
- ✅ **Post Tracking**: All posts tracked in Social_Media_Tracking directory
- ✅ **Batch File Support**: Windows batch files for easy command-line usage

## Quick Start

### 1. Install Dependencies

Dependencies are already installed. If you need to reinstall:

```bash
pip install linkedin-scraper-mcp patchright playwright
patchright install chromium
```

### 2. Authenticate with LinkedIn

**First-time setup required!**

Run the authentication script:

```bash
# Using Python
python linkedin_mcp_auth.py

# Or using batch file
linkedin_mcp_auth.bat
```

This will:
1. Open a browser window
2. Allow you to log in to LinkedIn (complete 2FA/captcha if needed)
3. Save your session to `~/.linkedin-mcp/profile/`

⚠️ **Important**: You have 5 minutes to complete login. LinkedIn may require mobile app confirmation.

### 3. Post to LinkedIn

```bash
# Using Python
python linkedin_mcp_auto_post.py "Your post topic"

# Using batch file
linkedin_mcp_auto_post.bat "Your post topic"

# With style options
python linkedin_mcp_auto_post.py "New project launch!" --style enthusiastic

# Headless mode (no browser GUI)
python linkedin_mcp_auto_post.py "Industry insights" --headless
```

## Usage Examples

### Basic Post

```bash
python linkedin_mcp_auto_post.py "Just completed an amazing AI automation project! #AI #Automation"
```

### Professional Style

```bash
python linkedin_mcp_auto_post.py "Excited to announce our new product launch" --style professional
```

### Casual Style

```bash
python linkedin_mcp_auto_post.py "Team celebration today! Great work everyone" --style casual
```

### Enthusiastic Style

```bash
python linkedin_mcp_auto_post.py "We hit 10K users! Thank you all for the support!" --style enthusiastic
```

### Debug Mode (Visible Browser)

```bash
python linkedin_mcp_auto_post.py "Debug post" --slow-mo 1000
```

## Configuration

### Environment Variables

Add to your `.env` file:

```bash
# LinkedIn MCP Configuration
LINKEDIN_MCP_PROFILE_PATH=~/.linkedin-mcp/profile
LINKEDIN_BROWSER_TIMEOUT=60000
LINKEDIN_BROWSER_HEADLESS=false
LINKEDIN_BROWSER_SLOW_MO=0
```

### Profile Location

- **Windows**: `C:\Users\<YourUsername>\.linkedin-mcp\profile\`
- **Linux/Mac**: `~/.linkedin-mcp/profile/`

## Session Management

### Check Session Status

```bash
python linkedin_mcp_auth.py --status
```

### Logout (Clear Profile)

```bash
python linkedin_mcp_auth.py --logout
```

### Re-authenticate

If your session expires:

```bash
python linkedin_mcp_auth.py
```

## Programmatic Usage

Use in your Python code:

```python
from linkedin_mcp_auto_post import LinkedInMCPAutoPoster

# Initialize poster
poster = LinkedInMCPAutoPoster()

# Generate and post content
content = poster.generate_post_content("AI automation", style="professional")
success = poster.post(content)

if success:
    print("Post published!")
else:
    print("Posting failed")
```

### Custom Profile Path

```python
poster = LinkedInMCPAutoPoster(profile_path="C:/custom/profile/path")
```

## Post Tracking

All posts are tracked in the `Social_Media_Tracking/` directory:

```
Social_Media_Tracking/
├── linkedin_20260310_143022_mcp.md
├── linkedin_20260310_150145_mcp.md
└── ...
```

Each tracking file contains:
- Post content
- Timestamp
- Status (posted/failed)
- Method used
- Error details (if failed)

## Troubleshooting

### "Not logged in" Error

**Solution**: Re-authenticate

```bash
python linkedin_mcp_auth.py
```

### Browser Timeout

**Solution**: Increase timeout or check internet connection

```bash
# Set environment variable
set LINKEDIN_BROWSER_TIMEOUT=120000

# Or use in code
poster = LinkedInMCPAutoPoster()
# Timeout is configurable in the post() method
```

### Captcha Challenges

LinkedIn may show captcha for automated access:

1. Run authentication again
2. Complete the captcha manually
3. Session will be saved for future use

### Session Expires

Sessions may expire after some time:

```bash
# Check status
python linkedin_mcp_auth.py --status

# Re-authenticate if needed
python linkedin_mcp_auth.py
```

### Post Editor Not Found

LinkedIn UI may have changed:

1. Update the script with new selectors
2. Use visible mode for debugging:
   ```bash
   python linkedin_mcp_auto_post.py "test" --slow-mo 1000
   ```

## MCP Server Command-Line Options

Direct MCP server usage:

```bash
# Login
python -m linkedin_mcp_server --login

# Check status
python -m linkedin_mcp_server --status

# Logout
python -m linkedin_mcp_server --logout

# Custom profile
python -m linkedin_mcp_server --login --user-data-dir "C:/custom/profile"

# Debug mode (visible browser)
python -m linkedin_mcp_server --login --no-headless

# Custom timeout
python -m linkedin_mcp_server --timeout 15000
```

## Integration with Other Tools

### MCP Client Configuration

Add to your MCP client config (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "python",
      "args": ["-m", "linkedin_mcp_server"]
    }
  }
}
```

### Scheduler Integration

Use with Windows Task Scheduler:

```batch
@echo off
cd /d "F:\hackthone_0"
python linkedin_mcp_auto_post.py "Scheduled post content" --headless
```

## API vs MCP Server

This project uses the **MCP Server** approach (browser automation) instead of the official LinkedIn API because:

| Feature | MCP Server | Official API |
|---------|-----------|--------------|
| Personal Profiles | ✅ Yes | ❌ Limited |
| Company Pages | ✅ Yes | ✅ Yes |
| Setup Complexity | ⚠️ Medium | ❌ High |
| Rate Limits | ⚠️ Browser-based | ✅ Defined |
| Cost | ✅ Free | ✅ Free (basic) |
| 2FA Support | ✅ Yes | ❌ Complex |

## Best Practices

1. **Don't spam**: Post 1-3 times per day maximum
2. **Use persistent sessions**: Authenticate once, reuse profile
3. **Monitor posts**: Check tracking files for success/failure
4. **Handle errors**: Always check return codes
5. **Respect LinkedIn ToS**: Use responsibly and ethically

## Security Notes

⚠️ **Important Security Considerations**:

1. **Profile Protection**: The browser profile contains your LinkedIn session. Keep it secure!
2. **No Sharing**: Never share your `~/.linkedin-mcp/profile/` directory
3. **Access Control**: Ensure file permissions restrict access to your profile
4. **Terms of Service**: Using automation tools may violate LinkedIn's Terms of Service. Use at your own risk.

## Advanced Usage

### Custom User Agent

```python
from patchright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        profile_path,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
```

### Custom Viewport

```python
browser = p.chromium.launch_persistent_context(
    profile_path,
    viewport={'width': 1920, 'height': 1080}
)
```

### Proxy Support

```python
browser = p.chromium.launch_persistent_context(
    profile_path,
    proxy={
        "server": "http://proxy.example.com:8080",
        "username": "user",
        "password": "pass"
    }
)
```

## File Structure

```
F:\hackthone_0\
├── linkedin_mcp_auth.py          # Authentication script
├── linkedin_mcp_auto_post.py     # Auto-posting script
├── linkedin_mcp_auth.bat         # Windows auth batch file
├── linkedin_mcp_auto_post.bat    # Windows post batch file
├── LINKEDIN_MCP_INTEGRATION.md   # This documentation
├── .env.example                  # Environment template
└── Social_Media_Tracking/        # Post tracking directory
    └── linkedin_*.md             # Post tracking files
```

## Related Files

- `linkedin_auto_post_playwright.py` - Original Playwright poster
- `Skills/linkedin_watcher_simple.py` - LinkedIn watcher utility
- `get_linkedin_access_token.py` - Official API token helper

## Support

For issues with the LinkedIn MCP Server:
- GitHub: https://github.com/stickerdaniel/linkedin-mcp-server
- Documentation: https://github.com/stickerdaniel/linkedin-mcp-server#readme

For issues with this integration:
- Check the troubleshooting section above
- Review error messages in the console
- Check tracking files in `Social_Media_Tracking/`

## License

This integration follows the Apache 2.0 license of the LinkedIn MCP Server.

---

**Last Updated**: March 10, 2026  
**Version**: 1.0.0
