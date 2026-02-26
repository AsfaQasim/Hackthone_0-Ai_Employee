# Scheduler Setup Guide

## Overview

The AI Employee System uses a scheduler to run the main loop automatically every 5 minutes. This ensures that:
- Watchers check for new emails, messages, and content
- Inbox items are processed
- Pending plans are executed
- Dashboard is updated

## Quick Start

### Windows

1. **Run the setup script** (as Administrator for best results):
   ```cmd
   python setup_scheduler.py
   ```

2. **Follow the prompts** to set up the scheduler

3. **Verify the task** is created:
   - Press `Win+R`
   - Type `taskschd.msc` and press Enter
   - Look for `AIEmployeeMainLoop` in the task list

### Linux/Mac

1. **Run the setup script**:
   ```bash
   python3 setup_scheduler.py
   ```

2. **Follow the prompts** to set up the scheduler

3. **Verify the cron job**:
   ```bash
   crontab -l
   ```

## Manual Setup

### Windows Task Scheduler

```cmd
python Skills/scheduler.py setup --script main_loop.py --interval 5
```

### Cron (Linux/Mac)

```bash
python3 Skills/scheduler.py setup --script main_loop.py --interval 5
```

## Check Status

```bash
python Skills/scheduler.py status
```

## Remove Scheduler

### Using Setup Script

```bash
python setup_scheduler.py
```
Then choose option 3 to remove.

### Using Scheduler Directly

```bash
python Skills/scheduler.py remove
```

## What Runs Every 5 Minutes?

The `main_loop.py` script executes the following:

1. **Run Watchers**
   - Gmail Watcher checks for new emails
   - Other watchers check their respective sources

2. **Process Inbox**
   - Claude Code processes items in `/Inbox`
   - Items are moved to `/Needs_Action` or `/Done`

3. **Execute Plans**
   - Ralph Wiggum Loop executes pending plans
   - Multi-step tasks are completed autonomously

4. **Update Dashboard**
   - `Dashboard.md` is updated with current status
   - Activity summaries are generated

## Logs

All execution logs are saved to:
```
Logs/main_loop.log
```

You can monitor the logs to see what the system is doing:

### Windows
```cmd
type Logs\main_loop.log
```

### Linux/Mac
```bash
tail -f Logs/main_loop.log
```

## Customizing the Interval

To change the interval from 5 minutes to something else:

```bash
python Skills/scheduler.py setup --interval 10
```

This will run the main loop every 10 minutes instead.

## Troubleshooting

### Windows: "Access Denied"

Run Command Prompt as Administrator:
1. Right-click Command Prompt
2. Select "Run as Administrator"
3. Run the setup script again

### Linux/Mac: "Permission Denied"

Make sure you have permission to edit crontab:
```bash
crontab -e
```

If this works, the scheduler should work too.

### Task Not Running

**Windows:**
1. Open Task Scheduler (`taskschd.msc`)
2. Find `AIEmployeeMainLoop`
3. Right-click → Run
4. Check if it executes successfully

**Linux/Mac:**
1. Check cron logs:
   ```bash
   grep CRON /var/log/syslog
   ```

2. Make sure the script path is absolute:
   ```bash
   crontab -l
   ```

### Python Not Found

Make sure Python is in your PATH:

**Windows:**
```cmd
where python
```

**Linux/Mac:**
```bash
which python3
```

If not found, you may need to specify the full path to Python in the scheduler setup.

## Advanced Usage

### Custom Script Path

```bash
python Skills/scheduler.py setup --script /path/to/custom_script.py
```

### Different Intervals

```bash
# Every 1 minute
python Skills/scheduler.py setup --interval 1

# Every 15 minutes
python Skills/scheduler.py setup --interval 15

# Every hour (60 minutes)
python Skills/scheduler.py setup --interval 60
```

## Integration with AI Employee System

The scheduler is part of Task 12.1 in the AI Employee System implementation plan. It provides:

- **Automated execution**: No manual intervention needed
- **Reliable scheduling**: Uses OS-native schedulers
- **Cross-platform**: Works on Windows, Linux, and Mac
- **Easy management**: Simple setup and removal

## Next Steps

After setting up the scheduler:

1. **Verify it's running**: Check logs after 5 minutes
2. **Monitor Dashboard**: Watch `Dashboard.md` for updates
3. **Test watchers**: Send a test email to verify Gmail Watcher
4. **Review logs**: Check `Logs/main_loop.log` for activity

## Support

If you encounter issues:

1. Check the logs: `Logs/main_loop.log`
2. Verify the scheduler status: `python Skills/scheduler.py status`
3. Try removing and recreating: `python setup_scheduler.py`

---

**Status**: Task 12.1 Complete ✓
