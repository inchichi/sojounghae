# Selected-Feature Experiment Results

- Dataset: `cell2celltrain.csv`
- Selected features: `20`
- Train set size: `40,837`
- Test set size: `10,210`

## Selected Features

`CurrentEquipmentDays`, `MonthsInService`, `RetentionCalls`, `OverageMinutes`, `MonthlyMinutes`, `TotalRecurringCharge`, `PercChangeMinutes`, `UniqueSubs`, `Handsets`, `AgeHH1`, `MadeCallToRetentionTeam`, `HandsetRefurbished`, `RespondsToMailOffers`, `HandsetWebCapable`, `CreditRating`, `HandsetPrice`, `DroppedBlockedCalls`, `ActiveSubs`, `ReferralsMadeBySubscriber`, `AdjustmentsToCreditRating`

## Results

| Model | Train sec | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Selected / Logistic Regression | 2.9 | 0.6080 | 0.5803 | 0.3579 | 0.5751 | 0.4413 |
| Selected / Random Forest | 1.4 | 0.6605 | 0.7117 | 0.4992 | 0.1999 | 0.2854 |
| Selected / XGBoost | 0.4 | 0.6741 | 0.6248 | 0.4037 | 0.6332 | 0.4931 |
