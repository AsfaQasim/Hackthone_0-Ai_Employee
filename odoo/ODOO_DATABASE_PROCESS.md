# Odoo Database Process Guide

This guide explains the complete database process in Odoo, from setup to daily operations.

## Table of Contents

1. [Database Architecture](#database-architecture)
2. [Database Setup Process](#database-setup-process)
3. [Database Connection Flow](#database-connection-flow)
4. [Database Operations](#database-operations)
5. [Database Management](#database-management)
6. [Backup & Recovery](#backup--recovery)
7. [Troubleshooting](#troubleshooting)

---

## Database Architecture

### Components

```
┌─────────────────────────────────────────────────────────┐
│                    Odoo Web Interface                     │
│                    (Port 8069)                            │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ JSON-RPC / ORM Calls
                     │
┌────────────────────▼────────────────────────────────────┐
│                   Odoo Application                        │
│                   (odoo:17.0 container)                   │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Odoo ORM Layer                       │   │
│  │  - Models (account.move, res.partner, etc.)      │   │
│  │  - Methods (create, write, search, unlink)       │   │
│  │  - Business Logic                                 │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ PostgreSQL Protocol
                     │ (Port 5432)
                     │
┌────────────────────▼────────────────────────────────────┐
│                  PostgreSQL Database                      │
│                  (postgres:15 container)                  │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Database: odoo_db                     │   │
│  │                                                   │   │
│  │  Tables:                                          │   │
│  │  - account_move (Invoices)                        │   │
│  │  - res_partner (Customers/Vendors)                │   │
│  │  - product_template (Products)                    │   │
│  │  - res_users (Users)                              │   │
│  │  - ir_model (Models Metadata)                     │   │
│  │  - ... (200+ Odoo tables)                         │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Key Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Defines Odoo + PostgreSQL containers |
| `config/odoo.conf` | Odoo server configuration with DB settings |
| `odoo_postgresql_data/` | PostgreSQL data volume (persistent) |
| `odoo_data/` | Odoo filestore (attachments, etc.) |

---

## Database Setup Process

### Step 1: Start Database Container

```bash
cd F:\hackthone_0\odoo
docker-compose up -d db
```

**What happens:**
1. Docker pulls `postgres:15` image
2. Creates container `odoo_postgres`
3. Sets environment variables:
   - `POSTGRES_USER=odoo`
   - `POSTGRES_PASSWORD=odoo_password`
   - `POSTGRES_DB=postgres`
4. Mounts volume `odoo_postgresql_data` for persistence
5. Runs health check every 10 seconds

### Step 2: Start Odoo Application

```bash
docker-compose up -d odoo
```

**What happens:**
1. Docker pulls `odoo:17.0` image
2. Creates container `odoo_community`
3. Reads DB connection from `config/odoo.conf`:
   ```ini
   db_host = db
   db_port = 5432
   db_user = odoo
   db_password = odoo_password
   db_name = postgres
   ```
4. Waits for DB health check to pass
5. Odoo connects to PostgreSQL

### Step 3: Create Odoo Database

**Via Web Interface:**
1. Open http://localhost:8069
2. Fill in database creation form:
   - **Database Name**: `odoo_db`
   - **Email**: `admin@yourcompany.com`
   - **Password**: Choose strong password
   - **Language**: English
   - **Country**: Your country

**Via Command Line (Alternative):**
```bash
curl -X POST http://localhost:8069/web/database/create \
  -H "Content-Type: application/json" \
  -d '{
    "master_pwd": "admin_master_password",
    "name": "odoo_db",
    "login": "admin",
    "password": "your_password",
    "lang": "en_US",
    "country_code": "US"
  }'
```

**What happens internally:**
1. Odoo creates new PostgreSQL database `odoo_db`
2. Creates all required tables (200+)
3. Inserts base data (users, companies, etc.)
4. Creates filestore directory

### Step 4: Verify Database Connection

```bash
# Check container status
docker-compose ps

# Check Odoo logs
docker-compose logs odoo

# Check database logs
docker-compose logs db

# Connect to PostgreSQL directly
docker exec -it odoo_postgres psql -U odoo -d odoo_db
```

---

## Database Connection Flow

### 1. MCP Server → Odoo → Database

```
┌─────────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  MCP Server     │      │  Odoo Web    │      │  Odoo App    │      │  PostgreSQL  │
│  (Python)       │      │  Interface   │      │  Container   │      │  Container   │
└────────┬────────┘      └──────┬───────┘      └──────┬───────┘      └──────┬───────┘
         │                      │                      │                      │
         │ 1. HTTP POST         │                      │                      │
         │    /jsonrpc          │                      │                      │
         │─────────────────────>│                      │                      │
         │                      │                      │                      │
         │                      │ 2. Route to          │                      │
         │                      │    controller        │                      │
         │                      │─────────────────────>│                      │
         │                      │                      │                      │
         │                      │                      │ 3. ORM Method        │
         │                      │                      │    execute_kw        │
         │                      │                      │─────────────────────>│
         │                      │                      │                      │
         │                      │                      │ 4. SQL Query         │
         │                      │                      │    (SELECT/INSERT)   │
         │                      │                      │─────────────────────>│
         │                      │                      │                      │
         │                      │                      │ 5. Result Set        │
         │                      │                      │<─────────────────────│
         │                      │                      │                      │
         │                      │ 6. Format Response   │                      │
         │                      │<─────────────────────│                      │
         │                      │                      │                      │
         │ 7. JSON Response     │                      │                      │
         │<─────────────────────│                      │                      │
         │                      │                      │                      │
```

### 2. Example: Create Invoice Flow

**MCP Server Code:**
```python
# Skills/mcp_servers/odoo_mcp_server.py
invoice_id = self._execute_kw('account.move', 'create', [invoice_data])
```

**JSON-RPC Request:**
```json
POST http://localhost:8069/jsonrpc
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "object",
    "method": "execute_kw",
    "args": [
      "odoo_db",
      2,  // uid
      "password",
      "account.move",
      "create",
      [{
        "move_type": "out_invoice",
        "partner_id": 1,
        "invoice_line_ids": [...]
      }]
    ]
  },
  "id": 1
}
```

**SQL Generated by Odoo:**
```sql
INSERT INTO account_move (
    move_type, partner_id, invoice_date, state, create_uid, create_date
) VALUES (
    'out_invoice', 1, '2026-03-13', 'draft', 2, NOW()
) RETURNING id;
```

---

## Database Operations

### CRUD Operations via ORM

#### Create
```python
# Create customer
partner_id = odoo._execute_kw('res.partner', 'create', [{
    'name': 'John Doe',
    'email': 'john@example.com',
    'phone': '+1234567890'
}])

# SQL Equivalent:
# INSERT INTO res_partner (name, email, phone, create_date)
# VALUES ('John Doe', 'john@example.com', '+1234567890', NOW())
```

#### Read
```python
# Search and read customers
customers = odoo._execute_kw('res.partner', 'search_read', [
    [('customer_rank', '>', 0)],  # Domain filter
    ['name', 'email', 'phone'],   # Fields
    0,                             # Offset
    10                             # Limit
])

# SQL Equivalent:
# SELECT name, email, phone FROM res_partner
# WHERE customer_rank > 0
# LIMIT 10 OFFSET 0
```

#### Update
```python
# Update customer
odoo._execute_kw('res.partner', 'write', [
    [1],  # Record IDs
    {'phone': '+9876543210'}  # Values to update
])

# SQL Equivalent:
# UPDATE res_partner SET phone = '+9876543210' WHERE id = 1
```

#### Delete
```python
# Delete customer
odoo._execute_kw('res.partner', 'unlink', [[1]])

# SQL Equivalent:
# DELETE FROM res_partner WHERE id = 1
```

### Database Tables Reference

| Model | Table | Description |
|-------|-------|-------------|
| `res.partner` | `res_partner` | Customers, Vendors, Contacts |
| `account.move` | `account_move` | Invoices, Bills |
| `account.move.line` | `account_move_line` | Invoice Lines |
| `product.template` | `product_template` | Products |
| `res.users` | `res_users` | System Users |
| `sale.order` | `sale_order` | Sales Orders |
| `purchase.order` | `purchase_order` | Purchase Orders |
| `stock.picking` | `stock_picking` | Inventory Transfers |

---

## Database Management

### View Database Size

```bash
docker exec -it odoo_postgres psql -U odoo -d odoo_db -c "
SELECT 
    pg_size_pretty(pg_database_size('odoo_db')) as database_size;
"
```

### View Table Sizes

```bash
docker exec -it odoo_postgres psql -U odoo -d odoo_db -c "
SELECT 
    relname as table_name,
    pg_size_pretty(pg_total_relation_size(relid)) as total_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 10;
"
```

### View Active Connections

```bash
docker exec -it odoo_postgres psql -U odoo -d odoo_db -c "
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query
FROM pg_stat_activity
WHERE datname = 'odoo_db';
"
```

### Vacuum Database (Clean Up)

```bash
docker exec -it odoo_postgres psql -U odoo -d odoo_db -c "VACUUM ANALYZE;"
```

---

## Backup & Recovery

### Backup Database

#### Option 1: Using pg_dump
```bash
# Backup to SQL file
docker exec odoo_postgres pg_dump -U odoo odoo_db > backup_$(date +%Y%m%d).sql

# Backup with compression
docker exec odoo_postgres pg_dump -U odoo odoo_db | gzip > backup_$(date +%Y%m%d).sql.gz
```

#### Option 2: Using Odoo Backup API
```bash
curl -X POST http://localhost:8069/web/database/backup \
  -H "Content-Type: application/json" \
  -d '{
    "master_pwd": "admin_master_password",
    "name": "odoo_db",
    "backup_format": "zip"
  }' \
  --output backup_$(date +%Y%m%d).zip
```

#### Option 3: Backup Volume
```bash
# Stop Odoo
docker-compose down

# Copy volume data
docker run --rm \
  -v odoo_postgresql_data:/data:ro \
  -v $(pwd)/backup:/backup \
  alpine tar czf /backup/db_volume.tar.gz -C /data .
```

### Restore Database

#### From SQL Dump
```bash
# Drop existing database
docker exec -it odoo_postgres psql -U odoo -c "DROP DATABASE IF EXISTS odoo_db;"

# Create new database
docker exec -it odoo_postgres psql -U odoo -c "CREATE DATABASE odoo_db OWNER odoo;"

# Restore
docker exec -i odoo_postgres psql -U odoo odoo_db < backup_20260313.sql
```

#### From Volume Backup
```bash
# Stop Odoo
docker-compose down

# Restore volume
docker run --rm \
  -v odoo_postgresql_data:/data \
  -v $(pwd)/backup:/backup \
  alpine tar xzf /backup/db_volume.tar.gz -C /data

# Start Odoo
docker-compose up -d
```

### Automated Backup Script

Create `backup_odoo.bat`:

```batch
@echo off
set BACKUP_DIR=F:\hackthone_0\odoo\backups
set DATE=%date:~-4%%date:~3,2%%date:~0,2%

mkdir "%BACKUP_DIR%" 2>nul

echo Backing up Odoo database...
docker exec odoo_postgres pg_dump -U odoo odoo_db > "%BACKUP_DIR%\backup_%DATE%.sql"

echo Backup completed: %BACKUP_DIR%\backup_%DATE%.sql
```

---

## Troubleshooting

### Database Connection Error

**Symptom:** Odoo shows "Could not connect to database"

**Solutions:**
```bash
# 1. Check if DB container is running
docker-compose ps db

# 2. Check DB logs
docker-compose logs db

# 3. Restart DB container
docker-compose restart db

# 4. Verify network connectivity
docker exec odoo_community ping -c 3 db
```

### Database Already Exists Error

**Symptom:** Cannot create database, already exists

**Solution:**
```bash
# Drop existing database
docker exec -it odoo_postgres psql -U odoo -c "DROP DATABASE IF EXISTS odoo_db;"

# Recreate via web interface
# Visit http://localhost:8069
```

### Corrupted Database

**Symptom:** Odoo starts but shows errors

**Solutions:**
```bash
# 1. Try to repair
docker exec -it odoo_postgres psql -U odoo -d odoo_db -c "REINDEX DATABASE odoo_db;"

# 2. Restore from backup
# (See backup & recovery section)

# 3. Reset completely (WARNING: Deletes all data!)
docker-compose down -v
docker-compose up -d
```

### Slow Database Performance

**Solutions:**
```bash
# 1. Check slow queries
docker exec -it odoo_postgres psql -U odoo -d odoo_db -c "
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes'
ORDER BY duration DESC;
"

# 2. Vacuum and analyze
docker exec -it odoo_postgres psql -U odoo -d odoo_db -c "VACUUM ANALYZE;"

# 3. Check table bloat
docker exec -it odoo_postgres psql -U odoo -d odoo_db -c "
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;
"
```

### Access Denied Error

**Symptom:** "role does not exist" or "password authentication failed"

**Solution:**
```bash
# Reset PostgreSQL password
docker exec -it odoo_postgres psql -U postgres -c "
ALTER USER odoo WITH PASSWORD 'odoo_password';
"

# Update odoo.conf if needed
# config/odoo.conf:
# db_password = odoo_password

# Restart Odoo
docker-compose restart odoo
```

---

## Quick Reference Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f odoo
docker-compose logs -f db

# Restart services
docker-compose restart

# Access PostgreSQL shell
docker exec -it odoo_postgres psql -U odoo -d odoo_db

# Access Odoo shell
docker exec -it odoo_community odoo shell -d odoo_db

# Check database size
docker exec -it odoo_postgres psql -U odoo -d odoo_db -c "SELECT pg_size_pretty(pg_database_size('odoo_db'));"

# Backup database
docker exec odoo_postgres pg_dump -U odoo odoo_db > backup.sql

# Restore database
docker exec -i odoo_postgres psql -U odoo odoo_db < backup.sql

# Reset everything (WARNING: Deletes all data!)
docker-compose down -v
```

---

## Related Documentation

- [Odoo README.md](README.md) - General Odoo setup
- [Odoo MCP Server](../Skills/mcp_servers/odoo_mcp_server.py) - Python integration
- [Architecture](../ARCHITECTURE.md) - System architecture

## Resources

- [Odoo ORM Documentation](https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/15/)
- [Odoo JSON-RPC API](https://www.odoo.com/documentation/17.0/developer/reference/external/external-api.html)
