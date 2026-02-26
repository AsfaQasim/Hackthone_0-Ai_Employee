"""
Example Usage of Agent Skills System

Demonstrates how to use all four agent skills independently.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_skills import (
    summarize_task,
    create_plan,
    draft_reply,
    generate_linkedin_post
)


def demo_summarize_task():
    """Demonstrate task summarization."""
    print("\n" + "="*60)
    print("DEMO 1: Summarize Task")
    print("="*60)
    
    # Create a sample task file
    sample_task = """---
email_id: "test123"
sender: "John Doe <john@example.com>"
sender_email: "john@example.com"
sender_name: "John Doe"
subject: "Q1 Report Review Needed"
date: "2026-02-19T09:30:00Z"
priority: "high"
type: "email_task"
---

# Email: Q1 Report Review Needed

**From**: John Doe <john@example.com>
**Priority**: High

## Email Content

Hi there,

Could you please review the Q1 financial report by end of this week? 
We need to present it to the board on Monday.

The report includes:
- Revenue analysis
- Expense breakdown
- Profit margins
- Growth projections

Let me know if you have any questions.

Thanks,
John
"""
    
    # Write sample task
    task_path = "test_task.md"
    with open(task_path, 'w') as f:
        f.write(sample_task)
    
    # Summarize the task
    print(f"\nSummarizing task from: {task_path}")
    summary = summarize_task(task_path, max_length=100)
    
    print(f"\nSummary:\n{summary}")
    
    # Cleanup
    Path(task_path).unlink()


def demo_create_plan():
    """Demonstrate plan creation."""
    print("\n" + "="*60)
    print("DEMO 2: Create Plan")
    print("="*60)
    
    # Create a sample task
    sample_task = """---
type: "project_task"
priority: "high"
subject: "Launch New Product Feature"
---

# Task: Launch New Product Feature

We need to launch the new AI-powered analytics feature by end of Q1.

Requirements:
- Complete development and testing
- Prepare marketing materials
- Train sales team
- Coordinate with customer success

Deadline: March 31, 2026
"""
    
    task_path = "test_project.md"
    with open(task_path, 'w') as f:
        f.write(sample_task)
    
    # Create plan
    print(f"\nCreating plan from: {task_path}")
    plan_path = create_plan(task_path, output_dir="test_plans")
    
    print(f"\nPlan created: {plan_path}")
    
    # Show plan content
    if Path(plan_path).exists():
        with open(plan_path, 'r') as f:
            plan_content = f.read()
        print(f"\nPlan Preview (first 500 chars):\n{plan_content[:500]}...")
    
    # Cleanup
    Path(task_path).unlink()
    if Path(plan_path).exists():
        Path(plan_path).unlink()
    Path("test_plans").rmdir()


def demo_draft_reply():
    """Demonstrate email reply drafting."""
    print("\n" + "="*60)
    print("DEMO 3: Draft Reply")
    print("="*60)
    
    # Create a sample email task
    sample_email = """---
email_id: "test456"
sender: "Jane Smith <jane@client.com>"
sender_email: "jane@client.com"
sender_name: "Jane Smith"
subject: "Meeting Request for Next Week"
type: "email_task"
source: "gmail"
---

# Email: Meeting Request for Next Week

**From**: Jane Smith <jane@client.com>

## Email Content

Hi,

I'd like to schedule a meeting next week to discuss the project timeline 
and deliverables. 

Would Tuesday or Wednesday afternoon work for you?

Looking forward to connecting.

Best,
Jane
"""
    
    task_path = "test_email.md"
    with open(task_path, 'w') as f:
        f.write(sample_email)
    
    # Draft reply with different tones
    print(f"\nDrafting replies from: {task_path}\n")
    
    for tone in ["professional", "friendly"]:
        print(f"\n--- {tone.upper()} TONE ---")
        reply = draft_reply(task_path, tone=tone)
        print(reply)
    
    # Cleanup
    Path(task_path).unlink()


def demo_generate_linkedin_post():
    """Demonstrate LinkedIn post generation."""
    print("\n" + "="*60)
    print("DEMO 4: Generate LinkedIn Post")
    print("="*60)
    
    topics = [
        ("AI automation in business", "thought-leadership"),
        ("Team productivity tips", "professional"),
        ("My journey learning Python", "storytelling")
    ]
    
    for topic, style in topics:
        print(f"\n--- Topic: {topic} (Style: {style}) ---")
        post = generate_linkedin_post(
            topic=topic,
            style=style,
            include_hashtags=True,
            max_length=500  # Shorter for demo
        )
        print(post)
        print(f"\nLength: {len(post)} characters")


def demo_all_skills():
    """Run all skill demonstrations."""
    print("\n" + "="*70)
    print(" "*15 + "AGENT SKILLS SYSTEM DEMO")
    print("="*70)
    print("\nThis demo shows all four agent skills in action:")
    print("1. summarize_task - Generate task summaries")
    print("2. create_plan - Create execution plans")
    print("3. draft_reply - Draft email replies")
    print("4. generate_linkedin_post - Create LinkedIn content")
    
    try:
        demo_summarize_task()
        demo_create_plan()
        demo_draft_reply()
        demo_generate_linkedin_post()
        
        print("\n" + "="*70)
        print(" "*20 + "DEMO COMPLETE!")
        print("="*70)
        print("\nAll skills executed successfully.")
        print("Check the output above to see the results.")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    demo_all_skills()
