#!/usr/bin/env python3
"""Send one research paragraph to Gemini and save the revision and local diff."""

import argparse
from collections import Counter
from difflib import unified_diff
import json
import os
from pathlib import Path
import re
import sys
from tempfile import TemporaryDirectory
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_MODEL = "gemini-3.1-flash-lite"
PROMPT = (
    "Polish the English in the paragraph below for a research paper. Improve "
    "clarity, concision, and flow. Preserve the meaning, numbers, units, "
    "method names, citations, mappings between methods and results, and all "
    "evaluation conditions. Preserve the strength of the conclusions and keep "
    "any stated limits on where they apply explicit. "
    "Return only the revised paragraph."
)
NUMBERS = re.compile(
    r"(?<![\w.])[-+−]?(?:(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|\.\d+)"
    r"(?:[eE][+-]?\d+)?%?"
)


def polish(draft: str, model: str, instructions: str, api_key: str) -> str:
    prompt = PROMPT
    if instructions:
        prompt += f"\n\nAdditional editing instructions:\n{instructions}"
    prompt += f"\n\nPassage:\n{draft}"

    request = Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=json.dumps({"contents": [{"role": "user", "parts": [{"text": prompt}]}]}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    request.add_unredirected_header("x-goog-api-key", api_key)
    try:
        with urlopen(request, timeout=45) as response:
            result = json.load(response)
    except HTTPError as error:
        raise ValueError(f"Gemini API returned HTTP {error.code}.") from error
    except (URLError, TimeoutError) as error:
        raise ValueError("Could not reach the Gemini API. Check your network or proxy.") from error
    except (json.JSONDecodeError, UnicodeError) as error:
        raise ValueError("Gemini API returned an unreadable response.") from error

    candidates = result.get("candidates", [])
    if not candidates:
        raise ValueError("Gemini API returned no candidate text.")
    candidate = candidates[0]
    if candidate.get("finishReason") != "STOP":
        reason = candidate.get("finishReason", "unknown")
        raise ValueError(f"Gemini did not finish the revision ({reason}).")
    parts = candidate.get("content", {}).get("parts", [])
    revision = "".join(part.get("text", "") for part in parts if not part.get("thought")).strip()
    if not revision:
        raise ValueError("Gemini API returned an empty revision.")
    return revision + "\n"


def save_review(output_dir: Path, draft_name: str, draft: str, revision: str) -> None:
    changes = "".join(unified_diff(
        draft.splitlines(keepends=True), revision.splitlines(keepends=True),
        fromfile=draft_name, tofile="polished.md",
    ))
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output_dir.parent, prefix="handoff-") as temp_dir:
        review = Path(temp_dir) / "review"
        review.mkdir()
        (review / "polished.md").write_text(revision, encoding="utf-8", newline="\n")
        (review / "review.diff").write_text(changes, encoding="utf-8", newline="\n")
        review.rename(output_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="UTF-8 file containing the passage to send")
    parser.add_argument("--output-dir", type=Path, required=True, help="New directory for the revision and diff")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Gemini model ID (default: {DEFAULT_MODEL})")
    parser.add_argument("--instructions", default="", help="Extra editing instructions sent with the draft")
    parser.add_argument("--protect", action="append", default=[], help="Exact string to check locally (repeatable)")
    args = parser.parse_args()

    try:
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("Set GEMINI_API_KEY in your environment.")
        if not re.fullmatch(r"[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*", args.model):
            raise ValueError("Provide a Gemini model ID such as gemini-3.1-flash-lite.")
        if args.output_dir.exists() or args.output_dir.is_symlink():
            raise ValueError(f"Choose a new output directory. Already exists: {args.output_dir}")
        draft = args.draft.read_text(encoding="utf-8-sig")
        if not draft.strip():
            raise ValueError("The draft is empty.")
        if not draft.endswith("\n"):
            draft += "\n"

        revision = polish(draft, args.model, args.instructions, api_key)
        save_review(args.output_dir, args.draft.name, draft, revision)
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Revision: {args.output_dir / 'polished.md'}")
    print(f"Diff: {args.output_dir / 'review.diff'}")
    original_numbers = Counter(NUMBERS.findall(draft))
    revised_numbers = Counter(NUMBERS.findall(revision))
    if original_numbers != revised_numbers:
        removed = list((original_numbers - revised_numbers).elements())
        added = list((revised_numbers - original_numbers).elements())
        print(f"Review numeric changes. Removed: {removed}. Added: {added}.")
    for term in args.protect:
        if draft.count(term) != revision.count(term):
            print(f"Review change in occurrence count: {term!r}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
