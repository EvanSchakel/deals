## 2024-05-14 - String sanitization is a bottleneck
**Learning:** `str.replace` and `re.sub` inside `sanitize_text` are executed multiple times since `sanitize_text` is called for multiple fields upon `Listing` instantiation. Python's `str.translate` using a precomputed `maketrans` table is significantly faster than using multiple `str.replace` calls and uncompiled regex substitutions.
**Action:** Replace multiple chained replacements with `str.translate` for stripping control characters and replacing newlines.

## 2026-05-19 - Regex replacement optimization
**Learning:** Using `re.sub` in hot paths is computationally expensive when the replacement is not needed. `re.sub` takes significantly longer even when there are no matches, compared to string search or `re.search`.
**Action:** Added fast-path string inclusion checks (e.g., `if '\x1b' in text`) and simple regex search checks (e.g., `_HAS_DIGIT_RE.search(token)`) before executing `re.sub` in `strip_ansi` and `parse_price` functions.
