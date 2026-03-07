# Gold Tier - Quick Reference Card

## 🚀 Quick Start

```bash
# 1. Start Odoo
start_odoo.bat

# 2. Test integrations
test_gold_tier_integrations.bat

# 3. Generate CEO Briefing
python Skills/ceo_briefing_generator.py
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `odoo/docker-compose.yml` | Start Odoo |
| `Skills/mcp_servers/odoo_mcp_server.py` | Odoo integration |
| `Skills/mcp_servers/facebook_instagram_mcp_server.py` | Social media |
| `Skills/ceo_briefing_generator.py` | Weekly briefing |
| `.env` | Configuration |

---

## 🔧 Commands

### Odoo
```bash
start_odoo.bat          # Start Odoo
stop_odoo.bat           # Stop Odoo
docker-compose logs -f  # View logs
```

### Testing
```bash
python Skills/mcp_servers/odoo_mcp_server.py                        # Test Odoo
python Skills/mcp_servers/facebook_instagram_mcp_server.py          # Test Social
python Skills/ceo_briefing_generator.py                             # Generate briefing
python Skills/audit_logger.py stats --days 7                        # Audit stats
```

---

## 📊 MCP Tools

### Odoo
- `odoo_create_invoice` - Create invoice
- `odoo_get_account_summary` - Financial summary
- `odoo_get_customers` - List customers

### Facebook/Instagram
- `post_to_facebook` - Post to Facebook
- `post_to_instagram` - Post to Instagram
- `get_facebook_insights` - Analytics

---

## ⚙️ Environment

```env
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_db
ODOO_USERNAME=admin
ODOO_PASSWORD=your_password

FACEBOOK_PAGE_ACCESS_TOKEN=your_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_id
```

---

## ✅ Gold Tier Checklist

- [ ] Odoo running
- [ ] .env configured
- [ ] Facebook token set
- [ ] Instagram ID set
- [ ] Tests passing
- [ ] Briefing generates

---

**Full Guide**: GOLD_TIER_SETUP_GUIDE.md
**Completion**: GOLD_TIER_COMPLETE.md
