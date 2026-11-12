# 从结果表到英文 Results 段

假设我们在同一个文本分类测试集上比较 Mean Pooling 和 Attention Pooling。两种方法各跑一次，在同一设备、批大小为 1 的条件下测量推理延迟。

| 方法 | Macro-F1 | 推理延迟中位数 |
| --- | ---: | ---: |
| Mean Pooling | 0.842 | 18.4 ms |
| Attention Pooling | 0.856 | 23.1 ms |

数据为虚构。这个例子同时包含分数提升和延迟增加，适合检查润色有没有保留比较的两面，以及有没有把单次观察写成普遍结论。

[查看 Codex 自润色与 Gemini API 润色的对照](comparison.md)。两边使用同一初稿和同一指令，审阅表逐项核对实验条件、数据和结论强度。

## 一次实际润色

这次在 Antigravity 的无项目对话中运行，界面显示的模型是 `Gemini 4 Argon Medium`。发送内容为 [完整润色指令](gemini-prompt.md)，包括英文初稿和编辑要求。原始结果表和证据对应表留在本地。

[Codex 初稿](draft.md) · [Gemini 原始英文回复](polished.md) · [完整 diff](review.diff) · [采纳后的段落](accepted.md)

| 检查项 | 实际变化 | 审阅决定 |
| --- | --- | --- |
| Macro-F1 的比较 | 把重复的 `had a macro-F1` 改成 `achieved a macro-F1 of 0.856 compared to 0.842 for Mean Pooling`。两项数值和方法的对应关系一致。 | 采纳这处措辞，使对比更直接。 |
| 测试条件 | 把测试条件压缩成 `Evaluated on the same held-out test split in a single run per variant`，与 F1 比较合并。 | 保留原稿的独立句子，明确两个方法都使用同一测试划分，且各运行一次。 |
| 推理延迟 | 用 `Measured on the same device` 引出测量条件。Attention Pooling `23.1 ms`、Mean Pooling `18.4 ms` 和批大小 `1` 均保留。 | 采纳这处改写。 |
| 结论强度 | `suggest a trade-off … in this evaluation` 原样保留。 | 保留结论的语气和范围。 |

这次润色保留了数值、单位、方法名、实验条件和结论范围。采纳后的版本采用 Gemini 对 F1 和延迟的写法，并用独立一句交代两种方法共用的测试条件。

## 复跑

1. 用 Codex 读取 [结果表和实验条件](results.md)，写一段英文 Results，并为关键陈述记录出处。参见 [Codex 初稿](draft.md) 和 [证据对应表](evidence.md)。
2. 在 Antigravity 新建无项目对话，选择 Gemini，粘贴 [完整润色指令](gemini-prompt.md)。这份指令已经包含英文初稿。
3. 保存这次的原语言回复，例如 `my-polished.md`。如果界面开启了自动翻译，可以关闭后复核原文。用 [免 API 密钥的桌面版步骤](../../README.zh-CN.md#用-antigravity-免-api-密钥) 生成本地 diff，再核对方法与结果的对应关系、实验条件和结论范围。

也可以直接用仓库中保存的实际 Antigravity 回复试跑本地审阅。从仓库根目录运行下面的命令。

```sh
python .agents/skills/research-handoff/scripts/polish.py examples/results-polish/draft.md --revision examples/results-polish/polished.md --output-dir .research-handoff/desktop-demo
```
