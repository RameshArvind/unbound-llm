# Creating Utility Skills for Recurring Tasks

This guide focuses on creating **reusable utility skills** that solve recurring user problems.

## Core Philosophy

**Don't solve the same problem twice.**

When a user comes with a task:
1. Solve it (write the script, do the analysis)
2. Recognize if it's a recurring pattern
3. Create a skill so next time you can reuse it

## When to Create a Utility Skill

### ✅ Create a Skill When:

1. **Task has clear parameters**
   - "Count references on Wikipedia page X"
   - "Extract emails from website Y"
   - "Convert format A to format B"

2. **Pattern will recur**
   - Different Wikipedia pages
   - Different websites
   - Different files

3. **Core logic is reusable**
   - Same extraction pattern
   - Same transformation
   - Same analysis

4. **Can be parameterized**
   - URL changes, logic stays same
   - File changes, processing stays same
   - Input changes, algorithm stays same

### ❌ Don't Create a Skill When:

1. **Highly specific one-off**
   - "Rename these 3 specific files"
   - "Fix this one bug in this code"

2. **Requires deep context**
   - "Understand this entire codebase"
   - "Analyze our business model" (without template)

3. **Changes every time**
   - No stable pattern
   - Different logic each time

## Utility Skill Patterns

### Pattern 1: Web Data Extraction

**Example: Wikipedia Reference Counter**

**Problem:**
- User: "How many unique references on Dragon Ball Z Wikipedia page?"
- We write a script
- Later: "How many references on Sheikh Hasina page?"
- Instead of rewriting, use skill!

**Skill Structure:**
```
wikipedia-utils/
├── SKILL.md
└── scripts/
    ├── count_references.py    # Parameterized script
    ├── extract_infobox.py     # Another utility
    └── get_categories.py      # Another utility
```

**Key: Scripts take URL as parameter**

```python
#!/usr/bin/env python3
"""Count unique references on a Wikipedia page."""
import sys
import requests
from bs4 import BeautifulSoup

def count_references(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find references section
    refs = soup.find_all('li', {'id': lambda x: x and x.startswith('cite_note')})

    return len(refs)

if __name__ == "__main__":
    url = sys.argv[1]
    count = count_references(url)
    print(f"Unique references: {count}")
```

**SKILL.md describes:**
- What the scripts do
- How to use them
- What parameters they accept

### Pattern 2: File Format Conversion

**Example: Data Format Converter**

**Problem:**
- User: "Convert this CSV to JSON"
- Later: "Convert this TSV to YAML"
- Later: "Convert this Excel to CSV"

**Skill Structure:**
```
format-converter/
├── SKILL.md
└── scripts/
    ├── csv_to_json.py
    ├── json_to_csv.py
    ├── csv_to_yaml.py
    ├── excel_to_csv.py
    └── generic_convert.py    # Smart dispatcher
```

### Pattern 3: Text Analysis

**Example: Text Statistics**

**Problem:**
- User: "Count words in this document"
- Later: "Analyze readability of this text"
- Later: "Find most common words in this file"

**Skill Structure:**
```
text-analyzer/
├── SKILL.md
└── scripts/
    ├── word_count.py
    ├── readability.py
    ├── keyword_extraction.py
    └── sentiment.py
```

### Pattern 4: API Integration

**Example: GitHub API Utils**

**Problem:**
- User: "Get my GitHub stars count"
- Later: "List my repositories"
- Later: "Get commit stats"

**Skill Structure:**
```
github-utils/
├── SKILL.md
├── scripts/
│   ├── get_repos.py
│   ├── get_stars.py
│   ├── get_commits.py
│   └── github_api.py    # Shared API client
└── references/
    └── api-examples.md
```

### Pattern 5: Data Processing Pipeline

**Example: Log Analyzer**

**Problem:**
- User: "Extract errors from this log"
- Later: "Find slow requests in this log"
- Later: "Group logs by endpoint"

**Skill Structure:**
```
log-analyzer/
├── SKILL.md
└── scripts/
    ├── extract_errors.py
    ├── find_slow_requests.py
    ├── group_by_field.py
    └── log_parser.py    # Shared parsing logic
```

## Step-by-Step: Creating a Utility Skill

### Example: Wikipedia Reference Counter

**Step 1: User comes with request**
```
User: "How many unique references are on https://en.wikipedia.org/wiki/Dragon_Ball_Z?"
```

**Step 2: Solve it first**

Write the solution:
```python
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Dragon_Ball_Z"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
refs = soup.find_all('li', {'id': lambda x: x and x.startswith('cite_note')})
print(f"Unique references: {len(refs)}")
```

**Step 3: Recognize the pattern**

Ask yourself:
- ❓ Could this be asked for different Wikipedia pages? **YES**
- ❓ Is the core logic reusable? **YES**
- ❓ Can I parameterize it? **YES** (just change URL)

→ **This should be a skill!**

