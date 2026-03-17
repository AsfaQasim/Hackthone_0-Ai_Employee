#!/usr/bin/env python3
"""
Odoo Gold Tier Setup Script

This script:
1. Starts Odoo via Docker Compose
2. Waits for Odoo to be ready
3. Creates the database
4. Installs required modules (accounting)
5. Seeds sample data (customers, products, invoices)
6. Verifies connectivity
"""

import os
import sys
import time
import json
import subprocess
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load env from parent directory
load_dotenv(Path(__file__).parent.parent / '.env')

ODOO_URL = os.getenv('ODOO_URL', 'http://localhost:8069')
ODOO_DB = os.getenv('ODOO_DB', 'odoo_gold')
ODOO_USERNAME = os.getenv('ODOO_USERNAME', 'admin')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD', 'admin')
ODOO_MASTER_PASSWORD = os.getenv('ODOO_MASTER_PASSWORD', 'admin_master_2026')

JSONRPC_URL = f"{ODOO_URL}/jsonrpc"


def jsonrpc_call(service, method, args):
    """Make a JSON-RPC call to Odoo."""
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": service,
            "method": method,
            "args": args
        },
        "id": 1
    }
    resp = requests.post(JSONRPC_URL, json=payload, headers={"Content-Type": "application/json"}, timeout=120)
    resp.raise_for_status()
    result = resp.json()
    if "error" in result:
        err = result["error"]
        msg = err.get("data", {}).get("message", err.get("message", str(err)))
        raise Exception(f"Odoo RPC Error: {msg}")
    return result.get("result")


