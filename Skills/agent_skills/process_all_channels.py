"""
Process All Channels Skill

Silver Tier Integration Skill that processes all communication channels
(Gmail, WhatsApp, LinkedIn) in a unified manner and routes tasks appropriately.

This is the main coordination skill for Silver Tier autonomous operation.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import json
from .base_skill import BaseSkill


def process_all_channels(
    gmail_enabled: bool = True,
    whatsapp_enabled: bool = True,
    linkedin_enabled: bool = False,
    auto_respond: bool = False,
    require_approval: bool = True,
    vault_path: str = ".",
    model_name: str = "gpt-4"
) -> Dict[str, Any]:
    """
    Process all communication channels and route tasks.

    Args:
        gmail_enabled: Process Gmail messages
        whatsapp_enabled: Process WhatsApp messages
        linkedin_enabled: Process LinkedIn messages
        auto_respond: Enable automatic responses (use with caution)
        require_approval: Require approval for actions
        vault_path: Path to vault
        model_name: AI model to use

    Returns:
        Dictionary with processing results from all channels:
        - timestamp: Processing timestamp
        - channels: Results by channel
        - summary: Overall summary
        - tasks_created: Number of tasks created
        - responses_generated: Number of responses generated

    Example:
        >>> result = process_all_channels(
        ...     gmail_enabled=True,
        ...     whatsapp_enabled=True,
        ...     require_approval=True
        ... )
        >>> print(f"Tasks created: {result['tasks_created']}")
    """
    skill = ProcessAllChannelsSkill(model_name)
    return skill.execute(
        gmail_enabled,
        whatsapp_enabled,
        linkedin_enabled,
        auto_respond,
        require_approval,
        vault_path
    )


class ProcessAllChannelsSkill(BaseSkill):
    """Implementation of multi-channel processing skill."""

    def __init__(self, model_name: str = "gpt-4"):
        """Initialize the skill."""
        super().__init__(model_name)
        self.vault_path = None

    def execute(
        self,
        gmail_enabled: bool,
        whatsapp_enabled: bool,
        linkedin_enabled: bool,
        auto_respond: bool,
        require_approval: bool,
        vault_path: str
    ) -> Dict[str, Any]:
        """
        Execute multi-channel processing.

        Args:
            gmail_enabled: Gmail processing flag
            whatsapp_enabled: WhatsApp processing flag
            linkedin_enabled: LinkedIn processing flag
            auto_respond: Auto-response flag
            require_approval: Approval requirement flag
            vault_path: Vault path

        Returns:
            Processing results dictionary
        """
        self.vault_path = Path(vault_path)
        self.logger.info("Processing all communication channels")

        results = {
            'timestamp': datetime.now().isoformat(),
            'channels': {},
            'summary': {},
            'tasks_created': 0,
            'responses_generated': 0,
            'errors': []
        }

        # Process Gmail
        if gmail_enabled:
            try:
                gmail_results = self._process_gmail_channel(require_approval)
                results['channels']['gmail'] = gmail_results
                results['tasks_created'] += gmail_results.get('tasks_created', 0)
            except Exception as e:
                self.logger.error(f"Gmail processing failed: {e}")
                results['errors'].append(f"Gmail: {str(e)}")
                results['channels']['gmail'] = {'status': 'error', 'error': str(e)}

        # Process WhatsApp
        if whatsapp_enabled:
            try:
                whatsapp_results = self._process_whatsapp_channel(
                    auto_respond,
                    require_approval
                )
                results['channels']['whatsapp'] = whatsapp_results
                results['responses_generated'] += whatsapp_results.get('responses_generated', 0)
            except Exception as e:
                self.logger.error(f"WhatsApp processing failed: {e}")
                results['errors'].append(f"WhatsApp: {str(e)}")
                results['channels']['whatsapp'] = {'status': 'error', 'error': str(e)}

        # Process LinkedIn
        if linkedin_enabled:
            try:
                linkedin_results = self._process_linkedin_channel(
                    auto_respond,
                    require_approval
                )
                results['channels']['linkedin'] = linkedin_results
            except Exception as e:
                self.logger.error(f"LinkedIn processing failed: {e}")
                results['errors'].append(f"LinkedIn: {str(e)}")
                results['channels']['linkedin'] = {'status': 'error', 'error': str(e)}

        # Generate summary
        results['summary'] = self._generate_summary(results)

        # Update dashboard
        self._update_dashboard(results)

        self.logger.info(
            f"Channel processing complete. "
            f"Tasks: {results['tasks_created']}, "
            f"Responses: {results['responses_generated']}"
        )

        return results

    def _process_gmail_channel(self, require_approval: bool) -> Dict[str, Any]:
        """
        Process Gmail channel.

        Args:
            require_approval: Approval requirement flag

        Returns:
            Gmail processing results
        """
        self.logger.info("Processing Gmail channel")

        # Import and run Gmail processing
        try:
            from .process_gmail_messages import process_gmail_messages

            results = process_gmail_messages(
                credentials_path="config/gmail-credentials.json",
                token_path="config/gmail-token.json",
                output_dir=str(self.vault_path / "Inbox"),
                max_results=10,
                model_name=self.model_name
            )

            return {
                'status': 'success',
                'messages_processed': len(results),
                'tasks_created': len([r for r in results if r.get('status') == 'success']),
                'results': results
            }

        except ImportError as e:
            self.logger.warning(f"Gmail processing not available: {e}")
            return {
                'status': 'unavailable',
                'messages_processed': 0,
                'tasks_created': 0,
                'reason': 'Dependencies not installed'
            }

    def _process_whatsapp_channel(
        self,
        auto_respond: bool,
        require_approval: bool
    ) -> Dict[str, Any]:
        """
        Process WhatsApp channel.

        Args:
            auto_respond: Auto-response flag
            require_approval: Approval requirement flag

        Returns:
            WhatsApp processing results
        """
        self.logger.info("Processing WhatsApp channel")

        # Import and run WhatsApp processing
        try:
            from .process_whatsapp_messages import process_whatsapp_messages

            results = process_whatsapp_messages(
                inbox_dir=str(self.vault_path / "WhatsApp_Inbox"),
                outbox_dir=str(self.vault_path / "WhatsApp_Outbox"),
                model_name=self.model_name
            )

            # If auto-respond enabled and no approval required, send responses
            if auto_respond and not require_approval:
                self._send_whatsapp_responses(results)

            return {
                'status': 'success',
                'messages_processed': len(results),
                'responses_generated': len([r for r in results if r.get('status') == 'success']),
                'auto_respond': auto_respond,
                'results': results
            }

        except ImportError as e:
            self.logger.warning(f"WhatsApp processing not available: {e}")
            return {
                'status': 'unavailable',
                'messages_processed': 0,
                'responses_generated': 0,
                'reason': 'Module not available'
            }

    def _process_linkedin_channel(
        self,
        auto_respond: bool,
        require_approval: bool
    ) -> Dict[str, Any]:
        """
        Process LinkedIn channel.

        Args:
            auto_respond: Auto-response flag
            require_approval: Approval requirement flag

        Returns:
            LinkedIn processing results
        """
        self.logger.info("Processing LinkedIn channel")

        # For now, return placeholder
        # In production, this would integrate with LinkedIn API
        return {
            'status': 'placeholder',
            'messages_processed': 0,
            'responses_generated': 0,
            'reason': 'LinkedIn API integration pending'
        }

    def _send_whatsapp_responses(self, results: List[Dict]) -> None:
        """
        Send WhatsApp responses via MCP server.

        Args:
            results: Processing results with response files
        """
        try:
            from .mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer
            import asyncio

            server = WhatsAppMCPServer()

            for result in results:
                if result.get('status') != 'success':
                    continue

                # Read response file
                response_file = result.get('output_file')
                if not response_file:
                    continue

                content = self.read_markdown(response_file)
                metadata = self.extract_frontmatter(content)
                body = self.extract_body(content)

                # Extract recipient and response
                recipient = metadata.get('to', '')
                response_text = body.strip()

                if recipient and response_text:
                    # Send via MCP server
                    asyncio.run(server.execute_tool(
                        "send_whatsapp_message",
                        {
                            "recipient": recipient,
                            "message": response_text
                        }
                    ))

                    self.logger.info(f"Sent WhatsApp response to {recipient}")

            asyncio.run(server.cleanup())

        except Exception as e:
            self.logger.error(f"Failed to send WhatsApp responses: {e}")

    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate processing summary.

        Args:
            results: Channel processing results

        Returns:
            Summary dictionary
        """
        summary = {
            'total_channels_processed': 0,
            'successful_channels': 0,
            'failed_channels': 0,
            'total_tasks': results['tasks_created'],
            'total_responses': results['responses_generated'],
            'requires_attention': False,
            'attention_items': []
        }

        for channel, channel_results in results.get('channels', {}).items():
            summary['total_channels_processed'] += 1

            if channel_results.get('status') == 'success':
                summary['successful_channels'] += 1
            elif channel_results.get('status') == 'error':
                summary['failed_channels'] += 1
                summary['requires_attention'] = True
                summary['attention_items'].append(f"{channel}: {channel_results.get('error', 'Unknown error')}")

        return summary

    def _update_dashboard(self, results: Dict[str, Any]) -> None:
        """
        Update Dashboard.md with processing results.

        Args:
            results: Processing results
        """
        dashboard_file = self.vault_path / "Dashboard.md"

        try:
            # Read existing dashboard
            if dashboard_file.exists():
                content = self.read_markdown(str(dashboard_file))
            else:
                content = "# Dashboard\n\n## Overview\n\n"

            # Update channel processing section
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            update_section = f"""
## Channel Processing Update

**Last Updated**: {timestamp}

### Summary
- Tasks Created: {results['tasks_created']}
- Responses Generated: {results['responses_generated']}
- Channels Processed: {results['summary'].get('total_channels_processed', 0)}
- Successful: {results['summary'].get('successful_channels', 0)}
- Failed: {results['summary'].get('failed_channels', 0)}

### Channel Status
"""

            for channel, channel_results in results.get('channels', {}).items():
                status = channel_results.get('status', 'unknown')
                status_icon = "✅" if status == 'success' else "❌" if status == 'error' else "⚠️"
                update_section += f"- {status_icon} **{channel.title()}**: {status}\n"

            if results['summary'].get('requires_attention'):
                update_section += "\n### ⚠️ Attention Required\n"
                for item in results['summary'].get('attention_items', []):
                    update_section += f"- {item}\n"

            # Append update to dashboard
            if "## Channel Processing Update" not in content:
                content += "\n" + update_section
            else:
                # Replace existing section
                import re
                pattern = r'## Channel Processing Update.*?(?=##|\Z)'
                content = re.sub(pattern, update_section, content, flags=re.DOTALL)

            self.write_markdown(str(dashboard_file), content)
            self.logger.info("Dashboard updated")

        except Exception as e:
            self.logger.error(f"Failed to update dashboard: {e}")


