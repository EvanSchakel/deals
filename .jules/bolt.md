## 2024-05-14 - String sanitization is a bottleneck
**Learning:** `str.replace` and `re.sub` inside `sanitize_text` are executed multiple times since `sanitize_text` is called for multiple fields upon `Listing` instantiation. Python's `str.translate` using a precomputed `maketrans` table is significantly faster than using multiple `str.replace` calls and uncompiled regex substitutions.
**Action:** Replace multiple chained replacements with `str.translate` for stripping control characters and replacing newlines.

## 2026-05-11 - regex fast path
**Learning:** `re.sub` can be expensive even when there are no matches, especially when called repeatedly in a hot path like text sanitization for object initialization.
**Action:** Always consider adding a fast-path string inclusion check (`in`) before a regex `sub` to skip the regex completely if the required trigger character isn't present.
