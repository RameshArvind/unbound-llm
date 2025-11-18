# Enhanced Skill Creator - Build Reusable Solutions

**Date:** 2025-11-18
**Status:** ✅ Complete & Ready to Use

## Overview

The **skill-creator** has been enhanced to focus on creating **reusable utility skills** that solve recurring user problems. Instead of rewriting solutions for similar tasks, create a skill once and reuse it with different parameters.

---

## 🎯 Core Philosophy

### Don't Solve the Same Problem Twice

**Before (inefficient):**
```
User: "Count references on Dragon Ball Z Wikipedia page"
→ Write custom script
→ Solve it
→ Discard code

Later...
User: "Count references on Sheikh Hasina page"
→ Write custom script AGAIN
→ Solve it AGAIN
→ Discard code AGAIN
```

**After (efficient):**
```
User: "Count references on Dragon Ball Z Wikipedia page"
→ Write parameterized script
→ Create wikipedia-utils skill
→ Use it

Later...
User: "Count references on Sheikh Hasina page"
→ Use existing skill with new URL
→ DONE! No rewriting.
```

---

## 🚀 When to Create a Utility Skill

Ask yourself these questions:

### ✅ Create a Skill When:

1. **Task has clear parameters**
   - ✅ URL changes, logic stays same
   - ✅ File changes, processing stays same
   - ✅ Input changes, algorithm stays same

2. **Pattern will recur**
   - ✅ Different Wikipedia pages
   - ✅ Different data files
   - ✅ Different API endpoints

3. **Core logic is reusable**
   - ✅ Same extraction pattern
   - ✅ Same transformation
   - ✅ Same analysis approach

4. **Can be parameterized**
   - ✅ Command-line arguments
   - ✅ Environment variables
   - ✅ Config files

### ❌ Don't Create a Skill When:

1. **Highly specific one-off**
   - "Rename these 3 specific files"
   - "Fix this one bug in line 42"

2. **Requires deep context**
   - "Understand this entire codebase"
   - "Analyze our specific business model"

3. **Changes every time**
   - No stable pattern
   - Different logic each request

---

## 📚 What Was Added

### 1. Comprehensive Guide

**File:** `.claude/skills/skill-creator/references/utility-skills-guide.md`

**Includes:**
- When to create utility skills (decision framework)
- Common patterns (web scraping, data processing, API clients)
- Step-by-step walkthrough (Wikipedia example)
- Script design principles
- Parameterization strategies
- Multiple real examples

**5 Key Patterns:**
1. Web data extraction
2. File format conversion
3. Text analysis
4. API integration
5. Data processing pipelines

### 2. Complete Working Example

**Skill:** `.claude/skills/wikipedia-utils/`

**Demonstrates:**
- Parameterized Python script
- Clean error handling
- Clear documentation
- Example usage
- Requirements.txt

**Solves:**
- "Count references on page X"
- "Count references on page Y"
- "Count references on page Z"

Same script, different URLs. No rewriting!

### 3. Updated Skill Creator

**File:** `.claude/skills/skill-creator/SKILL.md`

**Added prominent section:**
- "Creating Utility Skills for Recurring Tasks"
- Placed right at the top (high visibility)
- Clear examples
- Decision criteria
- Link to comprehensive guide

---

## 🎓 How to Use

### Step 1: User Comes With a Task

```
User: "How many unique references are on the Dragon Ball Z Wikipedia page?"
```

### Step 2: Solve It First

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

### Step 3: Ask the Key Questions

- ❓ Could this be asked for different Wikipedia pages? **YES**
- ❓ Is the core logic reusable? **YES**
- ❓ Can I parameterize it (change URL)? **YES**

→ **This should be a skill!**

### Step 4: Create the Skill

**A. Make it parameterized:**
```python
#!/usr/bin/env python3
"""Count unique references on a Wikipedia page."""
import sys
import requests
from bs4 import BeautifulSoup

def count_references(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    refs = soup.find_all('li', {'id': lambda x: x and x.startswith('cite_note')})
    return len(refs)

if __name__ == "__main__":
    url = sys.argv[1]  # ← Takes URL as parameter!
    count = count_references(url)
    print(f"Unique references: {count}")
```

**B. Create skill structure:**
```bash
mkdir -p .claude/skills/wikipedia-utils/scripts
# Save script
# Write SKILL.md
# Add requirements.txt
```

**C. Document in SKILL.md:**
- What it does
- How to use it
- When to use it
- Examples

### Step 5: Use It Forever

**Next request:**
```
User: "Count references on Sheikh Hasina page"
```

**Your response:**
```bash
python .claude/skills/wikipedia-utils/scripts/count_references.py \
  "https://en.wikipedia.org/wiki/Sheikh_Hasina"

# Output: Unique references: 156
```

**No rewriting!** Just different parameter.

---

## 🎨 Common Utility Skill Patterns

### 1. Web Data Extraction

**Pattern:** Scrape data from websites

**Example Skills:**
- `wikipedia-utils` - Extract Wikipedia data
- `web-scraper` - General web scraping
- `email-extractor` - Extract emails from pages

**Key:** Parameterize the URL, keep logic same

### 2. File Format Conversion

**Pattern:** Convert between formats

**Example Skills:**
- `format-converter` - CSV ↔ JSON ↔ YAML
- `image-converter` - PNG ↔ JPG ↔ WebP
- `document-converter` - DOCX ↔ PDF ↔ MD

**Key:** Parameterize input/output files, keep conversion logic

