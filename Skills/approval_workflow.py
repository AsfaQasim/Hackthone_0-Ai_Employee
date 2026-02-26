"""
Approval Workflow

Implements human-in-the-loop approval for sensitive actions.
Creates approval request files, processes approvals/rejections, and enforces thresholds.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from enum import Enum
import json
import logging
import shutil


class RiskLevel(Enum):
    """Risk levels for actions requiring approval."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ApprovalStatus(Enum):
    """Status of an approval request."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class Action:
    """Represents an action that may require approval."""
    id: str
    action_type: str  # send_email, post_social, create_invoice, etc.
    tool_name: str
    arguments: Dict[str, Any]
    risk_level: RiskLevel
    requires_approval: bool
    created_at: datetime
    status: ApprovalStatus
    reasoning: Optional[str] = None


class ApprovalWorkflow:
    """
    Manages the approval workflow for sensitive actions.
    
    Creates approval request files in /Pending_Approval, processes approvals
    and rejections, and enforces approval thresholds based on risk levels.
    """
    
    def __init__(self, vault_path: str = "."):
        """
        Initialize the Approval Workflow.
        
        Args:
            vault_path: Path to the Obsidian vault root directory
        """
        self.vault_path = Path(vault_path)
        self.pending_approval_dir = self.vault_path / "Pending_Approval"
        self.needs_action_dir = self.vault_path / "Needs_Action"
        self.done_dir = self.vault_path / "Done"
        
        self.logger = logging.getLogger("approval_workflow")
        
        # Ensure directories exist
        self.pending_approval_dir.mkdir(parents=True, exist_ok=True)
        self.needs_action_dir.mkdir(parents=True, exist_ok=True)
        self.done_dir.mkdir(parents=True, exist_ok=True)
        
        # Define approval thresholds
        self.approval_thresholds = {
            "send_email": RiskLevel.MEDIUM,
            "post_to_linkedin": RiskLevel.MEDIUM,
            "post_to_facebook": RiskLevel.MEDIUM,
            "post_to_instagram": RiskLevel.MEDIUM,
            "post_to_twitter": RiskLevel.MEDIUM,
            "create_invoice_draft": RiskLevel.MEDIUM,
            "create_payment_draft": RiskLevel.HIGH,
            "delete_account": RiskLevel.HIGH,
            "sign_contract": RiskLevel.HIGH,
        }
    
    def assess_risk_level(self, action_type: str, arguments: Dict[str, Any]) -> RiskLevel:
        """
        Assess the risk level of an action.
        
        Args:
            action_type: Type of action (e.g., "send_email")
            arguments: Action arguments
            
        Returns:
            RiskLevel enum value
        """
        # Get default risk level for action type
        default_risk = self.approval_thresholds.get(action_type, RiskLevel.LOW)
        
        # Additional risk assessment logic can be added here
        # For example, check email recipients, payment amounts, etc.
        
        if action_type == "send_email":
            # Check if sending to external domain
            to_address = arguments.get("to", "")
            if "@" in to_address and not to_address.endswith("@internal.com"):
                return RiskLevel.MEDIUM
        
        elif action_type == "create_payment_draft":
            # Check payment amount
            amount = arguments.get("amount", 0)
            if amount > 10000:
                return RiskLevel.HIGH
        
        return default_risk
    
    def requires_approval(self, action_type: str, arguments: Dict[str, Any]) -> bool:
        """
        Determine if an action requires approval.
        
        Args:
            action_type: Type of action
            arguments: Action arguments
            
        Returns:
            True if approval is required, False otherwise
        """
        risk_level = self.assess_risk_level(action_type, arguments)
        
        # Medium and high risk actions require approval
        return risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH]
    
    def create_approval_request(self, action: Action) -> Path:
        """
        Create an approval request file in /Pending_Approval.
        
        Args:
            action: The Action object requiring approval
            
        Returns:
            Path to the created approval request file
        """
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"approval_{action.action_type}_{timestamp}.md"
        filepath = self.pending_approval_dir / filename
        
        # Create approval request content
        content = self._format_approval_request(action)
        
        # Write file
        filepath.write_text(content, encoding='utf-8')
        
        self.logger.info(f"Created approval request: {filepath}")
        return filepath
    
    def _format_approval_request(self, action: Action) -> str:
        """
        Format an approval request as markdown.
        
        Args:
            action: The Action object
            
        Returns:
            Formatted markdown string
        """
        # Format frontmatter
        frontmatter = f"""---
