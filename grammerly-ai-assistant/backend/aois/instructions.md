# AI Instructions

- This markdown file describes how the new AOI should behave when fixing content.
- The API will read this file to guide its behavior, and you can update it to tune the fixer.
- The fixer supports two modes:
  - text: fix natural language text (grammar, punctuation, spacing).
  - html: fix basic HTML syntax (tag balancing and basic tag closure).
- If OpenAI is configured (OPENAI_API_KEY present), the fixer will attempt to use OpenAI for more advanced fixes; otherwise, it will fall back to heuristic fixes.
- The endpoint to invoke is /aois/fix with a JSON payload containing payload and mode.

Example:

- Payload:
  payload: "This is an exampel of grammer! <div><span>text"
- mode: text

- Output:
  fixed: "This is an example of grammar! <div><span>text</span></div>"
