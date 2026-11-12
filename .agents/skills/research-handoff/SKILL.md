---
name: research-handoff
description: Draft an English Results paragraph from local experiment evidence or send a selected research draft to Gemini for English polishing and a local diff. Use when the user asks for the Codex-to-Gemini research writing workflow.
---

For drafting, read the result tables, figures, or notes the author identifies. Write one English Results paragraph and record the source file and row or figure for each material claim in a separate evidence note. Preserve measurement conditions, comparison direction, and uncertainty. Surface gaps that affect the claims.

For Gemini polishing, use the passage the author selects or supplies. If the author requests both drafting and Gemini polishing, use the Results paragraph you just drafted. Give the script a UTF-8 Markdown or text file containing that passage. Keep the evidence note and source files local. Send the passage when the user has requested Gemini polishing for it.

Run the command with the script path resolved relative to this skill and choose a new review directory. Use `--protect` for exact strings the author wants checked and `--instructions` for their additional editing requirements.

```sh
python <skill-dir>/scripts/polish.py <draft.md> --output-dir .research-handoff/review
```

Open `polished.md` and `review.diff` in the output directory. Report any warnings from the command and compare the method-to-value mapping, conditions, and strength of the conclusions against the draft and any local evidence. Give the author the review files and apply edits to the manuscript when they ask.
