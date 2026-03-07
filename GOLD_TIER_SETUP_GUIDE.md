# Gold Tier Setup Guide

## Overview

Gold Tier adds **Facebook**, **Instagram**, and **Odoo Accounting** integration to your AI Employee.

### What's New in Gold Tier:

1. ✅ **Odoo Community Edition** - Self-hosted accounting system (Docker Compose)
2. ✅ **Facebook Integration** - Post to Facebook Pages with analytics
3. ✅ **Instagram Integration** - Post to Instagram Business accounts
4. ✅ **Enhanced CEO Briefing** - Now includes accounting data from Odoo
5. ✅ **Audit Logging** - Comprehensive compliance tracking
6. ✅ **Error Recovery** - Automatic retry and graceful degradation

---

## Prerequisites

- Docker Desktop installed and running
- Python 3.13+
- Facebook Developer Account
- Instagram Business Account (connected to Facebook Page)

---

## Part 1: Setup Odoo Accounting

### Step 1: Start Odoo with Docker

```bash
cd F:\hackthone_0\odoo
docker-compose up -d
```

Wait 2-3 minutes for Odoo to initialize.

### Step 2: Access Odoo

Open browser: http://localhost:8069

### Step 3: Create Database

- **Database Name**: `odoo_db`
- **Email**: your-email@example.com
- **Password**: Choose a strong password
- **Language**: English
- **Country**: Your country

### Step 4: Install Accounting Module

1. Go to **Apps** from top menu
2. Search for "Invoicing" (free) or "Accounting" (full)
3. Click **Install**
4. Wait for installation to complete

### Step 5: Configure Odoo

1. Go to **Settings** → **Users & Companies**
2. Create your company profile
3. Add your logo, address, tax ID

### Step 6: Create Test Data

#### Create a Customer:
1. Go to **Invoicing** → **Customers**
2. Click **Create**
3. Add customer details (Name, Email, Phone)
4. Save

#### Create a Product:
1. Go to **Invoicing** → **Products**
2. Click **Create**
3. Add product details (Name, Price, Category)
4. Save

### Step 7: Test Odoo MCP Connection

Create `.env` file in project root:

```env
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_db
ODOO_USERNAME=admin
ODOO_PASSWORD=your_password
```

Test connection:

```bash
cd F:\hackthone_0
python Skills/mcp_servers/odoo_mcp_server.py
```

---

## Part 2: Setup Facebook Integration

### Step 1: Create Facebook App

1. Go to https://developers.facebook.com
2. Click **My Apps** → **Create App**
3. Select **Business** app type
4. Fill in app details:
   - **App Name**: Your AI Employee
   - **App Contact Email**: your-email@example.com
5. Click **Create App**

### Step 2: Add Facebook Login Product

1. In App Dashboard, click **Add Product**
2. Find **Facebook Login** and click **Set Up**
3. Configure:
   - **Valid OAuth Redirect URIs**: `https://localhost:8000/callback`
   - Save changes

### Step 3: Get Page Access Token

1. Go to **Graph API Explorer**: https://developers.facebook.com/tools/explorer/
2. Select your app from dropdown
3. Click **Get Token** → **Get Page Access Token**
4. Select your Facebook Page
5. Copy the generated token

### Step 4: Get Instagram Business Account ID

1. In Graph API Explorer, run this query:
   ```
   GET /me?fields=instagram_business_account
   ```
2. Copy the `instagram_business_account.id`

### Step 5: Configure Environment

Add to `.env` file:

```env
FACEBOOK_PAGE_ACCESS_TOKEN=your_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id_here
```

### Step 6: Test Facebook/Instagram Connection

```bash
python Skills/mcp_servers/facebook_instagram_mcp_server.py
```

---

## Part 3: Setup Instagram Business Account

### Requirements:

- Instagram **Business** or **Creator** account (not Personal)
- Connected to Facebook Page
- Public account (not private)

### Convert to Business Account:

1. Open Instagram app
2. Go to **Settings** → **Account**
3. Tap **Switch to Professional Account**
4. Select **Business**
5. Connect to your Facebook Page

---

## Part 4: Test Gold Tier Features

### Test Odoo Integration

```bash
# Get customers
python -c "from Skills.mcp_servers.odoo_mcp_server import OdooMCPServer; import asyncio; server = OdooMCPServer(); asyncio.run(server.execute_tool('odoo_get_customers', {'limit': 5}))"

# Create invoice
python -c "from Skills.mcp_servers.odoo_mcp_server import OdooMCPServer; import asyncio; server = OdooMCPServer(); asyncio.run(server.execute_tool('odoo_create_invoice', {'partner_name': 'Test Customer', 'partner_email': 'test@example.com', 'lines': [{'name': 'Consulting', 'quantity': 1, 'price_unit': 500}]}))"
```

### Test Facebook Posting

```bash
python -c "from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer; import asyncio; server = FacebookInstagramMCPServer(); asyncio.run(server.execute_tool('post_to_facebook', {'message': 'Test post from AI Employee! #GoldTier'}))"
```

### Test Instagram Posting

```bash
python -c "from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer; import asyncio; server = FacebookInstagramMCPServer(); asyncio.run(server.execute_tool('post_to_instagram', {'caption': 'Test post from AI Employee! #GoldTier', 'image_url': 'https://via.placeholder.com/1080x1080'}))"
```

---

## Part 5: Enhanced CEO Briefing with Odoo

The CEO Briefing now includes accounting data from Odoo:

### Generate Briefing:

```bash
python Skills/ceo_briefing_generator.py --vault . --with-odoo
```

### Briefing Includes:

