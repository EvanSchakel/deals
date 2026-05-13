## 2024-05-14 - String sanitization is a bottleneck
**Learning:** `str.replace` and `re.sub` inside `sanitize_text` are executed multiple times since `sanitize_text` is called for multiple fields upon `Listing` instantiation. Python's `str.translate` using a precomputed `maketrans` table is significantly faster than using multiple `str.replace` calls and uncompiled regex substitutions.
**Action:** Replace multiple chained replacements with `str.translate` for stripping control characters and replacing newlines.

## 2024-05-13 - Regex Fast Path with C1 Control Characters
**Learning:** When using regex fast-path pre-checks (`if 'char' in text:`), be extremely careful if the regex pattern matches ranges like C1 control chars (`[\x80-\x9F]`). Simple inclusion checks (like `if '\x1b' in text:`) will fail to trigger on other matching chars in the regex.
**Action:** Use `not text.isascii()` as an efficient, safe pre-check when a regex targets non-ASCII or C1 control characters. It runs fast at the C level and accurately catches when the regex might have work to do.
