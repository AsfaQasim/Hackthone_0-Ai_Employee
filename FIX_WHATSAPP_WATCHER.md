# Fix WhatsApp Watcher - Playwright Browser Installation

## The Problem
You're getting this error:
```
Executable doesn't exist at C:\Users\DENZEN COMPUTER\AppData\Local\ms-playwright\chromium-1208\chrome-win64\chrome.exe
```

This means Playwright is installed but the browser binaries are not downloaded.

## Solution

### Option 1: Run the batch file (Easiest)
1. Double-click `install_playwright_browsers.bat`
2. Wait for it to download (may take 2-5 minutes)
3. Press any key when done

### Option 2: Manual command
Open a NEW command prompt (not in this terminal) and run:
```bash
python -m playwright install chromium
```

### Option 3: Install all browsers
```bash
python -m playwright install
```

## Why This Happens
- Playwright package is installed ✓
- But browser binaries need separate download
- This is a one-time setup

## After Installation

Test WhatsApp watcher:
```bash
python Skills/whatsapp_watcher.py auth
```

This will:
1. Open a browser window
2. Show WhatsApp Web
3. Wait for you to scan QR code
4. Save your session

## Verify Installation

Check if chromium is installed:
```bash
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); print('Chromium path:', p.chromium.executable_path); p.stop()"
```

## Expected Download Size
- Chromium: ~150-200 MB
- Download time: 2-5 minutes (depending on internet speed)

## Troubleshooting

### Download fails
- Check internet connection
- Try running as administrator
- Disable antivirus temporarily

### Still getting error after install
- Close all terminals
- Open fresh terminal
- Try auth command again

### Want to use different browser
```bash
# Firefox
python -m playwright install firefox

# WebKit (Safari-like)
python -m playwright install webkit
```

Then modify `Skills/whatsapp_watcher.py` line 62:
```python
# Change from:
browser = p.chromium.launch_persistent_context(...)

# To:
browser = p.firefox.launch_persistent_context(...)
```

## Next Steps

Once browsers are installed:
1. ✓ Run `python Skills/whatsapp_watcher.py auth`
2. ✓ Scan QR code in browser
3. ✓ Test with `python Skills/whatsapp_watcher.py poll --dry-run`
4. ✓ Run real poll: `python Skills/whatsapp_watcher.py poll`

## Note
The background gmail watcher process is still running. You can stop it with Ctrl+C in that terminal if needed.
