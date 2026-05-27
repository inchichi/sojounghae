# CurrentEquipmentDays 제거 실험

- Dataset: `cell2celltrain.csv`
- Removed feature: `CurrentEquipmentDays`
- Rows: `51,047`
- Features used: `55`

## Baseline Models

| Model | Train sec | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 84.6 | 0.6025 | 0.5735 | 0.3543 | 0.5840 | 0.4410 |
| Random Forest | 2.0 | 0.6658 | 0.7178 | 0.5667 | 0.0880 | 0.1524 |
| XGBoost | 2.3 | 0.6763 | 0.6347 | 0.4093 | 0.6044 | 0.4881 |

## Tuned XGBoost

- OOF ROC-AUC: `0.6744`
- OOF F1: `0.4956`
- Best threshold: `0.445`

- Default threshold metrics: `{"roc_auc": 0.6757983975273935, "accuracy": 0.6250734573947111, "precision": 0.4028934677772907, "recall": 0.6247450713800136, "f1": 0.4898720682302772}`
- Tuned threshold metrics: `{"roc_auc": 0.6757983975273935, "accuracy": 0.5546523016650343, "precision": 0.36763978228599703, "recall": 0.7576478585995922, "f1": 0.49505830094392006}`
