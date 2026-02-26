# WhatsApp Setup Guide - Silver Tier

## Current Status
✅ WhatsApp Watcher implemented
✅ WhatsApp MCP Server implemented  
⏳ Authentication pending

## Steps to Complete Silver Tier

### Step 1: Authenticate WhatsApp
```cmd
python Skills/whatsapp_watcher.py auth
```

Yeh command:
- Chrome browser khol dega
- WhatsApp Web load karega
- QR code dikhayega
- Aapko apne phone se scan karna hoga

### Step 2: Test Message Reading
```cmd
python test_whatsapp_mcp.py
```

Interactive mode mein commands:
- `status` - Connection check karo
- `unread` - Unread chats dekho
- `read ContactName` - Messages padho
- `send ContactName Hello` - Message bhejo

### Step 3: Verify Silver Tier Requirements

Silver Tier Requirements:
1. ✅ **Read Messages**: `read_whatsapp_messages` tool
2. ✅ **Send Messages**: `send_whatsapp_message` tool
3. ✅ **Track Sent Messages**: Vault mein save hote hain
4. ✅ **Unread Detection**: `get_unread_whatsapp_chats` tool

## Available Tools

### 1. send_whatsapp_message
```python
{
    "recipient": "Contact Name or +923001234567",
    "message": "Your message text"
}
```

### 2. read_whatsapp_messages
```python
{
    "contact": "Contact Name",
    "count": 10  # Number of messages to read
}
```

### 3. get_unread_whatsapp_chats
```python
{}  # No parameters needed
```

### 4. check_whatsapp_status
```python
{}  # No parameters needed
```

## Integration with AI

WhatsApp MCP Server ko AI ke saath integrate karne ke liye:

```python
from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer

# Initialize
server = WhatsAppMCPServer()

# AI can call these tools:
# 1. Check unread messages
unread = await server.execute_tool("get_unread_whatsapp_chats", {})

# 2. Read specific chat
messages = await server.execute_tool("read_whatsapp_messages", {
    "contact": "John Doe",
    "count": 5
})

# 3. Send reply
response = await server.execute_tool("send_whatsapp_message", {
    "recipient": "John Doe",
    "message": "Thanks for your message!"
})
```

## Troubleshooting

### Issue: "WhatsApp Web not connected"
**Solution**: Run authentication first
```cmd
python Skills/whatsapp_watcher.py auth
```

### Issue: "No space left on device"
**Solution**: Free up disk space (at least 500MB needed)

### Issue: "Contact not found"
**Solution**: 
- Use exact contact name as shown in WhatsApp
- Or use phone number with country code: +923001234567

## Next Steps

1. **Authenticate** - Scan QR code
2. **Test** - Run test_whatsapp_mcp.py
3. **Integrate** - Connect with AI agent
4. **Automate** - Set up automatic message handling

## Silver Tier Completion Checklist

- [ ] WhatsApp authentication successful
- [ ] Can read messages from contacts
- [ ] Can send messages to contacts
- [ ] Messages tracked in vault
- [ ] Can detect unread chats
- [ ] AI can use WhatsApp tools

Once all checked, Silver Tier is complete! 🎉
