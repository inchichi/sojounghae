# 최종 비교 노트북

이 노트북은 현재까지의 실험을 한 번에 비교하기 위한 정리본이다.

## 모델 가족 기준 베이스라인

| Model | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.6084 | 0.5848 | 0.3625 | 0.5809 | 0.4464 |
| Random Forest | 0.6676 | 0.7200 | 0.5737 | 0.1098 | 0.1843 |
| XGBoost | 0.6820 | 0.6309 | 0.4087 | 0.6292 | 0.4955 |

## XGBoost 단계별 비교

| Stage | ROC-AUC | Accuracy | Precision | Recall | F1 | Threshold |
|---|---:|---:|---:|---:|---:|---:|
| Baseline XGBoost | 0.6820 | 0.6309 | 0.4087 | 0.6292 | 0.4955 | 0.500 |
| Engineered XGBoost | 0.6794 | 0.6305 | 0.4073 | 0.6203 | 0.4917 | 0.500 |
| Selected XGBoost | 0.6741 | 0.6248 | 0.4037 | 0.6332 | 0.4931 | 0.500 |
| Tuned XGBoost | 0.6805 | 0.5897 | 0.3878 | 0.7322 | 0.5070 | 0.465 |

## 베이스라인 대비 변화량

| Stage | ΔROC-AUC vs Baseline | ΔF1 vs Baseline |
|---|---:|---:|
| Engineered XGBoost | -0.0026 | -0.0038 |
| Selected XGBoost | -0.0079 | -0.0024 |
| Tuned XGBoost | -0.0015 | +0.0115 |

## 비교 그림

- `figures/xgb_stage_comparison.png`

## 해석

- 원본 피처 기준에서는 `XGBoost`가 가장 안정적이다.
- 문헌형 피처 추가와 단순 선택 피처는 `XGBoost`를 의미 있게 끌어올리지 못했다.
- 튜닝과 임계값 조정은 AUC보다 `F1`과 `Recall`을 개선하는 데 효과가 있었다.
- 따라서 현재 연구의 핵심은 `정확도 향상`보다 `유지 전략에 연결 가능한 설명과 임계값 조정`이다.

