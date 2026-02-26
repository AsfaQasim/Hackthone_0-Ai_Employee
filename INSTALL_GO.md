# Install Go for WhatsApp MCP Server

## Quick Install Steps

1. **Download Go Installer**
   - Visit: https://go.dev/dl/
   - Download: `go1.23.x.windows-amd64.msi` (latest version)
   - File size: ~150 MB

2. **Install Go**
   - Double-click the downloaded `.msi` file
   - Follow the installation wizard
   - Default location: `C:\Program Files\Go`
   - Installer will automatically add Go to PATH

3. **Verify Installation**
   ```cmd
   go version
   ```
   Should show: `go version go1.23.x windows/amd64`

4. **After Installing Go**
   Run these commands to set up WhatsApp MCP:
   ```cmd
   cd whatsapp-mcp\whatsapp-bridge
   go mod download
   go run main.go
   ```

5. **Scan QR Code**
   - QR code will appear in terminal
   - Open WhatsApp on phone
   - Go to Settings > Linked Devices > Link a Device
   - Scan the QR code

## Why We Need Go

The WhatsApp MCP server has two parts:
1. **Go Bridge** - Connects to WhatsApp Web API (needs Go)
2. **Python MCP Server** - Provides tools for AI (already have Python)

Without Go, we can't use the proper WhatsApp MCP server.

## Alternative: Use Existing Playwright Scripts

If you don't want to install Go right now, we can improve the Playwright automation scripts to work better. But the MCP server is more reliable and proper.

## Download Link

Direct download: https://go.dev/dl/go1.23.6.windows-amd64.msi
