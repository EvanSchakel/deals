## 2025-05-04 - [CRITICAL] Fix Terminal Output Injection (ANSI Spoofing)
**Vulnerability:** The application was vulnerable to ANSI spoofing by taking untrusted input (e.g. title, condition, description) and printing it directly to the terminal. Malicious input could include ANSI escape sequences to manipulate the output, hide warnings, or spoof terminal behavior.
**Learning:** Terminal output injection is a common vulnerability in CLI tools that directly echo user input.
**Prevention:** Sanitize untrusted input using a utility function like `strip_ansi` at the input boundary to remove ANSI escape sequences before processing or printing the data.
