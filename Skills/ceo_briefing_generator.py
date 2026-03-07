#!/usr/bin/env python3
"""
CEO Briefing Generator - Gold Tier

Generates weekly business audit and CEO briefing.
Analyzes tasks, revenue, bottlenecks, and provides recommendations.
Now integrated with Odoo for accounting data.
"""

import logging
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os

class CEOBriefingGenerator:
    """
    Generates weekly CEO briefing with:
    - Revenue summary (from Odoo)
    - Completed tasks
    - Bottlenecks
    - Proactive suggestions
    - Accounting metrics
    """

    def __init__(self, vault_path: str = ".", use_odoo: bool = True):
        self.vault_path = Path(vault_path)
        self.done_folder = self.vault_path / "Done"
        self.needs_action = self.vault_path / "Needs_Action"
        self.briefings_folder = self.vault_path / "Briefings"
        self.briefings_folder.mkdir(exist_ok=True)
        self.logger = logging.getLogger("CEOBriefing")
        self.use_odoo = use_odoo
        self.odoo_data = None
        
        # Try to initialize Odoo if enabled
        if self.use_odoo:
            try:
                from .mcp_servers.odoo_mcp_server import OdooMCPServer
                self.odoo_server = OdooMCPServer(
                    odoo_url=os.getenv('ODOO_URL', 'http://localhost:8069'),
                    db_name=os.getenv('ODOO_DB', 'odoo_db'),
                    username=os.getenv('ODOO_USERNAME', 'admin'),
                    password=os.getenv('ODOO_PASSWORD', '')
                )
                self.logger.info("Odoo integration enabled")
            except Exception as e:
                self.logger.warning(f"Odoo not available, using basic mode: {e}")
                self.use_odoo = False
                self.odoo_server = None
    
    def generate_weekly_briefing(self) -> str:
        """Generate complete weekly briefing"""
        self.logger.info("Generating weekly CEO briefing...")

        # Collect data
        completed_tasks = self._analyze_completed_tasks()
        pending_tasks = self._analyze_pending_tasks()
        bottlenecks = self._detect_bottlenecks()
        suggestions = self._generate_suggestions()
        
        # Get Odoo accounting data if available
        accounting_summary = None
        if self.use_odoo and self.odoo_server:
            try:
                accounting_summary = self._get_odoo_accounting_summary()
                self.logger.info("Odoo accounting data retrieved")
            except Exception as e:
                self.logger.warning(f"Failed to get Odoo data: {e}")
                accounting_summary = None

        # Generate briefing
        briefing = self._create_briefing_markdown(
            completed_tasks,
            pending_tasks,
            bottlenecks,
            suggestions,
            accounting_summary
        )

        # Save briefing
        filename = f"{datetime.now().strftime('%Y-%m-%d')}_CEO_Briefing.md"
        filepath = self.briefings_folder / filename
        filepath.write_text(briefing, encoding='utf-8')

        self.logger.info(f"Briefing saved: {filename}")
        return briefing
    
    def _get_odoo_accounting_summary(self) -> Dict:
        """Get accounting summary from Odoo"""
        if not self.odoo_server:
            return {}
        
        try:
            # Get account summary
            result = asyncio.run(self.odoo_server.execute_tool(
                "odoo_get_account_summary",
                {"period": "week"}
            ))
            
            # Parse the summary text
            summary_text = result.text
            
            # Extract key metrics
            revenue = 0
            expenses = 0
            net_profit = 0
            pending_payments = 0
            
            for line in summary_text.split('\n'):
                if 'Revenue' in line:
                    revenue = float(line.split('$')[1].replace(',', ''))
                elif 'Expenses' in line:
                    expenses = float(line.split('$')[1].replace(',', ''))
                elif 'Net Profit' in line:
                    net_profit = float(line.split('$')[1].replace(',', ''))
                elif 'Pending Payments' in line:
                    pending_payments = float(line.split('$')[1].replace(',', ''))
            
            return {
                'revenue': revenue,
                'expenses': expenses,
                'net_profit': net_profit,
                'pending_payments': pending_payments,
                'source': 'odoo'
            }
            
        except Exception as e:
            self.logger.error(f"Error getting Odoo summary: {e}")
            return {}
    
    def _analyze_completed_tasks(self) -> Dict:
        """Analyze tasks completed this week"""
        week_ago = datetime.now() - timedelta(days=7)
        
        completed = {
            "count": 0,
            "by_domain": {"email": 0, "whatsapp": 0, "linkedin": 0},
            "high_priority": 0,
            "tasks": []
        }
        
        if not self.done_folder.exists():
            return completed
        
        for task_file in self.done_folder.glob("*.md"):
            # Check if completed this week
            if task_file.stat().st_mtime > week_ago.timestamp():
                completed["count"] += 1
                
                # Categorize by domain
                name = task_file.name.lower()
                if "email" in name:
                    completed["by_domain"]["email"] += 1
                elif "whatsapp" in name:
                    completed["by_domain"]["whatsapp"] += 1
                elif "linkedin" in name:
                    completed["by_domain"]["linkedin"] += 1
                
                # Check priority
                if "high" in name or "urgent" in name:
                    completed["high_priority"] += 1
                
                completed["tasks"].append(task_file.stem)
        
        return completed
    
    def _analyze_pending_tasks(self) -> Dict:
        """Analyze pending tasks"""
        pending = {
            "count": 0,
            "overdue": 0,
            "high_priority": 0,
            "by_domain": {"email": 0, "whatsapp": 0, "linkedin": 0}
        }
        
        if not self.needs_action.exists():
            return pending
        
        for task_file in self.needs_action.glob("*.md"):
            pending["count"] += 1
            
            name = task_file.name.lower()
            
            # Categorize by domain
            if "email" in name:
                pending["by_domain"]["email"] += 1
            elif "whatsapp" in name:
                pending["by_domain"]["whatsapp"] += 1
            elif "linkedin" in name:
                pending["by_domain"]["linkedin"] += 1
            
            # Check priority
            if "high" in name or "urgent" in name:
                pending["high_priority"] += 1
            
            # Check if overdue (older than 3 days)
            three_days_ago = datetime.now() - timedelta(days=3)
            if task_file.stat().st_mtime < three_days_ago.timestamp():
                pending["overdue"] += 1
        
        return pending

    
    def _detect_bottlenecks(self) -> List[Dict]:
        """Detect bottlenecks in workflow"""
        bottlenecks = []
        
        # Check for overdue tasks
        if not self.needs_action.exists():
            return bottlenecks
        
        three_days_ago = datetime.now() - timedelta(days=3)
        
        for task_file in self.needs_action.glob("*.md"):
            if task_file.stat().st_mtime < three_days_ago.timestamp():
                days_old = (datetime.now() - datetime.fromtimestamp(task_file.stat().st_mtime)).days
                bottlenecks.append({
                    "task": task_file.stem,
                    "days_pending": days_old,
                    "severity": "high" if days_old > 7 else "medium"
                })
        
        return sorted(bottlenecks, key=lambda x: x["days_pending"], reverse=True)
    
    def _generate_suggestions(self) -> List[str]:
        """Generate proactive suggestions"""
        suggestions = []
        
        # Check pending task count
        if self.needs_action.exists():
            pending_count = len(list(self.needs_action.glob("*.md")))
            if pending_count > 10:
                suggestions.append(f"High pending task count ({pending_count}). Consider prioritizing or delegating.")
        
        # Check for old tasks
        if self.needs_action.exists():
            week_ago = datetime.now() - timedelta(days=7)
            old_tasks = [f for f in self.needs_action.glob("*.md") 
                        if f.stat().st_mtime < week_ago.timestamp()]
            if old_tasks:
                suggestions.append(f"{len(old_tasks)} tasks pending for over a week. Review and action.")
        
        # General suggestions
        suggestions.append("Schedule weekly review session to clear backlog.")
        suggestions.append("Consider automating recurring tasks.")
        
        return suggestions
    
    def _create_briefing_markdown(
        self,
        completed: Dict,
        pending: Dict,
        bottlenecks: List[Dict],
        suggestions: List[str],
        accounting_summary: Optional[Dict] = None
    ) -> str:
        """Create formatted briefing markdown"""

        briefing = f"""---
generated: {datetime.now().isoformat()}
period: {(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}
type: ceo_briefing
---

# Monday Morning CEO Briefing

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Period**: Last 7 days

---

## Executive Summary

This week's performance shows **{completed['count']} tasks completed** with **{pending['count']} tasks pending**.
{f"⚠️ {len(bottlenecks)} bottlenecks detected." if bottlenecks else "✅ No major bottlenecks detected."}
{f" **Revenue**: ${accounting_summary.get('revenue', 0):,.2f}" if accounting_summary else ""}

---

## Financial Overview

"""

        if accounting_summary and accounting_summary.get('source') == 'odoo':
            briefing += f"""### Accounting Summary (from Odoo)

- **Revenue**: ${accounting_summary.get('revenue', 0):,.2f}
- **Expenses**: ${accounting_summary.get('expenses', 0):,.2f}
- **Net Profit**: ${accounting_summary.get('net_profit', 0):,.2f}
- **Profit Margin**: {(accounting_summary.get('net_profit', 0) / max(accounting_summary.get('revenue', 1), 1) * 100):.1f}%
- **Pending Payments**: ${accounting_summary.get('pending_payments', 0):,.2f}

"""
        else:
            briefing += """### Accounting Summary

*Odoo integration not available. Financial data not tracked.*

"""

        briefing += f"""---

## Completed Tasks

**Total Completed**: {completed['count']} tasks

### By Domain
- 📧 **Email**: {completed['by_domain']['email']} tasks
- 💬 **WhatsApp**: {completed['by_domain']['whatsapp']} tasks
- 💼 **LinkedIn**: {completed['by_domain']['linkedin']} tasks

### Priority Breakdown
- 🔴 **High Priority**: {completed['high_priority']} tasks completed

---

## Pending Tasks

**Total Pending**: {pending['count']} tasks

### By Domain
- 📧 **Email**: {pending['by_domain']['email']} pending
- 💬 **WhatsApp**: {pending['by_domain']['whatsapp']} pending
- 💼 **LinkedIn**: {pending['by_domain']['linkedin']} pending

### Priority Status
- 🔴 **High Priority**: {pending['high_priority']} tasks
- ⚠️ **Overdue**: {pending['overdue']} tasks (>3 days old)

---

## Bottlenecks

"""

        if bottlenecks:
            briefing += "| Task | Days Pending | Severity |\n"
            briefing += "|------|--------------|----------|\n"
            for b in bottlenecks[:5]:  # Top 5 bottlenecks
                severity_emoji = "🔴" if b['severity'] == 'high' else "🟡"
                briefing += f"| {b['task'][:50]} | {b['days_pending']} days | {severity_emoji} {b['severity']} |\n"
        else:
            briefing += "✅ No bottlenecks detected. All tasks are being processed in a timely manner.\n"

        briefing += "\n---\n\n## Proactive Suggestions\n\n"

        for i, suggestion in enumerate(suggestions, 1):
            briefing += f"{i}. {suggestion}\n"

        # Add financial suggestions if Odoo data available
        if accounting_summary:
            if accounting_summary.get('pending_payments', 0) > 0:
                briefing += f"\n{len(suggestions) + 1}. Follow up on ${accounting_summary.get('pending_payments', 0):,.2f} in pending payments\n"
            if accounting_summary.get('net_profit', 0) < accounting_summary.get('revenue', 0) * 0.2:
                briefing += f"\n{len(suggestions) + 2}. Profit margin is low ({accounting_summary.get('net_profit', 0) / max(accounting_summary.get('revenue', 1), 1) * 100:.1f}%). Review expenses.\n"

        briefing += f"""
---

## Metrics Summary

| Metric | Value | Status |
|--------|-------|--------|
| Tasks Completed | {completed['count']} | {'✅' if completed['count'] > 5 else '⚠️'} |
| Tasks Pending | {pending['count']} | {'✅' if pending['count'] < 10 else '⚠️'} |
| High Priority | {pending['high_priority']} | {'✅' if pending['high_priority'] < 5 else '⚠️'} |
| Overdue Tasks | {pending['overdue']} | {'✅' if pending['overdue'] == 0 else '⚠️'} |
| Bottlenecks | {len(bottlenecks)} | {'✅' if len(bottlenecks) == 0 else '⚠️'} |
"""

        if accounting_summary:
            briefing += f"""| Revenue | ${accounting_summary.get('revenue', 0):,.2f} | {'✅' if accounting_summary.get('revenue', 0) > 0 else '⚠️'} |
| Net Profit | ${accounting_summary.get('net_profit', 0):,.2f} | {'✅' if accounting_summary.get('net_profit', 0) > 0 else '⚠️'} |
| Pending Payments | ${accounting_summary.get('pending_payments', 0):,.2f} | {'✅' if accounting_summary.get('pending_payments', 0) < 1000 else '⚠️'} |
"""

        briefing += f"""
---

## Recommendations

### Immediate Actions
1. Review and action {pending['high_priority']} high-priority tasks
2. Address {pending['overdue']} overdue tasks
3. Clear bottlenecks identified above
"""

        if accounting_summary:
            briefing += f"""
### Financial Actions
1. Follow up on ${accounting_summary.get('pending_payments', 0):,.2f} in unpaid invoices
2. Review expenses (${accounting_summary.get('expenses', 0):,.2f}) for cost optimization
3. Plan for next week's revenue target (${accounting_summary.get('revenue', 0) * 1.1:,.2f})
"""

        briefing += f"""
### This Week's Focus
1. Maintain task completion rate
2. Reduce pending task backlog
3. Prevent new bottlenecks

---

*Generated by AI Employee CEO Briefing System v2.0 (with Odoo Integration)*
"""

        return briefing


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CEO Briefing Generator")
    parser.add_argument("--vault", default=".", help="Vault path")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Generate briefing
    generator = CEOBriefingGenerator(args.vault)
    briefing = generator.generate_weekly_briefing()
    
    # Print to console
    print(briefing)
    
    # Save to custom location if specified
    if args.output:
        Path(args.output).write_text(briefing, encoding='utf-8')
        print(f"\nBriefing saved to: {args.output}")
