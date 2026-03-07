@echo off
REM Test Gold Tier Integrations
REM Gold Tier - Integration Test Script

echo ========================================
echo  Gold Tier Integration Tests
echo ========================================
echo.

cd /d "%~dp0"

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Copy .env.example to .env and configure your credentials.
    echo.
    pause
)

echo Running integration tests...
echo.

REM Test 1: Odoo Connection
echo [Test 1/6] Testing Odoo connection...
python -c "from Skills.mcp_servers.odoo_mcp_server import OdooMCPServer; import os; from dotenv import load_dotenv; load_dotenv(); server = OdooMCPServer(odoo_url=os.getenv('ODOO_URL', 'http://localhost:8069'), db_name=os.getenv('ODOO_DB', 'odoo_db'), username=os.getenv('ODOO_USERNAME', 'admin'), password=os.getenv('ODOO_PASSWORD', '')); print('✅ Odoo MCP Server initialized'); uid = server.authenticate(); print(f'✅ Odoo authenticated! UID: {uid}')" 2>&1
if errorlevel 1 (
    echo ❌ Odoo test failed. Check credentials and connection.
) else (
    echo ✅ Odoo connection test PASSED
)
echo.

REM Test 2: Get Odoo Customers
echo [Test 2/6] Getting Odoo customers...
python -c "from Skills.mcp_servers.odoo_mcp_server import OdooMCPServer; import asyncio; import os; from dotenv import load_dotenv; load_dotenv(); server = OdooMCPServer(odoo_url=os.getenv('ODOO_URL', 'http://localhost:8069'), db_name=os.getenv('ODOO_DB', 'odoo_db'), username=os.getenv('ODOO_USERNAME', 'admin'), password=os.getenv('ODOO_PASSWORD', '')); result = asyncio.run(server.execute_tool('odoo_get_customers', {'limit': 5})); print(result.text)" 2>&1
if errorlevel 1 (
    echo ❌ Odoo customers test failed.
) else (
    echo ✅ Odoo customers test PASSED
)
echo.

REM Test 3: Facebook Connection
echo [Test 3/6] Testing Facebook connection...
python -c "from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer; import os; from dotenv import load_dotenv; load_dotenv(); server = FacebookInstagramMCPServer(page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', '')); print('✅ Facebook MCP Server initialized'); result = asyncio.run(server.execute_tool('get_facebook_posts', {'limit': 1})); print(result.text)" 2>&1
if errorlevel 1 (
    echo ❌ Facebook test failed. Check access token.
) else (
    echo ✅ Facebook connection test PASSED
)
echo.

REM Test 4: Instagram Connection
echo [Test 4/6] Testing Instagram connection...
python -c "from Skills.mcp_servers.facebook_instagram_mcp_server import FacebookInstagramMCPServer; import os; from dotenv import load_dotenv; load_dotenv(); server = FacebookInstagramMCPServer(page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', ''), instagram_business_account_id=os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', '')); print('✅ Instagram MCP Server initialized')" 2>&1
if errorlevel 1 (
    echo ❌ Instagram test failed. Check account ID.
) else (
    echo ✅ Instagram connection test PASSED
)
echo.

REM Test 5: Audit Logger
echo [Test 5/6] Testing Audit Logger...
python Skills/audit_logger.py stats --days 7 2>&1
if errorlevel 1 (
    echo ❌ Audit Logger test failed.
) else (
    echo ✅ Audit Logger test PASSED
)
echo.

REM Test 6: Error Recovery
echo [Test 6/6] Testing Error Recovery system...
python -c "from Skills.error_recovery import error_recovery; print('✅ Error Recovery system initialized'); print(f'Error stats: {error_recovery.get_error_stats()}')" 2>&1
if errorlevel 1 (
    echo ❌ Error Recovery test failed.
) else (
    echo ✅ Error Recovery test PASSED
)
echo.

echo ========================================
echo  Integration Tests Complete!
echo ========================================
echo.
echo Check results above. If any tests failed:
echo 1. Check .env file configuration
echo 2. Verify services are running
echo 3. Check network connectivity
echo.
pause
