## 2024-05-24 - Interactive Form Clarity
**Learning:** CLI tool users benefit from explicit visual cues for optional fields, just as much as GUI users do. Using dimmed text for `(opt)` indicators is an effective way to guide the user without adding cognitive load or disrupting layout alignment.
**Action:** When working on CLI forms, ensure optional fields are explicitly marked and leverage existing color/formatting utilities (like `Color.DIM`) for visual hierarchy. Maintain column alignment by ensuring the visual length of prompts with colors are accounted for.

## 2024-05-18 - CLI Form State Management
**Learning:** In CLI tools that prompt for multiple fields sequentially, users get frustrated if validation only happens at the very end. They lose all the intermediate state (optional fields) they typed if a required field like Price fails to parse.
**Action:** Always validate required fields and complex types (like prices or dates) *immediately* after input in CLI prompt flows, re-prompting inline instead of discarding the entire transaction.
