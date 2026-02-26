# Gmail Watcher - Python Implementation

Python implementation of the Gmail Watcher Agent Skill with logging, retry logic, and dry-run mode.

## Features

- **OAuth 2.0 Authentication**: Secure Gmail API access
- **Exponential Backoff Retry**: Automatic retry with exponential backoff (up to 7 attempts)
- **Rate Limiting**: Respects Gmail API quotas (60 requests/minute)
- **Comprehensive Logging**: JSON audit trail + human-readable console output
- **Dry Run Mode**: Test without making any changes
- **Duplicate Prevention**: Tracks processed emails to avoid duplicates
- **Priority Detection**: Automatically assigns high/medium/low priority
- **HTML to Markdown**: Converts email HTML to clean markdown
- **Configurable Filters**: YAML-based importance criteria and priority rules

## Installation

### 1. Install Python Dependencies

```bash
pip install -r Skills/requirements.txt
```

### 2. Set Up Gmail API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials as `config/gmail-credentials.json`

### 3. Configure the Watcher

Edit `Skills/config/gmail_watcher_config.yaml` to customize:
- Polling interval
- Importance criteria (senders, keywords, labels)
- Priority rules
- Folder paths

## Usage

### Authenticate (First Time)

```bash
python Skills/gmail_watcher.py auth --config Skills/config/gmail_watcher_config.yaml
```

This will open a browser for OAuth authorization. After approval, a token is saved to `config/gmail-token.json`.

### Run Single Poll (Dry Run)

Test without making changes:

```bash
python Skills/gmail_watcher.py poll --config Skills/config/gmail_watcher_config.yaml --dry-run
```

### Run Single Poll (Live)

Process emails once:

```bash
python Skills/gmail_watcher.py poll --config Skills/config/gmail_watcher_config.yaml
```

### Start Continuous Polling

Run continuously with configured interval:

```bash
python Skills/gmail_watcher.py start --config Skills/config/gmail_watcher_config.yaml
```

Press `Ctrl+C` to stop.

## Configuration

### Importance Criteria

Emails must match at least one criterion (OR logic) to be processed:

```yaml
importanceCriteria:
  senderWhitelist:
    - "boss@company.com"
  keywordPatterns:
    - "urgent"
    - "action required"
  requiredLabels:
    - "IMPORTANT"
    - "STARRED"
  logicMode: "OR"  # OR or AND
```

### Priority Rules

Priority is assigned based on keywords, senders, and labels:

```yaml
priorityRules:
  highPriorityKeywords:
    - "urgent"
    - "asap"
    - "critical"
  vipSenders:
    - "ceo@company.com"
  highPriorityLabels:
    - "IMPORTANT"
  mediumPriorityKeywords:
    - "follow up"
    - "deadline"
```

### Rate Limiting

Prevents exceeding Gmail API quotas:

```yaml
rateLimitConfig:
  maxRequestsPerMinute: 60
  initialBackoffMs: 1000
  maxBackoffMs: 60000
  backoffMultiplier: 2
```

## Logging

### Log Files

Logs are written to `Logs/gmail_watcher/gmail-watcher.log` in JSON format:

```json
{"timestamp":"2026-02-14T09:35:00Z","level":"INFO","message":"Polling cycle initiated"}
{"timestamp":"2026-02-14T09:35:01Z","level":"INFO","message":"Retrieved 3 unread emails"}
{"timestamp":"2026-02-14T09:35:02Z","level":"INFO","message":"Important email detected: Q1 Report Review Needed (Priority: high)"}
{"timestamp":"2026-02-14T09:35:03Z","level":"INFO","message":"Created markdown file: Needs_Action/20260214_093500_q1-report-review-needed.md"}
```

### Console Output

Human-readable output is also printed to console:

```
[INFO] Polling cycle initiated
[INFO] Retrieved 3 unread emails
[INFO] Important email detected: Q1 Report Review Needed (Priority: high)
[INFO] Created markdown file: Needs_Action/20260214_093500_q1-report-review-needed.md
[INFO] Polling cycle completed in 2.34s: {'retrieved': 3, 'processed': 1, 'filtered': 2, 'created': 1, 'errors': 0}
```

## Retry Logic

The implementation includes robust retry logic with exponential backoff:

- **Initial backoff**: 1 second
- **Max backoff**: 60 seconds
- **Multiplier**: 2x per retry
- **Max attempts**: 7

Retry sequence: 1s → 2s → 4s → 8s → 16s → 32s → 60s

### Retry Behavior

- **4xx errors** (except 429): No retry, log and skip
- **429 (rate limit)**: Retry with backoff
- **5xx errors**: Retry with backoff
- **Network errors**: Retry with backoff

## Dry Run Mode

Use `--dry-run` to test without making changes:

```bash
python Skills/gmail_watcher.py poll --dry-run
```

In dry-run mode:
- ✓ Authenticates with Gmail
- ✓ Fetches emails
- ✓ Filters and prioritizes
- ✗ Does NOT create markdown files
- ✗ Does NOT update processed index
- ✗ Does NOT mark emails as read

All actions are logged with `[DRY RUN]` prefix.

## Output Format

### Markdown Files

Created in `Needs_Action/` folder:

