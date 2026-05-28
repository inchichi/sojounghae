# 소정해 폴더 메모

## 범위

이 폴더에서 확인한 파일:

- `data/raw/cell2celltrain.csv`
- `Draft_Paper_소정해.docx`
- `dataset_report.docx`
- `머신러닝_소정해_중간발표자료.pdf`

## 프로젝트 개요

이 폴더는 `Cell2Cell` 데이터셋을 바탕으로 한 통신사 고객 이탈 예측 프로젝트입니다.

핵심 주제:

- 사용 패턴, 서비스 품질, 재무, 충성도, 인구통계 변수로 고객 이탈을 예측
- `Logistic Regression`, `Random Forest`, `XGBoost` 비교
- 피처 엔지니어링과 해석 가능성을 통해 예측 결과를 유지 전략으로 연결

## CSV 요약: `data/raw/cell2celltrain.csv`

- 크기: `51,047행 x 58열`
- 타깃: `Churn`
- 클래스 분포:
  - `Yes`: `14,711`
  - `No`: `36,336`
  - 이탈률: `28.8%`
- 문서상으로는 라벨이 포함된 학습용 파티션으로 사용됨

중요한 데이터 품질 정보:

- `OverageMinutes`: `NA` 156개
- `RoamingCalls`: `NA` 156개
- `PercChangeRevenues`: `NA` 367개
- `ServiceArea`: 공백 24개
- `HandsetPrice`: `Unknown` 값이 매우 많음

원시 CSV에서 확인한 주요 분포:

- `MonthlyRevenue`: 평균 `58.834`, 중앙값 `48.460`
- `OverageMinutes`: 평균 `40.028`, 중앙값 `3.000`
- `RoamingCalls`: 평균 `1.236`, 중앙값 `0.000`
- `PercChangeRevenues`: 중앙값 `-0.300`
- `MonthsInService`: 범위 `6`~`61`, 중앙값 `16`

기억해둘 범주형 구조:

- `ServiceArea`: 748개 고유 코드
- `IncomeGroup`: `0`~`9`
- `CreditRating`: `1-Highest` ~ `7-Lowest`
- `PrizmCode`: `Other`, `Suburban`, `Town`, `Rural`
- `Homeownership`: `Known` / `Unknown`
- `MaritalStatus`: `Yes` / `No` / `Unknown`

## `dataset_report.docx`

이 문서는 중간보고용 데이터셋 현황 보고서입니다.

핵심 내용:

- 출처: Kaggle에 공개된 Cell2Cell Customer Churn Dataset
- 원천: Duke University / Teradata Center
- 수집 방식: 크롤링이나 API 없이 Kaggle에서 CSV 직접 다운로드
- 보고서상 데이터 규모: `51,047`개 레코드, `58`개 변수
- 훈련/테스트 분할 계획: `80/20`
- 피처 분류:
  - 사용 패턴
  - 서비스 품질
  - 단말기/가입 정보
  - 인구통계
  - 행동 및 마케팅 반응

보고서에 적힌 파이프라인:

- 데이터 수집
- 전처리
- 피처 엔지니어링
- 훈련/테스트 분할
- 로지스틱 회귀 베이스라인
- 앙상블 모델
- 정확도, 정밀도, 재현율, F1, AUC-ROC 평가

## `Draft_Paper_소정해.docx`

이 파일은 메인 논문 초안입니다.

제목:

- `Machine Learning-Based Customer Churn Prediction: An Ensemble Approach with Feature Engineering and Behavioral Analysis Using the Cell2Cell Dataset`

구성:

- 초록
- 서론
- 문헌 검토
- 연구 질문과 가설
- 예비 연구 방법론
- 예비 결과
- 참고문헌

주요 주장:

- Cell2Cell Telecom 데이터셋의 라벨 포함 `51,047`행, `58`개 피처를 사용
- 전처리: 중앙값 대체, 분위수 기반 이상치 클리핑, `log1p`, `RobustScaler`
- 모델: `Logistic Regression`, `Random Forest`, `XGBoost`
- 평가: 층화 5-fold 교차검증, 주요 지표는 `ROC-AUC`

연구 가설:

- `H1`: 앙상블 모델이 로지스틱 회귀보다 성능이 높다
- `H2`: 엔지니어링된 피처가 성능을 개선한다
- `H3`: 서비스 품질 변수의 중요도가 재무 변수보다 높다

보조 비용 충격 가설 그룹:

- `H1a`: 초과 사용 분은 이탈 확률을 높인다
- `H1b`: 로밍 통화는 이탈 확률을 높인다
- `H1c`: 매출 변화율은 이탈 확률을 높인다

