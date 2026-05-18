## 2024-05-14 - String sanitization is a bottleneck
**Learning:** `str.replace` and `re.sub` inside `sanitize_text` are executed multiple times since `sanitize_text` is called for multiple fields upon `Listing` instantiation. Python's `str.translate` using a precomputed `maketrans` table is significantly faster than using multiple `str.replace` calls and uncompiled regex substitutions.
**Action:** Replace multiple chained replacements with `str.translate` for stripping control characters and replacing newlines.

## 2024-05-14 - Fast path skipping for regex replacements
**Learning:** `re.sub` is a relatively expensive operation, even when no matches are found. The hot-path `sanitize_text` and `strip_ansi` methods called `ANSI_ESCAPE.sub('', text)` on every execution, causing unnecessary overhead when strings didn't contain escape sequences or control chars.
**Action:** Always add a fast-path inclusion check `if '\x1b' in text or not text.isascii():` to skip regex replacement if strings are guaranteed clean, saving significant time on high-throughput string processing.
