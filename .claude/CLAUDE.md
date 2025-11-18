# Claude Code Workflow: Skill-First Approach

## Overview

This document outlines the workflow for handling tasks in this project using Claude Code's skill system. The goal is to maximize reusability and efficiency by creating skills for all tasks by default.

## Core Principle

**DEFAULT TO CREATING SKILLS.** When in doubt, create a skill. Skills are cheap to create and invaluable for building up project capability. Never ask for confirmation before creating a skill - just create it and execute.

## Workflow

### 1. Task Reception

When a task request is received, follow this decision tree:

```
Task Request
    ↓
    ├─→ Check: Do we have an existing skill for this?
    │   ├─→ YES: Invoke the skill directly
    │   │         ↓
    │   │         Execute task using skill
    │   │         ↓
    │   │         Complete
    │   │
    │   └─→ NO: Continue to step 2
    │       ↓
    ├─→ DEFAULT: Create a new skill
    │         ↓
    │         Create skill structure (no confirmation needed)
    │         ↓
    │         Use the newly created skill
    │         ↓
    │         Complete
    │
    └─→ ONLY IF TRULY ONE-OFF: Execute directly
            (Examples: fixing a typo, quick exploratory read)
            ↓
            Use appropriate tools
            ↓
            Complete
```

### 2. Checking for Existing Skills

Before starting any task, check the available skills:
- Review the skills listed in the conversation context
- Skills are organized by location (user/project/managed)
- Look for skills whose descriptions match the task domain

**Available skill categories:**
- Skills are project-specific and will be built up over time
- Check the `.claude/skills/` directory for available skills in this project
- Use `skill-creator` to build new skills as needed

### 3. When to Create Skills (Default: Always)

**Create skills by default for:**
- Any task with more than one step
- Tasks that involve domain-specific knowledge
- Workflows that combine multiple tools
- Anything that could potentially be useful again
- Tasks that require specific context or expertise
- Code generation, analysis, or transformation tasks
- Report generation, documentation, or artifact creation
- **When uncertain - CREATE THE SKILL**

**Only skip skill creation for:**
- Trivial single-step operations (single typo fix, reading one file)
- Pure exploratory reads with no deliverable
- Immediate clarification questions

**Bias toward skill creation:** If you're asking yourself "should I create a skill?", the answer is YES.

### 4. Creating New Skills (Do This Automatically)

For any task without an existing skill, immediately create one:

1. **Create the skill without asking:**
   - Check if `.claude/skills/skill-creator/` exists in the project
   - Use the skill-creator script or create skills manually
   - **NEVER ask for permission or confirmation first.**

2. **Define the skill with:**
   - Clear name (kebab-case)
   - Precise description of when to use it
   - Detailed instructions for execution
   - Required tools and capabilities
   - Expected inputs and outputs

3. **Make the skill available:**
   - After creating the skill, it should be available in the `.claude/skills/` directory
   - Skills are loaded from this directory structure
   - Verify the skill exists and has proper structure

4. **Use the skill:**
   - Create the skill structure
   - Verify it's properly configured
   - Use the skill to complete the current task
   - No waiting, no asking, just do it

**Note:** Skills can be implemented as simple scripts or as powerful Claude Agent SDK Python scripts with custom tools. The skill-creator supports both approaches.

### 5. Benefits of This Approach

**Efficiency:**
- Avoid reinventing the wheel for common tasks
- Reduce token usage by leveraging specialized skills
- Faster execution with pre-defined workflows

**Consistency:**
- Standardized approaches to common problems
- Predictable output formats and quality
- Easier maintenance and updates

**Scalability:**
- Growing library of capabilities
- Knowledge preservation across sessions
- Easier onboarding for new tasks

**Quality:**
- Refined workflows based on best practices
- Domain expertise encoded in skills
- Better error handling and edge cases

## Implementation Notes

### For Claude Code

When processing a task:
1. **Always scan available skills first**
2. **If no skill exists, immediately create one (default action)**
3. **NEVER ask for confirmation before creating a skill**
4. **After creating a skill, make it available in `.claude/skills/`**
5. **Use the newly created skill to complete the current task**
6. **Create → Setup → Execute in one seamless flow**
7. **Bias heavily toward skill creation - it's the default, not the exception**
8. **Only execute directly for truly trivial one-off operations**

### Proactive Tool Usage: Never Ask, Just Do

**CRITICAL PRINCIPLE: You have powerful tools - USE THEM without asking for permission.**

When you need to accomplish something:
- ✅ **DO:** Use `run_terminal_cmd` to run wget, curl, grep, python scripts, etc.
- ✅ **DO:** Write and execute Python code to fetch, parse, analyze, or process data
- ✅ **DO:** Use grep to search files for patterns
- ✅ **DO:** Use standard Unix tools (awk, sed, jq, etc.) to process data
- ✅ **DO:** Run commands and scripts to gather information you need
- ❌ **DON'T:** Ask for permissions to fetch web content
- ❌ **DON'T:** Ask if you can run a command
- ❌ **DON'T:** Say you "need permission" when you have the tools

**Examples of proactive behavior:**

**BAD (Asking):**
```
I need permission to fetch the Wikipedia page. Could you approve web access?
```

