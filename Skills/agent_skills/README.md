# Agent Skills System

Modular AI skills for task processing. Each skill is a separate, importable function that calls AI models internally.

## Overview

The Agent Skills System provides a collection of reusable AI-powered functions for common business tasks:

- **summarize_task**: Generate concise summaries of task content
- **create_plan**: Break down tasks into actionable execution plans
- **draft_reply**: Generate email reply drafts
- **generate_linkedin_post**: Create engaging LinkedIn content

## Installation

```bash
# Install required dependencies
pip install pyyaml

# Optional: Install AI model client (OpenAI, Anthropic, etc.)
pip install openai  # or anthropic, etc.
```

## Quick Start

### Import Individual Skills

```python
from agent_skills import summarize_task, create_plan, draft_reply, generate_linkedin_post

# Summarize a task
summary = summarize_task("Needs_Action/email_20260219_120000.md")
print(summary)

# Create an execution plan
plan_path = create_plan("Needs_Action/project_task.md")
print(f"Plan created: {plan_path}")

# Draft an email reply
reply = draft_reply("Needs_Action/email_20260219_120000.md", tone="friendly")
print(reply)

# Generate a LinkedIn post
post = generate_linkedin_post("AI automation in business", style="thought-leadership")
print(post)
```

### Use from Command Line

```bash
# Summarize a task
python -m agent_skills.summarize_task Needs_Action/email_20260219_120000.md

# Create a plan
python -m agent_skills.create_plan Needs_Action/project_task.md

# Draft a reply
python -m agent_skills.draft_reply Needs_Action/email_20260219_120000.md professional

# Generate LinkedIn post
python -m agent_skills.generate_linkedin_post "AI automation tips" thought-leadership
```

## Skills Reference

### 1. summarize_task

Generate a concise summary of a task.

**Function Signature:**
```python
def summarize_task(
    task_filepath: str,
    max_length: int = 200,
    model_name: str = "gpt-4"
) -> str
```

**Parameters:**
- `task_filepath`: Path to the task markdown file
- `max_length`: Maximum summary length in words (default: 200)
- `model_name`: AI model to use (default: "gpt-4")

**Returns:** String containing the task summary

**Example:**
```python
summary = summarize_task(
    "Needs_Action/email_20260219_120000.md",
    max_length=100
)
# Output: "Client requests Q1 report review by Friday. High priority. 
#          Requires financial data analysis and executive summary."
```

---

### 2. create_plan

Generate a detailed execution plan with steps.

**Function Signature:**
```python
def create_plan(
    task_filepath: str,
    output_dir: str = "Plans",
    model_name: str = "gpt-4"
) -> str
```

**Parameters:**
- `task_filepath`: Path to the task markdown file
- `output_dir`: Directory to save the plan (default: "Plans")
- `model_name`: AI model to use (default: "gpt-4")

**Returns:** Path to the generated Plan.md file

**Example:**
```python
plan_path = create_plan(
    "Needs_Action/project_launch.md",
    output_dir="Plans/Q1"
)
# Output: "Plans/Q1/plan_20260219_120000.md"
```

**Generated Plan Format:**
```markdown
---
plan_id: plan_20260219120000
created: 2026-02-19T12:00:00
source_task: Needs_Action/project_launch.md
status: pending
current_step: 0
---

# Plan: Project Launch

## Goal
Successfully launch the new product by end of Q1

## Steps
1. Finalize product specifications (2 days)
2. Complete QA testing (1 week)
3. Prepare marketing materials (3 days)
4. Coordinate with sales team (2 days)
5. Execute launch (1 day)

## Dependencies
- Step 2 depends on Step 1
- Step 3 can run parallel to Step 2
- Step 4 depends on Step 3

## Success Criteria
- All features tested and approved
- Marketing materials reviewed
- Sales team trained
- Launch executed on schedule
```

---

### 3. draft_reply

Generate a draft email reply.

**Function Signature:**
```python
def draft_reply(
    task_filepath: str,
    tone: str = "professional",
    model_name: str = "gpt-4"
) -> str
```

**Parameters:**
- `task_filepath`: Path to the email task markdown file
- `tone`: Tone of reply - "professional", "friendly", "formal", "casual" (default: "professional")
- `model_name`: AI model to use (default: "gpt-4")

**Returns:** Draft reply text

**Example:**
```python
reply = draft_reply(
    "Needs_Action/email_20260219_120000.md",
    tone="friendly"
)
print(reply)
```

**Output:**
```
Hi John,

Thank you for reaching out about the Q1 report. I'd be happy to help with the review.

I'll need a few days to analyze the financial data and prepare the executive summary. 
I can have this completed by Friday as requested.

I'll reach out if I have any questions while reviewing the materials.

Best regards
```

---

### 4. generate_linkedin_post

Create engaging LinkedIn content.

**Function Signature:**
```python
def generate_linkedin_post(
    topic: str,
    style: str = "professional",
    include_hashtags: bool = True,
    max_length: int = 3000,
    model_name: str = "gpt-4"
) -> str
```

**Parameters:**
- `topic`: Topic or content for the post
- `style`: Post style - "professional", "casual", "thought-leadership", "storytelling" (default: "professional")
- `include_hashtags`: Include relevant hashtags (default: True)
- `max_length`: Maximum post length in characters (default: 3000)
- `model_name`: AI model to use (default: "gpt-4")

**Returns:** LinkedIn post content

**Example:**
```python
post = generate_linkedin_post(
    "AI automation in business",
    style="thought-leadership",
    include_hashtags=True
)
print(post)
```

