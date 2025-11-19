# Utility Skills Guide

Complete guide for creating reusable, parameterized utility skills.

## Table of Contents

This guide is split into focused sections:

1. **This file** - Core philosophy, when to create, and common patterns
2. **[utility-patterns.md](utility-patterns.md)** - Detailed implementation patterns and templates
3. **[utility-implementation.md](utility-implementation.md)** - Step-by-step creation process and design principles

## Core Philosophy

**Don't solve the same problem twice.**

Utility skills are parameterized solutions to recurring problems. Instead of rewriting the same code for different inputs, create a skill once and reuse it with different parameters.

**Example:**
- **Without skill**: Write code to count references on Dragon Ball Z Wikipedia page → Write code again for Sheikh Hasina page → Write code again for Bengali language page...
- **With skill**: Create `wikipedia-utils` skill → Use for ANY Wikipedia page with different URL parameter

## When to Create a Utility Skill

### Create a utility skill when:

✅ **Task has clear parameters**
- URL changes but logic stays same
- File path changes but processing stays same
- Input data changes but analysis stays same
- Same operation, different targets

✅ **Pattern will recur**
- Different Wikipedia pages
- Different files to process
- Different APIs to query
- Same workflow, different data

✅ **Core logic is reusable**
- The "what to do" doesn't change
- Only the "what to do it to" changes
- Can be parameterized easily

### Don't create a utility skill when:

❌ **Highly specific one-off task**
- Unique situation unlikely to repeat
- Context is too specific to generalize

❌ **Requires deep context each time**
- Every instance needs different logic
- No clear parameterization possible

❌ **Logic changes completely each time**
- Not actually the same task
- Too variable to standardize

## Common Utility Skill Patterns

### Pattern 1: Web Data Extraction

**Use case:** Fetch and analyze web content
**Parameters:** URL, selector/pattern, output format
**Examples:**
- Wikipedia reference counter
- GitHub stars fetcher
- News article analyzer
- Product price monitor

**Template:**
```python
def extract_data(url, selector, format='json'):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.select(selector)
    return format_output(data, format)
```

### Pattern 2: File Format Conversion

**Use case:** Convert between file formats
**Parameters:** Input file, output format, options
**Examples:**
- CSV to JSON converter
- Markdown to HTML
- Image format converter
- Data serializer

**Template:**
```python
def convert_file(input_path, output_format, **options):
    data = read_file(input_path)
    converted = transform(data, output_format, options)
    return write_output(converted, output_format)
```

### Pattern 3: Text Analysis

**Use case:** Analyze text content
**Parameters:** Text/file, analysis type, filters
**Examples:**
- Word counter
- Sentiment analyzer
- Keyword extractor
- Readability scorer

**Template:**
```python
def analyze_text(text, analysis_type='sentiment', **filters):
    processed = preprocess(text, filters)
    result = run_analysis(processed, analysis_type)
    return format_results(result)
```

### Pattern 4: Data Processing

**Use case:** Filter, transform, aggregate data
**Parameters:** Data source, operations, output
**Examples:**
- CSV filter/aggregator
- JSON transformer
- Log analyzer
- Report generator

**Template:**
```python
def process_data(source, operations, output_format):
    data = load_data(source)
    for op in operations:
        data = apply_operation(data, op)
    return export(data, output_format)
```

### Pattern 5: API Client

**Use case:** Interact with external APIs
**Parameters:** Endpoint, method, params
**Examples:**
- GitHub API client
- Slack bot utilities
- Weather API fetcher
- Database query tool

**Template:**
```python
def api_call(endpoint, method='GET', **params):
    url = build_url(endpoint, params)
    response = requests.request(method, url)
    return parse_response(response)
```

## Quick Reference: Creating a Utility Skill

1. **Identify the pattern**: What stays the same across uses?
2. **Extract parameters**: What changes each time?
3. **Create parameterized script**: Accept parameters, execute core logic
4. **Initialize skill**: `scripts/init_skill.py utility-name`
5. **Add script**: Place in `scripts/` directory
6. **Document usage**: In SKILL.md, show how to use with different parameters
7. **Test**: Try with different inputs to verify reusability

## Recognizing Skill Opportunities

Watch for these patterns in user requests:

- "Do [X] for [Y]" → Later: "Do [X] for [Z]"
- "Count/Extract/Analyze [thing] from [source]"
- "Convert [format A] to [format B]"
- "Fetch [data] from [URL/API]"
- Repetitive tasks with minor variations

**Example conversation:**
```
User: "How many references on Dragon Ball Z Wikipedia page?"
→ Think: This is "count references" on "any Wikipedia page"
→ Create: wikipedia-utils skill with URL parameter
→ Benefit: Works for ALL Wikipedia pages
```

## Skills vs One-Off Solutions

| Aspect | Utility Skill | One-Off Solution |
|--------|---------------|------------------|
| **Reusability** | High - works for many cases | Low - solves one instance |
| **Upfront effort** | Slightly more | Minimal |
| **Long-term value** | High - accumulates | Low - disposable |
| **Maintenance** | Easier - centralized | Harder - scattered |
| **When to use** | Pattern will recur | Truly unique case |

## Next Steps

**For detailed implementation guidance:**
- **Patterns and templates**: See [utility-patterns.md](utility-patterns.md)
- **Step-by-step process**: See [utility-implementation.md](utility-implementation.md)
- **Script design principles**: See [utility-implementation.md](utility-implementation.md#script-design-principles)
- **Parameterization strategies**: See [utility-implementation.md](utility-implementation.md#parameterization-strategies)
