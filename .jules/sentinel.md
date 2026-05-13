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
## 2024-05-13 - [DoS via Unbounded argparse Float Conversion]
**Vulnerability:** Python's built-in `float()` lacks the default string length limit that `int()` has (4300 digits). When used as an `argparse` type (e.g. `type=float`) or on untrusted interactive inputs, attackers can provide strings of millions of characters, exhausting memory and causing O(N^2) CPU spikes during float parsing and regex substitution.
**Learning:** `argparse`'s default `type=float` provides no defense against long inputs. Length limits must be explicitly enforced in a custom type function before calling `float()`, as the vulnerability surfaces *before* the application logic is reached.
**Prevention:** For any untrusted float inputs, enforce strict length limits (e.g., max 100 chars) using custom parsing functions (like `_safe_float`) at all boundaries (CLI arguments, standard input).