```markdown
---
email_id: "18d4f2a3b5c6e7f8"
sender: "John Doe <john@example.com>"
sender_email: "john@example.com"
sender_name: "John Doe"
subject: "Q1 Report Review Needed"
date: "Thu, 14 Feb 2026 09:30:00 -0800"
priority: "high"
labels: ["INBOX", "IMPORTANT"]
processed_at: "2026-02-14T09:35:00Z"
source: "gmail"
type: "email_task"
status: "pending"
---

# Email: Q1 Report Review Needed

**From**: John Doe <john@example.com>  
**Date**: Thu, 14 Feb 2026 09:30:00 -0800  
**Priority**: 🔴 High  
**Labels**: INBOX, IMPORTANT

## Email Content

Hi there,

Could you please review the Q1 report by end of week? 
Let me know if you have any questions.

Thanks,
John

---

## Action Items

- [ ] Review and respond to this email

## Links

- [View in Gmail](https://mail.google.com/mail/u/0/#inbox/18d4f2a3b5c6e7f8)

---

*Processed by Gmail Watcher Skill v1.0.0*
```

### Processed Index

Tracks processed emails in `.index/gmail-watcher-processed.json`:

```json
{
  "18d4f2a3b5c6e7f8": {
    "filename": "20260214_093500_q1-report-review-needed.md",
    "processedAt": "2026-02-14T09:35:00Z",
    "priority": "high"
  }
}
```

## Error Handling

### Authentication Errors

```
[ERROR] Authentication failed: invalid_grant
```

**Solution**: Delete `config/gmail-token.json` and re-authenticate:

```bash
python Skills/gmail_watcher.py auth
```

### Rate Limit Errors

```
[WARN] Rate limit reached, sleeping for 45.2s
```

**Solution**: Automatic - waits and retries. Adjust `maxRequestsPerMinute` in config if needed.

### Network Errors

```
[WARN] Request failed (attempt 1/7), retrying in 1.0s: Connection timeout
```

**Solution**: Automatic retry with exponential backoff.

### File System Errors

```
[ERROR] Failed to create markdown file: Permission denied
```

**Solution**: Check folder permissions for `Needs_Action/` and `Logs/`.

## Troubleshooting

### No Emails Detected

1. Check importance criteria in config
2. Verify emails match criteria (sender, keywords, labels)
3. Run with `--dry-run` to see filtering logic
4. Check logs: `tail -f Logs/gmail_watcher/gmail-watcher.log`

### Duplicate Files Created

1. Check index file: `cat .index/gmail-watcher-processed.json`
2. Verify index is being saved (check logs)
3. Ensure only one instance is running

### Authentication Issues

1. Verify `config/gmail-credentials.json` exists
2. Check credentials are for Desktop app (not Web app)
3. Ensure Gmail API is enabled in Google Cloud Console
4. Delete token and re-authenticate: `rm config/gmail-token.json`

## Performance

### Metrics

- **Polling interval**: 5 minutes (configurable)
- **Processing time**: ~2-5 seconds per email
- **API calls**: ~2-3 per email (list, get, modify)
- **Memory usage**: ~50-100 MB
- **CPU usage**: <5% average

### Optimization Tips

1. **Increase polling interval** for less frequent checks
2. **Reduce max emails per poll** to process fewer at once
3. **Use more specific filters** to reduce processing
4. **Disable mark-as-read** to save API calls

## Security

### OAuth 2.0

- No password storage
- Credentials stored locally only
- Token auto-refresh
- Scopes: `gmail.readonly`, `gmail.modify`

### Data Privacy

- All email content stays local
- No external services or cloud storage
- User controls all data
- Easy to delete or export

### Sensitive Data

- Tokens stored in `config/gmail-token.json`
- Keep this file secure (add to `.gitignore`)
- Never commit credentials to version control

## Scheduling

### Linux/Mac (cron)

Run every 5 minutes:

```bash
*/5 * * * * cd /path/to/workspace && python Skills/gmail_watcher.py poll --config Skills/config/gmail_watcher_config.yaml
```

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily, repeat every 5 minutes
4. Action: Start a program
5. Program: `python`
6. Arguments: `Skills/gmail_watcher.py poll --config Skills/config/gmail_watcher_config.yaml`
7. Start in: `C:\path\to\workspace`

### Systemd Service (Linux)

Create `/etc/systemd/system/gmail-watcher.service`:

```ini
[Unit]
Description=Gmail Watcher Agent Skill
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/workspace
ExecStart=/usr/bin/python3 Skills/gmail_watcher.py start --config Skills/config/gmail_watcher_config.yaml
Restart=on-failure
RestartSec=60

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable gmail-watcher
sudo systemctl start gmail-watcher
sudo systemctl status gmail-watcher
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=Skills --cov-report=html
```

### Code Structure

```
Skills/
├── gmail_watcher.py          # Main implementation
├── gmail_watcher.md          # Skill documentation
├── config/
│   └── gmail_watcher_config.yaml  # Configuration
├── requirements.txt          # Python dependencies
└── README_PYTHON.md         # This file
```

### Key Classes

- `GmailWatcher`: Main orchestrator
- `EmailMetadata`: Email data structure
- `Priority`: Priority enum (HIGH, MEDIUM, LOW)
- `GmailWatcherConfig`: Configuration data class

### Key Methods

- `authenticate()`: OAuth 2.0 flow
- `fetch_unread_emails()`: Get email IDs
- `get_email_content()`: Fetch full email
- `is_important()`: Filter by criteria
- `detect_priority()`: Assign priority
- `generate_markdown()`: Create markdown
- `poll_once()`: Single poll cycle
- `start_polling()`: Continuous polling

## License

See main project LICENSE file.

## Support

For issues or questions:
1. Check logs: `Logs/gmail_watcher/gmail-watcher.log`
2. Run with `--dry-run` to debug
3. Review configuration: `Skills/config/gmail_watcher_config.yaml`
4. Check Gmail API quotas in Google Cloud Console

## Version History

- **1.0.0** (2026-02-15): Initial Python implementation
  - OAuth 2.0 authentication
  - Exponential backoff retry
  - Rate limiting
  - Comprehensive logging
  - Dry run mode
  - Duplicate prevention
  - Priority detection
  - HTML to markdown conversion
