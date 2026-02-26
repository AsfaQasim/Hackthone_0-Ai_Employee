# Disk Space Issue - Chromium Installation Failed

## Problem
```
[Error: ENOSPC: no space left on device, write]
```

Chromium download 99% complete tha lekin disk space khatam ho gayi.

## Solution

### Option 1: Free Up Space (Recommended)
1. Delete temporary files
2. Empty Recycle Bin
3. Delete old downloads
4. Run Disk Cleanup

### Option 2: Install on Different Drive
Chromium ko F drive par install karne ke liye:

```bash
# Set environment variable
set PLAYWRIGHT_BROWSERS_PATH=F:\playwright-browsers

# Then install
python -m playwright install chromium
```

### Option 3: Use Existing Chrome
WhatsApp watcher ko modify karke system Chrome use kar sakte hain.

## Quick Fix Commands

### Check Disk Space
```bash
dir F:\
```

### Clean Temp Files
```bash
del /q /f %TEMP%\*
```

### Install to F Drive
```bash
set PLAYWRIGHT_BROWSERS_PATH=F:\playwright-browsers
python -m playwright install chromium
```

## After Freeing Space

1. Delete incomplete download:
```bash
rmdir /s /q "%LOCALAPPDATA%\ms-playwright\chromium-1208"
```

2. Retry installation:
```bash
python -m playwright install chromium --force
```

## Alternative: Use System Chrome

Modify `Skills/whatsapp_watcher.py` to use system Chrome instead of Chromium.

Change line 62 from:
```python
browser = p.chromium.launch_persistent_context(...)
```

To:
```python
browser = p.chromium.launch_persistent_context(
    str(self.session_path),
    headless=False,
    channel="chrome"  # Use system Chrome
)
```

## Disk Space Needed
- Chromium: ~173 MB
- Current: 99% downloaded (only 1-2 MB remaining)

## Recommendation
1. Free up at least 500 MB space
2. Delete incomplete chromium folder
3. Retry installation
4. Or use system Chrome if installed
