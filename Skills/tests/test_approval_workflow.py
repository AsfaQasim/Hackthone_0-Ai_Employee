"""
Unit tests for ApprovalWorkflow

Tests approval request creation, approval processing, rejection processing,
and threshold enforcement.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from approval_workflow import ApprovalWorkflow, Action, RiskLevel, ApprovalStatus


class TestApprovalWorkflow:
    """Test suite for ApprovalWorkflow."""
    
    @pytest.fixture
    def temp_vault(self):
        """Create a temporary vault directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def workflow(self, temp_vault):
        """Create an ApprovalWorkflow instance with temp vault."""
        return ApprovalWorkflow(vault_path=temp_vault)
    
    def test_workflow_initialization(self, workflow, temp_vault):
        """Test that workflow initializes correctly."""
        assert workflow.vault_path == Path(temp_vault)
        assert workflow.pending_approval_dir.exists()
        assert workflow.needs_action_dir.exists()
        assert workflow.done_dir.exists()
    
    def test_assess_risk_level_default(self, workflow):
        """Test default risk level assessment."""
        # Email should be medium risk
        risk = workflow.assess_risk_level("send_email", {"to": "test@external.com"})
        assert risk == RiskLevel.MEDIUM
        
        # Payment should be high risk
        risk = workflow.assess_risk_level("create_payment_draft", {"amount": 5000})
        assert risk == RiskLevel.HIGH
        
        # Unknown action should be low risk
        risk = workflow.assess_risk_level("unknown_action", {})
        assert risk == RiskLevel.LOW
    
    def test_assess_risk_level_payment_amount(self, workflow):
        """Test risk assessment based on payment amount."""
        # Small payment
        risk = workflow.assess_risk_level("create_payment_draft", {"amount": 100})
        assert risk == RiskLevel.HIGH  # Payments are always high risk
        
        # Large payment
        risk = workflow.assess_risk_level("create_payment_draft", {"amount": 50000})
        assert risk == RiskLevel.HIGH
    
    def test_requires_approval_medium_risk(self, workflow):
        """Test that medium risk actions require approval."""
        requires = workflow.requires_approval("send_email", {"to": "test@example.com"})
        assert requires is True
    
    def test_requires_approval_high_risk(self, workflow):
        """Test that high risk actions require approval."""
        requires = workflow.requires_approval("create_payment_draft", {"amount": 1000})
        assert requires is True
    
    def test_requires_approval_low_risk(self, workflow):
        """Test that low risk actions don't require approval."""
        requires = workflow.requires_approval("internal_notification", {})
        assert requires is False
    
    def test_create_approval_request(self, workflow):
        """Test creating an approval request file."""
        action = Action(
            id="test_001",
            action_type="send_email",
            tool_name="send_email",
            arguments={"to": "test@example.com", "subject": "Test", "body": "Test body"},
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            created_at=datetime.now(),
            status=ApprovalStatus.PENDING,
            reasoning="Test reasoning"
        )
        
        filepath = workflow.create_approval_request(action)
        
        assert filepath.exists()
        assert filepath.parent == workflow.pending_approval_dir
        assert "approval_send_email" in filepath.name
        
        # Check file content
        content = filepath.read_text()
        assert "approval_id: test_001" in content
        assert "action_type: send_email" in content
        assert "risk_level: medium" in content
        assert "Test reasoning" in content
        assert "test@example.com" in content
    
    def test_approval_request_format(self, workflow):
        """Test that approval request has correct format."""
        action = Action(
            id="test_002",
            action_type="post_to_linkedin",
            tool_name="post_to_linkedin",
            arguments={"content": "Test post", "visibility": "public"},
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            created_at=datetime.now(),
            status=ApprovalStatus.PENDING
        )
        
        filepath = workflow.create_approval_request(action)
        content = filepath.read_text()
        
        # Check required sections
        assert "# Approval Request:" in content
        assert "## Action Details" in content
        assert "## Proposed Action" in content
        assert "## Approval Instructions" in content
        assert "Move this file to /Needs_Action" in content
        assert "Move this file to /Done" in content
    
    def test_process_approval(self, workflow):
        """Test processing an approved action."""
        # Create approval request
        action = Action(
            id="test_003",
            action_type="send_email",
            tool_name="send_email",
            arguments={"to": "test@example.com", "subject": "Test", "body": "Test"},
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            created_at=datetime.now(),
            status=ApprovalStatus.PENDING
        )
        
        approval_file = workflow.create_approval_request(action)
        
        # Process approval
        success = workflow.process_approval(approval_file)
        
        assert success is True
        assert not approval_file.exists()  # File moved from Pending_Approval
        
        # Check file is in Needs_Action
        moved_file = workflow.needs_action_dir / approval_file.name
        assert moved_file.exists()
    
    def test_process_rejection(self, workflow):
        """Test processing a rejected action."""
        # Create approval request
        action = Action(
            id="test_004",
            action_type="send_email",
            tool_name="send_email",
            arguments={"to": "test@example.com", "subject": "Test", "body": "Test"},
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            created_at=datetime.now(),
            status=ApprovalStatus.PENDING
        )
        
        approval_file = workflow.create_approval_request(action)
        
        # Process rejection
        rejection_reason = "Email content needs revision"
        success = workflow.process_rejection(approval_file, rejection_reason)
        
        assert success is True
        assert not approval_file.exists()  # File moved from Pending_Approval
        
        # Check file is in Done
        moved_file = workflow.done_dir / approval_file.name
        assert moved_file.exists()
        
        # Check rejection metadata
        content = moved_file.read_text()
        assert "status: rejected" in content
        assert rejection_reason in content
        assert "**Rejected**:" in content
    
    def test_process_rejection_without_reason(self, workflow):
        """Test processing rejection without a reason."""
        action = Action(
            id="test_005",
            action_type="send_email",
            tool_name="send_email",
            arguments={"to": "test@example.com", "subject": "Test", "body": "Test"},
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            created_at=datetime.now(),
            status=ApprovalStatus.PENDING
        )
        
        approval_file = workflow.create_approval_request(action)
        success = workflow.process_rejection(approval_file)
        
        assert success is True
        moved_file = workflow.done_dir / approval_file.name
        assert moved_file.exists()
    
    def test_block_sensitive_action(self, workflow):
        """Test blocking sensitive actions without approval."""
        # Medium risk action should be blocked
        should_block, reason = workflow.block_sensitive_action(
            "send_email",
            {"to": "test@example.com", "subject": "Test", "body": "Test"}
        )
        
        assert should_block is True
        assert "requires approval" in reason
        assert "medium" in reason
        
        # Low risk action should not be blocked
        should_block, reason = workflow.block_sensitive_action(
            "internal_notification",
            {}
        )
        
        assert should_block is False
        assert reason == ""
    
    def test_get_pending_approvals(self, workflow):
        """Test getting list of pending approvals."""
        # Initially empty
        pending = workflow.get_pending_approvals()
        assert len(pending) == 0
        
        # Create some approval requests with delays to ensure unique timestamps
        import time
        for i in range(3):
            action = Action(
                id=f"test_{i}",
                action_type="send_email",
                tool_name="send_email",
                arguments={"to": f"test{i}@example.com", "subject": "Test", "body": "Test"},
                risk_level=RiskLevel.MEDIUM,
                requires_approval=True,
                created_at=datetime.now(),
                status=ApprovalStatus.PENDING
            )
            workflow.create_approval_request(action)
            time.sleep(1.1)  # Ensure unique timestamps (1 second resolution)
        
        # Check pending count
        pending = workflow.get_pending_approvals()
        assert len(pending) == 3
    
    def test_get_approval_count(self, workflow):
        """Test getting count of pending approvals."""
        assert workflow.get_approval_count() == 0
        
        # Create approval request
        action = Action(
            id="test_count",
            action_type="send_email",
            tool_name="send_email",
            arguments={"to": "test@example.com", "subject": "Test", "body": "Test"},
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            created_at=datetime.now(),
            status=ApprovalStatus.PENDING
        )
        workflow.create_approval_request(action)
        
        assert workflow.get_approval_count() == 1
    
    def test_approval_threshold_enforcement(self, workflow):
        """Test that approval thresholds are enforced correctly."""
        # Test various action types
        test_cases = [
            ("send_email", RiskLevel.MEDIUM, True),
            ("post_to_linkedin", RiskLevel.MEDIUM, True),
            ("create_payment_draft", RiskLevel.HIGH, True),
            ("internal_notification", RiskLevel.LOW, False),
        ]
        
        for action_type, expected_risk, should_require_approval in test_cases:
            risk = workflow.assess_risk_level(action_type, {})
            requires = workflow.requires_approval(action_type, {})
            
            assert risk == expected_risk, f"Risk level mismatch for {action_type}"
            assert requires == should_require_approval, f"Approval requirement mismatch for {action_type}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
