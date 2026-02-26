"""
LinkedIn Auto-Post CLI

Command-line interface for posting to LinkedIn.
"""

import sys
import codecs
import os
from pathlib import Path

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent / "Skills"))

from agent_skills import auto_post_social_media

def main():
    if len(sys.argv) < 2:
        print("="*70)
        print("LINKEDIN AUTO-POST CLI")
        print("="*70)
        print()
        print("Usage: python linkedin_post_cli.py \"Your topic here\"")
        print()
        print("Example:")
        print("   python linkedin_post_cli.py \"Just completed Silver Tier!\"")
        print("="*70)
        sys.exit(1)
    
    # Get topic from command line
    topic = sys.argv[1]
    
    print(f"\nGenerating LinkedIn post for: {topic}\n")
    
    # Generate post
    result = auto_post_social_media(
        content=topic,
        platforms=['linkedin'],
        schedule=False,
        require_approval=False,
        vault_path="."
    )
    
    print(f"\nStatus: {result['status']}")
    
    if result['status'] == 'success':
        print("\n[OK] Post created successfully!")
        
        for post in result.get('posts', []):
            print(f"\nPlatform: {post['platform']}")
            print(f"Post ID: {post['post_id']}")
            
            # Read and display content
            if post.get('tracking_file'):
                tracking_file = Path(post['tracking_file'])
                if tracking_file.exists():
                    content_text = tracking_file.read_text(encoding='utf-8')
                    
                    # Extract content section
                    if "## Content" in content_text:
                        post_content = content_text.split("## Content")[1].split("##")[0].strip()
                        
                        print("\n" + "="*70)
                        print("GENERATED LINKEDIN POST:")
                        print("="*70)
                        print()
                        print(post_content)
                        print()
                        print("="*70)
                        print()
                        print("COPY THE CONTENT ABOVE AND PASTE TO LINKEDIN!")
                        print()

if __name__ == "__main__":
    main()
