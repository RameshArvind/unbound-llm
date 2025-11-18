# Claude Code Workflow: Skill-First Approach

## Overview

This document outlines the workflow for handling tasks in this project using Claude Code's skill system. The goal is to maximize reusability and efficiency by creating skills for repeatable tasks.

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
    ├─→ Check: Is this task repeatable/scriptable?
    │   ├─→ YES: Create a new skill
    │   │         ↓
    │   │         Use skill-creator tool
    │   │         ↓
    │   │         Execute task using new skill
    │   │         ↓
    │   │         Complete
    │   │
    │   └─→ NO: Execute task directly
    │           ↓
    │           Use appropriate tools
    │           ↓
    │           Complete
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

### 3. Identifying Repeatable Tasks

A task is considered repeatable/scriptable if it:
- Follows a consistent process or pattern
- Could be requested multiple times with different inputs
- Has clear, definable steps that can be automated
- Provides value as a reusable capability

**Examples of repeatable tasks:**
- Generating specific types of reports or documents
- Running standardized code analysis workflows
- Creating artifacts with consistent structure/styling
- Performing domain-specific transformations
- Executing multi-step validation procedures

**Examples of non-repeatable tasks:**
- One-off exploratory analysis
- Highly context-specific bug fixes
- Unique architectural decisions
- Custom refactoring that won't be repeated

### 4. Creating New Skills

When you identify a repeatable task without an existing skill:

1. **Invoke the skill-creator tool:**
   ```
   Use the Skill tool with skill="skill-creator"
   ```

2. **Define the skill with:**
   - Clear name (kebab-case)
   - Precise description of when to use it
   - Detailed instructions for execution
   - Required tools and capabilities
   - Expected inputs and outputs

3. **Document the new skill:**
   - Update this file if needed
   - Ensure the skill description is discoverable
   - Add usage examples

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
1. Always scan available skills first
2. Prioritize skill usage over ad-hoc implementations
3. If creating a skill, invoke skill-creator proactively
4. Execute the task using the skill immediately after creation
5. Don't ask permission unless the task is ambiguous

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
2. Is it repeatable? → YES (weekly cadence)
3. Invoke `skill-creator`
4. Create `performance-report-generator` skill
5. Use new skill to generate report
6. Future weekly reports use this skill

### Example 3: One-off Fix
**Request:** "Fix the typo in the header"

**Workflow:**
1. Check skills → Not applicable
2. Is it repeatable? → NO (one-off fix)
3. Execute directly with Edit tool
4. Complete

## Conclusion

This skill-first approach ensures that our project builds up a library of reusable capabilities over time, making Claude Code increasingly efficient and consistent for common tasks while maintaining flexibility for unique situations.
