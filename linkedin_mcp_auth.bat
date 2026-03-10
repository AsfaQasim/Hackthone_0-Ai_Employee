@echo off
REM LinkedIn MCP Authentication Batch File
REM Authenticate with LinkedIn for automated posting

echo ================================================================
echo LINKEDIN MCP AUTHENTICATION
echo ================================================================
echo.
echo This will open a browser for you to log in to LinkedIn.
echo Your session will be saved for future automated posting.
echo.

python linkedin_mcp_auth.py %*

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================
    echo Authentication completed successfully!
    echo ================================================================
) else (
    echo.
    echo ================================================================
    echo Authentication failed. Please try again.
    echo ================================================================
)

pause
