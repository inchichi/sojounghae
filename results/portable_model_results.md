# Portable Model Results

- Portable set features used: `46`
- Baseline XGBoost ROC-AUC: `0.6688`
- Baseline XGBoost F1: `0.4785`
- Tuned XGBoost ROC-AUC: `0.6722`
- Tuned XGBoost F1: `0.4946`
- Best threshold: `0.445`

## Baseline Models

| Model | Train sec | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 99.9 | 0.5939 | 0.5599 | 0.3459 | 0.5918 | 0.4366 |
| Random Forest | 1.8 | 0.6580 | 0.7193 | 0.5745 | 0.0996 | 0.1698 |
| XGBoost | 1.9 | 0.6688 | 0.6242 | 0.3986 | 0.5982 | 0.4785 |

## Tuned XGBoost

- OOF ROC-AUC: `0.6679`
- OOF F1: `0.4907`
- Default threshold metrics: `{'roc_auc': 0.6721828166044164, 'accuracy': 0.6247796278158668, 'precision': 0.40288398514310686, 'recall': 0.6267845003399048, 'f1': 0.49049075674956777}`
- Tuned threshold metrics: `{'roc_auc': 0.6721828166044164, 'accuracy': 0.5476003917727718, 'precision': 0.3646925931902533, 'recall': 0.7681849082256968, 'f1': 0.4945836524783893}`
