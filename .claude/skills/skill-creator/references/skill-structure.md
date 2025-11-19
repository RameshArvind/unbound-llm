# Skill Structure and Anatomy

## Directory Structure

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

## SKILL.md (required)

Every SKILL.md consists of two parts:

### Frontmatter (YAML)

Contains `name` and `description` fields. These are the only fields that Claude reads to determine when the skill gets used, thus it is very important to be clear and comprehensive in describing what the skill is, and when it should be used.

**Requirements:**

**name:**
- Maximum 64 characters
- Lowercase letters, numbers, and hyphens only
- Cannot contain XML tags
- Cannot use reserved words: "anthropic", "claude"
- Must match the skill directory name exactly

**description:**
- Non-empty
- Maximum 1024 characters
- Cannot contain XML tags
- Must include triggering conditions
- Should explain both what the skill does AND when to use it

### Body (Markdown)

Instructions and guidance for using the skill. Only loaded AFTER the skill triggers (if at all).

**Guidelines:**
- Keep under 200 lines
- Use imperative/infinitive form
- Include concrete examples
- Reference bundled resources clearly
- Split longer content into reference files

## Bundled Resources (optional)

### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

**When to include:**
- Same code is being rewritten repeatedly
- Deterministic reliability is needed
- Complex operations that are error-prone when written by hand

**Examples:**
- `scripts/rotate_pdf.py` for PDF rotation tasks
- `scripts/extract_data.py` for data extraction
- `scripts/process_template.py` for template processing

**Benefits:**
- Token efficient (can execute without loading into context)
- Deterministic and reliable
- Reusable across multiple invocations

**Note:** Scripts may still need to be read by Claude for patching or environment-specific adjustments.

### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform Claude's process and thinking.

**When to include:**
- Documentation that Claude should reference while working
- Content too detailed for SKILL.md
- Information only needed for specific use cases

**Examples:**
- `references/schema.md` - Database schemas
- `references/api_reference.md` - API specifications
- `references/policies.md` - Company policies
- `references/workflows.md` - Detailed workflow guides

**Use cases:**
- Database schemas
- API documentation
- Domain knowledge
- Company policies
- Detailed workflow guides

**Benefits:**
- Keeps SKILL.md lean and under 200 lines
- Loaded only when Claude determines it's needed
- Progressive disclosure of information

**Best practices:**
- If files are large (>200 lines), include a table of contents at the top
- Keep references one level deep from SKILL.md
- Clearly indicate from SKILL.md when to read each reference
- Avoid duplication between SKILL.md and references

**Avoid duplication:** Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill—this keeps SKILL.md lean while making information discoverable without hogging the context window.

### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output Claude produces.

**When to include:**
- Skill needs files that will be used in the final output
- Templates, images, or boilerplate that get copied/modified
- Resources that are too large or not useful to read as text

**Examples:**
- `assets/logo.png` - Brand assets
- `assets/slides.pptx` - PowerPoint templates
- `assets/frontend-template/` - HTML/React boilerplate directories
- `assets/font.ttf` - Typography files
- `assets/sample_data.csv` - Example datasets

**Use cases:**
- Templates (PowerPoint, Word, etc.)
- Images and icons
- Boilerplate code directories
- Fonts
- Sample documents that get copied or modified

**Benefits:**
- Separates output resources from documentation
- Enables Claude to use files without loading them into context
- Supports complex output formats

## What NOT to Include in a Skill

A skill should only contain essential files that directly support its functionality. Do NOT create extraneous documentation or auxiliary files, including:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- CONTRIBUTING.md
- LICENSE.txt
- Test files or testing documentation
- Development notes or build scripts

**Rationale:** The skill should only contain the information needed for an AI agent to do the job at hand. It should not contain auxiliary context about the process that went into creating it, setup and testing procedures, user-facing documentation, etc. Creating additional documentation files just adds clutter and confusion.

## Progressive Disclosure Patterns

For detailed patterns and examples on how to organize skills with multiple variations, frameworks, or conditional details:

**See [progressive-disclosure.md](progressive-disclosure.md)**
