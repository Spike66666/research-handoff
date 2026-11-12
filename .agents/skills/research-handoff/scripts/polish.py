#!/usr/bin/env python3
"""Polish one research paragraph with Gemini and save a local review."""

import argparse
from collections import Counter
from contextlib import suppress
from difflib import unified_diff
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory, mkdtemp
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


def build_prompt(draft: str, instructions: str) -> str:
    prompt = PROMPT
    if instructions:
        prompt += f"\n\nAdditional editing instructions:\n{instructions}"
    return f"{prompt}\n\nPassage:\n{draft}"


def polish(prompt: str, model: str, api_key: str) -> str:
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


def polish_with_antigravity(prompt: str, model: str | None) -> str:
    executable = shutil.which("agy")
    if not executable:
        raise ValueError("Antigravity CLI (agy) was not found. Install it and sign in, or use --print-prompt and --revision with the desktop app.")

    command = [
        str(Path(executable).resolve()), "--input-format", "stream-json",
        "--output-format", "stream-json", "--disable-slash-commands",
    ]
    if model:
        command.append(f"--model={model}")
    message = {
        "event": "user",
        "message": {"content": "Revise this passage using only the text supplied here. Work without tools or file access.\n\n" + prompt},
    }
    account_env = {
        name: value for name, value in os.environ.items()
        if name.upper() not in {"GEMINI_API_KEY", "GOOGLE_API_KEY"}
    }
    # Start outside the manuscript repository and send the passage on stdin.
    workspace = Path(mkdtemp(prefix="research-handoff-"))
    try:
        completed = subprocess.run(
            command, cwd=workspace, env=account_env, input=json.dumps(message) + "\n",
            capture_output=True, encoding="utf-8", timeout=180, check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise ValueError("Antigravity CLI timed out before returning a revision.") from error
    finally:
        with suppress(OSError):
            workspace.rmdir()

    if completed.returncode:
        raise ValueError(f"Antigravity CLI exited with code {completed.returncode}. Run agy to verify Google account sign-in and agy models to check the model.")

    try:
        events = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
    except json.JSONDecodeError as error:
        raise ValueError("Antigravity CLI returned unreadable JSON. Update agy to a version that supports stream-json.") from error
    results = [event["result"] for event in events if event.get("event") == "result"]
    if len(results) != 1 or results[0].get("status") != "SUCCESS":
        raise ValueError("Antigravity CLI did not return a successful revision.")
    revision = results[0].get("response", "").strip()
    if not revision:
        raise ValueError("Antigravity CLI returned an empty revision.")
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
    parser.add_argument("draft", type=Path, help="UTF-8 file containing the original passage")
    parser.add_argument("--output-dir", type=Path, help="New directory for the revision and diff")
    parser.add_argument("--model", help=f"Override the model (API default: {DEFAULT_MODEL}; Antigravity default: your CLI selection)")
    parser.add_argument("--instructions", default="", help="Extra editing instructions sent with the draft")
    parser.add_argument("--protect", action="append", default=[], help="Exact string to check locally (repeatable)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--antigravity", action="store_true", help="Polish through the signed-in Antigravity CLI")
    mode.add_argument("--print-prompt", action="store_true", help="Print a prompt for the Antigravity desktop app")
    mode.add_argument("--revision", type=Path, help="Review a saved revision locally without a model call")
    args = parser.parse_args()
    if not args.print_prompt and args.output_dir is None:
        parser.error("--output-dir is required when saving a review")

    try:
        if args.model and not re.fullmatch(r"[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*", args.model):
            raise ValueError("Provide a model ID, for example gemini-3.1-flash-lite for the Gemini API.")
        draft = args.draft.read_text(encoding="utf-8-sig")
        if not draft.strip():
            raise ValueError("The draft is empty.")
        if not draft.endswith("\n"):
            draft += "\n"
        if args.print_prompt:
            print(build_prompt(draft, args.instructions), end="")
            return 0
        if args.output_dir.exists() or args.output_dir.is_symlink():
            raise ValueError(f"Choose a new output directory. Already exists: {args.output_dir}")

        if args.revision:
            revision = args.revision.read_text(encoding="utf-8-sig").strip()
            if not revision:
                raise ValueError("The saved revision is empty.")
            revision += "\n"
        elif args.antigravity:
            revision = polish_with_antigravity(build_prompt(draft, args.instructions), args.model)
        else:
            api_key = os.environ.get("GEMINI_API_KEY", "").strip()
            if not api_key:
                raise ValueError("Set GEMINI_API_KEY in your environment.")
            revision = polish(build_prompt(draft, args.instructions), args.model or DEFAULT_MODEL, api_key)
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
