# Feature Importance Analysis

- Dataset: `cell2celltrain.csv`
- Train set size: `40,837`
- Test set size: `10,210`

## Logistic Regression: Top Positive Coefficients

| feature                          |      value |
|:---------------------------------|-----------:|
| num__CurrentEquipmentDays        |  0.227733  |
| num__UniqueSubs                  |  0.0997333 |
| num__RetentionCalls              |  0.0728401 |
| cat__HandsetRefurbished_Yes      |  0.0670973 |
| cat__MadeCallToRetentionTeam_Yes |  0.0662593 |
| num__OverageMinutes              |  0.0559046 |
| cat__HandsetWebCapable_No        |  0.0507514 |
| cat__HandsetWebCapable_Yes       | -0.0487921 |
| num__AgeHH1                      | -0.0507102 |
| cat__MadeCallToRetentionTeam_No  | -0.0643    |
| cat__HandsetRefurbished_No       | -0.0651379 |
| num__MonthlyMinutes              | -0.0728915 |
| num__TotalRecurringCharge        | -0.0792146 |
| cat__CreditRating_5-Low          | -0.0848536 |
| num__PercChangeMinutes           | -0.0880785 |

## Logistic Regression: Top Negative Coefficients

| feature                          |      value |
|:---------------------------------|-----------:|
| num__PercChangeMinutes           | -0.0880785 |
| cat__CreditRating_5-Low          | -0.0848536 |
| num__TotalRecurringCharge        | -0.0792146 |
| num__MonthlyMinutes              | -0.0728915 |
| cat__HandsetRefurbished_No       | -0.0651379 |
| cat__MadeCallToRetentionTeam_No  | -0.0643    |
| num__AgeHH1                      | -0.0507102 |
| cat__HandsetWebCapable_Yes       | -0.0487921 |
| cat__HandsetWebCapable_No        |  0.0507514 |
| num__OverageMinutes              |  0.0559046 |
| cat__MadeCallToRetentionTeam_Yes |  0.0662593 |
| cat__HandsetRefurbished_Yes      |  0.0670973 |
| num__RetentionCalls              |  0.0728401 |
| num__UniqueSubs                  |  0.0997333 |
| num__CurrentEquipmentDays        |  0.227733  |

## XGBoost: Top Feature Importances

| feature                        |     value |
|:-------------------------------|----------:|
| cat__MadeCallToRetentionTeam   | 0.0553308 |
| num__CurrentEquipmentDays      | 0.0470285 |
| cat__HandsetRefurbished        | 0.043025  |
| num__MonthsInService           | 0.0406014 |
| num__RetentionCalls            | 0.0395935 |
| cat__HandsetWebCapable         | 0.0267802 |
| cat__RespondsToMailOffers      | 0.0265569 |
| num__MonthlyMinutes            | 0.0228716 |
| num__PercChangeMinutes         | 0.021236  |
| num__UniqueSubs                | 0.0208528 |
| num__TotalRecurringCharge      | 0.0207022 |
| num__Handsets                  | 0.0206727 |
| cat__CreditRating              | 0.0203284 |
| num__HandsetModels             | 0.0195008 |
| num__OverageMinutes            | 0.0186779 |
| num__AgeHH1                    | 0.0177899 |
| num__ActiveSubs                | 0.0175831 |
| num__ReferralsMadeBySubscriber | 0.016582  |
| num__HandsetPrice              | 0.0165561 |
| num__DroppedBlockedCalls       | 0.0165028 |

## Notes

- Logistic coefficients are from the one-hot encoded feature space.
- XGBoost importances are from the ordinal-encoded feature space.
- Positive coefficients increase churn probability, negative coefficients reduce it.
