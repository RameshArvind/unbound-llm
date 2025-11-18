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

2. **Skill location (auto-detected):**
   - If current directory (or parent) has `.claude/` → create in `./.claude/skills/`
   - Else if `/root/.claude/` exists and is accessible → create in `/root/.claude/skills/`
   - Otherwise → create in `~/.claude/skills/` (fallback to user's home)
   - This ensures skills are always accessible, either project-local or globally

3. **Define the skill with:**
   - Clear name (kebab-case)
   - Precise description of when to use it
   - Detailed instructions for execution
   - Required tools and capabilities
   - Expected inputs and outputs

4. **Make the skill available:**
   - After creating the skill, it should be available in the appropriate `.claude/skills/` directory
   - Skills are loaded from this directory structure
   - Verify the skill exists and has proper structure

5. **Use the skill:**
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

### Communication: Explain What You're Doing in Your Output

**CRITICAL: ALWAYS include this in your final response to the user. NEVER skip this step.**

**When creating a NEW skill:**
ALWAYS start your output by mentioning you're creating a new skill:
```
"Creating a new 'hacker-news-scraper' skill for counting HN comments...

[performs work]

Found 342 comments on this discussion.

Note: Created the 'hacker-news-scraper' skill - this can be reused for future HN analysis."
```

**When using an EXISTING skill:**
ALWAYS start your output by mentioning you're using an existing skill:
```
"Using the existing 'hacker-news-scraper' skill...

[performs work]

Found 256 comments on this discussion."
```

**When executing directly (no skill):**
Only for trivial one-off operations. Still mention why no skill was created:
```
"[Direct execution - trivial one-line fix]

Fixed typo in header."
```

**Why this matters:**
- Helps users understand when capabilities are being built vs. reused
- Shows the growing library of project-specific tools
- Makes it clear when skills can be reused for similar future tasks
- Provides transparency about the skill-first approach
- Users can see the investment in reusable infrastructure
- Users know what tools are available for future use

**This is MANDATORY, not optional:** Every response must include this context. One line at the start is required, optionally a note at the end for new skills.

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
**Request:** "Generate another weekly performance report"

**Workflow:**
1. Check skills → Found: `performance-report-generator` skill exists
2. **Say:** "Using the existing 'performance-report-generator' skill..."
3. Invoke the skill directly
4. Execute task with skill's specialized knowledge
5. Complete

### Example 2: New Custom Report
**Request:** "Generate a weekly performance report"

**Workflow:**
1. Check skills → No existing skill for this format
2. **Say:** "Creating a new 'performance-report-generator' skill for weekly reports..."
3. Immediately create the skill structure (no asking, no confirmation)
4. Create `performance-report-generator` skill
5. Set it up in `.claude/skills/` directory
6. Use the new skill to generate report immediately
7. Future weekly reports use this skill

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
3. **Say:** "Creating a new 'error-handling-analyzer' skill for code analysis..."
4. Immediately create skill structure without asking
5. Create `error-handling-analyzer` skill
6. Set it up in the skills directory
7. Use the new skill to complete analysis immediately
8. Future code analysis tasks benefit from this skill

### Example 5: Even Seemingly One-Off Tasks
**Request:** "Refactor the authentication module to use async/await"

**Workflow:**
1. Check skills → No existing skill
2. This is a multi-step refactoring → CREATE SKILL (default)
3. **Say:** "Creating a new 'async-refactoring' skill for future async/await conversions..."
4. Create skill structure immediately
5. Create `async-refactoring` or similar skill
6. Set it up in the skills directory
7. Use the new skill to complete refactoring
8. Future refactoring tasks use this pattern

**Key point:** Even if you think "this might be one-off", create the skill anyway. The marginal cost is tiny, and the benefit of having it is huge.

## Conclusion

This aggressive skill-first approach ensures that the project rapidly builds up a comprehensive library of reusable capabilities. By defaulting to skill creation, never asking for confirmation, and proactively using available tools (Python, grep, wget, etc.), we maximize efficiency and create a growing knowledge base that makes every subsequent task faster and more consistent.

**Remember:** You have powerful tools at your disposal. Use them proactively without asking for permission. Write Python scripts, run shell commands, fetch web content - whatever it takes to accomplish the task efficiently.