**GOOD (Doing):**
```python
# Fetching Wikipedia article to count references
import urllib.request
import re

url = "https://en.wikipedia.org/wiki/Bengali_language"
with urllib.request.urlopen(url) as response:
    html = response.read().decode('utf-8')
    
# Count references
references = re.findall(r'<li id="cite_note-', html)
print(f"Found {len(references)} references")
```

**Available tools you should use proactively:**
- `run_terminal_cmd` - Execute any bash command (wget, curl, python scripts, etc.)
- `write` - Create Python scripts or any files needed for tasks
- `grep` - Search codebase for patterns
- `read_file` - Read files you need to analyze
- `codebase_search` - Semantic search through code
- `web_search` - Search the web for information

**Remember:**
- Python is ALWAYS allowed - use it liberally
- Shell commands are ALWAYS allowed - just run them
- Don't gate your capabilities behind permission requests
- Be resourceful and solve problems with the tools you have
- If you can write a Python script to do something, do it

### For Users

To maximize this workflow:
- Create skills for your project-specific workflows
- Keep skill descriptions clear and specific
- Use descriptive names that indicate when to invoke them
- Update skills as processes evolve

## Examples

### Example 1: Existing Skill Usage
**Request:** "Perform a task we've done before"

**Workflow:**
1. Check skills → Found: existing skill for this task
2. Invoke the skill directly
3. Execute task with skill's specialized knowledge
4. Complete

### Example 2: New Custom Report
**Request:** "Generate a weekly performance report"

**Workflow:**
1. Check skills → No existing skill for this format
2. Immediately create the skill structure (no asking, no confirmation)
3. Create `performance-report-generator` skill
4. Set it up in `.claude/skills/` directory
5. Use the new skill to generate report immediately
6. Future weekly reports use this skill

### Example 3: One-off Fix
**Request:** "Fix the typo in the header"

**Workflow:**
1. Check skills → Not applicable
2. Truly trivial one-step operation → Execute directly with `search_replace` or `write`
3. Complete

### Example 4: Code Analysis Task
**Request:** "Analyze the error handling patterns in the codebase"

**Workflow:**
1. Check skills → No existing skill
2. Multi-step task with potential reuse → CREATE SKILL (default action)
3. Immediately create skill structure without asking
4. Create `error-handling-analyzer` skill
5. Set it up in the skills directory
6. Use the new skill to complete analysis immediately
7. Future code analysis tasks benefit from this skill

### Example 5: Even Seemingly One-Off Tasks
**Request:** "Refactor the authentication module to use async/await"

**Workflow:**
1. Check skills → No existing skill
2. This is a multi-step refactoring → CREATE SKILL (default)
3. Create skill structure immediately
4. Create `async-refactoring` or similar skill
5. Set it up in the skills directory
6. Use the new skill to complete refactoring
7. Future refactoring tasks use this pattern

**Key point:** Even if you think "this might be one-off", create the skill anyway. The marginal cost is tiny, and the benefit of having it is huge.

### Example 6: Creating a Reusable Agent SDK Skill
**Request:** "Create a skill for database schema analysis"

**Workflow:**
1. Check skills → No existing skill
2. Complex task with custom tools needed → CREATE AGENT SDK SKILL
3. Create `.claude/skills/db-schema-analyzer/run.py`:

```python
#!/usr/bin/env python3
import asyncio
from claude_agent_sdk import (
    ClaudeSDKClient, ClaudeAgentOptions, tool, 
    create_sdk_mcp_server
)
from typing import Any

@tool("query_db", "Execute SQL query", {"query": str})
async def query_db(args: dict[str, Any]) -> dict[str, Any]:
    # Custom database logic
    return {"content": [{"type": "text", "text": "Results..."}]}

@tool("get_schema", "Get table schema", {"table": str})
async def get_schema(args: dict[str, Any]) -> dict[str, Any]:
    # Custom schema retrieval
    return {"content": [{"type": "text", "text": "Schema..."}]}

async def main():
    server = create_sdk_mcp_server(
        name="db-tools", version="1.0.0",
        tools=[query_db, get_schema]
    )
    
    options = ClaudeAgentOptions(
        mcp_servers={"db": server},
        allowed_tools=[
            "mcp__db__query_db",
            "mcp__db__get_schema"
        ],
        system_prompt="Database schema analyzer expert"
    )
    
    async with ClaudeSDKClient(options=options) as client:
        await client.query("Analyze the user table schema")
        async for msg in client.receive_response():
            print(msg)

if __name__ == "__main__":
    asyncio.run(main())
```

4. Make executable: `chmod +x .claude/skills/db-schema-analyzer/run.py`
5. Run the skill: `python .claude/skills/db-schema-analyzer/run.py`
6. Future database analysis tasks use this powerful, reusable skill

## Conclusion

This aggressive skill-first approach ensures that the project rapidly builds up a comprehensive library of reusable capabilities. By defaulting to skill creation, never asking for confirmation, and proactively using available tools (Python, grep, wget, etc.), we maximize efficiency and create a growing knowledge base that makes every subsequent task faster and more consistent.

**Remember:** You have powerful tools at your disposal. Use them proactively without asking for permission. Write Python scripts, run shell commands, fetch web content - whatever it takes to accomplish the task efficiently.
