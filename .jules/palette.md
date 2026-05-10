## 2024-05-24 - Interactive Form Clarity
**Learning:** CLI tool users benefit from explicit visual cues for optional fields, just as much as GUI users do. Using dimmed text for `(opt)` indicators is an effective way to guide the user without adding cognitive load or disrupting layout alignment.
**Action:** When working on CLI forms, ensure optional fields are explicitly marked and leverage existing color/formatting utilities (like `Color.DIM`) for visual hierarchy. Maintain column alignment by ensuring the visual length of prompts with colors are accounted for.

## 2024-05-24 - Explicit Actionable UX
**Learning:** Adding explicit bracket notation for shortcuts (e.g. `[s]core`) drastically improves CLI discoverability compared to just showing a word list. Similarly, providing concrete examples in validation errors (e.g., "1200 or 1200.50" instead of just "invalid price") prevents users from getting stuck in an input loop. Note: when injecting quotes into Python f-strings, extract strings into variables to avoid string interpolation syntax errors.
**Action:** Always wrap the shortcut letter of CLI menu items in brackets, and ensure error messages provide an immediate, copy-pasteable example of what the system expects.