# Example usage
if __name__ == "__main__":
    import sys

    # Parse command line arguments
    gmail = '--no-gmail' not in sys.argv
    whatsapp = '--no-whatsapp' not in sys.argv
    linkedin = '--linkedin' in sys.argv
    auto = '--auto' in sys.argv
    approval = '--no-approval' not in sys.argv

    print("Processing all channels...\n")

    results = process_all_channels(
        gmail_enabled=gmail,
        whatsapp_enabled=whatsapp,
        linkedin_enabled=linkedin,
        auto_respond=auto,
        require_approval=approval
    )

    print(f"\n{'='*60}")
    print("CHANNEL PROCESSING SUMMARY")
    print(f"{'='*60}")
    print(f"Timestamp: {results['timestamp']}")
    print(f"\nTasks Created: {results['tasks_created']}")
    print(f"Responses Generated: {results['responses_generated']}")
    print(f"\nChannel Status:")

    for channel, channel_results in results.get('channels', {}).items():
        status = channel_results.get('status', 'unknown')
        status_icon = "✅" if status == 'success' else "❌" if status == 'error' else "⚠️"
        print(f"  {status_icon} {channel.title()}: {status}")

    if results.get('errors'):
        print(f"\nErrors:")
        for error in results['errors']:
            print(f"  ⚠️ {error}")

    print(f"\n{'='*60}")
