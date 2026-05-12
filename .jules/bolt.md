## 2024-05-14 - String sanitization is a bottleneck
**Learning:** `str.replace` and `re.sub` inside `sanitize_text` are executed multiple times since `sanitize_text` is called for multiple fields upon `Listing` instantiation. Python's `str.translate` using a precomputed `maketrans` table is significantly faster than using multiple `str.replace` calls and uncompiled regex substitutions.
**Action:** Replace multiple chained replacements with `str.translate` for stripping control characters and replacing newlines.

## 2024-05-14 - Fast-path string inclusion checks for regex
**Learning:** Executing `re.sub` is relatively expensive even when there are no matches. In hot paths, wrapping regex substitutions with a fast-path string inclusion check (e.g., `if 'char' in text:`) skips the regex operation when no match is expected, significantly improving performance.
**Action:** Add fast-path string inclusion checks before `re.sub` for regexes that are unlikely to match in the common case.
