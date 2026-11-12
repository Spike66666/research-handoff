# 同一段 Results 的 Codex 与 Gemini 润色对照

用同一份 Codex 初稿和同一条指令，各生成一次英文润色稿。Codex 使用新开的 CLI 会话，Gemini 使用此前实际测试过的 API 模型 `gemini-3.1-flash-lite`。两边的用户输入都是含初稿的编辑指令，实验结果表用于事后核对。[虚构实验结果](results.md) · [共用指令](gemini-prompt.md)

## 三版英文

**Codex 初稿**

> We used the same held-out test split to evaluate Mean Pooling and Attention Pooling in one run per variant. Attention Pooling had a macro-F1 of 0.856, while Mean Pooling had a macro-F1 of 0.842. On the same device at a batch size of 1, the median inference latency was 23.1 ms for Attention Pooling and 18.4 ms for Mean Pooling. These results suggest a trade-off between macro-F1 and inference latency in this evaluation.

**Codex 自润色**

> We evaluated Mean Pooling and Attention Pooling on the same held-out test split, with one run per variant. Attention Pooling achieved a macro-F1 of 0.856, compared with 0.842 for Mean Pooling. On the same device at a batch size of 1, median inference latency was 23.1 ms for Attention Pooling and 18.4 ms for Mean Pooling. These results suggest a trade-off between macro-F1 and inference latency in this evaluation.

**Gemini API 润色**

> We evaluated Mean Pooling and Attention Pooling using a single run on the same held-out test split. Attention Pooling achieved a macro-F1 of 0.856, while Mean Pooling achieved 0.842. With a batch size of 1 on the same device, the median inference latency was 23.1 ms for Attention Pooling and 18.4 ms for Mean Pooling. In this evaluation, these results suggest a trade-off between macro-F1 and inference latency.

## 对照结果表审阅

| 检查项 | Codex 自润色 | Gemini API 润色 |
| --- | --- | --- |
| 每种方法各运行一次 | `one run per variant` 明确保留了次数适用的对象。 | `using a single run` 可以读成两种方法共用一次运行。需恢复 `per variant`。 |
| Macro-F1 | `compared with 0.842 for Mean Pooling` 避免重复，并保留数值与方法的对应关系。 | `while Mean Pooling achieved 0.842` 同样省掉了重复的指标名称，数值对应正确。 |
| 延迟与测量条件 | 保留同一设备、批大小 `1` 和两种方法的延迟中位数。 | 调整了设备和批大小在句首的顺序，保留了相同测量条件和数值。 |
| 结论 | 保留 `suggest` 和 `in this evaluation`。 | 同样保留试探语气和评估范围，把范围移到句首。 |

这次我会直接采用 **Codex 自润色稿**。两版都缩短了 F1 的表达，Codex 还明确保留了每种方法的运行次数。Gemini 给出了另一种 F1 表达，运行次数的措辞则需要复核。结果来自一个虚构段落和一次非盲审阅，更稳定的质量判断需要多个段落的盲评。

[初稿原文](draft.md) · [Codex 原始输出](codex-polished.md) · [Gemini API 原始输出](gemini-api-polished.md)
