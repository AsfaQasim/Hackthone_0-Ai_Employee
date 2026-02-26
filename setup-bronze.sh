#!/bin/bash
# Bronze Tier Quick Setup Script
# Run this to set up your AI Employee foundation

echo "🚀 Bronze Tier AI Employee Setup"
echo "================================="
echo ""

# Check Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✅ Python found: $(python3 --version)"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pyyaml html2text

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Set up Gmail API credentials (see BRONZE_TIER_SETUP.md)"
echo "2. Save credentials to: config/gmail-credentials.json"
echo "3. Run: python Skills/gmail_watcher.py auth"
echo "4. Test: python Skills/gmail_watcher.py poll --dry-run"
echo ""
echo "📖 Full guide: BRONZE_TIER_SETUP.md"
