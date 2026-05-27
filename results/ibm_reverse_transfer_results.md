# IBM -> Cell2Cell Reverse Transfer

IBM Telco in-domain 모델을 Cell2Cell에 역방향으로 적용한 결과다.

## Comparison
| Setting | ROC-AUC | Accuracy | Precision | Recall | F1 | Best Threshold | Best F1 | Inverted AUC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| IBM in-domain holdout | 0.8388 | 0.7473 | 0.5162 | 0.7674 | 0.6172 | 0.625 | 0.6227 | - |
| IBM -> Cell2Cell reverse transfer | 0.4821 | 0.6426 | 0.2626 | 0.1328 | 0.1764 | 0.05 | 0.4175 | 0.5179 |

## Interpretation
- Reverse transfer is much weaker than IBM in-domain performance, so the IBM model does not generalize cleanly to Cell2Cell.
- The ROC-AUC is just below 0.5, which is far less catastrophic than the earlier Cell2Cell -> IBM transfer, but still not useful as a practical transfer model.
- The asymmetry suggests that the two telecom datasets share broad churn intent, but not the same feature semantics or decision boundaries.