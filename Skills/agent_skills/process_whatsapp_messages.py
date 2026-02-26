"""
Process WhatsApp Messages Skill

Reads WhatsApp messages from inbox, analyzes them with AI,
and generates intelligent responses.
"""

from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from .base_skill import BaseSkill


def process_whatsapp_messages(
    inbox_dir: str = "WhatsApp_Inbox",
    outbox_dir: str = "WhatsApp_Outbox",
    model_name: str = "gpt-4"
) -> List[Dict[str, str]]:
    """
    Process WhatsApp messages from inbox and generate AI responses.

    Args:
        inbox_dir: Directory containing incoming WhatsApp messages
        outbox_dir: Directory to save AI-generated responses
        model_name: AI model to use for response generation

    Returns:
        List of processed message dictionaries with keys:
        - input_file: Path to input message file
        - output_file: Path to generated response file
        - contact: Contact name
        - status: Processing status (success/error)

    Example:
        >>> results = process_whatsapp_messages()
        >>> for result in results:
        ...     print(f"Processed: {result['input_file']} -> {result['output_file']}")
    """
    skill = ProcessWhatsAppMessagesSkill(model_name)
    return skill.execute(inbox_dir, outbox_dir)


class ProcessWhatsAppMessagesSkill(BaseSkill):
    """Implementation of WhatsApp message processing skill."""

    def execute(self, inbox_dir: str, outbox_dir: str) -> List[Dict[str, str]]:
        """
        Execute WhatsApp message processing.

        Args:
            inbox_dir: Input directory
            outbox_dir: Output directory

        Returns:
            List of processing results
        """
        self.logger.info(f"Processing WhatsApp messages from {inbox_dir}")

        # Ensure directories exist
        inbox_path = Path(inbox_dir)
        outbox_path = Path(outbox_dir)
        outbox_path.mkdir(parents=True, exist_ok=True)

        if not inbox_path.exists():
            self.logger.warning(f"Inbox directory not found: {inbox_dir}")
            return []

        # Find all unprocessed message files
        message_files = list(inbox_path.glob("*.md"))
        processed_index = self._load_processed_index()

        results = []
        for msg_file in message_files:
            # Skip already processed messages
            if str(msg_file.absolute()) in processed_index:
                continue

            # Process the message
            result = self._process_single_message(msg_file, outbox_path)
            results.append(result)

            # Mark as processed
            if result['status'] == 'success':
                processed_index.append(str(msg_file.absolute()))
                self._save_processed_index(processed_index)

        self.logger.info(f"Processed {len(results)} WhatsApp messages")
        return results

    def _process_single_message(self, msg_file: Path, outbox_path: Path) -> Dict[str, str]:
        """
        Process a single WhatsApp message.

        Args:
            msg_file: Path to message file
            outbox_path: Output directory

        Returns:
            Processing result dictionary
        """
        try:
            # Read message content
            content = self.read_markdown(str(msg_file))
            metadata = self.extract_frontmatter(content)
            body = self.extract_body(content)

            # Extract message metadata
            contact = metadata.get('from', 'Unknown')
            timestamp = metadata.get('timestamp', datetime.now().isoformat())

            # Generate AI response
            response = self._generate_response(contact, body)

            # Save response to outbox
            response_file = self._save_response(
                outbox_path,
                contact,
                response,
                timestamp
            )

            self.logger.info(f"Generated response for {contact}")

            return {
                'input_file': str(msg_file),
                'output_file': str(response_file),
                'contact': contact,
                'status': 'success'
            }

        except Exception as e:
            self.logger.error(f"Failed to process {msg_file}: {e}")
            return {
                'input_file': str(msg_file),
                'output_file': '',
                'contact': 'Unknown',
                'status': 'error',
                'error': str(e)
            }

    def _generate_response(self, contact: str, message_content: str) -> str:
        """
        Generate AI response for a WhatsApp message.

        Args:
            contact: Contact name
            message_content: Message text

        Returns:
            AI-generated response
        """
        system_prompt = """You are a helpful AI assistant for WhatsApp messaging.
Your job is to generate friendly, concise, and helpful responses.
Guidelines:
- Be warm and conversational
- Keep responses concise (WhatsApp style)
- Be helpful and actionable
- Use appropriate emojis (sparingly)
- Match the tone of the original message"""

        user_prompt = f"""Generate a WhatsApp response for this message:

From: {contact}

Message:
{message_content}

Write a friendly, helpful response that:
1. Acknowledges their message
2. Addresses their main points
3. Is concise and conversational
4. Uses appropriate tone

Response:"""

        # Call AI model
        response = self.ai_client.call(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=500
        )

        return response.strip()

    def _save_response(self, outbox_path: Path, contact: str, response: str, timestamp: str) -> Path:
        """
        Save AI response to outbox.

        Args:
            outbox_path: Output directory
            contact: Contact name
            response: Response text
            timestamp: Original message timestamp

        Returns:
            Path to saved response file
        """
        # Generate filename
        ts = timestamp.replace('-', '').replace(':', '').replace('T', '_')[:15]
        safe_contact = contact.replace(' ', '_')[:20]
        filename = f"response_{ts}_to_{safe_contact}.md"
        filepath = outbox_path / filename

        # Create content with frontmatter
        content = f"""---
type: whatsapp_response
to: "{contact}"
timestamp: "{datetime.now().isoformat()}"
original_timestamp: "{timestamp}"
status: pending
---

# WhatsApp Response to {contact}

**To**: {contact}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status**: ⏳ Pending Review

## AI-Generated Response

{response}

---

## Instructions
1. Review the response above
2. Edit if needed
3. Copy and send via WhatsApp
4. Move this file to WhatsApp_Sent/ after sending
"""

        self.write_markdown(str(filepath), content)
        return filepath

    def _load_processed_index(self) -> List[str]:
        """Load processed messages index."""
        index_file = Path("WhatsApp_Inbox/.processed_index.json")
        if index_file.exists():
            import json
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []

    def _save_processed_index(self, index: List[str]) -> None:
        """Save processed messages index."""
        index_file = Path("WhatsApp_Inbox/.processed_index.json")
        import json
        index_file.parent.mkdir(parents=True, exist_ok=True)
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)


# Example usage
if __name__ == "__main__":
    results = process_whatsapp_messages()
    print(f"\nProcessed {len(results)} messages:")
    for result in results:
        status = "✅" if result['status'] == 'success' else "❌"
        print(f"  {status} {result['contact']}: {result['input_file']} -> {result['output_file']}")