approval_id: {action.id}
created: {action.created_at.isoformat()}
action_type: {action.action_type}
risk_level: {action.risk_level.value}
status: {action.status.value}
---

"""
        
        # Format action details
        action_details = f"""# Approval Request: {action.action_type.replace('_', ' ').title()}

## Action Details
- **Type**: {action.action_type}
- **Tool**: {action.tool_name}
- **Risk Level**: {action.risk_level.value.upper()}
- **Created**: {action.created_at.strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        # Add reasoning if provided
        if action.reasoning:
            action_details += f"""## Reasoning
{action.reasoning}

"""
        
        # Format proposed action
        proposed_action = f"""## Proposed Action
```json
{{
  "tool": "{action.tool_name}",
  "arguments": {json.dumps(action.arguments, indent=2)}
}}
```

"""
        
        # Add approval instructions
        instructions = """## Approval Instructions
- **To approve**: Move this file to /Needs_Action
- **To reject**: Move this file to /Done and add rejection reason below
- **To modify**: Edit the action JSON above, then move to /Needs_Action

## Rejection Reason (if applicable)
<!-- Add rejection reason here if rejecting -->

"""
        
        return frontmatter + action_details + proposed_action + instructions
    
    def process_approval(self, approval_file: Path) -> bool:
        """
        Process an approved action by moving it to /Needs_Action.
        
        Args:
            approval_file: Path to the approval request file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Move file to Needs_Action
            destination = self.needs_action_dir / approval_file.name
            shutil.move(str(approval_file), str(destination))
            
            self.logger.info(f"Approved: {approval_file.name}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error processing approval: {e}", exc_info=True)
            return False
    
    def process_rejection(self, approval_file: Path, rejection_reason: Optional[str] = None) -> bool:
        """
        Process a rejected action by moving it to /Done with metadata.
        
        Args:
            approval_file: Path to the approval request file
            rejection_reason: Optional reason for rejection
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read current content
            content = approval_file.read_text(encoding='utf-8')
            
            # Add rejection metadata
            if rejection_reason:
                rejection_section = f"\n\n## Rejection Reason\n{rejection_reason}\n"
                content += rejection_section
            
            # Update status in frontmatter
            content = content.replace("status: pending", "status: rejected")
            
            # Add rejection timestamp
            rejection_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            content += f"\n**Rejected**: {rejection_time}\n"
            
            # Write updated content
            approval_file.write_text(content, encoding='utf-8')
            
            # Move to Done
            destination = self.done_dir / approval_file.name
            shutil.move(str(approval_file), str(destination))
            
            self.logger.info(f"Rejected: {approval_file.name}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error processing rejection: {e}", exc_info=True)
            return False
    
    def block_sensitive_action(self, action_type: str, arguments: Dict[str, Any]) -> tuple[bool, str]:
        """
        Check if a sensitive action should be blocked (no approval).
        
        Args:
            action_type: Type of action
            arguments: Action arguments
            
        Returns:
            Tuple of (should_block, reason)
        """
        if self.requires_approval(action_type, arguments):
            risk_level = self.assess_risk_level(action_type, arguments)
            return True, f"Action '{action_type}' requires approval (risk level: {risk_level.value})"
        
        return False, ""
    
    def get_pending_approvals(self) -> list[Path]:
        """
        Get all pending approval requests.
        
        Returns:
            List of paths to pending approval files
        """
        return list(self.pending_approval_dir.glob("approval_*.md"))
    
    def get_approval_count(self) -> int:
        """
        Get the count of pending approvals.
        
        Returns:
            Number of pending approval requests
        """
        return len(self.get_pending_approvals())


# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create workflow
    workflow = ApprovalWorkflow()
    
    # Create a test action
    test_action = Action(
        id="action_001",
        action_type="send_email",
        tool_name="send_email",
        arguments={
            "to": "client@example.com",
            "subject": "Test Email",
            "body": "This is a test email."
        },
        risk_level=RiskLevel.MEDIUM,
        requires_approval=True,
        created_at=datetime.now(),
        status=ApprovalStatus.PENDING,
        reasoning="Testing the approval workflow system."
    )
    
    # Create approval request
    approval_file = workflow.create_approval_request(test_action)
    print(f"Created approval request: {approval_file}")
    
    # Check pending approvals
    pending = workflow.get_pending_approvals()
    print(f"Pending approvals: {len(pending)}")
