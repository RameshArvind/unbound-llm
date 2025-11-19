# Creating Secure Skills

When creating skills, follow these security best practices to ensure your skills are safe and trustworthy.

## Script Safety

- **Validate all inputs** - Never trust user input without validation
- **Use parameterized commands** - Avoid shell injection vulnerabilities
- **Limit file system access** - Only access necessary directories
- **Avoid hardcoded credentials** - Use environment variables or secure vaults
- **Error handling** - Fail safely without exposing sensitive information

**Example - Input validation:**
```python
import os
import re

def process_file(file_path):
    # Validate input
    if not file_path:
        raise ValueError("File path cannot be empty")

    # Prevent path traversal attacks
    if ".." in file_path or file_path.startswith("/"):
        raise ValueError("Invalid file path")

    # Sanitize filename
    safe_name = re.sub(r'[^\w\-.]', '', os.path.basename(file_path))

    # Work with validated path
    return process(safe_name)
```

## Instruction Safety

- **Clear scope** - Be explicit about what the skill does and doesn't do
- **No override instructions** - Don't tell Claude to ignore user preferences
- **Transparent operations** - Document all file operations and network calls
- **User consent** - For sensitive operations, instructions should confirm with user

**Example - Clear instructions:**
```markdown
## What This Skill Does

- Reads files from the current directory only
- Never modifies existing files
- Creates output in /tmp directory
- Does NOT access network or external resources

## What This Skill Does NOT Do

- Does not read system files or configuration
- Does not modify user data
- Does not make network requests
```

## External Dependencies

- **Document all dependencies** - List required packages and versions
- **Verify sources** - Only use reputable package sources (PyPI, npm, etc.)
- **Pin versions** - Specify exact versions to avoid supply chain attacks
- **Minimal dependencies** - Use only what's necessary

**Example - Document dependencies:**
```markdown
## Dependencies

Required packages (install with pip):
- requests==2.31.0 (HTTP library from PyPI)
- beautifulsoup4==4.12.2 (HTML parser from PyPI)

These are standard, widely-used packages from official sources.
```

## Testing

- **Test in isolation** - Verify behavior in sandboxed environment first
- **Review generated code** - Check that Claude produces safe code
- **Edge cases** - Test with malformed inputs and unexpected scenarios
- **Security review** - Have someone else review for security issues

**Testing checklist:**
- [ ] Tested with empty/null inputs
- [ ] Tested with malicious inputs (path traversal, command injection)
- [ ] Tested with extremely large inputs
- [ ] Tested with special characters and unicode
- [ ] Reviewed all file operations
- [ ] Reviewed all network calls
- [ ] Checked error messages don't leak sensitive info

## Common Vulnerabilities to Avoid

### Command Injection

**Bad:**
```python
import os
os.system(f"convert {user_input}.jpg output.png")  # Dangerous!
```

**Good:**
```python
import subprocess
subprocess.run(["convert", f"{validated_input}.jpg", "output.png"], check=True)
```

### Path Traversal

**Bad:**
```python
with open(f"data/{user_path}") as f:  # Can access ../../../etc/passwd
    content = f.read()
```

**Good:**
```python
import os
safe_path = os.path.basename(user_path)  # Remove directory components
with open(f"data/{safe_path}") as f:
    content = f.read()
```

### Information Disclosure

**Bad:**
```python
except Exception as e:
    print(f"Error: {e}")  # May expose system paths, credentials
```

**Good:**
```python
except FileNotFoundError:
    print("File not found")  # Generic, safe error message
except Exception:
    print("An error occurred")  # Log details elsewhere securely
```

## Security Review Checklist

Before publishing a skill:

- [ ] All user inputs are validated and sanitized
- [ ] No hardcoded credentials or sensitive data
- [ ] File operations limited to expected directories
- [ ] Network operations are documented and necessary
- [ ] Error messages don't expose system information
- [ ] Dependencies are from trusted sources with pinned versions
- [ ] Scripts use subprocess/parameterized commands, not shell strings
- [ ] Skill instructions don't override user preferences
- [ ] Tested with malicious/unexpected inputs
- [ ] Peer reviewed by another developer
