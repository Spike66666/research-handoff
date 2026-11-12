# Research Handoff 中文说明

**用 Codex 根据实验材料写 Results，用 Gemini 润色英文，再用 diff 审阅改动。** [English](README.md)

这个项目面向正在写英文论文的科研作者。Codex 可以从你指定的结果表或实验记录起草段落，并为关键陈述记录出处。随后，Gemini 润色你指定的段落，脚本在本地保存修改稿和差异，供你决定采纳哪些改动。

[已有 Antigravity？试试免 API 密钥的方式。](#用-antigravity-免-api-密钥)

## 快速开始

1. 克隆仓库并进入目录。

   ```sh
   git clone https://github.com/Spike66666/research-handoff.git
   cd research-handoff
   ```

2. 确认本机有 Python 3.10 或更新版本。在 [Google AI Studio](https://aistudio.google.com/apikey) 获取密钥，设置用户环境变量 `GEMINI_API_KEY`，再重新打开 Codex。[Windows、macOS 和 Linux 的配置步骤](https://aistudio.google.com/docs/api-key#set-api-env-var)
3. 在 Codex 打开仓库根目录，输入下面的指令。

   ```text
   $research-handoff 用 Gemini 润色 examples/results-polish/draft.md，给我看 diff。
   ```

也可以从仓库根目录直接运行脚本。只需 Python 标准库。

```sh
python .agents/skills/research-handoff/scripts/polish.py examples/results-polish/draft.md --output-dir .research-handoff/demo
```

脚本把草稿段落和编辑指令发给 Gemini，并在新目录里生成 `polished.md` 和 `review.diff`。原始实验材料和证据记录留在本地。每次运行请选一个新的输出目录。

## 用 Antigravity 免 API 密钥

**自动交接。** 安装官方 Antigravity CLI（`agy`），在终端运行一次 `agy`，用 Google 账号登录，并选择 Gemini 模型。之后可以在 Codex 里说「`$research-handoff` 用 Antigravity CLI 润色这个段落」，也可以直接运行下方命令。[CLI 安装指南](https://antigravity.google/docs/cli/tutorial) · [账号登录说明](https://antigravity.google/docs/install?tab=cli)

```sh
python .agents/skills/research-handoff/scripts/polish.py examples/results-polish/draft.md --antigravity --output-dir .research-handoff/antigravity
```

**只有桌面版。** 用第一条命令生成提示词，粘贴到 Antigravity 的无项目 Gemini 对话里，把原始英文回复保存为 `reply.md`。第二条命令在本地生成润色稿副本和 diff。

```sh
python .agents/skills/research-handoff/scripts/polish.py examples/results-polish/draft.md --print-prompt
python .agents/skills/research-handoff/scripts/polish.py examples/results-polish/draft.md --revision reply.md --output-dir .research-handoff/desktop
```

## 为什么保留 diff

在虚构的文本分类示例中，Gemini 和 Codex 都简化了 F1 的对比表达。Gemini 有一版把 `one run per variant` 改成 `using a single run`，需要回看实验条件才能判断是否该采纳。数字相同，实验条件也可能被写得含糊。[查看三版英文和逐项对照](examples/results-polish/comparison.md) · [查看从结果表到成稿的完整演示](examples/results-polish/README.md)

脚本会提示数字出现次数的变化。你也可以通过 `--protect "23.1 ms"` 或 `--protect "Mean Pooling"` 检查指定文本。审阅时还要核对数字对应的方法、实验条件和结论强度。

首版支持单段英文 Results。如果你试用了，欢迎分享哪条修改值得采纳，或者哪些科研细节最难核对。提供公开或虚构示例即可。[提交反馈](https://github.com/Spike66666/research-handoff/issues)
