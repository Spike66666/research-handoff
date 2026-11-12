# Synthetic text classification experiment

| Row | Variant | Macro-F1 | Median inference latency |
| --- | --- | ---: | ---: |
| R1 | Mean Pooling | 0.842 | 18.4 ms |
| R2 | Attention Pooling | 0.856 | 23.1 ms |

- Both variants were evaluated on the same held-out test split using one run per variant.
- The same device and batch size of 1 were used for both latency measurements.
- These data are fictional and designed to illustrate the writing workflow.
