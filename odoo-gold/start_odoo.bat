@echo off
echo ============================================
echo   Starting Odoo Gold Tier (Docker)
echo ============================================
cd /d "%~dp0"
docker compose up -d
echo.
echo Odoo starting at http://localhost:8069
echo Database: odoo_gold
echo Username: admin
echo Password: admin
echo.
echo Run "python setup_odoo.py" to initialize database and sample data.
pause