**Step 4: Create the skill**

```bash
# Initialize skill
mkdir -p .claude/skills/wikipedia-utils/scripts

# Create parameterized script
cat > .claude/skills/wikipedia-utils/scripts/count_references.py << 'EOF'
#!/usr/bin/env python3
"""Count unique references on a Wikipedia page."""
import sys
import requests
from bs4 import BeautifulSoup

def count_references(url):
    """Count unique references on a Wikipedia page."""
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    refs = soup.find_all('li', {'id': lambda x: x and x.startswith('cite_note')})
    return len(refs)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: count_references.py <wikipedia_url>")
        sys.exit(1)

    url = sys.argv[1]
    count = count_references(url)
    print(f"Unique references: {count}")
EOF

chmod +x .claude/skills/wikipedia-utils/scripts/count_references.py
```

**Step 5: Write SKILL.md**

```markdown
---
name: wikipedia-utils
description: Utilities for extracting data from Wikipedia pages. Use this skill when users ask questions about Wikipedia page content, such as counting references, extracting infobox data, getting categories, or analyzing page structure. Trigger when user provides a Wikipedia URL and wants to extract structured information from it.
---

# Wikipedia Utilities

Extract structured data from Wikipedia pages using parameterized scripts.

## Available Tools

### Count References

Count unique references on any Wikipedia page.

**Usage:**
```bash
python .claude/skills/wikipedia-utils/scripts/count_references.py <url>
```

**Example:**
```bash
python .claude/skills/wikipedia-utils/scripts/count_references.py \
  "https://en.wikipedia.org/wiki/Dragon_Ball_Z"

# Output: Unique references: 287
```

**When to use:**
- User asks "How many references..."
- User asks "Count citations..."
- User wants reference statistics

## Adding More Utilities

When users ask for other Wikipedia data:
1. Create a new script in `scripts/`
2. Make it parameterized (takes URL as input)
3. Update this SKILL.md

**Future utilities:**
- Extract infobox data
- Get page categories
- List external links
- Extract section headers
```

**Step 6: Test it**

```bash
# Test with original request
python .claude/skills/wikipedia-utils/scripts/count_references.py \
  "https://en.wikipedia.org/wiki/Dragon_Ball_Z"

# Test with new request
python .claude/skills/wikipedia-utils/scripts/count_references.py \
  "https://en.wikipedia.org/wiki/Sheikh_Hasina"
```

**Step 7: Use it for future requests**

Next time user asks about Wikipedia references:
1. Skill triggers automatically (from description)
2. Use existing script with new URL
3. Done! No rewriting needed.

## Skill Evolution

Skills grow over time:

### Version 1: Single Script
```
wikipedia-utils/
├── SKILL.md
└── scripts/
    └── count_references.py
```

User asks: "How many references on Dragon Ball Z page?"
→ Use count_references.py

### Version 2: Multiple Scripts

User asks: "What categories is this page in?"
→ Create `get_categories.py`

```
wikipedia-utils/
├── SKILL.md
└── scripts/
    ├── count_references.py
    └── get_categories.py
```

### Version 3: Comprehensive Utility

User asks: "Extract the infobox data"
→ Create `extract_infobox.py`

User asks: "Get all external links"
→ Create `get_external_links.py`

```
wikipedia-utils/
├── SKILL.md
└── scripts/
    ├── count_references.py
    ├── get_categories.py
    ├── extract_infobox.py
    ├── get_external_links.py
    └── wikipedia_api.py    # Shared utilities
```

## Parameterization Strategies

### Strategy 1: Command-Line Arguments

```python
import sys

def process(url, format='json'):
    # ...
    pass

if __name__ == "__main__":
    url = sys.argv[1]
    format = sys.argv[2] if len(sys.argv) > 2 else 'json'
    process(url, format)
```

**Usage:** `python script.py <url> [format]`

### Strategy 2: Environment Variables

```python
import os

API_KEY = os.environ.get('GITHUB_TOKEN', '')
MAX_RESULTS = int(os.environ.get('MAX_RESULTS', '100'))
```

**Usage:** `GITHUB_TOKEN=xxx python script.py`

### Strategy 3: Config File

```python
import json
from pathlib import Path

config_file = Path.home() / '.config' / 'myskill' / 'config.json'
if config_file.exists():
    config = json.loads(config_file.read_text())
```

### Strategy 4: Interactive Prompts

```python
url = input("Enter Wikipedia URL: ")
format = input("Output format (json/csv) [json]: ") or 'json'
```

**Choose based on:**
- CLI args: Simple, few parameters
- Env vars: Secrets, configuration
- Config file: Complex, persistent settings
- Interactive: User-friendly, exploratory

## Script Design Principles

### 1. Single Responsibility

Each script does ONE thing well:
- ✅ `count_references.py` - Count references
- ✅ `get_categories.py` - Get categories
- ❌ `wikipedia_tool.py --action count` - Too generic

