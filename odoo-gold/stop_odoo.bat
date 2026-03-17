@echo off
echo Stopping Odoo Gold Tier...
cd /d "%~dp0"
docker compose down
echo Done.
pause