- **Revenue Tracking** - From Odoo invoices
- **Expense Tracking** - From vendor bills
- **Profit Margins** - Calculated from accounting data
- **Pending Payments** - Unpaid invoices
- **Cash Flow Analysis** - Weekly/Monthly trends

---

## Part 6: Audit Logging

All actions are automatically logged to `Logs/audit/`:

### View Audit Logs:

```bash
# View today's logs
cat Logs/audit/$(date +%Y-%m-%d).json

# Get statistics
python Skills/audit_logger.py stats --days 7

# Generate report
python Skills/audit_logger.py report --days 30
```

### Log Retention:

- Logs kept for 90 days
- Automatic cleanup weekly
- JSON format for easy parsing

---

## Part 7: Error Recovery

Automatic error handling with retry logic:

### Features:

- **Exponential Backoff** - Retry with increasing delays
- **Graceful Degradation** - Fallback when services unavailable
- **Error Categorization** - Different handling for different error types
- **Human Alert** - Notifies when manual intervention needed

### Error Categories:

1. **Transient Errors** - Network timeouts, rate limits (auto-retry)
2. **Authentication Errors** - Expired tokens (pause + alert)
3. **Logic Errors** - AI misinterpretation (human review)
4. **Data Errors** - Corrupted files (quarantine)
5. **System Errors** - Disk full, crashes (auto-restart)

---

## Part 8: Ralph Wiggum Loop Enhancement

Multi-step autonomous task execution:

### Start Ralph Loop:

```bash
# Process all pending tasks
python Skills/ralph_loop.py "Process all files in /Needs_Action, move to /Done when complete" --max-iterations 10
```

### How It Works:

1. Claude reads tasks from `/Needs_Action`
2. Processes each task
3. Moves completed tasks to `/Done`
4. Loop continues until all tasks done or max iterations

---

## Quick Reference Commands

### Odoo Commands:

```bash
# Start Odoo
docker-compose -f odoo/docker-compose.yml up -d

# Stop Odoo
docker-compose -f odoo/docker-compose.yml down

# View Odoo logs
docker-compose -f odoo/docker-compose.yml logs -f odoo

# Reset Odoo (WARNING: Deletes all data!)
docker-compose -f odoo/docker-compose.yml down -v
```

### Facebook/Instagram Commands:

```bash
# Post to Facebook
python -c "from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer; import asyncio; server = FacebookInstagramMCPServer(); asyncio.run(server.execute_tool('post_to_facebook', {'message': 'Your message here'}))"

# Get Facebook insights
python -c "from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer; import asyncio; server = FacebookInstagramMCPServer(); asyncio.run(server.execute_tool('get_facebook_insights', {'metric': 'page_impressions', 'days': 7}))"

# Post to Instagram
python -c "from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer; import asyncio; server = FacebookInstagramMCPServer(); asyncio.run(server.execute_tool('post_to_instagram', {'caption': 'Your caption', 'image_url': 'https://example.com/image.jpg'}))"
```

### Audit & Monitoring:

```bash
# View audit stats
python Skills/audit_logger.py stats --days 7

# Generate audit report
python Skills/audit_logger.py report --days 30

# Cleanup old logs
python Skills/audit_logger.py cleanup
```

---

## Troubleshooting

### Odoo Won't Start

```bash
# Check if port 8069 is in use
netstat -ano | findstr :8069

# Change port in odoo/docker-compose.yml
ports:
  - "8070:8069"  # Use 8070 instead

# Restart
docker-compose down
docker-compose up -d
```

### Facebook API Error: "Invalid Token"

1. Token expired - generate new one
2. Check app permissions
3. Make sure Page Access Token (not User Token)

### Instagram Post Fails

1. Ensure Instagram is Business account
2. Check account is connected to Facebook Page
3. Verify account is public (not private)
4. Check image URL is publicly accessible

### Odoo MCP Connection Failed

```bash
# Test Odoo is running
curl http://localhost:8069

# Check .env file has correct credentials
cat .env | grep ODOO

# Test authentication
python Skills/mcp_servers/odoo_mcp_server.py
```

---

## Gold Tier Checklist

### Odoo Setup:
- [ ] Docker Compose started
- [ ] Odoo accessible at http://localhost:8069
- [ ] Database created
- [ ] Accounting module installed
- [ ] Test customer created
- [ ] Test product created
- [ ] Odoo MCP connection tested

### Facebook/Instagram Setup:
- [ ] Facebook App created
- [ ] Page Access Token generated
- [ ] Instagram Business Account ID obtained
- [ ] .env file configured
- [ ] Test post to Facebook successful
- [ ] Test post to Instagram successful

### Gold Tier Features:
- [ ] CEO Briefing with Odoo integration working
- [ ] Audit logging active
- [ ] Error recovery tested
- [ ] Ralph Wiggum loop tested

---

## Next Steps

After completing Gold Tier setup:

1. **Test End-to-End Workflow**:
   - Create invoice in Odoo
   - Post to Facebook/Instagram
   - Generate CEO Briefing
   - Review audit logs

2. **Customize for Your Business**:
   - Add your company logo to Odoo
   - Configure tax rates
   - Set up payment terms
   - Customize Facebook/Instagram posting templates

3. **Automate Workflows**:
   - Schedule weekly CEO briefings
   - Auto-post to social media
   - Set up recurring invoices
   - Configure automatic payment reminders

---

## Resources

- [Odoo Documentation](https://www.odoo.com/documentation/)
- [Facebook Graph API](https://developers.facebook.com/docs/graph-api/)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/)
- [Docker Compose Docs](https://docs.docker.com/compose/)

---

**Gold Tier Status**: Ready for autonomous business operations! 🚀
