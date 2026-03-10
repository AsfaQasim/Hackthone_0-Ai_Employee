@echo off
REM LinkedIn MCP Auto-Post Batch File
REM Automatically post to LinkedIn using Playwright

echo ================================================================
echo LINKEDIN MCP AUTO-POST
echo ================================================================
echo.

if "%~1"=="" (
    echo Usage: linkedin_mcp_auto_post.bat "Your topic"
    echo.
    echo Example:
    echo   linkedin_mcp_auto_post.bat "AI automation success!"
    echo.
    echo Options:
    echo   --style ^[professional^|casual^|enthusiastic^]
    echo   --headless  ^(Run without showing browser^)
    echo.
    echo To authenticate first:
    echo   linkedin_mcp_auth.bat
    echo.
    echo ================================================================
    pause
    exit /b 1
)

python linkedin_mcp_auto_post.py %*

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================
    echo Post published successfully!
    echo ================================================================
) else (
    echo.
    echo ================================================================
    echo Posting failed. Please check the error message above.
    echo ================================================================
)

pause
