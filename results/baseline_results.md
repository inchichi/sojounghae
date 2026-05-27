# Baseline Experiment Results

- Dataset: `cell2celltrain.csv`
- Rows: `51,047`
- Features used: `56`
- Numeric features: `35`
- Categorical features: `21`
- Train set size: `40,837`
- Test set size: `10,210`
- Positive class weight used for XGBoost: `2.4699`

| Model | Train sec | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 51.0 | 0.6084 | 0.5848 | 0.3625 | 0.5809 | 0.4464 |
| Random Forest | 1.9 | 0.6676 | 0.7200 | 0.5737 | 0.1098 | 0.1843 |
| XGBoost | 0.6 | 0.6820 | 0.6309 | 0.4087 | 0.6292 | 0.4955 |


## Notes

- `HandsetPrice` was converted to numeric with `Unknown` treated as missing.
- Logistic Regression uses one-hot encoding for categorical variables.
- Random Forest and XGBoost use ordinal encoding for categorical variables.
- Metrics are computed on the held-out 20% test split.
