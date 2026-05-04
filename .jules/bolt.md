## 2024-05-18 - [Pre-compile Regex]
**Learning:** The application heavily relies on regex for text parsing (price, RAM, storage) inside evaluation loops, and inline re.sub/re.findall adds overhead.
**Action:** Always pre-compile regexes at the module level using `re.compile()` in Python scripts to avoid repeated compilation during text processing.
