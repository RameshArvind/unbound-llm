# External Orchestration System - Complete Guide

**Created:** 2025-11-18
**Status:** ✅ Fully Implemented & Tested

## Overview

A simple, stateless orchestration system for managing complex research workflows using repeated Claude Code invocations.

**Key Principle:** Each invocation does **ONE thing** and sets up the next step.

---

## 🎯 Design Goals (All Achieved)

✅ **Simple outer orchestration** - Just call Claude Code repeatedly
✅ **One action per invocation** - Decompose, execute, or gather context
✅ **Setup for next** - Each invocation prepares the next step
✅ **MAIN_TASK coordination** - Simple 3-4 line state file
✅ **Skills do heavy lifting** - Not the orchestration layer

---

## 📁 Core Components

### 1. MAIN_TASK File

Location: `.tasks/MAIN_TASK`

**Format:**
```
STATUS: continue
NEXT: Decompose semiconductor-research task
TASK: semiconductor-research
FOCUS: Focus on AI chip market segment
```

**Fields:**
- `STATUS`: `continue` | `completed` | `blocked`
- `NEXT`: One sentence (max 15 words) - what to do next
- `TASK`: Current task name (optional)
- `FOCUS`: One sentence (max 15 words) - focus area (optional)

**Size:** < 100 tokens (incredibly efficient!)

### 2. Scripts

**Orchestration Scripts:**
- `read_main_task.py` - Read current state
- `update_main_task.py` - Update with next action
- `decompose_task.py` - Auto-decompose tasks

**Task Scripts:**
- `create_task.py` - Create tasks
- `change_task_state.py` - Update task state
- `list_tasks.py` - View all tasks

### 3. Decomposition Templates

Built-in templates in `decompose_task.py`:
- `research` - Basic pattern (gather → analyze → synthesize)
- `competitive-analysis` - Competitor comparison
- `market-research` - Market analysis
- `technical-deepdive` - Technical assessment

---

## 🔄 Complete Workflow Example

### Initial Setup

```bash
# Create main research task
python .claude/skills/task-creator/scripts/create_task.py semiconductor-research \
  --description "Analyze semiconductor industry AI chip market"

# Initialize MAIN_TASK
python .claude/skills/task-creator/scripts/update_main_task.py \
  continue "Decompose semiconductor-research task" --task semiconductor-research
```

### Invocation #1: Decompose

**External loop invokes Claude Code**

**Claude reads state:**
```bash
python .claude/skills/task-creator/scripts/read_main_task.py

# Output:
# ▶️  STATUS: CONTINUE
# 📋 NEXT: Decompose semiconductor-research task
# 🎯 CURRENT TASK: semiconductor-research
```

**Claude decomposes:**
```bash
python .claude/skills/task-creator/scripts/decompose_task.py semiconductor-research --auto

# Creates:
# - [pending]_semiconductor-research-data-gathering_task.md
# - [pending]_semiconductor-research-analysis_task.md
# - [pending]_semiconductor-research-synthesis_task.md
```

**Claude updates MAIN_TASK:**
```bash
python .claude/skills/task-creator/scripts/update_main_task.py \
  continue "Execute data-gathering subtask" \
  --task semiconductor-research-data-gathering \
  --focus "Focus on Q4 2024 data"
```

**Claude exits**

### Invocation #2: Execute First Subtask

**External loop invokes Claude Code again**

**Claude reads state:**
```bash
python read_main_task.py

# Output:
# ▶️  STATUS: CONTINUE
# 📋 NEXT: Execute data-gathering subtask
# 🎯 CURRENT TASK: semiconductor-research-data-gathering
# 💡 FOCUS: Focus on Q4 2024 data
```

**Claude executes (using task-executor subagent or directly):**
```bash
# Mark as running
python change_task_state.py semiconductor-research-data-gathering running

# Use context-fetcher to gather data efficiently
# Create context files, outputs, etc.

# Mark as completed
python change_task_state.py semiconductor-research-data-gathering completed
```

