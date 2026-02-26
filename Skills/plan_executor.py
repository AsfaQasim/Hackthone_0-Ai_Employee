"""
Plan Executor

Reads Plan.md files and executes steps sequentially, updating progress.
Integrates with the Ralph Wiggum loop for autonomous multi-step task completion.
"""

import logging
import re
from pathlib import Path
from datetime import datetime, UTC
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import yaml


@dataclass
class PlanExecutorConfig:
    """Configuration for Plan Executor"""
    vault_path: str = "."
    plans_folder: str = "Plans"
    done_folder: str = "Done"
    log_folder: str = "Logs/plan_executor"
    dry_run: bool = False


class PlanExecutor:
    """
    Executes plans from Plan.md files.
    
    Reads plans, executes steps sequentially, and updates progress.
    """
    
    def __init__(self, config: PlanExecutorConfig):
        """
        Initialize the Plan Executor.
        
        Args:
            config: Executor configuration
        """
        self.config = config
        self.vault_path = Path(config.vault_path).absolute()
        self.plans_folder = self.vault_path / config.plans_folder
        self.done_folder = self.vault_path / config.done_folder
        self.logger = self._setup_logging()
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _setup_logging(self) -> logging.Logger:
        """Configure logging"""
        logger = logging.getLogger("PlanExecutor")
        logger.setLevel(logging.INFO)
        
        # Create log directory
        log_dir = Path(self.config.log_folder)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # File handler
        log_file = log_dir / "plan-executor.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            '{"timestamp":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('[PlanExecutor] %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        
        # Set console encoding to UTF-8 for Windows compatibility
        import sys
        if hasattr(sys.stdout, 'reconfigure'):
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except:
                pass  # Ignore if reconfigure fails
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _ensure_directories(self):
        """Create required directories"""
        self.plans_folder.mkdir(parents=True, exist_ok=True)
        self.done_folder.mkdir(parents=True, exist_ok=True)
        Path(self.config.log_folder).mkdir(parents=True, exist_ok=True)
    
    def list_plans(self) -> List[Path]:
        """
        List all plan files in the Plans folder.
        
        Returns:
            List of plan file paths
        """
        try:
            plans = list(self.plans_folder.glob("*.md"))
            self.logger.info(f"Found {len(plans)} plan files")
            return plans
        except Exception as e:
            self.logger.error(f"Failed to list plans: {e}")
            return []
    
    def read_plan(self, plan_path: Path) -> Optional[Dict]:
        """
        Read and parse a plan file.
        
        Args:
            plan_path: Path to plan file
            
        Returns:
            Dictionary with plan metadata and steps
        """
        try:
            content = plan_path.read_text(encoding='utf-8')
            
            # Extract frontmatter
            frontmatter = self._extract_frontmatter(content)
            
            # Extract steps
            steps = self._extract_steps(content)
            
            return {
                'path': plan_path,
                'name': plan_path.stem,
                'frontmatter': frontmatter,
                'steps': steps,
                'content': content
            }
        
        except Exception as e:
            self.logger.error(f"Failed to read plan {plan_path}: {e}")
            return None
    
    def _extract_frontmatter(self, content: str) -> Dict:
        """Extract YAML frontmatter from plan"""
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except yaml.YAMLError as e:
                self.logger.warning(f"Failed to parse frontmatter: {e}")
                return {}
        return {}
    
    def _extract_steps(self, content: str) -> List[Dict]:
        """
        Extract steps from plan content.
        
        Steps are identified by numbered lines or checkboxes.
        
        Returns:
            List of step dictionaries
        """
        steps = []
        
        # Remove frontmatter
        content_without_frontmatter = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        
        # Find numbered steps (e.g., "1. Step description")
        numbered_pattern = r'^\s*(\d+)\.\s+(.+?)$'
        
        # Find checkbox steps (e.g., "- [ ] Step description")
        checkbox_pattern = r'^\s*-\s+\[([ x])\]\s+(.+?)$'
        
        for line in content_without_frontmatter.split('\n'):
            # Check for numbered steps
            match = re.match(numbered_pattern, line)
            if match:
                step_num = int(match.group(1))
                step_text = match.group(2).strip()
                
                # Check if step is sensitive
                is_sensitive = self._is_sensitive_step(step_text)
                
                steps.append({
                    'number': step_num,
                    'text': step_text,
                    'completed': False,
                    'sensitive': is_sensitive,
                    'type': 'numbered'
                })
                continue
            
            # Check for checkbox steps
            match = re.match(checkbox_pattern, line)
            if match:
                is_completed = match.group(1) == 'x'
                step_text = match.group(2).strip()
                
                # Check if step is sensitive
                is_sensitive = self._is_sensitive_step(step_text)
                
                steps.append({
                    'number': len(steps) + 1,
                    'text': step_text,
                    'completed': is_completed,
                    'sensitive': is_sensitive,
                    'type': 'checkbox'
                })
        
        return steps
    
    def _is_sensitive_step(self, step_text: str) -> bool:
        """Check if step contains sensitive keywords"""
        sensitive_patterns = [
            r'\bsend\b', r'\bemail\s+(to|reply)', r'\bpost\b', r'\bpublish\b', 
            r'\bdelete\b', r'\bremove\b', r'\bpay\b', r'\bpayment\b', 
            r'\btransfer\b', r'\binvoice\b', r'\bcharge\b',
            r'\bapprove\b', r'\bauthorize\b', r'\bconfirm\b', r'\bexecute\b'
        ]
        
        text_lower = step_text.lower()
        return any(re.search(pattern, text_lower) for pattern in sensitive_patterns)
    
    def get_next_step(self, plan: Dict) -> Optional[Dict]:
        """
        Get the next incomplete step from a plan.
        
        Args:
            plan: Plan dictionary
            
        Returns:
            Next step dictionary, or None if all complete
        """
        for step in plan['steps']:
            if not step['completed']:
                return step
        return None
    
    def execute_plan(self, plan_path: Path) -> bool:
        """
        Execute a plan file step by step.
        
        Args:
            plan_path: Path to plan file
            
        Returns:
            True if plan completed successfully
        """
        self.logger.info(f"Executing plan: {plan_path.name}")
        
        # Read plan
        plan = self.read_plan(plan_path)
        if not plan:
            return False
        
        # Execute steps
        total_steps = len(plan['steps'])
        completed_steps = sum(1 for s in plan['steps'] if s['completed'])
        
        self.logger.info(f"Plan has {total_steps} steps, {completed_steps} already complete")
        
        while True:
            # Get next step
            next_step = self.get_next_step(plan)
            
            if not next_step:
                self.logger.info("All steps completed!")
                self._mark_plan_complete(plan_path)
                return True
            
            # Execute step
            self.logger.info(f"Executing step {next_step['number']}: {next_step['text']}")
            
            if next_step['sensitive']:
                self.logger.warning(f"[!] Step {next_step['number']} is SENSITIVE - requires approval")
                # In a real implementation, this would create an approval request
                # For now, we'll just log and mark as needing approval
                return False
            
            # Execute the step (placeholder - in real implementation, this would call Claude or MCP)
            success = self._execute_step(next_step)
            
            if success:
                # Mark step as complete
                next_step['completed'] = True
                self._update_plan_progress(plan_path, plan)
                self.logger.info(f"[OK] Step {next_step['number']} completed")
            else:
                self.logger.error(f"[FAIL] Step {next_step['number']} failed")
                return False
        
        return True
    
    def _execute_step(self, step: Dict) -> bool:
        """
        Execute a single step.
        
        This is a placeholder. In a real implementation, this would:
        1. Parse the step text to determine action
        2. Call appropriate MCP server or Claude Code
        3. Verify completion
        
        Args:
            step: Step dictionary
            
        Returns:
            True if step executed successfully
        """
        if self.config.dry_run:
            self.logger.info(f"[DRY RUN] Would execute: {step['text']}")
            return True
        
        # Placeholder: In real implementation, this would execute the actual step
        # For now, we just log it
        self.logger.info(f"Executing: {step['text']}")
        
        # Simulate execution
        import time
        time.sleep(0.5)
        
        return True
    
    def _update_plan_progress(self, plan_path: Path, plan: Dict):
        """
        Update plan file with current progress.
        
        Args:
            plan_path: Path to plan file
            plan: Plan dictionary with updated steps
        """
        if self.config.dry_run:
            self.logger.info(f"[DRY RUN] Would update plan progress")
            return
        
        try:
            content = plan['content']
            
            # Update checkbox steps
            for step in plan['steps']:
                if step['type'] == 'checkbox':
                    # Find the checkbox line and update it
                    checkbox_char = 'x' if step['completed'] else ' '
                    old_pattern = rf'(-\s+\[[ x]\]\s+{re.escape(step["text"])})'
                    new_text = f'- [{checkbox_char}] {step["text"]}'
                    content = re.sub(old_pattern, new_text, content)
            
            # Update frontmatter with progress
            frontmatter = plan['frontmatter']
            total_steps = len(plan['steps'])
            completed_steps = sum(1 for s in plan['steps'] if s['completed'])
            
            frontmatter['progress'] = f"{completed_steps}/{total_steps}"
            frontmatter['last_updated'] = datetime.now(UTC).isoformat() + 'Z'
            
            # Reconstruct content with updated frontmatter
            new_frontmatter = yaml.dump(frontmatter, default_flow_style=False)
            content_without_frontmatter = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
            new_content = f"---\n{new_frontmatter}---\n{content_without_frontmatter}"
            
            # Write back
            plan_path.write_text(new_content, encoding='utf-8')
            self.logger.info(f"Updated plan progress: {completed_steps}/{total_steps}")
        
        except Exception as e:
            self.logger.error(f"Failed to update plan progress: {e}")
    
    def _mark_plan_complete(self, plan_path: Path):
        """
        Mark plan as complete and move to Done folder.
        
        Args:
            plan_path: Path to plan file
        """
        if self.config.dry_run:
            self.logger.info(f"[DRY RUN] Would move plan to Done folder")
            return
        
        try:
            # Move to Done folder
            dest_path = self.done_folder / plan_path.name
            plan_path.rename(dest_path)
            self.logger.info(f"Plan completed and moved to Done: {dest_path}")
        
        except Exception as e:
            self.logger.error(f"Failed to mark plan complete: {e}")
    
    def execute_all_plans(self) -> Dict[str, int]:
        """
        Execute all plans in the Plans folder.
        
        Returns:
            Dictionary with execution statistics
        """
        self.logger.info("Executing all plans...")
        
        stats = {
            'total': 0,
            'completed': 0,
            'failed': 0,
            'pending_approval': 0
        }
        
        plans = self.list_plans()
        stats['total'] = len(plans)
        
        for plan_path in plans:
            try:
                success = self.execute_plan(plan_path)
                if success:
                    stats['completed'] += 1
                else:
                    stats['pending_approval'] += 1
            except Exception as e:
                self.logger.error(f"Failed to execute plan {plan_path.name}: {e}")
                stats['failed'] += 1
        
        self.logger.info(f"Plan execution complete: {stats}")
        return stats


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Plan Executor for AI Employee")
    parser.add_argument(
        "command",
        choices=["list", "execute", "execute-all"],
        help="Command to execute"
    )
    parser.add_argument(
        "--plan",
        help="Plan file name (for execute command)"
    )
    parser.add_argument(
        "--vault-path",
        default=".",
        help="Path to vault root directory"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (no modifications)"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create config
    config = PlanExecutorConfig(
        vault_path=args.vault_path,
        dry_run=args.dry_run
    )
    
    # Create executor
    executor = PlanExecutor(config)
    
    if args.command == "list":
        print("\n" + "="*60)
        print("AVAILABLE PLANS")
        print("="*60 + "\n")
        
        plans = executor.list_plans()
        for plan_path in plans:
            plan = executor.read_plan(plan_path)
            if plan:
                total_steps = len(plan['steps'])
                completed_steps = sum(1 for s in plan['steps'] if s['completed'])
                print(f"[PLAN] {plan['name']}")
                print(f"       Progress: {completed_steps}/{total_steps} steps")
                print()
    
    elif args.command == "execute":
        if not args.plan:
            print("Error: --plan argument required for execute command")
            exit(1)
        
        plan_path = Path(args.vault_path) / "Plans" / args.plan
        if not plan_path.exists():
            print(f"Error: Plan file not found: {plan_path}")
            exit(1)
        
        print("\n" + "="*60)
        print(f"EXECUTING PLAN: {args.plan}")
        print("="*60 + "\n")
        
        success = executor.execute_plan(plan_path)
        if success:
            print("\n[SUCCESS] Plan executed successfully")
        else:
            print("\n[INCOMPLETE] Plan execution incomplete (may require approval)")
    
    elif args.command == "execute-all":
        print("\n" + "="*60)
        print("EXECUTING ALL PLANS")
        print("="*60 + "\n")
        
        stats = executor.execute_all_plans()
        
        print(f"\nExecution Summary:")
        print(f"  Total plans: {stats['total']}")
        print(f"  Completed: {stats['completed']}")
        print(f"  Pending approval: {stats['pending_approval']}")
        print(f"  Failed: {stats['failed']}")
