---
name: research-handoff
description: Draft an English Results paragraph from local experiment evidence or polish a selected passage with Gemini through the API or a signed-in Antigravity account. Use when the user asks for the Codex-to-Gemini research writing workflow and a local diff.
---

For drafting, read the result tables, figures, or notes the author identifies. Write one English Results paragraph and record the source file and row or figure for each material claim in a separate evidence note. Preserve measurement conditions, comparison direction, and uncertainty. Surface gaps that affect the claims.

For Gemini polishing, use the passage the author selects or supplies. If the author requests both drafting and Gemini polishing, use the Results paragraph you just drafted. Give the script a UTF-8 Markdown or text file containing that passage. Keep the evidence note and source files local. Send the passage when the user has requested Gemini polishing for it.

Resolve the script path relative to this skill. Use the Gemini API by default and choose Antigravity when the author requests it:

- **Gemini API:** Run `python <skill-dir>/scripts/polish.py <draft.md> --output-dir .research-handoff/review`.
- **Antigravity CLI:** Add `--antigravity` to the command. Use the author's configured Gemini model or a model slug they specify. If `agy` is unavailable or signed out, explain how to sign in or offer the desktop handoff.
- **Antigravity desktop:** Run the script with `<draft.md> --print-prompt`. When the author asks you to operate Antigravity and computer use is available, use a new conversation outside a project with a Gemini model selected. Paste the prompt and save the original-language reply to a local UTF-8 text file. Otherwise, give the author the prompt to paste and ask them for the reply. Run the script with `<draft.md> --revision <reply.md> --output-dir .research-handoff/review` to review it locally.

Choose a new review directory for each run. Use `--protect` for exact strings the author wants checked. Pass `--instructions` when generating a prompt or requesting a revision with extra editing requirements.

Open `polished.md` and `review.diff` in the output directory. Report any warnings from the command and compare the method-to-value mapping, conditions, and strength of the conclusions against the draft and any local evidence. Give the author the review files and apply edits to the manuscript when they ask.
