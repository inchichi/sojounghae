# 외부 데이터 정리

현재 다운로드한 비교용 데이터는 아래와 같다.

## 1. credit_card_churn
- 파일: `data/external/credit_card_churn/BankChurners.csv`
- 의미: 기존 고객 이탈 여부를 다루는 신용카드 고객 churn 데이터
- 역할: Cell2Cell과 가장 유사한 비교용 데이터
- 원본: Zenodo `Prediction of Churning Credit Card Customers`

## 2. bank_customer_churn
- 파일: `data/external/bank_customer_churn/BankChurn.csv`
- 의미: 은행 고객의 `Exited` 여부를 다루는 churn 데이터
- 역할: 보조 비교용 데이터
- 원본: Hugging Face `kusha7/bank-churn`

## 3. ibm_telco
- 파일: `data/external/ibm_telco/Telco-Customer-Churn.csv`
- 의미: IBM Telco 고객 이탈 샘플 데이터
- 역할: 통신사 도메인 외부 테스트용 데이터
- 원본: IBM sample repository / Cloud Pak for Data telco churn sample

## 사용 기준
- 본 비교 실험의 우선순위는 `credit_card_churn`이다.
- `bank_customer_churn`은 도메인 차이를 넓혀 볼 때 보조 벤치마크로 사용한다.
- `ibm_telco`는 같은 통신사 도메인에서 Cell2Cell 모델이 직접 transfer되는지 확인하는 외부 테스트용이다.
