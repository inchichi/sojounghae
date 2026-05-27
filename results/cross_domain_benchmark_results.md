# Cross-Domain Benchmark Results

## Cell2Cell Holdout (threshold = 0.5)
| model | roc_auc | accuracy | precision | recall | f1 |
|---|---:|---:|---:|---:|---:|
| Full model | 0.6805 | 0.6228 | 0.4034 | 0.6451 | 0.4964 |
| Portable model | 0.6669 | 0.6190 | 0.3973 | 0.6230 | 0.4852 |

## BankChurners External Test (threshold = 0.5)
| model | roc_auc | accuracy | precision | recall | f1 |
|---|---:|---:|---:|---:|---:|
| Full model | 0.5732 | 0.4577 | 0.1851 | 0.6982 | 0.2926 |
| Portable model | 0.5663 | 0.3044 | 0.1659 | 0.8267 | 0.2764 |

## BankChurners Threshold Sensitivity
| model | best_threshold | best_f1 | roc_auc | accuracy | precision | recall | f1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Full model | 0.5000 | 0.2926 | 0.5732 | 0.4577 | 0.1851 | 0.6982 | 0.2926 |
| Portable model | 0.5700 | 0.2925 | 0.5663 | 0.5205 | 0.1917 | 0.6171 | 0.2925 |

## Portable Feature Schema
- tenure
- age
- income_group
- marital_status
- children_present
- relationship_depth
- transaction_volume
- monetary_volume
- balance_capacity
- utilization_or_overage
- change_volume
- change_amount
- contact_intensity
- credit_rating
- credit_card_holder

## Notes
- Full model uses the original Cell2Cell feature space and receives many missing values on BankChurners. This is the strict external stress test.
- Portable model uses a reduced schema built from common concepts that can be mapped to BankChurners.
- On BankChurners, both models keep similar ranking quality, but calibration differs; threshold sensitivity is included as a reference.
