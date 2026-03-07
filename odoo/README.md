# Odoo Setup

This directory contains Docker Compose setup for self-hosted Odoo Community Edition.

## Quick Start

### 1. Start Odoo

```bash
docker-compose up -d
```

Wait 2-3 minutes for Odoo to initialize.

### 2. Access Odoo

Open browser: http://localhost:8069

### 3. Create Database

- Database Name: `odoo_db`
- Email: your-email@example.com
- Password: Choose a strong password
- Language: English
- Country: Your country
- Phone Number: Optional

### 4. Install Accounting Module

After login:
1. Go to Apps
2. Search for "Accounting"
3. Click "Install" on "Invoicing" (free) or "Accounting" (full)

## Services

- **Odoo Web Interface**: http://localhost:8069
- **PostgreSQL**: Internal (port 5432 in container)
- **Nginx Proxy**: http://localhost:80

## Default Credentials

- **Master Password**: admin_master_password (change in odoo.conf)
- **Database User**: odoo
- **Database Password**: odoo_password

## Directory Structure

```
odoo/
├── docker-compose.yml      # Docker services configuration
├── nginx.conf              # Nginx reverse proxy config
├── config/
│   └── odoo.conf           # Odoo server configuration
├── addons/                  # Custom addons (create this folder)
├── ssl/                     # SSL certificates (for HTTPS)
└── README.md               # This file
```

## Odoo JSON-RPC API

Odoo provides JSON-RPC API for integration:

**Endpoint**: `http://localhost:8069/jsonrpc`

### Example: Authenticate

```python
import requests

url = "http://localhost:8069/jsonrpc"
headers = {"Content-Type": "application/json"}

# Authenticate
payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "common",
        "method": "authenticate",
        "args": ["odoo_db", "admin", "your_password", {}]
    },
    "id": 1
}

response = requests.post(url, headers=headers, json=payload)
uid = response.json()["result"]
print(f"Authenticated UID: {uid}")
```

### Example: Create Invoice

```python
# Create invoice
payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "object",
        "method": "execute_kw",
        "args": [
            "odoo_db",
            uid,
            "your_password",
            "account.move",
            "create",
            [{
                "move_type": "out_invoice",
                "partner_id": 1,  # Customer ID
                "invoice_line_ids": [(0, 0, {
                    "product_id": 1,
                    "quantity": 1,
                    "price_unit": 100.0
                })]
            }]
        ]
    },
    "id": 2
}

response = requests.post(url, headers=headers, json=payload)
invoice_id = response.json()["result"]
```

## Common Operations

### Start Odoo
```bash
docker-compose up -d
```

### Stop Odoo
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f odoo
```

### Reset Database
```bash
docker-compose down -v  # Removes all data!
```

### Backup Database
```bash
docker exec odoo_postgres pg_dump -U odoo odoo_db > backup.sql
```

### Restore Database
```bash
docker exec -i odoo_postgres psql -U odoo odoo_db < backup.sql
```

## Troubleshooting

### Odoo Won't Start
```bash
# Check logs
docker-compose logs odoo

# Restart services
docker-compose restart
```

### Database Connection Error
```bash
# Check if DB is running
docker-compose ps

# Check DB logs
docker-compose logs db
```

### Port Already in Use
Change port in docker-compose.yml:
```yaml
ports:
  - "8070:8069"  # Use 8070 instead of 8069
```

## Integration with AI Employee

The Odoo MCP Server (`Skills/mcp_servers/odoo_mcp_server.py`) connects to Odoo via JSON-RPC.

### Configuration

Create `.env` file in project root:

```env
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_db
ODOO_USERNAME=admin
ODOO_PASSWORD=your_password
```

### Available MCP Tools

- `odoo_create_invoice` - Create customer invoice
- `odoo_create_vendor_bill` - Create vendor bill
- `odoo_get_invoices` - List invoices
- `odoo_get_customers` - List customers
- `odoo_get_products` - List products
- `odoo_create_partner` - Create customer/vendor
- `odoo_get_account_summary` - Get account summary
- `odoo_search_records` - Generic search

## Security Notes

1. **Change default passwords** in odoo.conf
2. **Enable HTTPS** for production (see ssl/ folder)
3. **Don't expose** database port externally
4. **Regular backups** of PostgreSQL data
5. **Keep Odoo updated** to latest version

## Resources

- [Odoo Documentation](https://www.odoo.com/documentation/)
- [Odoo JSON-RPC API](https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html)
- [Odoo GitHub](https://github.com/odoo/odoo)
- [Docker Odoo](https://hub.docker.com/_/odoo)

## Next Steps

1. ✅ Start Odoo with Docker Compose
2. ✅ Install Accounting module
3. ✅ Create test customers and products
4. ✅ Test Odoo MCP Server integration
5. ✅ Configure CEO Briefing to read from Odoo