### 3. Text Analysis

**Pattern:** Analyze text documents

**Example Skills:**
- `text-analyzer` - Word count, readability, keywords
- `sentiment-analyzer` - Sentiment analysis
- `language-detector` - Detect language

**Key:** Parameterize text input, keep analysis same

### 4. API Integration

**Pattern:** Interact with APIs

**Example Skills:**
- `github-utils` - GitHub API operations
- `slack-utils` - Slack API operations
- `notion-utils` - Notion API operations

**Key:** Parameterize resources, keep API calls same

### 5. Data Processing

**Pattern:** Process data files

**Example Skills:**
- `log-analyzer` - Parse and analyze logs
- `csv-processor` - Filter, aggregate CSV data
- `json-transformer` - Transform JSON structures

**Key:** Parameterize data files, keep processing logic

---

## 📖 Script Design Principles

### 1. Single Responsibility
Each script does **ONE thing** well:
- ✅ `count_references.py` - Count references
- ✅ `get_categories.py` - Get categories
- ❌ `wikipedia_tool.py --action count` - Too generic

### 2. Clear Input/Output
```python
def count_references(url: str) -> int:
    """
    Count unique references on a Wikipedia page.

    Args:
        url: Full Wikipedia page URL

    Returns:
        Number of unique references
    """
    # Clear contract!
```

### 3. Error Handling
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

### 4. Help Text
```python
if len(sys.argv) != 2:
    print("""
Usage: count_references.py <wikipedia_url>

Example:
    python count_references.py "https://en.wikipedia.org/wiki/Python"
    """)
    sys.exit(1)
```

### 5. Parameterization
```bash
# Command-line arguments
python script.py <url> [format]

# Environment variables
GITHUB_TOKEN=xxx python script.py

# Config file
~/.config/myskill/config.json
```

---

## 🔍 Real Example: Wikipedia Utils

### Structure
```
.claude/skills/wikipedia-utils/
├── SKILL.md                     # Documentation
├── requirements.txt             # Dependencies
└── scripts/
    └── count_references.py      # Parameterized script
```

### Usage

**Task 1:**
```bash
python scripts/count_references.py \
  "https://en.wikipedia.org/wiki/Dragon_Ball_Z"

# Output: Unique references: 287
```

**Task 2:**
```bash
python scripts/count_references.py \
  "https://en.wikipedia.org/wiki/Sheikh_Hasina"

# Output: Unique references: 156
```

**Task 3:**
```bash
python scripts/count_references.py \
  "https://en.wikipedia.org/wiki/Python_(programming_language)"

# Output: Unique references: 234
```

**Same script, different URLs. That's the power of utility skills!**

---

## 📦 Skill Evolution

Skills grow organically:

### Version 1: Single Script
```
User: "Count references on page X"
→ Create count_references.py
```

### Version 2: Multiple Scripts
```
User: "What categories is this page in?"
→ Add get_categories.py
```

### Version 3: Comprehensive Utility
```
User: "Extract the infobox"
→ Add extract_infobox.py

User: "Get external links"
→ Add get_external_links.py
```

**Result:**
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

**Don't build everything upfront. Start small, grow as needed.**

---

## ✅ Benefits

### Token Efficiency
- Write once, use many times
- No repeated explanations
- Scripts documented in skill

### Time Efficiency
- No rewriting same logic
- Faster responses
- Consistent quality

### Maintainability
- One place to update
- Version controlled
- Easy to test

### User Experience
- Faster responses
- Consistent behavior
- Reliable solutions

---

## 🎯 Quick Decision Tree

```
User comes with a task
        ↓
Can core logic be reused with different params?
        ↓
    YES → Create utility skill
        ↓
    NO → Is it highly specific one-off?
        ↓
    YES → Just solve it
        ↓
    NO → Does it require deep context each time?
        ↓
    YES → Just solve it
        ↓
Otherwise → Create utility skill
```

---

## 📚 Documentation

All documentation is in place:

1. **Main Guide**
   - `.claude/skills/skill-creator/SKILL.md` (updated)
   - Prominent section on utility skills

2. **Comprehensive Reference**
   - `.claude/skills/skill-creator/references/utility-skills-guide.md`
   - Complete patterns and examples

3. **Working Example**
   - `.claude/skills/wikipedia-utils/`
   - Real, tested code

---

## 🚀 Start Creating Utility Skills

### When you solve a task, ask:
1. Could this be asked again with different parameters?
2. Is the core logic reusable?
3. Can I parameterize it?

### If 2+ YES:
1. Make the solution parameterized
2. Create a skill folder
3. Write SKILL.md
4. Use it forever!

### Examples to look for:
- Web scraping (different URLs)
- Data processing (different files)
- API calls (different resources)
- Format conversion (different inputs)
- Text analysis (different documents)

---

## 🎉 Summary

**skill-creator** is now enhanced to help you create **reusable utility skills** that solve recurring problems.

**Key additions:**
- ✅ Complete guide for utility skills
- ✅ Decision framework (when to create)
- ✅ 5 common patterns
- ✅ Real working example (wikipedia-utils)
- ✅ Script design principles
- ✅ Updated skill-creator SKILL.md

**Philosophy:**
- Don't solve the same problem twice
- Parameterize and reuse
- Build skills organically
- Start small, grow as needed

**Result:**
When users come with recurring patterns, you can create skills that handle those patterns forever, making future requests instant instead of requiring fresh solutions.

**Start looking for patterns in user requests and turn them into skills!**