예비 로지스틱 회귀 결과:

- `OverageMinutes`: 유의한 양의 효과
- `RoamingCalls`: 유의한 양의 효과
- `PercChangeRevenues`: 유의하지 않음

문헌 검토의 큰 흐름:

- 초기 수익 중심 / 전통적 머신러닝
- 딥러닝 및 하이브리드 시대
- 고도화된 딥러닝
- 설명 가능한 AI와 비즈니스 정렬

## `머신러닝_소정해_중간발표자료.pdf`

이 파일은 같은 프로젝트의 중간발표 자료입니다.

발표 흐름:

- 왜 고객 이탈 예측이 중요한가
- 문헌 검토 타임라인
- 연구 진화 과정
- 데이터셋 후보와 선택 이유
- 전처리 방법론
- 기존 연구의 가설
- 우리 연구의 가설
- 변수 설계와 ML 접근법
- 전체 연구 프레임워크
- 10주 일정

눈여겨볼 내용:

- 고객 이탈 예측을 비즈니스 유지 전략으로 설명
- Cell2Cell을 규모와 피처 풍부성 때문에 선택
- IBM Telco보다 Cell2Cell이 더 적합하다고 비교
- 발표자료의 전처리는 논문 초안보다 단순함

## 중요한 차이점 / 메모

- 발표자료에는 `71,047`행이 언급되지만, 현재 CSV는 `51,047`행입니다.
- 가장 자연스러운 해석은, CSV가 라벨이 포함된 학습용 데이터이고 발표자료는 더 큰 원본 규모나 초기 추정치를 반영했다는 점입니다.
- `HandsetPrice`는 `Unknown` 값이 매우 많으므로 전처리에서 주의가 필요합니다.
- `PercChangeRevenues`는 빈칸이 아니라 `NA`로 결측이 들어 있습니다.

## 현재 실험 상태

