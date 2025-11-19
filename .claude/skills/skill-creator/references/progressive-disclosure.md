## Progressive Disclosure Patterns

When skills grow large, use these patterns to keep SKILL.md under 200 lines:

### Pattern 1: High-level guide with references

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[brief code example]

## Advanced features

- **Form filling**: See [forms.md](references/forms.md) for complete guide
- **API reference**: See [api_reference.md](references/api_reference.md) for all methods
- **Examples**: See [examples.md](references/examples.md) for common patterns
```

Claude loads forms.md, api_reference.md, or examples.md only when needed.

### Pattern 2: Domain-specific organization

For skills with multiple domains, organize content by domain to avoid loading irrelevant context:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── references/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

When a user asks about sales metrics, Claude only reads sales.md.

### Pattern 3: Framework variants

For skills supporting multiple frameworks or variants, organize by variant:

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

When the user chooses AWS, Claude only reads aws.md.

### Pattern 4: Conditional details

Show basic content, link to advanced content:

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [docx_js.md](references/docx_js.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [redlining.md](references/redlining.md)
**For OOXML details**: See [ooxml.md](references/ooxml.md)
```

Claude reads redlining.md or ooxml.md only when the user needs those features.

## Important Guidelines

- **Keep SKILL.md under 200 lines** - Split content into references when approaching this limit
- **Avoid deeply nested references** - Keep references one level deep from SKILL.md
- **Structure longer reference files** - For files >200 lines, include a table of contents at the top
- **Clear navigation** - Reference files clearly from SKILL.md with "when to read" guidance
- **No redundancy** - Don't duplicate content between SKILL.md and references