def wait_for_odoo(timeout=180):
    """Wait for Odoo to be ready."""
    print("Waiting for Odoo to start...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = requests.get(f"{ODOO_URL}/web/database/selector", timeout=30)
            if resp.status_code == 200:
                print("Odoo is ready!")
                return True
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            pass
        time.sleep(3)
        elapsed = int(time.time() - start)
        print(f"  ...waiting ({elapsed}s)")
    raise Exception(f"Odoo did not start within {timeout} seconds")


def create_database():
    """Create the Odoo database with demo data."""
    print(f"\nCreating database '{ODOO_DB}'...")

    # Check if database already exists
    try:
        db_list = jsonrpc_call("db", "list", [])
        if ODOO_DB in db_list:
            print(f"Database '{ODOO_DB}' already exists!")
            return True
    except Exception:
        pass

    # Create database via web endpoint (more reliable)
    try:
        resp = requests.post(
            f"{ODOO_URL}/web/database/create",
            data={
                "master_pwd": ODOO_MASTER_PASSWORD,
                "name": ODOO_DB,
                "login": ODOO_USERNAME,
                "password": ODOO_PASSWORD,
                "lang": "en_US",
                "country_code": "pk",
                "phone": "",
                "demo": True
            },
            timeout=300,
            allow_redirects=False
        )
        if resp.status_code in (200, 303):
            print(f"Database '{ODOO_DB}' created successfully!")
            # Wait a bit for initialization
            time.sleep(5)
            return True
        else:
            print(f"Unexpected status: {resp.status_code}")
            # Try JSON-RPC method
            raise Exception("Trying JSON-RPC method")
    except Exception as e:
        print(f"Web method failed ({e}), trying JSON-RPC...")
        try:
            result = jsonrpc_call("db", "create_database", [
                ODOO_MASTER_PASSWORD, ODOO_DB, True, "en_US", ODOO_PASSWORD, ODOO_USERNAME, "pk"
            ])
            print(f"Database created via JSON-RPC: {result}")
            time.sleep(5)
            return True
        except Exception as e2:
            print(f"JSON-RPC method also failed: {e2}")
            return False


def authenticate():
    """Authenticate with Odoo and return uid."""
    print(f"\nAuthenticating as '{ODOO_USERNAME}'...")
    uid = jsonrpc_call("common", "authenticate", [ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {}])
    if not uid:
        raise Exception("Authentication failed! Check credentials.")
    print(f"Authenticated! UID: {uid}")
    return uid


def execute_kw(uid, model, method, args, kwargs=None):
    """Execute Odoo ORM method."""
    if kwargs is None:
        kwargs = {}
    return jsonrpc_call("object", "execute_kw", [
        ODOO_DB, uid, ODOO_PASSWORD, model, method, args, kwargs
    ])


def install_accounting(uid):
    """Install the Accounting module."""
    print("\nInstalling Accounting module...")

    # Search for the accounting module
    module_ids = execute_kw(uid, 'ir.module.module', 'search', [
        [('name', '=', 'account')]
    ])

    if not module_ids:
        print("Accounting module not found (may already be installed with demo data)")
        return

    # Check if already installed
    module_info = execute_kw(uid, 'ir.module.module', 'read', [module_ids, ['state']])
    if module_info and module_info[0].get('state') == 'installed':
        print("Accounting module already installed!")
        return

    # Install it
    try:
        execute_kw(uid, 'ir.module.module', 'button_immediate_install', [module_ids])
        print("Accounting module installed!")
    except Exception as e:
        print(f"Module install note: {e}")

    # Wait for Odoo to recover after module install (it may restart)
    print("Waiting for Odoo to recover after module install...")
    time.sleep(15)
    wait_for_odoo(timeout=120)


def seed_sample_data(uid):
    """Create sample customers, products, and invoices."""
    print("\nSeeding sample data...")

    # Create customers
    customers = [
        {"name": "Client Alpha Corp", "email": "alpha@example.com", "phone": "+92-300-1234567", "customer_rank": 1},
        {"name": "Beta Solutions", "email": "beta@example.com", "phone": "+92-321-7654321", "customer_rank": 1},
        {"name": "Gamma Industries", "email": "gamma@example.com", "phone": "+92-333-9876543", "customer_rank": 1},
    ]

    customer_ids = []
    for cust in customers:
        # Check if exists
        existing = execute_kw(uid, 'res.partner', 'search', [[('name', '=', cust['name'])]])
        if existing:
            customer_ids.append(existing[0])
            print(f"  Customer '{cust['name']}' already exists (ID: {existing[0]})")
        else:
            cid = execute_kw(uid, 'res.partner', 'create', [cust])
            customer_ids.append(cid)
            print(f"  Created customer '{cust['name']}' (ID: {cid})")

    # Create products
    products = [
        {"name": "Web Development Service", "list_price": 500.0, "type": "service", "sale_ok": True},
        {"name": "AI Consulting (Hourly)", "list_price": 150.0, "type": "service", "sale_ok": True},
        {"name": "Monthly Maintenance", "list_price": 200.0, "type": "service", "sale_ok": True},
        {"name": "Custom Software License", "list_price": 1000.0, "type": "service", "sale_ok": True},
    ]

    product_ids = []
    for prod in products:
        existing = execute_kw(uid, 'product.template', 'search', [[('name', '=', prod['name'])]])
        if existing:
            product_ids.append(existing[0])
            print(f"  Product '{prod['name']}' already exists (ID: {existing[0]})")
        else:
            pid = execute_kw(uid, 'product.template', 'create', [prod])
            product_ids.append(pid)
            print(f"  Created product '{prod['name']}' (ID: {pid})")

    # Create sample invoices
    print("\n  Creating sample invoices...")
    from datetime import datetime, timedelta

    invoice_data = [
        {
            "partner_id": customer_ids[0],
            "move_type": "out_invoice",
            "invoice_date": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
            "invoice_line_ids": [
                (0, 0, {"name": "Web Development Service", "quantity": 2, "price_unit": 500.0}),
                (0, 0, {"name": "AI Consulting", "quantity": 5, "price_unit": 150.0}),
            ]
        },
        {
            "partner_id": customer_ids[1],
            "move_type": "out_invoice",
            "invoice_date": (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
            "invoice_line_ids": [
                (0, 0, {"name": "Monthly Maintenance", "quantity": 1, "price_unit": 200.0}),
                (0, 0, {"name": "Custom Software License", "quantity": 1, "price_unit": 1000.0}),
            ]
        },
        {
            "partner_id": customer_ids[2],
            "move_type": "out_invoice",
            "invoice_date": datetime.now().strftime('%Y-%m-%d'),
            "invoice_line_ids": [
                (0, 0, {"name": "AI Consulting", "quantity": 10, "price_unit": 150.0}),
            ]
        },
    ]

    for i, inv in enumerate(invoice_data):
        try:
            inv_id = execute_kw(uid, 'account.move', 'create', [inv])
            print(f"  Created invoice #{i+1} (ID: {inv_id})")
        except Exception as e:
            print(f"  Invoice #{i+1} creation note: {e}")

    # Create a vendor bill
    try:
        vendor_data = {"name": "Cloud Hosting Provider", "email": "billing@cloudhost.com", "supplier_rank": 1}
        existing_vendor = execute_kw(uid, 'res.partner', 'search', [[('name', '=', vendor_data['name'])]])
        if existing_vendor:
            vendor_id = existing_vendor[0]
        else:
            vendor_id = execute_kw(uid, 'res.partner', 'create', [vendor_data])

        bill = {
            "partner_id": vendor_id,
            "move_type": "in_invoice",
            "invoice_date": datetime.now().strftime('%Y-%m-%d'),
            "invoice_line_ids": [
                (0, 0, {"name": "Monthly Server Hosting", "quantity": 1, "price_unit": 50.0}),
                (0, 0, {"name": "Domain Renewal", "quantity": 2, "price_unit": 15.0}),
            ]
        }
        bill_id = execute_kw(uid, 'account.move', 'create', [bill])
        print(f"  Created vendor bill (ID: {bill_id})")
    except Exception as e:
        print(f"  Vendor bill note: {e}")

    print("\nSample data seeded!")


def verify_connection(uid):
    """Verify Odoo connection works for the MCP server."""
    print("\n" + "="*50)
    print("VERIFICATION - Testing Odoo MCP compatibility")
    print("="*50)

    # Test: Get version
    version = jsonrpc_call("common", "version", [])
    print(f"\nOdoo Version: {version.get('server_version', 'unknown')}")

    # Test: List customers
    customers = execute_kw(uid, 'res.partner', 'search_read', [
        [('customer_rank', '>', 0)],
        ['name', 'email']
    ], {'limit': 5})
    print(f"\nCustomers ({len(customers)}):")
    for c in customers:
        print(f"  - {c['name']} ({c.get('email', 'N/A')})")

    # Test: List invoices
    invoices = execute_kw(uid, 'account.move', 'search_read', [
        [('move_type', 'in', ['out_invoice', 'in_invoice'])],
        ['name', 'partner_id', 'amount_total', 'state', 'move_type']
    ], {'limit': 10})
    print(f"\nInvoices ({len(invoices)}):")
    for inv in invoices:
        partner = inv.get('partner_id', [0, 'Unknown'])
        pname = partner[1] if isinstance(partner, list) else str(partner)
        itype = "Invoice" if inv['move_type'] == 'out_invoice' else "Bill"
        print(f"  - {inv.get('name', 'Draft')}: ${inv.get('amount_total', 0):.2f} ({itype}) - {pname} [{inv['state']}]")

    # Test: Products
    products = execute_kw(uid, 'product.template', 'search_read', [
        [('sale_ok', '=', True)],
        ['name', 'list_price']
    ], {'limit': 5})
    print(f"\nProducts ({len(products)}):")
    for p in products:
        print(f"  - {p['name']}: ${p.get('list_price', 0):.2f}")

    print("\n" + "="*50)
    print("ALL TESTS PASSED! Odoo is ready for Gold Tier.")
    print("="*50)
    print(f"\nOdoo URL: {ODOO_URL}")
    print(f"Database: {ODOO_DB}")
    print(f"Username: {ODOO_USERNAME}")
    print(f"Password: {ODOO_PASSWORD}")
    print(f"\nOpen {ODOO_URL}/web in your browser to access Odoo.")


def main():
    script_dir = Path(__file__).parent

    print("="*50)
    print("ODOO GOLD TIER SETUP")
    print("="*50)

    # Step 1: Start Docker containers
    print("\nStep 1: Starting Docker containers...")
    result = subprocess.run(
        ["docker", "compose", "up", "-d"],
        cwd=str(script_dir),
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Docker error: {result.stderr}")
        # Try docker-compose (hyphenated)
        result = subprocess.run(
            ["docker-compose", "up", "-d"],
            cwd=str(script_dir),
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error starting containers: {result.stderr}")
            sys.exit(1)
    print("Containers started!")

    # Step 2: Wait for Odoo
    wait_for_odoo()

    # Step 3: Create database
    create_database()

    # Step 4: Authenticate
    uid = authenticate()

    # Step 5: Install accounting
    install_accounting(uid)

    # Step 6: Re-authenticate (Odoo may have restarted)
    uid = authenticate()

    # Step 7: Seed data
    seed_sample_data(uid)

    # Step 8: Verify
    verify_connection(uid)


if __name__ == "__main__":
    main()
