## 2024-05-14 - String sanitization is a bottleneck
**Learning:** `str.replace` and `re.sub` inside `sanitize_text` are executed multiple times since `sanitize_text` is called for multiple fields upon `Listing` instantiation. Python's `str.translate` using a precomputed `maketrans` table is significantly faster than using multiple `str.replace` calls and uncompiled regex substitutions.
**Action:** Replace multiple chained replacements with `str.translate` for stripping control characters and replacing newlines.

## 2024-05-18 - Fast path string inclusion checks for regex
**Learning:** For performance, regular expressions checking for non-ASCII characters or complex structures (like ANSI escape sequences) can be surprisingly expensive even on clean data. It is often much faster to short-circuit the regex by performing an O(n) C-implemented pre-check, such as `not text.isascii()` and `'\x1b' in text`.
**Action:** Always add an early return fast path check like `if 'char' in text:` or `not text.isascii()` before applying `re.sub` in hot paths if a common path (like valid ASCII characters) doesn't need substitution.
