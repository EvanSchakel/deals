## 2025-02-14 - Prevent Terminal Output Injection (ANSI Spoofing)
**Vulnerability:** User input values (e.g. from the CLI or prompts) could contain ANSI escape sequences (like \033[2J to clear the screen or \033[91m to change colors) which would be rendered by the CLI tool during output.
**Learning:** Terminal output injection can allow malicious users to spoof error messages, hide text, or mimic system prompts by controlling the terminal's display state. When dealing with untrusted user input that gets printed directly to stdout, standard string sanitization isn't enough.
**Prevention:** Sanitize untrusted input at the boundary using a pre-compiled regular expression to strip out ANSI escape codes before instantiating objects or passing them further down the application stack.
