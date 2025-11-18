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
    │         Use skill-creator tool (no confirmation needed)
    │         ↓
    │         Reload skills to make available
    │         ↓
    │         Invoke newly created skill
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
- Code generation and design (frontend-design, web-artifacts-builder)
- Visual creation (canvas-design, algorithmic-art, slack-gif-creator)
- Testing and validation (webapp-testing)
- Development tools (mcp-builder, skill-creator)
- Communication (internal-comms)
- Styling and theming (theme-factory, brand-guidelines)
- File operations (context-fetcher)

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

1. **Invoke the skill-creator tool without asking:**
   ```
   Use the Skill tool with skill="skill-creator"
   ```
   **NEVER ask for permission or confirmation first.**

2. **Define the skill with:**
   - Clear name (kebab-case)
   - Precise description of when to use it
   - Detailed instructions for execution
   - Required tools and capabilities
   - Expected inputs and outputs

3. **Reload skills immediately after creation:**
   - After creating the skill, use the Bash tool to reload Claude Code skills
   - This makes the new skill available in the current session
   - Command: Run the appropriate skill reload mechanism for your session

4. **Execute immediately:**
   - Create the skill
   - Reload to make it available
   - Invoke the newly created skill to complete the current task
   - No waiting, no asking, just do it

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
4. **After creating a skill, immediately reload to make it available**
5. **Invoke the newly created skill to complete the current task**
6. **Create → Reload → Execute in one seamless flow**
7. **Bias heavily toward skill creation - it's the default, not the exception**
8. **Only execute directly for truly trivial one-off operations**

### For Users

To maximize this workflow:
- Create skills for your project-specific workflows
- Keep skill descriptions clear and specific
- Use descriptive names that indicate when to invoke them
- Update skills as processes evolve

## Examples

### Example 1: Frontend Development
**Request:** "Create a landing page for our product"

**Workflow:**
1. Check skills → Found: `frontend-design`
2. Invoke `frontend-design` skill
3. Execute task with skill's specialized knowledge
4. Complete

### Example 2: New Custom Report
**Request:** "Generate a weekly performance report"

**Workflow:**
1. Check skills → No existing skill for this format
2. Immediately invoke `skill-creator` (no asking, no confirmation)
3. Create `performance-report-generator` skill
4. Reload skills to make it available in current session
5. Invoke the new skill to generate report immediately
6. Future weekly reports use this skill

### Example 3: One-off Fix
**Request:** "Fix the typo in the header"

**Workflow:**
1. Check skills → Not applicable
2. Truly trivial one-step operation → Execute directly with Edit tool
3. Complete

### Example 4: Code Analysis Task
**Request:** "Analyze the error handling patterns in the codebase"

**Workflow:**
1. Check skills → No existing skill
2. Multi-step task with potential reuse → CREATE SKILL (default action)
3. Immediately invoke `skill-creator` without asking
4. Create `error-handling-analyzer` skill
5. Reload skills to make it available
6. Invoke the new skill to complete analysis immediately
7. Future code analysis tasks benefit from this skill

### Example 5: Even Seemingly One-Off Tasks
**Request:** "Refactor the authentication module to use async/await"

**Workflow:**
1. Check skills → No existing skill
2. This is a multi-step refactoring → CREATE SKILL (default)
3. Invoke `skill-creator` immediately
4. Create `async-refactoring` or similar skill
5. Reload skills to make it available
6. Invoke the new skill to complete refactoring
7. Future refactoring tasks use this pattern

**Key point:** Even if you think "this might be one-off", create the skill anyway. The marginal cost is tiny, and the benefit of having it is huge.

## Conclusion

This aggressive skill-first approach ensures that our project rapidly builds up a comprehensive library of reusable capabilities. By defaulting to skill creation and never asking for confirmation, we maximize efficiency and create a growing knowledge base that makes every subsequent task faster and more consistent.
