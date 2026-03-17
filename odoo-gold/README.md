# Odoo Gold Tier - Accounting Integration

Self-hosted Odoo Community Edition integrated with the AI Employee via JSON-RPC MCP server.

## Quick Start

```bash
# 1. Start Odoo containers
cd odoo-gold
docker compose up -d

# 2. Wait ~60 seconds for Odoo to initialize, then run setup
python setup_odoo.py

# 3. Verify integration
python test_odoo_integration.py
```

## Access

- **Odoo Web UI**: http://localhost:8069
- **Database**: odoo_gold
- **Username**: admin
- **Password**: admin

## Architecture

```
odoo-gold/
  docker-compose.yml   # Odoo 17 + PostgreSQL 16
  config/odoo.conf     # Odoo server configuration
  addons/              # Custom addons (if any)
  setup_odoo.py        # Database creation + sample data
  test_odoo_integration.py  # Verify JSON-RPC connectivity
```

## MCP Integration

The Odoo MCP server (`Skills/mcp_servers/odoo_mcp_server.py`) connects via JSON-RPC and provides:

| Tool | Description |
|------|-------------|
| odoo_create_invoice | Create customer invoice |
| odoo_create_vendor_bill | Create vendor bill |
| odoo_get_invoices | List invoices |
| odoo_get_customers | List customers |
| odoo_get_products | List products |
| odoo_create_partner | Create customer/vendor |
| odoo_get_account_summary | Get financial summary |
| odoo_search_records | Generic model search |

## CEO Briefing Integration

The CEO Briefing generator (`Skills/ceo_briefing_generator.py`) pulls data from Odoo for:
- Weekly revenue and expenses
- Pending payments
- Profit margins
- Invoice status

## Environment Variables

Set in `.env`:
```
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_gold
ODOO_USERNAME=admin
ODOO_PASSWORD=admin
ODOO_MASTER_PASSWORD=admin_master_2026
```

## Sample Data

Setup script creates:
- 3 customers (Alpha Corp, Beta Solutions, Gamma Industries)
- 4 service products (Web Dev, AI Consulting, Maintenance, Software License)
- 3 customer invoices + 1 vendor bill

## Troubleshooting

**Containers won't start**: Check Docker Desktop is running. Run `docker compose logs`.

**Database creation fails**: Access http://localhost:8069/web/database/manager to create manually.

**Authentication fails**: Default credentials are admin/admin. Check `.env` values.
