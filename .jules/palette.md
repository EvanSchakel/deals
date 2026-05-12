## 2024-05-24 - Interactive Form Clarity
**Learning:** CLI tool users benefit from explicit visual cues for optional fields, just as much as GUI users do. Using dimmed text for `(opt)` indicators is an effective way to guide the user without adding cognitive load or disrupting layout alignment.
**Action:** When working on CLI forms, ensure optional fields are explicitly marked and leverage existing color/formatting utilities (like `Color.DIM`) for visual hierarchy. Maintain column alignment by ensuring the visual length of prompts with colors are accounted for.

## 2024-05-12 - CLI Keyboard Shortcut Discoverability and Actionable Errors
**Learning:** For terminal-based CLI applications, keyboard shortcuts should be explicitly indicated using brackets in prompts (e.g., `[s]core`) to improve discoverability and usability. Additionally, input validation errors should provide actionable examples for users (e.g., "Please enter a number, e.g., 1200 or 1200.50").
**Action:** Use bracket notation for interactive CLI menu shortcuts and ensure validation errors specify the correct format.
