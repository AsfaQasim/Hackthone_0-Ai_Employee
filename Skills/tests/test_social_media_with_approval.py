"""
Unit tests for SocialMediaWithApproval integration

Tests the integration between social media posting and approval workflow.
"""

import pytest
import sys
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media_with_approval import SocialMediaWithApproval


class TestSocialMediaWithApproval:
    """Test suite for SocialMediaWithApproval integration."""
    
    @pytest.fixture
    def temp_vault(self):
        """Create a temporary vault directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def system(self, temp_vault):
        """Create a SocialMediaWithApproval instance with temp vault."""
        return SocialMediaWithApproval(vault_path=temp_vault)
    
    def test_system_initialization(self, system):
        """Test that the integrated system initializes correctly."""
        assert system.approval_workflow is not None
        assert system.social_media_server is not None
        assert system.drafts_dir.exists()
    
    def test_generate_post_draft(self, system):
        """Test generating a social media post draft."""
        draft_file = system.generate_post_draft(
            "linkedin",
            "Test post content",
            {"visibility": "public"}
        )
        
        assert draft_file.exists()
        assert draft_file.parent == system.drafts_dir
        assert "draft_linkedin" in draft_file.name
        
        # Check draft content
        content = draft_file.read_text()
        assert "platform: linkedin" in content
        assert "status: draft" in content
        assert "Test post content" in content
        assert "Visibility: public" in content
    
    def test_generate_post_draft_with_media(self, system):
        """Test generating a draft with media."""
        draft_file = system.generate_post_draft(
            "instagram",
            "Test Instagram post",
            {
                "visibility": "public",
                "media_url": "https://example.com/image.jpg",
                "location": "New York"
            }
        )
        
        content = draft_file.read_text()
        assert "Media URL: https://example.com/image.jpg" in content
        assert "Location: New York" in content
    
    def test_create_post_approval_request(self, system):
        """Test creating an approval request for a post."""
        approval_file = system.create_post_approval_request(
            "linkedin",
            "Test post for approval",
            {
                "content": "Test post for approval",
                "visibility": "public"
            }
        )
        
        assert approval_file.exists()
        assert approval_file.parent == system.approval_workflow.pending_approval_dir
        
        # Check approval content
        content = approval_file.read_text()
        assert "action_type: post_to_linkedin" in content
        assert "risk_level: medium" in content
        assert "Test post for approval" in content
    
    @pytest.mark.asyncio
    async def test_publish_approved_post(self, system):
        """Test publishing an approved post."""
        # Create approval request
        approval_file = system.create_post_approval_request(
            "linkedin",
            "Test approved post",
            {
                "content": "Test approved post",
                "visibility": "public"
            }
        )
        
        # Publish the post
        result = await system.publish_approved_post(approval_file)
        
        assert "Successfully posted to LinkedIn" in result.text
        
        # Check that tracking file was created
        tracking_files = list(system.social_media_server.tracking_dir.glob("linkedin_*.md"))
        assert len(tracking_files) >= 1
    
    def test_get_pending_post_approvals(self, system):
        """Test getting pending social media post approvals."""
        # Initially empty
        pending = system.get_pending_post_approvals()
        assert len(pending) == 0
        
        # Create some approval requests
        system.create_post_approval_request(
            "linkedin",
            "Test post 1",
            {"content": "Test post 1", "visibility": "public"}
        )
        
        system.create_post_approval_request(
            "facebook",
            "Test post 2",
            {"content": "Test post 2", "visibility": "friends"}
        )
        
        # Check pending count
        pending = system.get_pending_post_approvals()
        assert len(pending) == 2
    
    @pytest.mark.asyncio
    async def test_track_engagement(self, system):
        """Test tracking engagement metrics."""
        # Create and publish a post
        approval_file = system.create_post_approval_request(
            "linkedin",
            "Test engagement tracking",
            {
                "content": "Test engagement tracking",
                "visibility": "public"
            }
        )
        
        result = await system.publish_approved_post(approval_file)
        
        # Extract post ID from result
        import re
        post_id_match = re.search(r'Post ID: (\S+)', result.text)
        assert post_id_match is not None
        post_id = post_id_match.group(1)
        
        # Update engagement metrics
        success = system.track_engagement(
            post_id,
            {
                'likes': 42,
                'comments': 5,
                'shares': 3,
                'views': 150
            }
        )
        
        assert success is True
        
        # Verify metrics were updated
        tracking_files = list(system.social_media_server.tracking_dir.glob(f"*{post_id[:8]}*.md"))
        assert len(tracking_files) == 1
        
        content = tracking_files[0].read_text()
        assert "Likes: 42" in content
        assert "Comments: 5" in content
        assert "Shares: 3" in content
        assert "Views: 150" in content
    
    def test_generate_weekly_summary(self, system):
        """Test generating a weekly summary."""
        summary = system.generate_weekly_summary()
        
        assert "# Weekly Social Media Summary" in summary
        assert "## Posts by Platform" in summary
        assert "## Total Engagement" in summary
        assert "## Pending Approvals" in summary
    
    @pytest.mark.asyncio
    async def test_end_to_end_workflow(self, system):
        """Test complete workflow: draft → approval → publish → track."""
        # Step 1: Generate draft
        draft = system.generate_post_draft(
            "linkedin",
            "End-to-end test post",
            {"visibility": "public"}
        )
        assert draft.exists()
        
        # Step 2: Create approval request
        approval = system.create_post_approval_request(
            "linkedin",
            "End-to-end test post",
            {
                "content": "End-to-end test post",
                "visibility": "public"
            }
        )
        assert approval.exists()
        
        # Step 3: Publish approved post
        result = await system.publish_approved_post(approval)
        assert "Successfully posted" in result.text
        
        # Step 4: Verify tracking
        tracking_files = list(system.social_media_server.tracking_dir.glob("linkedin_*.md"))
        assert len(tracking_files) >= 1
        
        # Step 5: Generate summary
        summary = system.generate_weekly_summary()
        assert "Linkedin:" in summary or "LinkedIn:" in summary or "linkedin:" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
