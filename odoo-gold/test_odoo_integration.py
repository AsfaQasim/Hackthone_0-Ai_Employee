#!/usr/bin/env python3
"""
Test Odoo MCP Integration - Gold Tier Verification

Tests all Odoo JSON-RPC operations that the MCP server uses.
Run this after setup_odoo.py to verify everything works.
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

ODOO_URL = os.getenv('ODOO_URL', 'http://localhost:8069')
ODOO_DB = os.getenv('ODOO_DB', 'odoo_gold')
ODOO_USERNAME = os.getenv('ODOO_USERNAME', 'admin')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD', 'admin')

JSONRPC_URL = f"{ODOO_URL}/jsonrpc"

passed = 0
failed = 0


def jsonrpc(service, method, args):
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {"service": service, "method": method, "args": args},
        "id": 1
    }
    resp = requests.post(JSONRPC_URL, json=payload, timeout=30)
    result = resp.json()
    if "error" in result:
        raise Exception(result["error"].get("data", {}).get("message", str(result["error"])))
    return result["result"]


def execute_kw(uid, model, method, args, kwargs=None):
    return jsonrpc("object", "execute_kw", [
        ODOO_DB, uid, ODOO_PASSWORD, model, method, args, kwargs or {}
    ])


def test(name, func):
    global passed, failed
    try:
        result = func()
        print(f"  PASS: {name}")
        passed += 1
        return result
    except Exception as e:
        print(f"  FAIL: {name} -> {e}")
        failed += 1
        return None


def main():
    global passed, failed
    print("=" * 55)
    print("  ODOO GOLD TIER - INTEGRATION TEST SUITE")
    print("=" * 55)
    print(f"  URL: {ODOO_URL}")
    print(f"  DB:  {ODOO_DB}")
    print()

    # 1. Connection
    print("[1/8] Connection Test")
    test("Odoo is reachable", lambda: requests.get(f"{ODOO_URL}/web", timeout=10))

    # 2. Version
    print("[2/8] Version Check")
    ver = test("Get server version", lambda: jsonrpc("common", "version", []))
    if ver:
        print(f"        Server: {ver.get('server_version', '?')}")

    # 3. Authentication
    print("[3/8] Authentication")
    uid = test("Authenticate as admin", lambda: jsonrpc("common", "authenticate", [ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {}]))
    if not uid:
        print("\nCannot continue without authentication. Exiting.")
        sys.exit(1)
    print(f"        UID: {uid}")

    # 4. Partners/Customers
    print("[4/8] Partners (Customers/Vendors)")
    customers = test("List customers", lambda: execute_kw(uid, 'res.partner', 'search_read', [
        [('customer_rank', '>', 0)], ['name', 'email']
    ], {'limit': 5}))
    if customers:
        print(f"        Found {len(customers)} customers")

    test("Create test partner", lambda: execute_kw(uid, 'res.partner', 'create', [{
        'name': f'Test Partner {datetime.now().strftime("%H%M%S")}',
        'email': 'test@example.com',
        'customer_rank': 1
    }]))

    # 5. Products
    print("[5/8] Products")
    products = test("List products", lambda: execute_kw(uid, 'product.template', 'search_read', [
        [('sale_ok', '=', True)], ['name', 'list_price']
    ], {'limit': 5}))
    if products:
        print(f"        Found {len(products)} products")

    # 6. Invoices
    print("[6/8] Invoices (account.move)")
    invoices = test("List invoices", lambda: execute_kw(uid, 'account.move', 'search_read', [
        [('move_type', 'in', ['out_invoice', 'in_invoice'])],
        ['name', 'amount_total', 'state', 'move_type', 'partner_id']
    ], {'limit': 10}))
    if invoices:
        revenue = sum(i['amount_total'] for i in invoices if i['move_type'] == 'out_invoice')
        expenses = sum(i['amount_total'] for i in invoices if i['move_type'] == 'in_invoice')
        print(f"        Found {len(invoices)} invoices")
        print(f"        Revenue: ${revenue:,.2f} | Expenses: ${expenses:,.2f}")

    # 7. Accounting Summary (what CEO Briefing uses)
    print("[7/8] Accounting Summary (CEO Briefing Data)")
    now = datetime.now()
    start = (now - timedelta(days=30)).strftime('%Y-%m-%d')

    summary_invoices = test("Get monthly invoices", lambda: execute_kw(uid, 'account.move', 'search_read', [
        [('move_type', 'in', ['out_invoice', 'in_invoice']),
         ('invoice_date', '>=', start)],
        ['move_type', 'amount_total', 'payment_state', 'state']
    ], {'limit': 100}))
    if summary_invoices:
        rev = sum(i['amount_total'] for i in summary_invoices if i['move_type'] == 'out_invoice')
        exp = sum(i['amount_total'] for i in summary_invoices if i['move_type'] == 'in_invoice')
        pending = sum(i['amount_total'] for i in summary_invoices if i.get('payment_state') != 'paid')
        print(f"        Month Revenue: ${rev:,.2f}")
        print(f"        Month Expenses: ${exp:,.2f}")
        print(f"        Pending: ${pending:,.2f}")

    # 8. Generic search
    print("[8/8] Generic Model Search")
    test("Search res.company", lambda: execute_kw(uid, 'res.company', 'search_read', [
        [], ['name', 'currency_id']
    ], {'limit': 1}))

    # Summary
    print()
    print("=" * 55)
    total = passed + failed
    print(f"  Results: {passed}/{total} passed, {failed} failed")
    if failed == 0:
        print("  STATUS: ALL TESTS PASSED!")
        print()
        print("  Odoo is fully integrated and ready for:")
        print("    - MCP Server (Skills/mcp_servers/odoo_mcp_server.py)")
        print("    - CEO Briefing (Skills/ceo_briefing_generator.py)")
        print("    - Weekly Accounting Audit")
    else:
        print("  STATUS: SOME TESTS FAILED - check above for details")
    print("=" * 55)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
