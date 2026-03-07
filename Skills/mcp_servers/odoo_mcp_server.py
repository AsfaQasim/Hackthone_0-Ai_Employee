"""
Odoo MCP Server - Gold Tier

Integrates with self-hosted Odoo Community Edition via JSON-RPC API.
Provides accounting and business management capabilities.

Reference: https://github.com/AlanOgic/mcp-odoo-adv
"""

import logging
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

from .base_mcp_server import BaseMCPServer, Tool, TextContent


class OdooMCPServer(BaseMCPServer):
    """
    Odoo MCP Server for accounting and business management.

    Connects to self-hosted Odoo via JSON-RPC API (Odoo 17+).
    """

    def __init__(
        self,
        name: str = "odoo_mcp_server",
        odoo_url: str = "http://localhost:8069",
        db_name: str = "odoo_db",
        username: str = "admin",
        password: str = "",
        vault_path: str = "."
    ):
        """
        Initialize Odoo MCP Server.

        Args:
            name: Server name
            odoo_url: Odoo instance URL
            db_name: Database name
            username: Odoo username (admin)
            password: Odoo password
            vault_path: Path to vault for tracking
        """
        self.odoo_url = odoo_url.rstrip('/')
        self.db_name = db_name
        self.username = username
        self.password = password
        self.vault_path = Path(vault_path)
        self.tracking_dir = self.vault_path / "Odoo_Tracking"
        self.tracking_dir.mkdir(parents=True, exist_ok=True)
        
        self.jsonrpc_url = f"{self.odoo_url}/jsonrpc"
        self.uid = None  # Authenticated user ID
        self.logger = logging.getLogger("OdooMCPServer")
        
        super().__init__(name)

    def register_tools(self) -> None:
        """Register Odoo tools."""

        # Create invoice tool
        create_invoice_tool = Tool(
            name="odoo_create_invoice",
            description="Create a customer invoice in Odoo",
            inputSchema={
                "type": "object",
                "properties": {
                    "partner_id": {
                        "type": "integer",
                        "description": "Customer ID (or provide partner_name to create)"
                    },
                    "partner_name": {
                        "type": "string",
                        "description": "Customer name (if creating new customer)"
                    },
                    "partner_email": {
                        "type": "string",
                        "description": "Customer email"
                    },
                    "lines": {
                        "type": "array",
                        "description": "Invoice line items",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {"type": "integer"},
                                "name": {"type": "string"},
                                "quantity": {"type": "number"},
                                "price_unit": {"type": "number"}
                            },
                            "required": ["name", "quantity", "price_unit"]
                        }
                    },
                    "invoice_date": {
                        "type": "string",
                        "description": "Invoice date (YYYY-MM-DD)"
                    },
                    "payment_term": {
                        "type": "string",
                        "description": "Payment terms"
                    }
                },
                "required": ["lines"]
            }
        )
        self.add_tool(create_invoice_tool)

        # Create vendor bill tool
        create_bill_tool = Tool(
            name="odoo_create_vendor_bill",
            description="Create a vendor bill in Odoo",
            inputSchema={
                "type": "object",
                "properties": {
                    "partner_id": {
                        "type": "integer",
                        "description": "Vendor ID"
                    },
                    "partner_name": {
                        "type": "string",
                        "description": "Vendor name (if creating new)"
                    },
                    "lines": {
                        "type": "array",
                        "description": "Bill line items",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {"type": "integer"},
                                "name": {"type": "string"},
                                "quantity": {"type": "number"},
                                "price_unit": {"type": "number"}
                            },
                            "required": ["name", "quantity", "price_unit"]
                        }
                    },
                    "bill_date": {
                        "type": "string",
                        "description": "Bill date (YYYY-MM-DD)"
                    }
                },
                "required": ["lines"]
            }
        )
        self.add_tool(create_bill_tool)

        # Get invoices tool
        get_invoices_tool = Tool(
            name="odoo_get_invoices",
            description="Get list of invoices from Odoo",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "enum": ["draft", "posted", "cancel"],
                        "description": "Filter by state"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results"
                    },
                    "partner_id": {
                        "type": "integer",
                        "description": "Filter by customer"
                    }
                }
            }
        )
        self.add_tool(get_invoices_tool)

        # Get customers tool
        get_customers_tool = Tool(
            name="odoo_get_customers",
            description="Get list of customers from Odoo",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results"
                    }
                }
            }
        )
        self.add_tool(get_customers_tool)

        # Get products tool
        get_products_tool = Tool(
            name="odoo_get_products",
            description="Get list of products from Odoo",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results"
                    }
                }
            }
        )
        self.add_tool(get_products_tool)

        # Create partner tool
        create_partner_tool = Tool(
            name="odoo_create_partner",
            description="Create a new customer/vendor in Odoo",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Partner name"
                    },
                    "email": {
                        "type": "string",
                        "description": "Email address"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Phone number"
                    },
                    "is_customer": {
                        "type": "boolean",
                        "description": "Is a customer (default: True)"
                    },
                    "is_supplier": {
                        "type": "boolean",
                        "description": "Is a vendor (default: False)"
                    }
                },
                "required": ["name"]
            }
        )
        self.add_tool(create_partner_tool)

        # Get account summary tool
        get_summary_tool = Tool(
            name="odoo_get_account_summary",
            description="Get accounting summary (revenue, expenses, pending)",
            inputSchema={
                "type": "object",
                "properties": {
                    "period": {
                        "type": "string",
                        "enum": ["week", "month", "quarter", "year"],
                        "description": "Time period"
                    }
                }
            }
        )
        self.add_tool(get_summary_tool)

        # Generic search tool
        search_tool = Tool(
            name="odoo_search_records",
            description="Search records in any Odoo model",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "description": "Odoo model name (e.g., account.move, res.partner)"
                    },
                    "domain": {
                        "type": "array",
                        "description": "Search domain filters"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results"
                    },
                    "fields": {
                        "type": "array",
                        "description": "Fields to return",
                        "items": {"type": "string"}
                    }
                },
                "required": ["model"]
            }
        )
        self.add_tool(search_tool)

    def _jsonrpc_call(self, service: str, method: str, args: List[Any]) -> Any:
        """
        Make JSON-RPC call to Odoo.

        Args:
            service: Service name (common, object)
            method: Method to call
            args: Method arguments

        Returns:
            JSON-RPC response result
        """
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

        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(
                self.jsonrpc_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                error = result["error"]
                raise Exception(f"Odoo error: {error.get('data', {}).get('message', error.get('message', 'Unknown error'))}")
            
            return result.get("result")
            
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to Odoo. Is it running?")
        except requests.exceptions.Timeout:
            raise Exception("Odoo request timed out")
        except Exception as e:
            raise Exception(f"Odoo API error: {str(e)}")

    def authenticate(self) -> int:
        """
        Authenticate with Odoo.

        Returns:
            User ID (uid)

        Raises:
            Exception: If authentication fails
        """
        if self.uid:
            return self.uid

        try:
            uid = self._jsonrpc_call(
                "common",
                "authenticate",
                [self.db_name, self.username, self.password, {}]
            )
            
            if not uid:
                raise Exception("Authentication failed. Check credentials.")
            
            self.uid = uid
            self.logger.info(f"Authenticated with Odoo as user {uid}")
            return uid
            
        except Exception as e:
            self.logger.error(f"Odoo authentication failed: {e}")
            raise

    def _execute_kw(
        self,
        model: str,
        method: str,
        args: List[Any]
    ) -> Any:
        """
        Execute Odoo ORM method.

        Args:
            model: Odoo model name
            method: Method to execute
            args: Method arguments

        Returns:
            Method result
        """
        if not self.uid:
            self.authenticate()

        return self._jsonrpc_call(
            "object",
            "execute_kw",
            [self.db_name, self.uid, self.password, model, method, args]
        )

    def _track_action(self, action_type: str, action_data: Dict[str, Any], result: Any):
        """Track Odoo action in vault"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"odoo_{action_type}_{timestamp}.md"
        filepath = self.tracking_dir / filename

        content = f"""---
type: odoo_{action_type}
timestamp: {datetime.now().isoformat()}
status: success
---

# Odoo {action_type.replace('_', ' ').title()}

**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Model**: {action_data.get('model', 'N/A')}
**Method**: {action_data.get('method', 'N/A')}

## Parameters
```json
{str(action_data.get('params', {}))}
```

## Result
```json
{str(result)}
```
"""

        filepath.write_text(content, encoding='utf-8')
        self.logger.info(f"Tracked Odoo action: {filename}")

    async def handle_tool_call(self, name: str, arguments: Dict[str, Any]) -> TextContent:
        """Handle tool call requests"""
        try:
            if name == "odoo_create_invoice":
                return await self._create_invoice(arguments)
            elif name == "odoo_create_vendor_bill":
                return await self._create_vendor_bill(arguments)
            elif name == "odoo_get_invoices":
                return await self._get_invoices(arguments)
            elif name == "odoo_get_customers":
                return await self._get_customers(arguments)
            elif name == "odoo_get_products":
                return await self._get_products(arguments)
            elif name == "odoo_create_partner":
                return await self._create_partner(arguments)
            elif name == "odoo_get_account_summary":
                return await self._get_account_summary(arguments)
            elif name == "odoo_search_records":
                return await self._search_records(arguments)
            else:
                return TextContent(
                    type="text",
                    text=f"Error: Unknown tool '{name}'"
                )

        except Exception as e:
            error_msg = f"Error executing {name}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return TextContent(
                type="text",
                text=f"Error: {error_msg}"
            )

    async def _create_invoice(self, arguments: Dict[str, Any]) -> TextContent:
        """Create customer invoice"""
        lines = arguments.get('lines', [])
        partner_id = arguments.get('partner_id')
        partner_name = arguments.get('partner_name')
        partner_email = arguments.get('partner_email')
        invoice_date = arguments.get('invoice_date', datetime.now().strftime('%Y-%m-%d'))
        payment_term = arguments.get('payment_term')

        # Create partner if name provided
        if partner_name and not partner_id:
            partner_result = await self._create_partner({
                'name': partner_name,
                'email': partner_email,
                'is_customer': True
            })
            if "Error" not in partner_result.text:
                partner_id = int(partner_result.text.split(':')[-1].strip())

        if not partner_id:
            return TextContent(
                type="text",
                text="Error: Either partner_id or partner_name is required"
            )

        # Prepare invoice lines
        invoice_lines = []
        for line in lines:
            invoice_lines.append((0, 0, {
                'name': line.get('name', 'Service'),
                'quantity': line.get('quantity', 1),
                'price_unit': line.get('price_unit', 0)
            }))

        # Create invoice
        invoice_data = {
            'move_type': 'out_invoice',
            'partner_id': partner_id,
            'invoice_date': invoice_date,
            'invoice_line_ids': invoice_lines
        }

        if payment_term:
            invoice_data['invoice_payment_term_id'] = payment_term

        invoice_id = self._execute_kw('account.move', 'create', [invoice_data])
        
        self._track_action('create_invoice', {
            'model': 'account.move',
            'method': 'create',
            'params': {'partner_id': partner_id, 'lines': lines}
        }, invoice_id)

        return TextContent(
            type="text",
            text=f"Successfully created invoice. Invoice ID: {invoice_id}"
        )

    async def _create_vendor_bill(self, arguments: Dict[str, Any]) -> TextContent:
        """Create vendor bill"""
        lines = arguments.get('lines', [])
        partner_id = arguments.get('partner_id')
        partner_name = arguments.get('partner_name')
        bill_date = arguments.get('bill_date', datetime.now().strftime('%Y-%m-%d'))

        # Create partner if name provided
        if partner_name and not partner_id:
            partner_result = await self._create_partner({
                'name': partner_name,
                'is_supplier': True
            })
            if "Error" not in partner_result.text:
                partner_id = int(partner_result.text.split(':')[-1].strip())

        if not partner_id:
            return TextContent(
                type="text",
                text="Error: Either partner_id or partner_name is required"
            )

        # Prepare bill lines
        bill_lines = []
        for line in lines:
            bill_lines.append((0, 0, {
                'name': line.get('name', 'Expense'),
                'quantity': line.get('quantity', 1),
                'price_unit': line.get('price_unit', 0)
            }))

        # Create bill
        bill_data = {
            'move_type': 'in_invoice',
            'partner_id': partner_id,
            'invoice_date': bill_date,
            'invoice_line_ids': bill_lines
        }

        bill_id = self._execute_kw('account.move', 'create', [bill_data])
        
        self._track_action('create_vendor_bill', {
            'model': 'account.move',
            'method': 'create',
            'params': {'partner_id': partner_id, 'lines': lines}
        }, bill_id)

        return TextContent(
            type="text",
            text=f"Successfully created vendor bill. Bill ID: {bill_id}"
        )

    async def _get_invoices(self, arguments: Dict[str, Any]) -> TextContent:
        """Get list of invoices"""
        domain = []
        
        state = arguments.get('state')
        if state:
            domain.append(('state', '=', state))
        
        partner_id = arguments.get('partner_id')
        if partner_id:
            domain.append(('partner_id', '=', partner_id))

        limit = arguments.get('limit', 10)

        invoices = self._execute_kw('account.move', 'search_read', [
            domain,
            ['name', 'partner_id', 'amount_total', 'state', 'invoice_date', 'payment_state'],
            0,
            limit
        ])

        result_text = f"Found {len(invoices)} invoices:\n\n"
        for inv in invoices:
            partner = inv.get('partner_id', ['Unknown'])[1] if inv.get('partner_id') else 'Unknown'
            result_text += f"- {inv.get('name', 'N/A')}: ${inv.get('amount_total', 0):.2f} ({inv.get('state', 'draft')}) - {partner}\n"

        return TextContent(type="text", text=result_text)

    async def _get_customers(self, arguments: Dict[str, Any]) -> TextContent:
        """Get list of customers"""
        limit = arguments.get('limit', 10)

        customers = self._execute_kw('res.partner', 'search_read', [
            [('customer_rank', '>', 0)],
            ['name', 'email', 'phone', 'city', 'country_id'],
            0,
            limit
        ])

        result_text = f"Found {len(customers)} customers:\n\n"
        for cust in customers:
            result_text += f"- {cust.get('name', 'Unknown')} ({cust.get('email', 'No email')})\n"

        return TextContent(type="text", text=result_text)

    async def _get_products(self, arguments: Dict[str, Any]) -> TextContent:
        """Get list of products"""
        limit = arguments.get('limit', 10)

        products = self._execute_kw('product.template', 'search_read', [
            [('sale_ok', '=', True)],
            ['name', 'list_price', 'default_code'],
            0,
            limit
        ])

        result_text = f"Found {len(products)} products:\n\n"
        for prod in products:
            result_text += f"- {prod.get('name', 'Unknown')}: ${prod.get('list_price', 0):.2f}\n"

        return TextContent(type="text", text=result_text)

    async def _create_partner(self, arguments: Dict[str, Any]) -> TextContent:
        """Create new partner (customer/vendor)"""
        name = arguments.get('name')
        email = arguments.get('email')
        phone = arguments.get('phone')
        is_customer = arguments.get('is_customer', True)
        is_supplier = arguments.get('is_supplier', False)

        if not name:
            return TextContent(
                type="text",
                text="Error: Partner name is required"
            )

        partner_data = {
            'name': name,
            'email': email or '',
            'phone': phone or '',
            'customer_rank': 1 if is_customer else 0,
            'supplier_rank': 1 if is_supplier else 0
        }

        partner_id = self._execute_kw('res.partner', 'create', [partner_data])
        
        self._track_action('create_partner', {
            'model': 'res.partner',
            'method': 'create',
            'params': partner_data
        }, partner_id)

        return TextContent(
            type="text",
            text=f"Successfully created partner. Partner ID: {partner_id}"
        )

    async def _get_account_summary(self, arguments: Dict[str, Any]) -> TextContent:
        """Get accounting summary"""
        period = arguments.get('period', 'month')
        
        # Calculate date range
        from datetime import timedelta
        now = datetime.now()
        if period == 'week':
            start_date = now - timedelta(days=7)
        elif period == 'month':
            start_date = now - timedelta(days=30)
        elif period == 'quarter':
            start_date = now - timedelta(days=90)
        elif period == 'year':
            start_date = now - timedelta(days=365)
        else:
            start_date = now - timedelta(days=30)

        # Get invoices
        invoices = self._execute_kw('account.move', 'search_read', [
            [('move_type', 'in', ['out_invoice', 'in_invoice']), 
             ('state', '=', 'posted'),
             ('invoice_date', '>=', start_date.strftime('%Y-%m-%d'))],
            ['move_type', 'amount_total', 'payment_state'],
            0,
            1000
        ])

        # Calculate totals
        revenue = sum(inv['amount_total'] for inv in invoices if inv['move_type'] == 'out_invoice')
        expenses = sum(inv['amount_total'] for inv in invoices if inv['move_type'] == 'in_invoice')
        pending = sum(inv['amount_total'] for inv in invoices if inv['payment_state'] != 'paid')

        summary = f"""# Accounting Summary - Last {period}

**Period**: {start_date.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}

## Financial Overview

- **Revenue**: ${revenue:,.2f}
- **Expenses**: ${expenses:,.2f}
- **Net Profit**: ${revenue - expenses:,.2f}

## Payment Status

- **Pending Payments**: ${pending:,.2f}
- **Total Invoices**: {len(invoices)}

## Key Metrics

- **Profit Margin**: {(revenue - expenses) / revenue * 100 if revenue > 0 else 0:.1f}%
- **Expense Ratio**: {expenses / revenue * 100 if revenue > 0 else 0:.1f}%
"""

        return TextContent(type="text", text=summary)

    async def _search_records(self, arguments: Dict[str, Any]) -> TextContent:
        """Generic search for any Odoo model"""
        model = arguments.get('model')
        domain = arguments.get('domain', [])
        limit = arguments.get('limit', 10)
        fields = arguments.get('fields')

        if not model:
            return TextContent(
                type="text",
                text="Error: Model name is required"
            )

        records = self._execute_kw(model, 'search_read', [
            domain,
            fields or ['id', 'name', 'create_date'],
            0,
            limit
        ])

        result_text = f"Found {len(records)} records in {model}:\n\n"
        for rec in records:
            result_text += f"- ID {rec.get('id')}: {rec.get('name', 'N/A')}\n"

        return TextContent(type="text", text=result_text)


# Example usage
if __name__ == "__main__":
    import asyncio
    import os
    from dotenv import load_dotenv

    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    async def test_odoo_server():
        """Test Odoo MCP Server"""
        server = OdooMCPServer(
            odoo_url=os.getenv('ODOO_URL', 'http://localhost:8069'),
            db_name=os.getenv('ODOO_DB', 'odoo_db'),
            username=os.getenv('ODOO_USERNAME', 'admin'),
            password=os.getenv('ODOO_PASSWORD', '')
        )

        # List tools
        print("Available Odoo tools:")
        for tool in server.list_tools():
            print(f"  - {tool['name']}: {tool['description']}")

        # Test authentication
        try:
            uid = server.authenticate()
            print(f"\n✅ Authenticated! UID: {uid}")

            # Test get customers
            result = await server.execute_tool("odoo_get_customers", {"limit": 5})
            print(f"\nCustomers: {result.text}")

        except Exception as e:
            print(f"\n❌ Error: {e}")

    asyncio.run(test_odoo_server())
