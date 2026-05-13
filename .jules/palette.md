## 2024-05-24 - Interactive Form Clarity
**Learning:** CLI tool users benefit from explicit visual cues for optional fields, just as much as GUI users do. Using dimmed text for `(opt)` indicators is an effective way to guide the user without adding cognitive load or disrupting layout alignment.
**Action:** When working on CLI forms, ensure optional fields are explicitly marked and leverage existing color/formatting utilities (like `Color.DIM`) for visual hierarchy. Maintain column alignment by ensuring the visual length of prompts with colors are accounted for.

## 2024-05-13 - Add keyboard shortcuts and actionable error messages
**Learning:** Explicitly indicating keyboard shortcuts in menu prompts and providing actionable examples for input validation errors improves CLI usability and clarity for users.
**Action:** Consistently use brackets (e.g., `[s]core`) to indicate shortcuts and always include valid formatting examples in error messages (e.g., 'Please enter a number, e.g., 1200 or 1200.50') to guide correct input.
