# Git Clone Authentication Fix

## The Problem
You're getting a "Clone timed out after 60s" error, which typically means authentication issues with private repositories.

## Quick Solutions (Choose One)

### Solution 1: Use Personal Access Token (Recommended)
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name like "Git Access"
4. Select scopes: `repo` (full control of private repositories)
5. Click "Generate token"
6. Copy the token (save it somewhere safe)

Then clone using:
```bash
git clone https://YOUR_USERNAME:YOUR_TOKEN@github.com/owner/repository.git
```

### Solution 2: Configure Git Credential Storage
```bash
git config --global credential.helper store
git config --global user.name "YOUR_USERNAME"
git config --global user.email "YOUR_EMAIL"
```

Then when you clone, it will prompt for username/password. Use your GitHub username and the personal access token as the password.

### Solution 3: Manual GitHub CLI Installation
1. Open your browser
2. Go to https://cli.github.com/
3. Download "gh_2.62.0_windows_amd64.msi"
4. Run the installer
5. Open a new command prompt
6. Run: `gh auth login`
7. Follow the prompts to authenticate

### Solution 4: Use SSH (If you prefer)
1. Generate SSH key: `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`
2. Add to SSH agent: `ssh-add ~/.ssh/id_rsa`
3. Copy public key: `cat ~/.ssh/id_rsa.pub`
4. Add to GitHub: Settings → SSH and GPG keys → New SSH key
5. Clone using SSH: `git clone git@github.com:owner/repository.git`

## Test Your Setup
After setting up authentication, test with:
```bash
git clone https://github.com/octocat/Hello-World.git
```

## Troubleshooting
- If still getting timeouts, check your internet connection
- Disable battery saver mode if enabled
- Try cloning a public repository first to test
- Make sure the repository URL is correct
- Verify you have access to the repository

## What Repository Are You Trying to Clone?
Please share the repository URL so I can provide specific instructions.