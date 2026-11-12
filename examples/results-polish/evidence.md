# Evidence for the Codex draft

| Draft claim | Source in [results.md](results.md) |
| --- | --- |
| Both variants used the same held-out test split, with one run per variant. | First note under the table. |
| Attention Pooling and Mean Pooling achieved macro-F1 scores of 0.856 and 0.842, respectively. | R2 and R1, Macro-F1 column. |
| Attention Pooling and Mean Pooling had median inference latencies of 23.1 ms and 18.4 ms, respectively. | R2 and R1, Median inference latency column. The second note gives the device and batch-size conditions. |
| The observed comparison suggests a trade-off within this evaluation. | R2 vs. R1 shows both a higher macro-F1 and a longer median latency. The scope is limited by the single run per variant. |

Sanity check: `0.856 − 0.842 = 0.014` macro-F1 and `23.1 − 18.4 = 4.7 ms`. The evidence provides no uncertainty estimate or significance test.
