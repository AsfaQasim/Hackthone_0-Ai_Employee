"""
Complete Gmail Workflow - Reply to Asfa's Email

1. Read email from Inbox
2. AI generates reply
3. MCP Server sends email
"""

import asyncio
from pathlib import Path
import sys
import codecs

# Configure UTF-8 for Windows
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

sys.path.insert(0, str(Path(__file__).parent / "Skills"))

from agent_skills import summarize_task, create_plan, draft_reply
from mcp_servers.email_mcp_server import EmailMCPServer


async def reply_to_asfa():
    """
    Complete workflow to reply to Asfa's email using MCP Server
    """
    
    print("="*70)
    print("GMAIL WORKFLOW - REPLY TO ASFA'S EMAIL")
    print("="*70)
    print()
    
    # STEP 1: Find Asfa's email
    print("[STEP 1] Finding Asfa's email...")
    email_file = Path("Inbox/hello_asfa.md")
    
    if not email_file.exists():
        print("[ERROR] Email not found!")
        return
    
    print(f"[OK] Found: {email_file.name}")
    print()
    
    # STEP 2: AI summarizes the email
    print("[STEP 2] AI summarizing email...")
    summary = summarize_task(str(email_file))
    print(f"Summary: {summary}")
    print()
    
    # STEP 3: AI creates action plan
    print("[STEP 3] AI creating action plan...")
    plan_path = create_plan(str(email_file))
    print(f"Plan created: {plan_path}")
    print()
    
    # STEP 4: AI drafts reply
    print("[STEP 4] AI drafting reply...")
    reply_text = draft_reply(str(email_file), tone="friendly")
    print("AI-Generated Reply:")
    print("-"*70)
    print(reply_text)
    print("-"*70)
    print()
    
    # STEP 5: MCP Server sends the email
    print("[STEP 5] Sending reply via Email MCP Server...")
    print()
    
    # Initialize MCP Server
    server = EmailMCPServer()
    
    # Send email using MCP tool
    print("Calling MCP Server tool: send_email")
    print()
    
    # This is the actual MCP Server call
    result = await server.execute_tool(
        "send_email",
        {
            "to": "asfa.khan@example.com",
            "subject": "Re: Hello - Quick Question",
            "body": reply_text,
            "html": False
        }
    )
    
    print()
    print(f"MCP Server Response: {result.text}")
    print()
    
    # STEP 6: Summary
    print("="*70)
    print("WORKFLOW COMPLETE!")
    print("="*70)
    print()
    print("What happened:")
    print("1. [OK] Found Asfa's email in Inbox/")
    print("2. [OK] AI summarized the email")
    print("3. [OK] AI created action plan")
    print("4. [OK] AI drafted friendly reply")
    print("5. [OK] MCP Server sent the email")
    print()
    print("Email sent to: asfa.khan@example.com")
    print("Subject: Re: Hello - Quick Question")
    print("="*70)


if __name__ == "__main__":
    print("\n[START] Starting complete Gmail + MCP workflow...\n")
    asyncio.run(reply_to_asfa())
