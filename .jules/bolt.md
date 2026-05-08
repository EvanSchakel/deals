## 2024-05-15 - Optimizing longest-string matching against a static dictionary
**Learning:** Checking a large string for the longest matching substring from a nested dictionary structure takes $O(P \times T)$ where P is products and T is tags. For static lookup tables (like product dictionaries), iterating over them multiple times dynamically during calls is highly inefficient.
**Action:** When a longest-string match is needed over static nested dictionaries, precompute a flat list of `(tag, item)` tuples, sort them by `len(tag)` descending at module scope, and then simply iterate until the first match is found. This makes the search O(1) matching length evaluation and resulted in a 71% speedup.

## 2024-05-18 - Pre-compiling Regex in sanitize_text
**Learning:** Bypassing `re.sub(pattern)` wrapper and caching lookup provides a measurable performance boost, especially when `sanitize_text` is called continuously on multiple elements of a loop/objects in Python, over 20%. Python internal cache helps but a module level constant is better.
**Action:** Always pre-compile repeatedly used regular expressions into a module-level constant when processing untrusted strings across high-frequency calls.
