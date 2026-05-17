## 2024-05-14 - String sanitization is a bottleneck
**Learning:** `str.replace` and `re.sub` inside `sanitize_text` are executed multiple times since `sanitize_text` is called for multiple fields upon `Listing` instantiation. Python's `str.translate` using a precomputed `maketrans` table is significantly faster than using multiple `str.replace` calls and uncompiled regex substitutions.
**Action:** Replace multiple chained replacements with `str.translate` for stripping control characters and replacing newlines.

## 2024-05-17 - Fast-path check for ANSI stripping
**Learning:** `re.sub` is expensive even when compiled. Adding a fast-path inclusion check using `in` and `.isascii()` before applying the regex can significantly speed up string processing when the expected pattern is not present. For the `ANSI_ESCAPE` regex, `'\x1b' not in text and text.isascii()` efficiently guards against unnecessary regex executions.
**Action:** When applying regular expressions on strings, especially in a hot path or over large inputs, consider if there's a cheap `in` check or string method (like `.isascii()`) that can safely exclude the majority of cases without invoking the regex engine.
