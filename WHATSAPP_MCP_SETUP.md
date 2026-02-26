# WhatsApp MCP Server Setup Guide

## What is This?

This is a proper WhatsApp MCP server that:
- ✅ Uses WhatsApp Web multidevice API (no tokens needed!)
- ✅ Stores messages locally in SQLite
- ✅ Supports sending/receiving media files
- ✅ More reliable than Playwright automation
- ✅ Works with Claude/AI agents

## Architecture

```
AI Agent (Claude/OpenAI)
    ↓
Python MCP Server (whatsapp-mcp-server/)
    ↓
Go WhatsApp Bridge (whatsapp-bridge/)
    ↓
WhatsApp Web API
```

## Prerequisites

1. **Go** - Download from: https://go.dev/dl/
   - Install Go 1.21 or later
   - Add to PATH

2. **Python** - Already have it
   
3. **uv** (Python package manager) - Install with:
   ```cmd
   pip install uv
   ```

## Installation Steps

### Step 1: Install Go Bridge

```cmd
cd whatsapp-mcp\whatsapp-bridge
go mod download
go build
```

This will create `whatsapp-bridge.exe`

### Step 2: Run Go Bridge (First Time)

```cmd
cd whatsapp-mcp\whatsapp-bridge
go run main.go
```

**You'll see a QR code!** Scan it with your phone:
1. Open WhatsApp on phone
2. Settings > Linked Devices
3. Link a Device
4. Scan the QR code

The bridge will stay running in the background.

### Step 3: Install Python MCP Server

```cmd
cd whatsapp-mcp\whatsapp-mcp-server
uv sync
```

### Step 4: Configure MCP in Kiro

Create or update `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "whatsapp": {
      "command": "uv",
      "args": [
        "--directory",
        "F:/hackthone_0/whatsapp-mcp/whatsapp-mcp-server",
        "run",
        "whatsapp-mcp-server"
      ],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Important**: Update the path `F:/hackthone_0/` to your actual path!

### Step 5: Start Everything

1. **Terminal 1** - Run Go Bridge:
   ```cmd
   cd whatsapp-mcp\whatsapp-bridge
   go run main.go
   ```
   Keep this running!

2. **Terminal 2** - Test MCP Server:
   ```cmd
   cd whatsapp-mcp\whatsapp-mcp-server
   uv run whatsapp-mcp-server
   ```

## Available MCP Tools

Once connected, AI can use these tools:

1. **search_messages** - Search WhatsApp messages
2. **get_messages** - Get messages from a chat
3. **search_contacts** - Find contacts
4. **send_message** - Send text message
5. **send_image** - Send image file
6. **send_video** - Send video file
7. **send_document** - Send document
8. **send_audio** - Send audio file
9. **download_media** - Download received media

## Testing

### Test 1: Check if Bridge is Running

```cmd
curl http://localhost:8080/health
```

Should return: `{"status":"ok"}`

### Test 2: Use MCP Tools

In Kiro, ask:
```
Can you search my WhatsApp messages for "test"?
```

Or:
```
Send a WhatsApp message to Asyfa saying "Hello from AI!"
```

## Troubleshooting

### "Go not found"
Install Go from: https://go.dev/dl/

### "uv not found"
```cmd
pip install uv
```

### "QR code expired"
Restart the Go bridge and scan again

### "Connection refused"
Make sure Go bridge is running in Terminal 1

### "Database locked"
Only one instance of Go bridge can run at a time

## Advantages Over Playwright

| Feature | Playwright (Old) | WhatsApp MCP (New) |
|---------|------------------|-------------------|
| Reliability | ⚠️ Breaks often | ✅ Stable |
| Media Support | ❌ No | ✅ Yes |
| Message Storage | ❌ No | ✅ SQLite |
| Speed | 🐌 Slow | ⚡ Fast |
| AI Integration | ⚠️ Manual | ✅ Native MCP |
| Authentication | 🔄 Expires often | ✅ Persistent |

## Next Steps

1. Install Go
2. Run Go bridge and scan QR code
3. Configure MCP in Kiro
4. Test with AI!

## Silver Tier with WhatsApp MCP

✅ Read messages - `get_messages` tool
✅ Send messages - `send_message` tool  
✅ Track messages - SQLite database
✅ Detect unread - `search_messages` tool
✅ AI Integration - Native MCP support

This is the PROPER way to do WhatsApp automation! 🚀
