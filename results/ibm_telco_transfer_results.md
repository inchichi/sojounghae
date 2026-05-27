# IBM Telco Transfer Benchmark

Dataset churn rate: `0.2654`

## Comparison
| Setting | ROC-AUC | Accuracy | Precision | Recall | F1 | Inverted AUC |
|---|---:|---:|---:|---:|---:|---:|
| Full transfer | 0.2657 | 0.3811 | 0.1321 | 0.2392 | 0.1702 | 0.7343 |
| Portable transfer | 0.2987 | 0.5295 | 0.0797 | 0.0733 | 0.0764 | 0.7013 |
| IBM in-domain | 0.8388 | 0.7473 | 0.5162 | 0.7674 | 0.6172 | nan |

## Threshold Diagnostics
- Full transfer: `best_t=0.050`, `best_f1=0.4194`
- Portable transfer: `best_t=0.050`, `best_f1=0.4194`
- IBM in-domain: `best_t=0.625`, `best_f1=0.6227`

## Notes
- Full transfer and portable transfer both fall below ROC-AUC 0.5, so the current Cell2Cell model does not directly transfer to IBM Telco.
- The inverted AUC values (`1 - AUC`) are above 0.70 for both transfer settings, which indicates a directional mismatch rather than random ranking.
- IBM in-domain XGBoost is much stronger, so the core issue is cross-domain feature alignment, not dataset difficulty.