- 원본 피처 기준으로는 `XGBoost`가 가장 좋았습니다.
- 문헌형 엔지니어링 피처와 중요도 기반 선택 피처는 큰 성능 개선을 만들지 못했습니다.
- 이후 `XGBoost`를 튜닝한 결과, `ROC-AUC 0.6819` 수준의 교차검증 성능과 `F1 0.5070` 수준의 테스트 성능을 얻었습니다.
- 최적 임계값은 `0.465`였고, SHAP 상위 변수는 `CurrentEquipmentDays`, `MonthlyMinutes`, `MonthsInService`, `PercChangeMinutes`, `UniqueSubs`, `TotalRecurringCharge`, `CreditRating`, `OverageMinutes`, `DroppedCalls`, `AgeHH1`였습니다.
- 추가 ablation에서 `CurrentEquipmentDays`를 제거하면 `XGBoost`의 `ROC-AUC`가 약간 낮아지고 `F1`도 떨어졌습니다. 즉, 이 변수는 현재 Cell2Cell 설정에서는 유효하지만, 범용성을 우선하면 별도 모델로 분리하는 것이 맞습니다.
- 범용성 우선으로 방향을 바꾸면서 `CurrentEquipmentDays`, `ServiceArea`, `PrizmCode`, `Handset*`, `NewCellphoneUser` 계열을 제외한 portable set도 다시 실험했습니다. portable set에서는 `XGBoost`가 ROC-AUC `0.6688`, F1 `0.4785`였고, 튜닝 후 ROC-AUC `0.6722`, F1 `0.4946` 수준이었습니다.
- 이후 `BankChurners` 외부 데이터로 교차 도메인 벤치마크를 수행했습니다. Cell2Cell holdout에서는 Full model이 Portable model보다 약간 좋았고, BankChurners 외부에서는 Full model AUC `0.5732`, Portable model AUC `0.5663`으로 둘 다 낮아졌습니다. 다만 외부에서 임계값을 다시 맞추면 Portable model의 F1이 Full model과 거의 같은 수준까지 올라가서, ranking 자체는 비슷하지만 calibration 차이가 있다는 점이 확인됐습니다.
- IBM Telco 샘플 데이터로도 추가 외부 테스트를 수행했습니다. 현재 Cell2Cell 기본 모델은 IBM Telco에 직접 이식되지 않았고, Full transfer AUC `0.2657`, Portable transfer AUC `0.2987`로 둘 다 0.5 아래였습니다. 반면 IBM in-domain XGBoost는 AUC `0.8388`, F1 `0.6172`로 훨씬 높아서, 문제는 모델 자체보다 cross-domain feature alignment에 있습니다.
- 역방향으로 IBM -> Cell2Cell 전이도 확인했습니다. IBM in-domain holdout 성능은 높았지만 Cell2Cell 역전이는 ROC-AUC `0.4821`, F1 `0.1764`로 떨어졌습니다. 즉, 두 통신사 데이터는 churn이라는 문제는 비슷해도 feature 의미와 경계가 서로 충분히 다릅니다.
- 추가로 `core5/core6/core8` 공통 코어 진단을 수행했습니다. `tenure`, `billing`, `partner`, `dependents`처럼 양쪽에 대응되는 피처만 남겨도 Cell2Cell -> IBM 전이는 ROC-AUC `0.3425`~`0.2791`로 여전히 0.5 아래였고, domain classifier AUC는 `0.9670`~`1.0000`까지 올라가 두 데이터가 공통 피처 공간에서도 거의 완벽히 구분됐습니다. 특히 `tenure`와 `billing` 계열의 feature-target 관계가 두 데이터에서 다르게 나타나서, 단순히 특화 컬럼을 빼는 것만으로는 범용 transfer가 해결되지 않는다는 점이 확인됐습니다.
- 이후 단독 그룹 실험에서는 `billing`만 썼을 때 Cell2Cell -> IBM AUC가 `0.6289`, `payment`만 썼을 때는 `0.5565`로 일부 전이 신호가 남아 있었고, `tenure`와 `household` 단독은 0.5 아래였습니다. 즉, 전이 가능한 축이 일부 있긴 하지만, 여러 축을 한 번에 묶으면 충돌이 커지는 구조입니다.
- 추가로 billing/payment 중심의 더 작은 portable schema를 다시 실험했습니다. `billing2`(`monthly_billing`, `total_billing`)는 raw에서 Cell2Cell -> IBM AUC `0.6061`, rank에서 `0.6396`, CORAL에서 `0.6837`까지 올라갔고, IBM -> Cell2Cell도 `0.5243`~`0.5256` 수준으로 약간 개선됐습니다. 반면 `billing3`에 `payment_card`를 얹으면 Cell2Cell -> IBM raw AUC가 `0.3327`로 크게 무너졌고, rank/CORAL로 어느 정도 복구되긴 했지만 `billing2`보다 일관성이 떨어졌습니다. 따라서 지금 portable schema의 중심은 `billing2`가 더 적합합니다.
- 마지막으로 `billing2 + CORAL`을 기준 portable 모델로 고정한 뒤 credit 계열 proxy를 추가해 봤습니다. `billing2_credit_score`와 `billing2_credit_family`는 Cell2Cell -> IBM CORAL AUC를 각각 `0.4796`, `0.5108`으로 떨어뜨렸고, domain classifier AUC는 `0.9993`~`1.0000`까지 상승했습니다. 즉, credit 축은 현재 설정에서는 일반화 축이 아니라 도메인 특화 신호에 가깝고, 최종 portable 모델은 `billing2 + CORAL`로 고정하는 것이 맞습니다.
- 최근 BankChurners 재검증에서는 최종 portable schema인 `billing2`를 사용해 Cell2Cell -> BankChurners 전이를 다시 확인했습니다. Cell2Cell holdout은 `AUC 0.5569~0.5576`, BankChurners holdout은 `AUC 0.8638~0.8725`였지만, Cell2Cell -> BankChurners transfer는 raw `AUC 0.5000`, rank `0.4476`, CORAL `0.4551`로 여전히 낮았습니다. BankChurners -> Cell2Cell도 raw `0.5000`, rank `0.4973`, CORAL `0.5087` 수준이라, 최종 portable 모델이 BankChurners까지 범용성을 확보했다고 보기에는 아직 부족합니다.
- 이후 더 추상적인 공통 표현으로 방향을 바꿔 `abstract_shared` 스키마를 실험했습니다. 여기에는 `tenure`, `age`, `partner_flag`, `children_flag`, `relationship_depth`, `activity_volume`, `monetary_volume`, `capacity`, `pressure_ratio`, `change_intensity`, `support_intensity`와 각종 tenure/volume 정규화 비율이 들어갑니다. 이 스키마는 `billing2`보다 Cell2Cell -> BankChurners transfer AUC를 `0.6031`까지 끌어올렸고, BankChurners -> Cell2Cell reverse도 CORAL에서 `0.5316`까지 올라갔습니다. 또 `Cell2Cell + BankChurners` pooled multi-source 학습에서는 Cell2Cell holdout `AUC 0.6474~0.6470`, BankChurners holdout `AUC 0.9856~0.9858`로 두 도메인 모두를 동시에 잘 맞췄습니다. 따라서 현재 가장 설득력 있는 방향은 `billing2` 단독이 아니라 `abstract_shared + pooled multi-source`입니다.
- 하지만 같은 `abstract_shared`를 IBM Telco까지 포함한 3차 도메인 테스트에 걸어보면 결과가 다시 약해졌습니다. Cell2Cell -> IBM은 CORAL에서 `AUC 0.5496` 수준이었고, BankChurners -> IBM은 raw `0.4927`, rank `0.3067`, CORAL `0.3399`로 더 낮았습니다. pooled multi-source로 Cell2Cell+BankChurners를 같이 학습해도 IBM holdout은 `AUC 0.5518~0.5608`에 머물렀고, domain classifier AUC가 `0.9999~1.0000`인 점을 보면 IBM과의 분리는 여전히 매우 큽니다. 즉, `abstract_shared`는 Cell2Cell/BankChurners 쌍에는 유효하지만 IBM까지 포함한 진짜 다도메인 범용성은 아직 확보되지 않았습니다.
- 이어서 `abstract_shared` 위에서 KMeans 클러스터링과 cluster-router를 실험했습니다. 군집 자체의 domain purity는 매우 높아서 사실상 도메인 분리 신호에 가까웠고, 단순 cluster-augmented 모델은 IBM AUC `0.5982`로 큰 개선이 없었습니다. 하지만 cluster별 전문가를 두는 router는 IBM holdout AUC를 `0.7131`까지 끌어올려, 전역 단일 모델보다 훨씬 나은 성능을 보였습니다. 즉, 현재 가장 유망한 구조는 `완전한 범용 표현` 하나를 찾는 것보다 `domain-aware routing / mixture-of-experts`입니다.
- 이후에는 클러스터를 Cell2Cell에서만 학습하고 IBM/BankChurners에 그대로 전이하는 source-only cluster transfer도 돌렸습니다. Cell2Cell baseline transfer는 IBM AUC `0.3661`, BankChurners AUC `0.4961`으로 약했지만, Cell2Cell cluster-router는 IBM AUC `0.5420`, BankChurners AUC `0.5726`까지 올렸습니다. 즉, Cell2Cell 클러스터 구조는 IBM에는 꽤 도움이 되었지만 BankChurners까지 보편적으로 옮겨가지는 못했고, 클러스터는 여전히 `도메인-aware 분기 장치`에 가깝다는 점이 확인됐습니다.
- 이후 `abstract_shared`에서 `tenure`와 tenure 기반 정규화 비율을 제거한 cluster-router도 다시 돌려봤습니다. 이 버전에서는 baseline pooled IBM AUC가 `0.5869`로 조금 올라갔지만, cluster-router의 IBM AUC는 `0.6133`에 그쳐 이전 `0.7131`보다 낮았습니다. 즉, `tenure`는 universal core로는 불안정했지만 클러스터 라우팅에서는 분기 신호로도 일부 유효했다는 뜻입니다. 따라서 `tenure`는 완전 제거보다는, 범용 core와 routing용 신호를 분리해 다루는 것이 더 적절합니다.
- 최근에는 세 도메인(`Cell2Cell`, `BankChurners`, `IBM`)을 한 번에 pooled training으로 묶어 최종 범용성을 점검했습니다. `with_tenure`에서는 pooled baseline 평균 AUC `0.8247`, 평균 F1 `0.6436`, cluster-router 평균 AUC `0.8232`, 평균 F1 `0.6448`이었고, `no_tenure`에서는 pooled baseline 평균 AUC `0.8123`, 평균 F1 `0.6366`, cluster-router 평균 AUC `0.8132`, 평균 F1 `0.6343`이었습니다. 결론적으로 세 도메인을 함께 학습하면 BankChurners와 IBM은 매우 강하게 맞지만, Cell2Cell이 가장 약하며, router는 전역 baseline을 크게 앞서기보다 도메인별 균형을 맞추는 역할에 가깝습니다.
- 따라서 현재 해석은 `이탈 원인 설명 + 유지 전략 연결`보다 한 단계 더 나아가, `포터블 피처 세트 구축 + 외부 데이터 교차 검증`이 핵심입니다.

## 한 줄 요약

이 폴더의 핵심은 다음입니다:

- 통신사 고객 이탈 예측
- Cell2Cell 데이터셋
- 비용 충격과 서비스 품질 기반 피처 엔지니어링
- `Logistic Regression`, `Random Forest`, `XGBoost` 비교
- 해석 가능성과 유지 전략 도출
