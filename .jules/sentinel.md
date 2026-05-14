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

## 2024-05-20 - [Fix float conversion DoS]
**Vulnerability:** Excessively long string inputs to `float()` conversion in Python can cause excessive CPU usage, leading to Denial of Service (DoS), especially since `float()` lacks a default digit limit unlike `int()`.
**Learning:** Python's built-in `type=float` in `argparse` and direct `float()` calls in string parsers are vulnerable. The `parse_price` function and CLI args parser could be exploited.
**Prevention:** Always enforce a strict string length limit (e.g., max 30 characters) before passing untrusted input to the `float()` constructor. Use custom type converter functions in `argparse` to enforce this.
