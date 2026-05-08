## 2025-05-04 - Terminal Output Spoofing in CLI App
**Vulnerability:** Command-line tool accepted and printed user input containing ANSI escape sequences, allowing terminal injection and output spoofing (e.g., hiding actual output and printing forged, high-deal-score outputs).
**Learning:** Terminal applications need to treat all user-provided text as untrusted. The standard library doesn't automatically escape ANSI sequences for `sys.stdout`. Output coloring/formatting must be done around sanitized text.
**Prevention:** Filter out ANSI escape sequences (CSI commands) and non-whitespace control characters from all user-controlled inputs upon ingestion, before any processing or output mapping.
## 2024-03-24 - [Terminal Output Spoofing Prevention]
**Vulnerability:** Terminal output spoofing / UI redressing via unescaped carriage returns (\r) and newlines (\n).
**Learning:** Even after stripping ANSI sequences, raw \r or \n in user input allows malicious listings to overwrite terminal lines and forge "fake" outputs (e.g. spoofing a positive deal score).
**Prevention:** In CLI tools that output untrusted data directly to the terminal, sanitize input by replacing \r and \n with spaces, or use robust escaping for control characters.
## 2024-05-08 - [Numeric Input Validation]
**Vulnerability:** Incomplete validation of numeric arguments (e.g., price). Python evaluates `float('nan') <= 0` and `float('inf') <= 0` as `False`, bypassing simple `< 0` checks.
**Learning:** Checking if a float is less than or equal to 0 does not reject `NaN` or `Infinity` values. These edge cases require explicit validation, usually via the `math` module.
**Prevention:** Use `math.isnan()` and `math.isinf()` (or similar numeric bounds checking) to properly validate untrusted floating-point inputs and ensure they are finite numbers before processing them further.
