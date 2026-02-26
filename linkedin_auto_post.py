"""
Auto-Post to LinkedIn - Complete Workflow

Generates AI-powered LinkedIn posts and saves them for review and posting.
"""

import sys
import codecs

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from Skills.agent_skills import auto_post_social_media, approve_and_post
from pathlib import Path
import datetime

# Use ASCII-safe symbols
CHECK = "[OK]"
INFO = "[INFO]"

def post_to_linkedin(content: str, require_approval: bool = False):
    """
    Post content to LinkedIn.
    
    Args:
        content: Topic or content to post
        require_approval: If True, creates approval request. If False, posts directly.
    
    Returns:
        Dictionary with post results
    """
    print("="*70)
    print("AUTO-POST TO LINKEDIN")
    print("="*70)
    print()
    
    # Post to LinkedIn (and optionally other platforms)
    result = auto_post_social_media(
        content=content,
        platforms=['linkedin'],
        schedule=False,
        require_approval=require_approval,
        vault_path="."
    )
    
    print(f"\nStatus: {result['status']}")
    
    if result['status'] == 'success':
        print("\n✅ Post created successfully!")
        for post in result.get('posts', []):
            print(f"\nPlatform: {post['platform']}")
            print(f"Post ID: {post['post_id']}")
            print(f"Tracking file: {post['tracking_file']}")
            
            # Read and display the generated content
            if post.get('tracking_file'):
                tracking_file = Path(post['tracking_file'])
                if tracking_file.exists():
                    content_text = tracking_file.read_text(encoding='utf-8')
                    # Extract just the content section
                    if "## Content" in content_text:
                        post_content = content_text.split("## Content")[1].split("##")[0].strip()
                        print(f"\n📝 Generated Content:")
                        print("-"*70)
                        print(post_content)
                        print("-"*70)
    
    elif result['status'] == 'pending_approval':
        print(f"\n⏳ Approval required: {result['approval_file']}")
        print("Review the file and run:")
        print(f"   python -m Skills.agent_skills.auto_post_social_media --approve {result['approval_file']}")
    
    print("\n" + "="*70)
    
    return result


def quick_linkedin_post(topic: str):
    """
    Quick LinkedIn post generator.
    
    Args:
        topic: Topic to post about
    """
    print("\n[LINKEDIN] GENERATING POST...")
    print()
    
    result = post_to_linkedin(topic, require_approval=False)
    
    print("\nNEXT STEPS:")
    print("1. Copy the generated content above")
    print("2. Go to LinkedIn: https://www.linkedin.com/")
    print("3. Click 'Start a post'")
    print("4. Paste and post!")
    print("5. Update the tracking file with engagement metrics")
    
    return result


def scheduled_linkedin_post(topic: str):
    """
    Schedule a LinkedIn post for later (creates approval request).
    
    Args:
        topic: Topic to post about
    """
    print("\n🔗 CREATING LINKEDIN POST (WITH APPROVAL)...")
    print()
    
    result = post_to_linkedin(topic, require_approval=True)
    
    return result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Get topic from command line
        topic = " ".join(sys.argv[1:])
        quick_linkedin_post(topic)
    else:
        # Demo mode
        print("="*70)
        print("LINKEDIN AUTO-POST - DEMO MODE")
        print("="*70)
        print()
        print("Usage:")
        print("   python -m Skills.agent_skills.auto_post_social_media \"Your topic here\"")
        print()
        print("Example:")
        print("   python -m Skills.agent_skills.auto_post_social_media \"AI automation tips\"")
        print()
        print("="*70)
        
        # Run demo
        demo_topic = "Excited to share our AI Employee project! 🚀 #AI #Automation"
        print(f"\nRunning demo with topic: {demo_topic}")
        print()
        quick_linkedin_post(demo_topic)