### 2. Clear Input/Output

```python
# Good: Clear inputs and outputs
def count_references(url: str) -> int:
    """
    Count unique references on a Wikipedia page.

    Args:
        url: Full Wikipedia page URL

    Returns:
        Number of unique references
    """
    # ...
    return count

# Bad: Unclear
def process(data):
    # What is data? What does this return?
    return result
```

### 3. Error Handling

```python
def count_references(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        refs = soup.find_all('li', {'id': lambda x: x and x.startswith('cite_note')})
        return len(refs)
    except Exception as e:
        print(f"Error parsing page: {e}", file=sys.stderr)
        sys.exit(1)
```

### 4. Help Text

```python
if len(sys.argv) != 2:
    print("""
Usage: count_references.py <wikipedia_url>

Count unique references on a Wikipedia page.

Example:
    python count_references.py "https://en.wikipedia.org/wiki/Python_(programming_language)"

Output:
    Unique references: 234
    """, file=sys.stderr)
    sys.exit(1)
```

### 5. Testability

```python
# Separate logic from CLI
def count_references(url):
    """Pure function - easy to test."""
    # ...
    return count

# CLI wrapper
if __name__ == "__main__":
    url = sys.argv[1]
    result = count_references(url)
    print(f"Unique references: {result}")
```

## Common Utility Skill Templates

### Web Scraping Skill

```
web-scraper/
├── SKILL.md
└── scripts/
    ├── extract_emails.py       # Extract emails from URL
    ├── extract_links.py        # Extract all links
    ├── download_images.py      # Download all images
    └── scraper_utils.py        # Shared utilities
```

### Data Processing Skill

```
data-processor/
├── SKILL.md
└── scripts/
    ├── csv_stats.py            # CSV statistics
    ├── json_flatten.py         # Flatten nested JSON
    ├── merge_files.py          # Merge multiple files
    └── filter_data.py          # Filter by criteria
```

### API Client Skill

```
api-client/
├── SKILL.md
├── scripts/
│   ├── list_resources.py       # List resources
│   ├── get_resource.py         # Get single resource
│   ├── create_resource.py      # Create resource
│   └── api_client.py           # Shared client
└── references/
    └── api-docs.md             # API reference
```

### File Operations Skill

```
file-ops/
├── SKILL.md
└── scripts/
    ├── batch_rename.py         # Rename files by pattern
    ├── organize_by_date.py     # Organize by creation date
    ├── find_duplicates.py      # Find duplicate files
    └── bulk_convert.py         # Convert file formats
```

## Tips for Utility Skills

### 1. Start Small, Grow Organically

Don't try to build everything upfront:
- Start with one script
- Add more as users request them
- Refactor when patterns emerge

### 2. Shared Utilities Module

When multiple scripts share logic:
```python
# scripts/wikipedia_api.py
import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    """Shared: Fetch and parse Wikipedia page."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')

# scripts/count_references.py
from wikipedia_api import fetch_page

def count_references(url):
    soup = fetch_page(url)  # Use shared function
    refs = soup.find_all('li', {'id': lambda x: x and x.startswith('cite_note')})
    return len(refs)
```

### 3. Document in SKILL.md

For each script, document:
- What it does
- Input parameters
- Output format
- Example usage
- When to use it

### 4. Version Dependencies

If scripts need packages, document in SKILL.md:
```markdown
## Requirements

```bash
pip install requests beautifulsoup4 lxml
```

Or include `requirements.txt` in skill folder.
```

### 5. Make Scripts Discoverable

In SKILL.md, organize by use case:
```markdown
## Use Cases

### Counting Things
- `count_references.py` - Count page references
- `count_sections.py` - Count page sections

### Extracting Data
- `extract_infobox.py` - Extract infobox data
- `extract_categories.py` - Extract page categories
```

## Real Example: Complete Wikipedia Utils Skill

See `.claude/skills/wikipedia-utils/` for a fully implemented example.

Key features:
- Multiple parameterized scripts
- Shared utilities module
- Clear documentation
- Error handling
- Examples

This skill can handle:
- "Count references on page X"
- "Get categories for page Y"
- "Extract infobox from page Z"

All without rewriting code - just different parameters!

## Recognizing Skill Opportunities

When solving a task, ask:
1. **Is this parameterizable?** Can I change URL/file/input and reuse logic?
2. **Will users ask this again?** Similar requests likely?
3. **Is the pattern clear?** Same type of processing each time?
4. **Can I generalize it?** Turn specific solution into general tool?

If **3+ yes** → Create a skill!

## Skills vs One-Off Solutions

**Create a skill when:**
- Pattern is clear and reusable
- Multiple similar requests expected
- Can parameterize easily
- Logic is stable

**Just solve it when:**
- Highly specific one-off
- Unlikely to recur
- Too context-dependent
- Changes every time

**When in doubt:** Solve it first, then decide if it's worth making a skill.