**Output:**
```
🚀 The Future of Work is Here

AI automation isn't just about replacing tasks—it's about amplifying human potential.

Here's what I've learned implementing AI in our workflow:

1. Start small: Automate repetitive tasks first
2. Focus on value: Free up time for strategic work
3. Iterate constantly: AI improves with feedback

The companies winning today aren't the ones with the most AI—they're the ones using it most thoughtfully.

What's your experience with AI automation? I'd love to hear your thoughts.

#AI #Automation #FutureOfWork #BusinessInnovation #Productivity
```

---

## Architecture

### Base Components

**BaseSkill Class:**
- Provides common functionality for all skills
- Handles file I/O (read/write markdown)
- Extracts frontmatter and body content
- Manages logging

**AIModelClient Class:**
- Abstracts AI model calls
- Supports multiple models (OpenAI, Anthropic, local models)
- Handles prompt formatting
- Manages temperature and token limits

### Skill Structure

Each skill follows this pattern:

```python
# Public function (easy to import)
def skill_name(params) -> result:
    skill = SkillNameSkill(model_name)
    return skill.execute(params)

# Implementation class (inherits from BaseSkill)
class SkillNameSkill(BaseSkill):
    def execute(self, params) -> result:
        # 1. Read input
        # 2. Build AI prompt
        # 3. Call AI model
        # 4. Format output
        # 5. Return result
```

## Configuration

### AI Model Configuration

Set your AI model API key as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key-here"
# or
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Custom Model Integration

To use a different AI model, modify `base_skill.py`:

```python
class AIModelClient:
    def call(self, prompt: str, system_prompt: Optional[str] = None, 
             temperature: float = 0.7, max_tokens: int = 2000) -> str:
        # Replace with your AI model API call
        import openai
        
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
```

## Testing

### Unit Tests

```python
import pytest
from agent_skills import summarize_task, create_plan, draft_reply, generate_linkedin_post

def test_summarize_task():
    summary = summarize_task("test_data/sample_task.md", max_length=50)
    assert len(summary) > 0
    assert len(summary.split()) <= 60  # Allow some buffer

def test_create_plan():
    plan_path = create_plan("test_data/sample_task.md", output_dir="test_output")
    assert os.path.exists(plan_path)
    
def test_draft_reply():
    reply = draft_reply("test_data/sample_email.md", tone="professional")
    assert "Hi" in reply or "Dear" in reply
    assert "Best" in reply or "Regards" in reply

def test_generate_linkedin_post():
    post = generate_linkedin_post("Test topic", include_hashtags=True)
    assert len(post) <= 3000
    assert "#" in post
```

### Integration Tests

```python
def test_end_to_end_workflow():
    # 1. Summarize task
    summary = summarize_task("Needs_Action/email_20260219_120000.md")
    
    # 2. Create plan
    plan_path = create_plan("Needs_Action/email_20260219_120000.md")
    
    # 3. Draft reply
    reply = draft_reply("Needs_Action/email_20260219_120000.md")
    
    # 4. Generate LinkedIn post about the task
    post = generate_linkedin_post(summary, style="professional")
    
    assert all([summary, plan_path, reply, post])
```

## Best Practices

### 1. Error Handling

Always wrap skill calls in try-except blocks:

```python
try:
    summary = summarize_task("Needs_Action/task.md")
except FileNotFoundError:
    print("Task file not found")
except Exception as e:
    print(f"Error: {e}")
```

### 2. Logging

Enable logging to track skill execution:

```python
import logging
logging.basicConfig(level=logging.INFO)

summary = summarize_task("Needs_Action/task.md")
# Logs: "Summarizing task: Needs_Action/task.md"
# Logs: "Generated summary: 150 characters"
```

### 3. Model Selection

Choose appropriate models for different tasks:

```python
# Fast, cheap model for summaries
summary = summarize_task("task.md", model_name="gpt-3.5-turbo")

# More capable model for complex plans
plan = create_plan("task.md", model_name="gpt-4")

# Creative model for LinkedIn posts
post = generate_linkedin_post("topic", model_name="gpt-4")
```

### 4. Batch Processing

Process multiple tasks efficiently:

```python
from pathlib import Path

tasks = Path("Needs_Action").glob("*.md")
summaries = {}

for task in tasks:
    try:
        summaries[task.name] = summarize_task(str(task))
    except Exception as e:
        print(f"Failed to summarize {task.name}: {e}")

print(f"Summarized {len(summaries)} tasks")
```

## Extending the System

### Adding New Skills

1. Create a new file in `agent_skills/`:

```python
# agent_skills/new_skill.py
from .base_skill import BaseSkill

def new_skill(input_param: str, model_name: str = "gpt-4") -> str:
    skill = NewSkill(model_name)
    return skill.execute(input_param)

class NewSkill(BaseSkill):
    def execute(self, input_param: str) -> str:
        # Implementation
        pass
```

2. Add to `__init__.py`:

```python
from .new_skill import new_skill
__all__ = [..., 'new_skill']
```

3. Document in README

## Troubleshooting

### Common Issues

**Issue: "No module named 'agent_skills'"**
- Solution: Ensure you're in the correct directory or add to PYTHONPATH

**Issue: "API key not found"**
- Solution: Set environment variable: `export OPENAI_API_KEY="your-key"`

**Issue: "File not found"**
- Solution: Use absolute paths or ensure working directory is correct

**Issue: "AI model timeout"**
- Solution: Increase timeout or use a faster model

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new skills
4. Submit a pull request

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review example usage in this README
