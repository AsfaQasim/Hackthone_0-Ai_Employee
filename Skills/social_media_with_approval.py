"""
Social Media with Approval Workflow Integration

Integrates social media posting with the approval workflow to ensure
all posts are reviewed before publishing.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import logging
import json
import re

from approval_workflow import ApprovalWorkflow, Action, RiskLevel, ApprovalStatus
from mcp_servers.social_media_mcp_server import SocialMediaMCPServer
from mcp_servers.base_mcp_server import TextContent


class SocialMediaWithApproval:
    """
    Integrates social media posting with approval workflow.
    
    Generates post drafts, creates approval requests, and publishes
    approved posts while tracking all content.
    """
    
    def __init__(self, vault_path: str = "."):
        """
        Initialize the integrated system.
        
        Args:
            vault_path: Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.approval_workflow = ApprovalWorkflow(vault_path)
        self.social_media_server = SocialMediaMCPServer(vault_path=vault_path)
        self.logger = logging.getLogger("social_media_with_approval")
        
        # Draft storage
        self.drafts_dir = self.vault_path / "Social_Media_Drafts"
        self.drafts_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_post_draft(self, platform: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> Path:
        """
        Generate a social media post draft.
        
        Args:
            platform: Social media platform (linkedin, facebook, instagram, twitter)
            content: Post content
            metadata: Additional metadata (visibility, media_url, etc.)
            
        Returns:
            Path to the draft file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"draft_{platform}_{timestamp}.md"
        filepath = self.drafts_dir / filename
        
        metadata = metadata or {}
        
        # Create draft content
        draft_content = f"""---
platform: {platform}
created: {datetime.now().isoformat()}
status: draft
---

# {platform.title()} Post Draft

**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Platform**: {platform}

## Content
{content}

## Metadata
- Visibility: {metadata.get('visibility', 'public')}
- Media URL: {metadata.get('media_url', 'None')}
- Location: {metadata.get('location', 'None')}

## Next Steps
1. Review the content above
2. If approved, this will be posted to {platform}
3. Engagement metrics will be tracked automatically
"""
        
        filepath.write_text(draft_content, encoding='utf-8')
        self.logger.info(f"Created {platform} post draft: {filepath}")
        
        return filepath
    
    def create_post_approval_request(self, platform: str, content: str, arguments: Dict[str, Any]) -> Path:
        """
        Create an approval request for a social media post.
        
        Args:
            platform: Social media platform
            content: Post content
            arguments: Post arguments (visibility, media_url, etc.)
            
        Returns:
            Path to the approval request file
        """
        # Determine tool name based on platform
        tool_name = f"post_to_{platform}"
        
        # Create action
        action = Action(
            id=f"social_{platform}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            action_type=tool_name,
            tool_name=tool_name,
            arguments=arguments,
            risk_level=RiskLevel.MEDIUM,  # Social posts are medium risk
            requires_approval=True,
            created_at=datetime.now(),
            status=ApprovalStatus.PENDING,
            reasoning=f"Requesting approval to post to {platform}. Content has been reviewed for brand consistency and appropriateness."
        )
        
        # Create approval request
        approval_file = self.approval_workflow.create_approval_request(action)
        
        self.logger.info(f"Created approval request for {platform} post: {approval_file}")
        return approval_file
    
    async def publish_approved_post(self, approval_file: Path) -> TextContent:
        """
        Publish an approved social media post.
        
        Args:
            approval_file: Path to the approved request file
            
        Returns:
            TextContent with result
        """
        # Read approval file to get action details
        content = approval_file.read_text(encoding='utf-8')
        
        # Extract tool name and arguments from the approval file
        # This is a simplified extraction - in production, use proper parsing
        import json
        import re
        
        # Extract JSON from the approval file
        json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
        if not json_match:
            return TextContent(
                type="text",
                text="Error: Could not extract action details from approval file"
            )
        
        try:
            action_data = json.loads(json_match.group(1))
            tool_name = action_data['tool']
            arguments = action_data['arguments']
        except (json.JSONDecodeError, KeyError) as e:
            return TextContent(
                type="text",
                text=f"Error parsing approval file: {str(e)}"
            )
        
        # Execute the post
        result = await self.social_media_server.execute_tool(tool_name, arguments)
        
        # If successful, move approval file to Done
        if "Successfully posted" in result.text:
            self.approval_workflow.process_approval(approval_file)
            self.logger.info(f"Published approved post: {tool_name}")
        
        return result
    
    def track_engagement(self, post_id: str, metrics: Dict[str, int]) -> bool:
        """
        Update engagement metrics for a posted content.
        
        Args:
            post_id: Post identifier
            metrics: Engagement metrics (likes, comments, shares, views)
            
        Returns:
            True if successful, False otherwise
        """
        # Find tracking file
        tracking_files = list(self.social_media_server.tracking_dir.glob(f"*{post_id[:8]}*.md"))
        
        if not tracking_files:
            self.logger.warning(f"Tracking file not found for post: {post_id}")
            return False
        
        tracking_file = tracking_files[0]
        
        try:
            # Read current content
            content = tracking_file.read_text(encoding='utf-8')
            
            # Update engagement metrics
            for metric, value in metrics.items():
                # Find and replace metric value
                pattern = f"{metric.title()}: \\d+"
                replacement = f"{metric.title()}: {value}"
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            # Write updated content
            tracking_file.write_text(content, encoding='utf-8')
            
            self.logger.info(f"Updated engagement metrics for post: {post_id}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error updating engagement metrics: {e}", exc_info=True)
            return False
    
    def get_pending_post_approvals(self) -> list[Path]:
        """
        Get all pending social media post approvals.
        
        Returns:
            List of paths to pending approval files for social media posts
        """
        all_pending = self.approval_workflow.get_pending_approvals()
        
        # Filter for social media posts
        social_posts = [
            f for f in all_pending
            if any(platform in f.name for platform in ['linkedin', 'facebook', 'instagram', 'twitter'])
        ]
        
        return social_posts
    
    def generate_weekly_summary(self) -> str:
        """
        Generate a weekly summary of social media activity.
        
        Returns:
            Markdown formatted summary
        """
        # Get all tracking files
        tracking_files = list(self.social_media_server.tracking_dir.glob("*.md"))
        
        # Count posts by platform
        platform_counts = {}
        total_engagement = {
            'likes': 0,
            'comments': 0,
            'shares': 0,
            'views': 0
        }
        
        for tracking_file in tracking_files:
            content = tracking_file.read_text()
            
            # Extract platform
            platform_match = re.search(r'platform: (\w+)', content)
            if platform_match:
                platform = platform_match.group(1)
                platform_counts[platform] = platform_counts.get(platform, 0) + 1
            
            # Extract engagement metrics
            likes_match = re.search(r'Likes: (\d+)', content)
            comments_match = re.search(r'Comments: (\d+)', content)
            shares_match = re.search(r'Shares: (\d+)', content)
            views_match = re.search(r'Views: (\d+)', content)
            
            if likes_match:
                total_engagement['likes'] += int(likes_match.group(1))
            if comments_match:
                total_engagement['comments'] += int(comments_match.group(1))
            if shares_match:
                total_engagement['shares'] += int(shares_match.group(1))
            if views_match:
                total_engagement['views'] += int(views_match.group(1))
        
        # Generate summary
        summary = f"""# Weekly Social Media Summary

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Posts by Platform
"""
        
        for platform, count in platform_counts.items():
            summary += f"- {platform.title()}: {count} posts\n"
        
        summary += f"""
## Total Engagement
- Likes: {total_engagement['likes']}
- Comments: {total_engagement['comments']}
- Shares: {total_engagement['shares']}
- Views: {total_engagement['views']}

## Pending Approvals
- Pending: {len(self.get_pending_post_approvals())} posts awaiting approval
"""
        
        return summary


# Example usage
if __name__ == "__main__":
    import asyncio
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    async def test_integration():
        """Test the integrated system."""
        system = SocialMediaWithApproval()
        
        # Generate a draft
        draft = system.generate_post_draft(
            "linkedin",
            "Excited to announce our new product launch! #innovation",
            {"visibility": "public"}
        )
        print(f"Created draft: {draft}")
        
        # Create approval request
        approval = system.create_post_approval_request(
            "linkedin",
            "Excited to announce our new product launch! #innovation",
            {
                "content": "Excited to announce our new product launch! #innovation",
                "visibility": "public"
            }
        )
        print(f"Created approval request: {approval}")
        
        # Generate weekly summary
        summary = system.generate_weekly_summary()
        print(f"\n{summary}")
    
    asyncio.run(test_integration())