**Claude updates MAIN_TASK:**
```bash
python update_main_task.py \
  continue "Execute analysis subtask" \
  --task semiconductor-research-analysis
```

**Claude exits**

### Invocation #3-4: Continue Pattern

Each invocation:
1. Read MAIN_TASK
2. Do ONE action
3. Update MAIN_TASK
4. Exit

### Final Invocation: Mark Complete

```bash
python update_main_task.py completed "All research completed"
```

External loop sees `STATUS: completed` and stops.

---

## 🚀 External Loop Implementation

### Option 1: Manual

```bash
# Check what's next
python .claude/skills/task-creator/scripts/read_main_task.py

# Invoke Claude Code based on what MAIN_TASK says
# (Manually or via SDK)

# Repeat
```

### Option 2: Simple Bash Loop

```bash
#!/bin/bash
# orchestrate.sh

while true; do
  STATUS=$(python .claude/skills/task-creator/scripts/read_main_task.py --json | jq -r '.status')

  if [ "$STATUS" == "completed" ]; then
    echo "✅ Workflow completed!"
    break
  fi

  # Show next action
  python .claude/skills/task-creator/scripts/read_main_task.py

  # Invoke Claude Code here
  # (you provide the mechanism)

  sleep 5
done
```

### Option 3: Python SDK Loop

```python
import subprocess
import json
import time

def read_main_task():
    result = subprocess.run(
        ["python", ".claude/skills/task-creator/scripts/read_main_task.py", "--json"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def invoke_claude_code(prompt):
    # Your Claude Code SDK invocation here
    # This is where you'd call the SDK
    pass

while True:
    state = read_main_task()

    if state["status"] == "completed":
        print("✅ Completed!")
        break

    # Invoke with appropriate prompt
    invoke_claude_code(f"Read MAIN_TASK and execute: {state['next']}")

    time.sleep(10)
```

---

## 📊 Benefits Achieved

### Token Efficiency ⭐⭐⭐

**MAIN_TASK file:**
- < 100 tokens (vs thousands for orchestration logic)
- Each invocation starts fresh
- No accumulated context bloat

**Skills/subagents:**
- Do the heavy lifting
- Have the domain knowledge
- Use context-fetcher for efficiency

### Simplicity ⭐⭐⭐

**Outer loop:**
- Just calls Claude Code repeatedly
- Checks MAIN_TASK status
- No complex logic

**Claude's job:**
- Read MAIN_TASK (3-4 lines)
- Do ONE thing
- Update MAIN_TASK
- Exit

### Auditability ⭐⭐⭐

**Every invocation leaves a trail:**
- Task states: `[pending]` → `[running]` → `[completed]`
- MAIN_TASK history (can version control)
- Each task documents what was done

**Can reconstruct entire workflow:**
- What order things happened
- What was the focus at each step
- What outputs were produced

### Resumability ⭐⭐⭐

**Pause at any point:**
- MAIN_TASK shows where you are
- Tasks show their states
- Just resume by reading MAIN_TASK

**Survive crashes:**
- No long-running process
- State is persisted
- Pick up where you left off

---

## 🧪 Tested & Working

All scripts tested:

✅ `create_task.py` - Creates tasks with proper structure
✅ `decompose_task.py` - Auto-decomposes with templates
✅ `read_main_task.py` - Reads and displays state
✅ `update_main_task.py` - Updates state correctly
✅ `change_task_state.py` - Updates task states
✅ `list_tasks.py` - Lists all tasks

---

## 📖 Documentation

**Primary:**
- `.claude/skills/task-creator/SKILL.md` - Main skill doc (updated with orchestration section)
- `.claude/skills/task-creator/references/orchestration-pattern.md` - Complete guide

**Includes:**
- Concept explanation
- Workflow patterns
- Example loops
- Best practices
- Common patterns

---

## 🎯 Action Types

Each invocation does ONE of:

1. **Decompose** - Break task into subtasks
   ```bash
   python decompose_task.py <task> --auto
   python update_main_task.py continue "Execute first subtask"
   ```

