# WhatsApp Quick Guide - Silver Tier ✅

## Authentication Complete! 🎉

Ab aap WhatsApp messages read aur send kar sakte hain.

## Interactive Mode Commands

### 1. Status Check
```
status
```
Yeh check karega ki WhatsApp Web connected hai ya nahi.

### 2. Unread Chats Dekho
```
unread
```
Yeh saare unread chats ki list dikhayega with preview.

### 3. Messages Padhna
```
read ContactName
```

**Examples:**
```
read Anisa
read John Doe
read Mom
```

Yeh last 10 messages dikhayega us contact se.

### 4. Message Bhejna
```
send ContactName Your message here
```

**Examples:**
```
send Anisa Hello, how are you?
send John Doe Thanks for your message
send Mom I'll be home soon
```

### 5. Exit
```
quit
```

---

## Python Code se Use Karna

Agar aap Python code mein use karna chahte hain:

```python
import asyncio
from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer

async def main():
    server = WhatsAppMCPServer()
    
    # 1. Check status
    status = await server.execute_tool("check_whatsapp_status", {})
    print(status.text)
    
    # 2. Get unread chats
    unread = await server.execute_tool("get_unread_whatsapp_chats", {})
    print(unread.text)
    
    # 3. Read messages
    messages = await server.execute_tool("read_whatsapp_messages", {
        "contact": "Anisa",
        "count": 10
    })
    print(messages.text)
    
    # 4. Send message
    result = await server.execute_tool("send_whatsapp_message", {
        "recipient": "Anisa",
        "message": "Hello from AI!"
    })
    print(result.text)
    
    await server.cleanup()

asyncio.run(main())
```

---

## Message Tracking

Jab bhi aap message bhejte hain, automatically track hota hai:

**Location:** `WhatsApp_Sent/whatsapp_TIMESTAMP_RECIPIENT.md`

**Example:**
```
WhatsApp_Sent/whatsapp_20260223_001234_Anisa.md
```

Har sent message ka markdown file banta hai with:
- Recipient name
- Timestamp
- Message content
- Status (✅ Sent or ❌ Failed)

---

## Silver Tier Requirements ✅

✅ **Read WhatsApp messages** - `read ContactName` command
✅ **Send messages through AI** - `send ContactName Message` command
✅ **Automatic tracking** - Messages saved in `WhatsApp_Sent/`
✅ **Unread detection** - `unread` command

---

## Troubleshooting

### "Contact not found"
- Contact ka exact naam use karein jaise WhatsApp mein hai
- Ya phone number use karein: `+923001234567`

### "WhatsApp Web not connected"
- Authentication phir se karein: `python authenticate_whatsapp.py`

### Messages nahi dikh rahe
- Thoda wait karein, page load hone do
- Contact name spelling check karein

---

## Next Steps

1. **Test karein** - Kisi contact ko message bhejo
2. **Verify** - `WhatsApp_Sent/` folder check karein
3. **Integrate** - AI agent ke saath connect karein
4. **Automate** - Automatic responses setup karein

**Silver Tier Complete!** 🎉
