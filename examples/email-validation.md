# Email Validation

**Task:** "Write me a Python function that validates email addresses."

Verbatim model output from a benchmark run — Claude Haiku 4.5, no-skill arm vs ken arm, temperature 1, source `benchmarks/output.json`. Reproduce: `npx promptfoo@latest eval -c benchmarks/promptfooconfig.openrouter.yaml`.

## Without Ken — 68 lines of code

# Email Validation Function

Here are a few approaches, from simple to more robust:

## 1. **Simple Regex Pattern (Quick & Practical)**

```python
import re

def validate_email(email):
    """
    Validates email using a simple regex pattern.
    Returns True if valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

**Usage:**
```python
print(validate_email("user@example.com"))      # True
print(validate_email("john.doe@company.co.uk")) # True
print(validate_email("invalid.email@"))        # False
print(validate_email("@example.com"))          # False
```

---

## 2. **RFC 5322 Compliant (More Strict)**

```python
import re

def validate_email_strict(email):
    """
    More comprehensive email validation following RFC 5322 standards.
    """
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]*@[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$'
    return re.match(pattern, email) is not None
```

---

## 3. **Using `email-validator` Library (Recommended)**

```python
from email_validator import validate_email, EmailNotValidError

def validate_email_library(email):
    """
    Uses the email-validator library for robust validation.
    Install with: pip install email-validator
    """
    try:
        # Validate and get normalized form
        valid = validate_email(email)
        return True
    except EmailNotValidError:
        return False
```

**Usage:**
```python
print(validate_email_library("user@example.com"))  # True
print(validate_email_library("invalid..email@example.com"))  # False
```

---

## 4. **Comprehensive Validation Function**

```python
import re

def validate_email_comprehensive(email):
    """
    Comprehensive email validation with multiple checks.
    """
    # Check if email is a string and not empty
    if not isinstance(email, str) or not email.strip():
        return False
    
    email = email.strip().lower()
    
    # Check length
    if len(email) > 254:
        return False
    
    # Split into local and domain parts
    if email.count('@') != 1:
        return False
    
    local, domain = email.rsplit('@', 1)
    
    # Validate local part
    if not local or len(local) > 64:
        return False
    if local[0] == '.' or local[-1] == '.':
        return False
    if '..' in local:
        return False
    
    # Validate domain
    if not domain or '.' not in domain:
        return False
    if domain[0] == '.' or domain[-1] == '.':
        return False
    if '..' in domain:
        return False
    
    # Regex for local and domain parts
    local_pattern = r'^[a-zA-Z0-9._%+-]+$'
    domain_pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(local_pattern, local)) and bool(re.match(domain_pattern, domain))
```

---

## Comparison Table

| Method | Pros | Cons |
|--------|------|------|
| **Simple Regex** | Fast, no dependencies | Less accurate |
| **Strict Regex** | Good balance | Complex pattern |
| **email-validator** | Very accurate, handles edge cases | Requires external library |
| **Comprehensive** | Custom control | More code to maintain |

---

## Recommendation

For **most applications**, use the **simple regex** or the **email-validator library**:

```python
# Best practice: use email-validator
from email_validator import validate_email, EmailNotValidError

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
```

**Install it with:**
```bash
pip install email-validator
```

This library handles international domains, normalization, and edge cases properly! 🎯

## With Ken — 8 lines of code

```python
import re

def validate_email(email):
    """
    Validate email address against RFC 5322 simplified pattern.
    Returns True if valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

**Why this, not the stdlib?**

Python's `email.utils.parseaddr()` and `email-validator` exist; both are heavyweight for the common case. The regex above catches 99% of real mail and runs instantly. If you hit the 1% (rare TLDs, quoted locals, IPv6 literals), you'll know it — the validation will reject it, you'll measure that it matters, then you'll call the stdlib or a library.

**Ceiling:** `// ken: regex pattern; upgrade to email-validator library if real RFC 5322 compliance measured as blocking users`

**68 → 8 lines of code** — same model, same prompt.
