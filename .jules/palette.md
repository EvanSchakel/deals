## 2024-05-24 - Interactive Form Clarity
**Learning:** CLI tool users benefit from explicit visual cues for optional fields, just as much as GUI users do. Using dimmed text for `(opt)` indicators is an effective way to guide the user without adding cognitive load or disrupting layout alignment.
**Action:** When working on CLI forms, ensure optional fields are explicitly marked and leverage existing color/formatting utilities (like `Color.DIM`) for visual hierarchy. Maintain column alignment by ensuring the visual length of prompts with colors are accounted for.

## 2024-05-14 - Explicit CLI Shortcuts and Error Examples
**Learning:** In terminal applications, users may not realize that the first letter of a menu option is a shortcut unless explicitly indicated (e.g., using `[s]core` rather than just `score`). Additionally, input validation errors without examples (like "Could not parse price") leave users guessing the expected format.
**Action:** Always wrap shortcut keys in brackets within CLI prompts, help menus, and error fallbacks. Ensure input validation errors include concrete, actionable examples (e.g., "Please enter a number, e.g., 1200 or 1200.50").
