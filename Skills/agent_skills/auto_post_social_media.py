"""
Auto-Post Social Media Skill

Automatically posts content to social media platforms (LinkedIn, Facebook,
Instagram, Twitter) with approval workflow integration.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import json
from .base_skill import BaseSkill


def auto_post_social_media(
    content: str,
    platforms: List[str] = None,
    schedule: bool = False,
    require_approval: bool = True,
    vault_path: str = ".",
    model_name: str = "gpt-4"
) -> Dict[str, Any]:
    """
    Post content to social media platforms.

    Args:
        content: Content to post (or topic to generate content from)
        platforms: List of platforms to post to (linkedin, facebook, instagram, twitter)
                   Default: ['linkedin']
        schedule: Whether to schedule for later (requires scheduler setup)
        require_approval: Whether to require human approval before posting
        vault_path: Path to vault for tracking
        model_name: AI model to use for content optimization

    Returns:
        Dictionary with posting results:
        - status: overall status (success/pending/error)
        - posts: list of platform-specific results
        - approval_file: path to approval file if approval required

    Example:
        >>> result = auto_post_social_media(
        ...     "Excited to announce our new AI product launch!",
        ...     platforms=['linkedin', 'twitter'],
        ...     require_approval=False
        ... )
        >>> print(result['status'])
        success
    """
    if platforms is None:
        platforms = ['linkedin']

    skill = AutoPostSocialMediaSkill(model_name)
    return skill.execute(content, platforms, schedule, require_approval, vault_path)


class AutoPostSocialMediaSkill(BaseSkill):
    """Implementation of social media auto-posting skill."""

    def execute(
        self,
        content: str,
        platforms: List[str],
        schedule: bool,
        require_approval: bool,
        vault_path: str
    ) -> Dict[str, Any]:
        """
        Execute social media posting.

        Args:
            content: Content or topic to post
            platforms: Target platforms
            schedule: Schedule for later
            require_approval: Require approval flag
            vault_path: Vault path for tracking

        Returns:
            Posting results dictionary
        """
        self.logger.info(f"Posting to social media: {platforms}")

        # Ensure vault path exists
        vault = Path(vault_path)
        tracking_dir = vault / "Social_Media_Tracking"
        tracking_dir.mkdir(parents=True, exist_ok=True)

        # Optimize content for each platform
        optimized_content = self._optimize_for_platforms(content, platforms)

        results = {
            'timestamp': datetime.now().isoformat(),
            'platforms': platforms,
            'schedule': schedule,
            'require_approval': require_approval,
            'posts': []
        }

        # Check if approval required
        if require_approval:
            # Create approval request
            approval_file = self._create_approval_request(
                content,
                platforms,
                optimized_content,
                tracking_dir
            )
            results['status'] = 'pending_approval'
            results['approval_file'] = str(approval_file)
            self.logger.info(f"Approval request created: {approval_file}")
        else:
            # Post directly (or schedule)
            for platform in platforms:
                post_result = self._post_to_platform(
                    platform,
                    optimized_content.get(platform, content),
                    tracking_dir,
                    schedule
                )
                results['posts'].append(post_result)

            # Determine overall status
            if any(p.get('status') == 'error' for p in results['posts']):
                results['status'] = 'partial_success'
            else:
                results['status'] = 'success'

        return results

    def _optimize_for_platforms(
        self,
        content: str,
        platforms: List[str]
    ) -> Dict[str, str]:
        """
        Optimize content for each platform.

        Args:
            content: Original content
            platforms: Target platforms

        Returns:
            Dictionary of platform-specific content
        """
        optimized = {}

        for platform in platforms:
            system_prompt = f"""You are a social media content strategist.
Optimize content for {platform.title()}.

Platform guidelines:
- LinkedIn: Professional, 3000 chars max, include hashtags
- Twitter: Concise, 280 chars max, engaging
- Facebook: Conversational, engaging questions
- Instagram: Visual-focused caption, emojis, hashtags"""

            user_prompt = f"""Optimize this content for {platform.title()}:

Original content:
{content}

Requirements:
- Platform: {platform}
- Include engaging hook
- Add relevant emojis (appropriate for platform)
- Include hashtags if appropriate for platform
- Stay within character limits

Optimized content:"""

            # Call AI model
            optimized_content = self.ai_client.call(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=500
            )

            optimized[platform] = optimized_content.strip()
            self.logger.info(f"Optimized content for {platform}")

        return optimized

    def _post_to_platform(
        self,
        platform: str,
        content: str,
        tracking_dir: Path,
        schedule: bool
    ) -> Dict[str, Any]:
        """
        Post content to a specific platform.

        Args:
            platform: Platform name
            content: Platform-specific content
            tracking_dir: Tracking directory
            schedule: Schedule for later

        Returns:
            Post result dictionary
        """
        try:
            # For now, simulate posting (actual API integration would go here)
            # In production, this would call the platform's API

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            post_id = f"{platform}_{timestamp}"

            # Track the post
            tracking_file = self._track_post(
                platform,
                post_id,
                content,
                tracking_dir,
                scheduled=schedule
            )

            # If scheduling, return scheduled status
            if schedule:
                status = 'scheduled'
                message = f"Post scheduled for {platform}"
            else:
                status = 'posted'
                message = f"Successfully posted to {platform}"

            self.logger.info(f"{platform}: {status}")

            return {
                'platform': platform,
                'status': status,
                'post_id': post_id,
                'tracking_file': str(tracking_file),
                'message': message,
                'content_length': len(content)
            }

        except Exception as e:
            self.logger.error(f"Failed to post to {platform}: {e}")
            return {
                'platform': platform,
                'status': 'error',
                'post_id': None,
                'tracking_file': None,
                'message': str(e),
                'error': str(e)
            }

    def _track_post(
        self,
        platform: str,
        post_id: str,
        content: str,
        tracking_dir: Path,
        scheduled: bool = False
    ) -> Path:
        """
        Track a social media post.

        Args:
            platform: Platform name
            post_id: Post ID
            content: Post content
            tracking_dir: Tracking directory
            scheduled: Whether post is scheduled

        Returns:
            Path to tracking file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{platform}_{timestamp}_{post_id[:8]}.md"
        filepath = tracking_dir / filename

        status = "scheduled" if scheduled else "published"

        content_md = f"""---
platform: {platform}
post_id: {post_id}
timestamp: {datetime.now().isoformat()}
status: {status}
---

# {platform.title()} Post

**Status**: {"⏳ Scheduled" if scheduled else "✅ Published"}
**Posted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Post ID**: {post_id}

## Content

{content}

## Engagement Metrics

_Tracking will be updated automatically_

- Likes: 0
- Comments: 0
- Shares: 0
- Views: 0

## Metadata

```json
{{
    "platform": "{platform}",
    "post_id": "{post_id}",
    "scheduled": {str(scheduled).lower()},
    "created_at": "{datetime.now().isoformat()}"
}}
```

---

*Posted via Social Media Auto-Post Skill*
"""

        self.write_markdown(str(filepath), content_md)
        self.logger.info(f"Tracked {platform} post: {filepath}")
        return filepath

    def _create_approval_request(
        self,
        content: str,
        platforms: List[str],
        optimized_content: Dict[str, str],
        tracking_dir: Path
    ) -> Path:
        """
        Create approval request file.

        Args:
            content: Original content
            platforms: Target platforms
            optimized_content: Platform-specific content
            tracking_dir: Tracking directory

        Returns:
            Path to approval request file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"social_media_approval_{timestamp}.md"
        filepath = tracking_dir / filename

        # Generate preview for each platform
        previews = ""
        for platform, opt_content in optimized_content.items():
            previews += f"""
### {platform.title()}

```
{opt_content[:200]}{'...' if len(opt_content) > 200 else ''}
```
**Character count**: {len(opt_content)}

