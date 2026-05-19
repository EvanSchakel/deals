## 2025-05-04 - Terminal Output Spoofing in CLI App
**Vulnerability:** Command-line tool accepted and printed user input containing ANSI escape sequences, allowing terminal injection and output spoofing (e.g., hiding actual output and printing forged, high-deal-score outputs).
**Learning:** Terminal applications need to treat all user-provided text as untrusted. The standard library doesn't automatically escape ANSI sequences for `sys.stdout`. Output coloring/formatting must be done around sanitized text.
**Prevention:** Filter out ANSI escape sequences (CSI commands) and non-whitespace control characters from all user-controlled inputs upon ingestion, before any processing or output mapping.
## 2024-03-24 - [Terminal Output Spoofing Prevention]
**Vulnerability:** Terminal output spoofing / UI redressing via unescaped carriage returns (\r) and newlines (\n).
**Learning:** Even after stripping ANSI sequences, raw \r or \n in user input allows malicious listings to overwrite terminal lines and forge "fake" outputs (e.g. spoofing a positive deal score).
**Prevention:** In CLI tools that output untrusted data directly to the terminal, sanitize input by replacing \r and \n with spaces, or use robust escaping for control characters.
## 2024-03-24 - [Input Length Limits]
**Vulnerability:** Denial of Service (DoS) via memory exhaustion or integer string conversion limits (`ValueError: Exceeds the limit for integer string conversion`).
**Learning:** Python limits large string-to-int conversions by default (4300 digits). Processing arbitrarily large strings in regexes or conversions can crash the application or exhaust memory.
**Prevention:** Always cap untrusted input length at the earliest ingestion point (e.g. `text = text[:10000]`), and validate length before type conversions (e.g. `len(r) <= 10` before `int(r)`).
## 2025-05-19 - Python float() DoS Vulnerability
**Vulnerability:** Denial of Service (DoS) via CPU/memory exhaustion using excessively long strings passed to Python's `float()` constructor, particularly in `argparse` type conversions and regex extraction flows.
**Learning:** Python's `float()` constructor lacks a default digit limit (unlike `int()`). Parsing arbitrarily large strings (e.g., hundreds of thousands of digits) can hang the application. This is especially risky when untrusted input is passed directly via `argparse` (e.g., `type=float`).
**Prevention:** Always implement explicit string length validation (e.g., max 20-30 characters) before converting untrusted input to floats to prevent potential DoS attacks. Use custom type functions for `argparse` that enforce these limits.
