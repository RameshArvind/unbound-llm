---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks—they transform Claude from a general-purpose agent into a specialized agent
equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex and repetitive tasks
5. **Reusable utility scripts** - Parameterized tools that solve recurring user problems ⭐

### Where Skills Work

Skills are supported across multiple Claude platforms:

| Platform | Custom Skills | Pre-built Skills (pptx, xlsx, docx, pdf) |
|----------|---------------|-------------------------------------------|
| **Claude Code** | ✅ Filesystem-based | ❌ Not available |
| **Claude API** | ✅ Workspace-wide | ✅ Available |
| **Agent SDK** | ✅ Via `.claude/skills/` | ❌ Not available |
| **Claude.ai** | ✅ User-only (uploaded as zip) | ✅ Available |

**Important:** Custom skills don't sync across platforms. Skills created for Claude Code must be separately uploaded to other platforms if needed.

### Runtime Environment Constraints

Different platforms have different runtime capabilities that affect skill behavior:

| Platform | Network Access | Package Installation | Environment |
|----------|----------------|---------------------|-------------|
| **Claude Code** | ✅ Full access | ✅ Allowed | Local development environment |
| **Claude API** | ❌ Restricted | ❌ Pre-configured only | Controlled sandbox |
| **Claude.ai** | ⚠️ Variable | ❌ Not allowed | Web-based environment |

**Design implications:**
- **Claude Code skills** can freely use network requests, install packages, and access local files
- **Claude API skills** must use pre-installed dependencies and cannot fetch external resources
- **Cross-platform skills** should avoid network dependencies and use only standard libraries

## Creating Utility Skills for Recurring Tasks ⭐

**Don't solve the same problem twice.** If a task has clear parameters and the core logic is reusable, create a utility skill!

**Example:** User asks "How many references on Dragon Ball Z Wikipedia page?" → Create a parameterized `wikipedia-utils` skill that works for ANY Wikipedia page.

**When to create:**
- ✅ Task has clear parameters (URL, file, input changes but logic stays same)
- ✅ Pattern will recur (different pages, files, etc.)
- ✅ Core logic is reusable

**For complete guide**, including examples, patterns, and implementation: **See [utility-skills-guide.md](references/utility-skills-guide.md)**

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Claude needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.

**Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.

**Low freedom (specific scripts, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of Claude as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

### Anatomy of a Skill

Every skill requires:
- **SKILL.md** (required) - YAML frontmatter + markdown instructions (keep under 200 lines)
- **Bundled resources** (optional) - scripts/, references/, assets/

**For detailed structure**, including frontmatter requirements, bundled resource types, and progressive disclosure patterns: **See [skill-structure.md](references/skill-structure.md)**

### Progressive Disclosure Design Principle

Skills use a **three-level loading architecture** to manage context efficiently. This ensures only relevant content occupies the context window at any given time:

| Level | When Loaded | Token Cost | Content |
|-------|-------------|------------|---------|
| **1: Metadata** | Always (at startup) | ~100 tokens per skill | Name and description from YAML frontmatter |
| **2: Instructions** | When skill triggers | <5k tokens (keep under 200 lines) | SKILL.md body with step-by-step guidance |
| **3: Resources** | As needed by Claude | Effectively unlimited | Scripts (executed via bash), references (loaded on demand), assets (used in output) |

**Key benefits:**
- **Level 1** is always loaded so Claude knows what skills are available
- **Level 2** only loads when the skill is actually needed
- **Level 3** resources can be unlimited because scripts execute without loading into context, and reference files load only when Claude determines they're needed

#### Progressive Disclosure Patterns

**Key principle:** Keep SKILL.md under 200 lines. Split content into reference files when approaching this limit.

**Common patterns:**
- Link to advanced topics from basic content
- Organize by domain (finance.md, sales.md) or framework (aws.md, gcp.md)
- Load only relevant sections as needed

**See [skill-structure.md](references/skill-structure.md)** for detailed patterns and examples.

## Security Considerations

When creating skills, follow security best practices to avoid vulnerabilities like command injection, path traversal, and information disclosure.

**For complete security guidelines**, including code examples, testing checklists, and common vulnerabilities: **See [security.md](references/security.md)**

## Skill Creation Process

**Quick overview:**

1. **Understand** - Get concrete examples of skill usage
2. **Plan** - Identify reusable scripts, references, assets
3. **Initialize** - Run `scripts/init_skill.py <skill-name>`
4. **Edit** - Implement resources and write SKILL.md (keep under 200 lines)
5. **Package** - Run `scripts/package_skill.py <path/to/skill>`
6. **Iterate** - Test, improve, repeat

**For detailed step-by-step guide**, including examples, usage patterns, and best practices: **See [creation-process.md](references/creation-process.md)**

### Quick Start

```bash
# Initialize a new skill (auto-detects location)
scripts/init_skill.py my-skill-name

# Package when done
scripts/package_skill.py path/to/my-skill-name
```