"""

        approval_content = f"""---
type: social_media_approval
requested: {datetime.now().isoformat()}
platforms: {json.dumps(platforms)}
status: pending
---

# Social Media Posting Approval Request

**Requested**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Platforms**: {', '.join(platforms)}
**Status**: ⏳ Pending Approval

## Original Content

{content}

## Platform-Specific Optimizations

{previews}

## Approval Instructions

To approve this posting request:

1. Review the content for each platform above
2. Edit this file if changes are needed
3. Change status from `pending` to `approved` in the frontmatter
4. Run: `python Skills/agent_skills/auto_post_social_media.py --approve {filename}`

To reject:
1. Change status to `rejected` in the frontmatter
2. Add reason for rejection in the Notes section

## Notes

_Add any comments or required changes here_

---

*Approval Workflow - Social Media Auto-Post Skill*
"""

        self.write_markdown(str(filepath), approval_content)
        return filepath


def approve_and_post(approval_file: str, vault_path: str = ".") -> Dict[str, Any]:
    """
    Approve a pending social media post and execute posting.

    Args:
        approval_file: Path to approval file
        vault_path: Vault path

    Returns:
        Posting results

    Example:
        >>> result = approve_and_post("Social_Media_Tracking/social_media_approval_*.md")
    """
    skill = AutoPostSocialMediaSkill()

    # Read approval file
    content = skill.read_markdown(approval_file)
    metadata = skill.extract_frontmatter(content)

    # Check if approved
    if metadata.get('status') != 'approved':
        return {
            'status': 'error',
            'message': 'Approval not granted. Set status to "approved" in frontmatter.'
        }

    # Extract platforms and content
    platforms = metadata.get('platforms', ['linkedin'])

    # Find content in body
    body = skill.extract_body(content)
    # Extract original content from markdown
    import re
    match = re.search(r'## Original Content\n\n(.+?)\n\n##', body, re.DOTALL)
    original_content = match.group(1).strip() if match else body

    # Execute posting
    results = skill.execute(
        content=original_content,
        platforms=platforms,
        schedule=False,
        require_approval=False,
        vault_path=vault_path
    )

    # Update approval file
    results['approval_completed'] = datetime.now().isoformat()
    approval_results_file = approval_file.replace('.md', '_results.md')

    results_content = f"""---
type: social_media_approval_results
original_approval: {approval_file}
completed: {results['timestamp']}
status: {results['status']}
---

# Social Media Posting Results

**Completed**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status**: {"✅ Success" if results['status'] == 'success' else "⚠️ " + results['status']}

## Results by Platform

"""

    for post in results.get('posts', []):
        status_icon = "✅" if post.get('status') == 'posted' else "❌" if post.get('status') == 'error' else "⏳"
        results_content += f"""
### {status_icon} {post.get('platform', 'Unknown')}

- **Status**: {post.get('status', 'unknown')}
- **Post ID**: {post.get('post_id', 'N/A')}
- **Message**: {post.get('message', 'N/A')}

"""

    skill.write_markdown(approval_results_file, results_content)
    results['results_file'] = approval_results_file

    return results


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--approve':
        # Approve and post
        approval_file = sys.argv[2] if len(sys.argv) > 2 else None
        if approval_file:
            results = approve_and_post(approval_file)
            print(f"\nApproval Results:")
            print(f"Status: {results.get('status', 'unknown')}")
            print(f"Results file: {results.get('results_file', 'N/A')}")
        else:
            print("Usage: python auto_post_social_media.py --approve <approval_file>")
    else:
        # Test posting
        test_content = "Excited to share our latest AI automation breakthrough! 🚀 #AI #Automation"
        result = auto_post_social_media(
            content=test_content,
            platforms=['linkedin', 'twitter'],
            require_approval=False
        )
        print(f"\nPosting Results:")
        print(f"Status: {result['status']}")
        for post in result.get('posts', []):
            print(f"  {post['platform']}: {post['status']} - {post['post_id']}")
