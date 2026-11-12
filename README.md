# Research Handoff · A Codex Skill for Research Writing

**Invoke `$research-handoff` in Codex** to draft a Results paragraph from experiment evidence, polish the English with Gemini, and review the diff before editing your manuscript.

[View the Codex skill](.agents/skills/research-handoff/SKILL.md) · [Quickstart](#quickstart) · [Worked example](#worked-example) · [Use Antigravity without an API key](#antigravity-without-an-api-key) · [中文说明](README.zh-CN.md)

The skill can record where the draft's claims came from. Its Python helper sends the selected passage to Gemini and saves the revision and diff locally for author review.

```text
Experiment evidence → Codex draft → Gemini polish → Local diff → Author review
```

## Worked example

In a synthetic classification experiment, Attention Pooling achieved a macro-F1 of `0.856` versus `0.842` for Mean Pooling. The higher score came with a higher median inference latency, `23.1 ms` versus `18.4 ms`. Each variant ran once.

| Version | Wording about the evaluation | What the author can check |
| --- | --- | --- |
| [Codex draft](examples/results-polish/draft.md) | `in one run per variant` | The run count is explicit. |
| [Gemini API revision](examples/results-polish/gemini-api-polished.md) | `using a single run` | The shorter phrasing can read as one shared run. |
| [Codex revision](examples/results-polish/codex-polished.md) | `with one run per variant` | The wording stays concise and retains the per-variant condition. |

Both revisions made the F1 comparison more concise. In this example, the Codex revision kept the run count clearer. The review step lets the author compare useful edits against the evidence before accepting them. [Full side-by-side comparison (中文)](examples/results-polish/comparison.md) · [Raw evidence](examples/results-polish/results.md)

## Quickstart

1. Clone the repository and enter it.

   ```sh
   git clone https://github.com/Spike66666/research-handoff.git
   cd research-handoff
   ```

2. Use Python 3.10 or later. Create a Gemini API key in [Google AI Studio](https://aistudio.google.com/apikey) and set `GEMINI_API_KEY` in the environment from which you run Codex or Python. See [Google's setup instructions for Windows, macOS, and Linux](https://aistudio.google.com/docs/api-key#set-api-env-var).
3. Open the repository root in Codex and enter:

   ```text
   $research-handoff Polish examples/results-polish/draft.md with Gemini and show me the diff.
   ```

To add the skill to another project, copy the [research-handoff skill directory](.agents/skills/research-handoff) into that project's `.agents/skills/` directory, then open the project in Codex.

You can also run the script directly with the Python standard library.

```sh
python .agents/skills/research-handoff/scripts/polish.py examples/results-polish/draft.md --output-dir .research-handoff/demo
```

Open `polished.md` and `review.diff` in the new output directory. Choose a fresh directory for each run. The script sends the passage and editing instructions to the Gemini API. The experiment sources and the generated diff stay on your machine.

Use `--protect "23.1 ms"` or `--protect "Mean Pooling"` to flag changes in the occurrence count of exact text. The script also checks for added or removed numeric tokens. Review the method-to-value mapping, experimental conditions, and wording of the conclusions before applying edits. Use `--model` to select a model. The default is `gemini-3.1-flash-lite`.

## Antigravity without an API key

**Automatic handoff.** Install the official `agy` CLI and run `agy` once to sign in with your Google account. Select a Gemini model in the CLI. Then ask Codex to use `$research-handoff` with Antigravity, or run the command below. The script uses your CLI session and writes the same review files. [CLI installation](https://antigravity.google/docs/cli/tutorial) · [Account sign-in](https://antigravity.google/docs/install?tab=cli)

```sh
python .agents/skills/research-handoff/scripts/polish.py examples/results-polish/draft.md --antigravity --output-dir .research-handoff/antigravity
```

**Desktop app.** Use `--print-prompt` to generate the prompt for a new Antigravity conversation outside a project. Copy the original reply to `reply.md`, then generate the diff locally. [Worked Antigravity example (中文)](examples/results-polish/README.md)

```sh
python .agents/skills/research-handoff/scripts/polish.py examples/results-polish/draft.md --print-prompt
python .agents/skills/research-handoff/scripts/polish.py examples/results-polish/draft.md --revision reply.md --output-dir .research-handoff/desktop
```

## Feedback

This preview targets a single English Results paragraph. If you try it, share which revisions you kept or which scientific details were hard to verify. A small public or synthetic example is enough to reproduce the issue. [Open an issue](https://github.com/Spike66666/research-handoff/issues)
