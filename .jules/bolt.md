## 2024-05-14 - String sanitization is a bottleneck
**Learning:** `str.replace` and `re.sub` inside `sanitize_text` are executed multiple times since `sanitize_text` is called for multiple fields upon `Listing` instantiation. Python's `str.translate` using a precomputed `maketrans` table is significantly faster than using multiple `str.replace` calls and uncompiled regex substitutions.
**Action:** Replace multiple chained replacements with `str.translate` for stripping control characters and replacing newlines.

## 2026-05-16 - Fast-path check bypasses regex substitutions
**Learning:** `re.sub` is relatively slow, even when it doesn't match anything. Running `ANSI_ESCAPE.sub` unconditionally acts as a bottleneck since most strings don't contain ANSI sequences. Applying a C-optimized pre-check like `not text.isascii()` and checking for specific characters like `\x1b` significantly improves performance when `re.sub` doesn't need to match.
**Action:** When using regex substitution in hot paths, consider if it's possible to implement a fast-path string inclusion check or property check (like `isascii()`) to bypass the regex when matches are unlikely.
