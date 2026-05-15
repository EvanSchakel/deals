## 2024-05-14 - String sanitization is a bottleneck
**Learning:** `str.replace` and `re.sub` inside `sanitize_text` are executed multiple times since `sanitize_text` is called for multiple fields upon `Listing` instantiation. Python's `str.translate` using a precomputed `maketrans` table is significantly faster than using multiple `str.replace` calls and uncompiled regex substitutions.
**Action:** Replace multiple chained replacements with `str.translate` for stripping control characters and replacing newlines.

## 2024-05-18 - Fast-path for non-ASCII regexes
**Learning:** `re.sub` for regexes matching C1 control characters (like `[\x80-\x9F]`) is expensive to run unconditionally. Checking for string inclusion (e.g., `\x1b`) isn't enough because extended characters are also targeted.
**Action:** Use `not text.isascii()` as an efficient, O(n) C-implemented pre-check to fast-path around the regex when no match is expected, saving unnecessary operations on normal inputs.
