## 2024-05-24 - Interactive Form Clarity
**Learning:** CLI tool users benefit from explicit visual cues for optional fields, just as much as GUI users do. Using dimmed text for `(opt)` indicators is an effective way to guide the user without adding cognitive load or disrupting layout alignment.
**Action:** When working on CLI forms, ensure optional fields are explicitly marked and leverage existing color/formatting utilities (like `Color.DIM`) for visual hierarchy. Maintain column alignment by ensuring the visual length of prompts with colors are accounted for.
## 2024-05-15 - Improve CLI Shortcuts and Actionable Error Messages
**Learning:** CLI menus and error messages often neglect visual cues for keyboard shortcuts and concrete examples for validation failures. Providing bracketed shortcuts (e.g., `[s]core`) and specific input examples (e.g., "e.g., 1200 or 1200.50") significantly improves discoverability and user recovery from errors.
**Action:** Always visually indicate keyboard shortcuts in CLI prompts and their corresponding fallback messages, and ensure input validation errors provide concrete, actionable examples.
