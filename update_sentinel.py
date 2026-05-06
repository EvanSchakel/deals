import os

journal_path = '.jules/sentinel.md'
content = """## 2024-03-24 - [Terminal Output Spoofing Prevention]
**Vulnerability:** Terminal output spoofing / UI redressing via unescaped carriage returns (\\r) and newlines (\\n).
**Learning:** Even after stripping ANSI sequences, raw \\r or \\n in user input allows malicious listings to overwrite terminal lines and forge "fake" outputs (e.g. spoofing a positive deal score).
**Prevention:** In CLI tools that output untrusted data directly to the terminal, sanitize input by replacing \\r and \\n with spaces, or use robust escaping for control characters.
"""

os.makedirs('.jules', exist_ok=True)
if not os.path.exists(journal_path):
    with open(journal_path, 'w') as f:
        f.write("# Sentinel Security Journal\n\n")

with open(journal_path, 'a') as f:
    f.write(content)
