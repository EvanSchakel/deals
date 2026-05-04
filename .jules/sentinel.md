## 2025-02-14 - Fix Terminal Output Injection (ANSI Spoofing)
**Vulnerability:** User-provided inputs (title, price, condition) were printed to the terminal without stripping ANSI escape sequences. A malicious user could provide a string containing ANSI escape codes that could spoof the output.
**Learning:** Terminal output injection is a common vector in command-line applications that accept unstructured string inputs and echo them to standard output.
**Prevention:** Apply a module-level regex filter (like `ANSI_ESCAPE_RE`) to strip ANSI escape codes from untrusted user input before passing it to downstream functions or displaying it to the user.
