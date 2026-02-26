# GitHub Push Error Fix

## Error Message
```
remote: push declined due to repository rule violations
error: failed to push some refs
```

## Common Causes

1. **Sensitive data in commit** (credentials, tokens)
2. **Branch protection rules** (main branch protected)
3. **Large files** (over 100MB)

---

## Solution 1: Remove Sensitive Files from Git History

### Step 1: Check what's being committed

```bash
git status
```

### Step 2: Remove sensitive files from staging

```bash
# Remove gmail token if accidentally added
git rm --cached config/gmail-token.json

# Remove gmail credentials if accidentally added
git rm --cached config/gmail-credentials.json

# Remove .env if accidentally added
git rm --cached .env

# Remove WhatsApp session if accidentally added
git rm --cached -r .whatsapp_session/
```

### Step 3: Commit the removal

```bash
git commit -m "Remove sensitive files from git"
```

### Step 4: Push again

```bash
git push origin main
```

---

## Solution 2: If Files Already Pushed

If sensitive files are already in git history, you need to remove them:

### Option A: Use BFG Repo-Cleaner (Recommended)

```bash
# Download BFG
# https://rtyley.github.io/bfg-repo-cleaner/

# Remove sensitive files from history
java -jar bfg.jar --delete-files gmail-token.json
java -jar bfg.jar --delete-files gmail-credentials.json
java -jar bfg.jar --delete-files .env

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push
git push origin main --force
```

### Option B: Use git filter-branch

```bash
# Remove gmail-token.json from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config/gmail-token.json" \
  --prune-empty --tag-name-filter cat -- --all

# Remove gmail-credentials.json from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config/gmail-credentials.json" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin main --force
```

---

## Solution 3: Branch Protection Issue

If main branch is protected:

### Option A: Push to Different Branch

```bash
# Create new branch
git checkout -b bronze-tier-complete

# Push to new branch
git push origin bronze-tier-complete

# Create Pull Request on GitHub
```

### Option B: Disable Branch Protection (if you're admin)

1. Go to: https://github.com/AsfaQasim/Hackthone_0-AI_Employee/settings/branches
2. Find "main" branch rules
3. Click "Edit" or "Delete"
4. Disable protection temporarily
5. Push your changes
6. Re-enable protection

---

## Solution 4: Large Files Issue

If you have large files (>100MB):

### Check for large files

```bash
# Find files larger than 50MB
find . -type f -size +50M
```

### Use Git LFS for large files

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.pma"
git lfs track "*.db"

# Add .gitattributes
git add .gitattributes

# Commit and push
git commit -m "Add Git LFS tracking"
git push origin main
```

---

## Quick Fix (Most Common)

Most likely issue is sensitive files. Try this:

```bash
# 1. Remove sensitive files from staging
git rm --cached config/gmail-token.json
git rm --cached config/gmail-credentials.json
git rm --cached .env

# 2. Make sure .gitignore is correct
git add .gitignore

# 3. Commit
git commit -m "Remove sensitive files and update gitignore"

# 4. Push
git push origin main
```

---

## Alternative: Start Fresh

If nothing works, create a clean commit:

```bash
# 1. Stash current changes
git stash

# 2. Pull latest
git pull origin main

# 3. Apply stash
git stash pop

# 4. Check what's changed
git status

# 5. Add only safe files
git add Dashboard.md
git add Company_Handbook.md
git add Skills/
git add README.md
# ... add other safe files

# 6. Commit
git commit -m "Bronze Tier complete - safe files only"

# 7. Push
git push origin main
```

---

## Verify .gitignore is Working

```bash
# Check what will be committed
git status

# Should NOT see:
# - config/gmail-token.json
# - config/gmail-credentials.json
# - .env
# - .whatsapp_session/
# - venv/
# - node_modules/

# If you see these, they're not being ignored properly
```

---

## After Fixing

### Rotate Credentials

If you accidentally pushed credentials:

1. **Gmail Token**: Delete `config/gmail-token.json` and re-authenticate
2. **Gmail Credentials**: Create new OAuth credentials in Google Cloud Console
3. **.env secrets**: Change any API keys or passwords

### Update .gitignore

Make sure these are in .gitignore:

```
# Secrets
.env
config/gmail-credentials.json
config/gmail-token.json
*.pem
*.key

# Sessions
.whatsapp_session/
.linkedin_session/

# Large files
*.db
*.pma
```

---

## Summary

**Most likely cause**: Sensitive files (gmail-token.json) in commit

**Quick fix**:
```bash
git rm --cached config/gmail-token.json
git commit -m "Remove sensitive files"
git push origin main
```

**If that doesn't work**: Push to a new branch instead

```bash
git checkout -b bronze-complete
git push origin bronze-complete
```

Then create a Pull Request on GitHub.
