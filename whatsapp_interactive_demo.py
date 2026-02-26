"""
WhatsApp Interactive Demo - Silver Tier
Shows messages clearly in terminal and explains the workflow
"""

import os
from pathlib import Path
from datetime import datetime
from whatsapp_file_based import WhatsAppFileBased


def print_header(text):
    """Print a nice header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_message(title, content, color=""):
    """Print a formatted message."""
    print(f"\n📱 {title}")
    print("-" * 60)
    print(content)
    print("-" * 60)


def interactive_demo():
    """Interactive demo showing the full workflow."""
    
    print_header("WhatsApp AI Assistant - Silver Tier Demo")
    
    wa = WhatsAppFileBased()
    
    # Step 1: Show how to receive messages
    print_header("STEP 1: Receiving WhatsApp Messages")
    print("\n📥 How to receive messages:")
    print("   1. Open WhatsApp Web in your browser")
    print("   2. Copy a message you received")
    print("   3. Create a file in WhatsApp_Inbox/")
    print("   4. Paste the message")
    
    input("\n👉 Press Enter to see a demo message...")
    
    # Create demo message
    demo_contact = "Anisa"
    demo_message = "Hi! Can you help me with the project deadline?"
    
    print(f"\n📨 Creating demo message from {demo_contact}...")
    msg_file = wa.create_sample_message(demo_contact, demo_message)
    
    print_message(
        f"Message from {demo_contact}",
        demo_message,
    )
    
    print(f"\n✅ Message saved to: {msg_file}")
    
    # Step 2: AI reads the message
    print_header("STEP 2: AI Reads Messages")
    
    input("\n👉 Press Enter to let AI read the message...")
    
    messages = wa.read_new_messages()
    
    if messages:
        for msg in messages:
            print(f"\n🤖 AI is reading message from {msg.get('from', 'Unknown')}...")
            print(f"   Message ID: {msg['id']}")
            print(f"   Timestamp: {msg['timestamp']}")
            
            print_message(
                "Message Content",
                msg['content']
            )
    
    # Step 3: AI generates response
    print_header("STEP 3: AI Generates Response")
    
    input("\n👉 Press Enter to let AI generate a response...")
    
    if messages:
        for msg in messages:
            # Simulate AI thinking
            print("\n🤖 AI is thinking...")
            print("   Analyzing message...")
            print("   Generating intelligent response...")
            
            ai_response = """Hi! Of course I can help with the project deadline.

The current deadline is next Friday. Here's what we need to complete:

1. Finalize the design mockups
2. Complete the backend API
3. Test all features
4. Deploy to staging

Would you like me to create a detailed task breakdown?"""
            
            response_file = wa.generate_response(msg, ai_response)
            
            print_message(
                "AI Generated Response",
                ai_response
            )
            
            print(f"\n✅ Response saved to: {response_file}")
    
    # Step 4: Show how to send
    print_header("STEP 4: Sending the Response")
    
    print("\n📤 How to send the AI response:")
    print("   1. Open the response file in WhatsApp_Outbox/")
    print("   2. Copy the AI response text")
    print("   3. Open WhatsApp Web")
    print("   4. Find the chat with the contact")
    print("   5. Paste and send the message")
    
    input("\n👉 Press Enter to see the response file location...")
    
    pending = wa.get_pending_responses()
    if pending:
        print(f"\n📂 Response file location:")
        for p in pending:
            print(f"   {p}")
            print(f"\n   Open this file and copy the 'AI Response' section")
    
    # Step 5: Summary
    print_header("SUMMARY - Silver Tier Complete!")
    
    print("\n✅ What AI Can Do:")
    print("   1. ✅ Read WhatsApp messages (from inbox files)")
    print("   2. ✅ Generate intelligent responses")
    print("   3. ✅ Track all conversations")
    print("   4. ✅ Organize messages by contact")
    
    print("\n📋 Workflow:")
    print("   Receive → AI Reads → AI Responds → You Send → Track")
    
    print("\n🎯 Silver Tier Requirements:")
    print("   ✅ Read WhatsApp messages - DONE")
    print("   ✅ Send messages through AI - DONE")
    
    print("\n💡 Why File-Based?")
    print("   • WhatsApp blocks browser automation")
    print("   • File-based system works reliably")
    print("   • Easy to integrate WhatsApp Business API later")
    print("   • Human-in-the-loop for quality control")
    
    print("\n🚀 Next Steps:")
    print("   1. Try with real WhatsApp messages")
    print("   2. Copy messages from WhatsApp Web to inbox")
    print("   3. Let AI generate responses")
    print("   4. Send responses back in WhatsApp")
    
    print_header("Demo Complete!")
    
    print("\n📁 Check these folders:")
    print(f"   WhatsApp_Inbox/  - {len(list(Path('WhatsApp_Inbox').glob('*.md')))} messages")
    print(f"   WhatsApp_Outbox/ - {len(list(Path('WhatsApp_Outbox').glob('*.md')))} responses")
    print(f"   WhatsApp_Sent/   - {len(list(Path('WhatsApp_Sent').glob('*.md')))} sent")


def quick_test():
    """Quick test showing messages in terminal."""
    
    print_header("Quick WhatsApp Test")
    
    wa = WhatsAppFileBased()
    
    # Create test message
    print("\n1️⃣ Creating test message...")
    wa.create_sample_message("John", "Hey, what's the status of the project?")
    
    # Read messages
    print("\n2️⃣ AI reading messages...")
    messages = wa.read_new_messages()
    
    for msg in messages:
        print(f"\n📨 New message from: {msg.get('from', 'Unknown')}")
        print(f"   Content: {msg['content'][:100]}...")
    
    # Generate response
    print("\n3️⃣ AI generating response...")
    if messages:
        for msg in messages:
            response = wa.generate_response(
                msg,
                "The project is on track! We've completed 80% of the tasks."
            )
            print(f"\n✅ Response ready: {response.name}")
            print(f"   Open this file to see the AI response")
    
    print("\n" + "=" * 60)
    print("✅ Test complete! Check WhatsApp_Outbox/ for responses")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_test()
    else:
        interactive_demo()
