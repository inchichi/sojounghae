# XGBoost 튜닝 및 SHAP 추가 결과

- 튜닝 방식: `RandomizedSearchCV`
- 교차검증: `5-fold`
- 후보 수: `6`
- 최적 CV ROC-AUC: `0.6819`
- 최종 테스트 F1: `0.5070` at threshold `0.465`

## 핵심 해석

- AUC 개선폭은 크지 않았지만, 임계값 조정으로 F1이 개선됐다.
- SHAP 상위 변수는 `CurrentEquipmentDays`, `MonthlyMinutes`, `MonthsInService`, `PercChangeMinutes`, `UniqueSubs`, `TotalRecurringCharge`, `CreditRating`, `OverageMinutes`, `DroppedCalls`, `AgeHH1` 순으로 나타났다.
- 즉, 튜닝 이후에도 유지 기간, 사용량, 유지/단말 관련 변수의 중요성이 가장 크다.
