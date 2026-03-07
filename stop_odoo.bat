@echo off
REM Stop Odoo Docker Compose services
REM Gold Tier - Odoo Shutdown Script

echo ========================================
echo  Gold Tier - Stopping Odoo Services
echo ========================================
echo.

cd /d "%~dp0odoo"

echo Stopping Odoo containers...
docker-compose down

if errorlevel 1 (
    echo.
    echo ERROR: Failed to stop Odoo services!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  ✅ Odoo Services Stopped
echo ========================================
echo.
echo To start again: start_odoo.bat
echo.
pause
