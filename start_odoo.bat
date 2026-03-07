@echo off
REM Start Odoo with Docker Compose
REM Gold Tier - Odoo Setup Script

echo ========================================
echo  Gold Tier - Starting Odoo Services
echo ========================================
echo.

cd /d "%~dp0odoo"

echo Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not running!
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo Docker is running. Starting Odoo...
echo.

docker-compose up -d

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start Odoo services!
    echo Check Docker Desktop is running and try again.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Odoo Services Starting...
echo ========================================
echo.
echo Waiting for Odoo to initialize (this takes 2-3 minutes)...
echo.

REM Wait for services to be healthy
:wait_loop
timeout /t 10 /nobreak >nul
docker-compose ps | findstr "odoo_community" | findstr "healthy" >nul 2>&1
if errorlevel 1 (
    echo   Still starting... please wait...
    goto wait_loop
)

echo.
echo ========================================
echo  ✅ Odoo is Ready!
echo ========================================
echo.
echo Access Odoo at: http://localhost:8069
echo.
echo Next Steps:
echo 1. Open http://localhost:8069 in your browser
echo 2. Create a new database
echo 3. Install the Accounting/Invoicing module
echo 4. Configure .env file with Odoo credentials
echo.
echo To view logs: docker-compose logs -f odoo
echo To stop Odoo: docker-compose down
echo.
pause