2. **Execute** - Do one task's work
   ```bash
   python change_task_state.py <task> running
   # ... do the work ...
   python change_task_state.py <task> completed
   python update_main_task.py continue "Execute next subtask"
   ```

3. **Gather Context** - Collect specific information
   ```bash
   # Use context-fetcher to gather efficiently
   # Save to task folder
   python update_main_task.py continue "Execute analysis"
   ```

4. **Synthesize** - Combine subtask results
   ```bash
   # Read all subtask outputs
   # Create synthesis report
   python update_main_task.py completed "All done"
   ```

5. **Check Status** - Review and decide
   ```bash
   python list_tasks.py --by-state
   # Determine what to do next
   python update_main_task.py continue "Next action"
   ```

---

## 💡 Usage Tips

### Keep NEXT Concise
- Max 15 words
- One clear action
- Examples:
  - ✅ "Decompose semiconductor-research task"
  - ✅ "Execute market-sizing subtask"
  - ❌ "We need to decompose the task and then execute the first subtask and make sure we focus on the data"

### One Action Per Invocation
- Resist doing multiple things
- Decompose → update → exit
- Execute → update → exit

### Use FOCUS Sparingly
- Only when there's something specific to emphasize
- Max 15 words
- Examples:
  - "Focus on Q4 2024 data"
  - "Prioritize cost analysis"
  - "Check for recent policy changes"

### Let Skills/Subagents Work
- MAIN_TASK is coordination only
- task-creator skill has the knowledge
- task-executor subagent has the workflow
- context-fetcher skill has the efficiency

---

## 🔧 Integration with Existing System

Works seamlessly with:
- ✅ task-creator skill (defines tasks)
- ✅ task-executor subagent (executes tasks)
- ✅ context-fetcher skill (reads efficiently)
- ✅ All existing task management scripts

**No breaking changes** - External orchestration is optional. Can still use tasks manually.

---

## 📈 Comparison

### Before (Single Long Session)

```
Claude invokes:
  1. Create task
  2. Decompose into subtasks
  3. Execute subtask 1
  4. Execute subtask 2
  5. Execute subtask 3
  6. Synthesize
  7. Complete

Problems:
- Long context
- Can't pause/resume easily
- Complex orchestration logic
- Token bloat
```

### After (External Orchestration)

```
Invocation 1: Create + decompose
Invocation 2: Execute subtask 1
Invocation 3: Execute subtask 2
Invocation 4: Execute subtask 3
Invocation 5: Synthesize

Benefits:
- Fresh context each time
- Pause/resume anywhere
- Simple coordination (MAIN_TASK)
- Token efficient
- Auditable
```

---

## 🎉 Summary

You now have a **complete external orchestration system** that:

1. ✅ **Keeps outer loop simple** - Just invoke Claude Code repeatedly
2. ✅ **One action per invocation** - Decompose, execute, or gather
3. ✅ **Sets up next step** - MAIN_TASK coordinates
4. ✅ **Minimal coordination** - 3-4 lines in MAIN_TASK
5. ✅ **Skills do heavy lifting** - Not the orchestration layer
6. ✅ **Token efficient** - No bloat
7. ✅ **Auditable** - Full trail
8. ✅ **Resumable** - Pause/resume anywhere

**Ready to use!** Start with manual invocations to understand the pattern, then build your external loop.

---

## Next Steps

1. **Try it manually:**
   ```bash
   # Create a task
   python create_task.py my-research

   # Set up MAIN_TASK
   python update_main_task.py continue "Decompose my-research task" --task my-research

   # Read and follow
   python read_main_task.py
   ```

2. **Build your external loop** (optional)
   - Simple bash script
   - Python with SDK
   - CI/CD pipeline
   - Whatever fits your workflow

3. **Iterate**
   - Start simple
   - Add complexity as needed
   - Let the pattern guide you

The system is designed to be simple, flexible, and powerful. Enjoy!
