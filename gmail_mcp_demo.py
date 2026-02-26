"""
Gmail Watcher + Email MCP Server - Complete Workflow

Shows how Gmail Watcher creates tasks and MCP Server sends emails.
"""

import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "Skills"))

from agent_skills import summarize_task, create_plan, draft_reply
from mcp_servers.email_mcp_server import EmailMCPServer


async def process_gmail_and_respond():
    """
    Complete workflow:
    1. Gmail Watcher creates tasks
    2. AI processes tasks
    3. MCP Server sends replies
    """
    
    print("="*70)
    print("GMAIL WATCHER + EMAIL MCP SERVER - COMPLETE WORKFLOW")
    print("="*70)
    print()
    
    # STEP 1: Check for new emails in Inbox
    print("[STEP 1] Checking Inbox for tasks...")
    inbox_folder = Path("Inbox")
    
    if not inbox_folder.exists():
        print("[INFO] No Inbox folder found. Run Gmail Watcher first:")
        print("   python Skills/gmail_watcher.py poll")
        return
    
    email_tasks = list(inbox_folder.glob("*.md"))
    
    if not email_tasks:
        print("[INFO] No email tasks found. Run Gmail Watcher first:")
        print("   python Skills/gmail_watcher.py poll")
        return
    
    print(f"[OK] Found {len(email_tasks)} email tasks")
    print()
    
    # STEP 2: Process each email with AI
    print("[STEP 2] Processing emails with AI...")
    print()
    
    for email_file in email_tasks[:3]:  # Process first 3 emails
        print(f"Processing: {email_file.name}")
        
        # AI summarizes
        summary = summarize_task(str(email_file))
        print(f"  Summary: {summary[:100]}...")
        
        # AI drafts reply
        reply = draft_reply(str(email_file), tone="professional")
        print(f"  Reply drafted: {len(reply)} characters")
        print()
    
    print("[OK] AI processing complete")
    print()
    
    # STEP 3: Send replies using Email MCP Server
    print("[STEP 3] Sending replies via Email MCP Server...")
    print()
    
    # Initialize MCP server
    server = EmailMCPServer()
    
    # Example: Send a test email
    print("Example: Sending email via MCP Server...")
    print()
    
    # This would actually send an email (commented out for safety)
    # Uncomment to actually send:
    """
    result = await server.execute_tool(
        "send_email",
        {
            "to": "recipient@example.com",
            "subject": "Test from Gmail Watcher + MCP",
            "body": "This email was sent automatically using Gmail Watcher and MCP Server!"
        }
    )
    print(result.text)
    """
    
    print("[INFO] Email MCP Server is ready to send emails")
    print("[INFO] To actually send, uncomment the send_email code above")
    print()
    
    await server.cleanup()
    
    # STEP 4: Summary
    print("="*70)
    print("WORKFLOW COMPLETE")
    print("="*70)
    print()
    print("What happened:")
    print("1. ✅ Gmail Watcher created tasks in Inbox/")
    print("2. ✅ AI processed tasks (summarize, draft reply)")
    print("3. ✅ Email MCP Server ready to send replies")
    print()
    print("Next steps:")
    print("   - Review AI-drafted replies")
    print("   - Send using MCP Server (uncomment code)")
    print("   - Or send manually via Gmail")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(process_gmail_and_respond())
