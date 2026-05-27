# Feature Engineering Experiment Results

- Dataset: `cell2celltrain.csv`
- Rows: `51,047`
- Base features: `56`
- Engineered features added: `7`
- Train set size: `40,837`
- Test set size: `10,210`

## Base Features

| Model | Train sec | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Base / Logistic Regression | 50.2 | 0.6084 | 0.5848 | 0.3625 | 0.5809 | 0.4464 |
| Base / Random Forest | 1.9 | 0.6676 | 0.7200 | 0.5737 | 0.1098 | 0.1843 |
| Base / XGBoost | 0.7 | 0.6820 | 0.6309 | 0.4087 | 0.6292 | 0.4955 |

## Engineered Features

| Model | Train sec | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Engineered / Logistic Regression | 114.4 | 0.5215 | 0.4507 | 0.3017 | 0.6893 | 0.4197 |
| Engineered / Random Forest | 1.9 | 0.6668 | 0.7177 | 0.5579 | 0.0982 | 0.1671 |
| Engineered / XGBoost | 0.6 | 0.6794 | 0.6305 | 0.4073 | 0.6203 | 0.4917 |

## Engineered Minus Base

| Model | ROC-AUC Δ | Accuracy Δ | F1 Δ |
|---|---:|---:|---:|
| Logistic Regression | -0.0868 | -0.1341 | -0.0267 |
| Random Forest | -0.0008 | -0.0023 | -0.0173 |
| XGBoost | -0.0027 | -0.0004 | -0.0038 |

## Engineered Feature Definitions

- `PositiveRevenueShock = max(PercChangeRevenues, 0)`
- `RevenuePerTenure = MonthlyRevenue / (MonthsInService + 1)`
- `CallDropRate = DroppedCalls / (DroppedCalls + BlockedCalls + UnansweredCalls + 1)`
- `ServiceIssueIndex = DroppedCalls + BlockedCalls + CustomerCareCalls`
- `Overage_X_PosRevenue = OverageMinutes × PositiveRevenueShock`
- `Roaming_X_PosRevenue = RoamingCalls × PositiveRevenueShock`
- `Overage_X_Roaming = OverageMinutes × RoamingCalls`
