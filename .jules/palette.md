## 2024-05-24 - Interactive Form Clarity
**Learning:** CLI tool users benefit from explicit visual cues for optional fields, just as much as GUI users do. Using dimmed text for `(opt)` indicators is an effective way to guide the user without adding cognitive load or disrupting layout alignment.
**Action:** When working on CLI forms, ensure optional fields are explicitly marked and leverage existing color/formatting utilities (like `Color.DIM`) for visual hierarchy. Maintain column alignment by ensuring the visual length of prompts with colors are accounted for.

## 2024-05-24 - CLI Prompts and Error Guidance
**Learning:** Explicitly indicating keyboard shortcuts in menu prompts using brackets (e.g., `[s]core`) and providing actionable examples for input validation errors (e.g., 'Please enter a number, e.g., 1200 or 1200.50') significantly improves CLI usability.
**Action:** When updating primary menu prompts to include shortcuts, always ensure the corresponding `help` menu and fallback error messages reflect the updated bracketed options.
