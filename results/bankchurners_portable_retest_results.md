# BankChurners Portable Retest

## Setup
- Source domain: Cell2Cell
- Target domain: BankChurners
- Portable schema: `billing2 = monthly_billing + total_billing`
- Cell2Cell mapping: `MonthlyRevenue`, `TotalRecurringCharge`
- BankChurners mapping: `Total_Trans_Amt`, `Credit_Limit`
- Methods: `raw`, `rank normalization`, `CORAL`

## Dataset Size
- Cell2Cell rows: `51,047`; churn rate `0.2882`
- BankChurners rows: `10,127`; attrition rate `0.1607`

## Cell2Cell Holdout
| split | method | roc_auc | accuracy | precision | recall | f1 |
|---|---|---|---|---|---|---|
| Cell2Cell holdout | raw | 0.5569 | 0.5534 | 0.3263 | 0.5167 | 0.4 |
| Cell2Cell holdout | rank | 0.5576 | 0.5542 | 0.3258 | 0.5116 | 0.398 |
| Cell2Cell holdout | coral | 0.5573 | 0.544 | 0.3232 | 0.5326 | 0.4023 |

## BankChurners Holdout
| split | method | roc_auc | accuracy | precision | recall | f1 |
|---|---|---|---|---|---|---|
| BankChurners holdout | raw | 0.8725 | 0.7883 | 0.4164 | 0.7969 | 0.547 |
| BankChurners holdout | rank | 0.8725 | 0.7883 | 0.4164 | 0.7969 | 0.547 |
| BankChurners holdout | coral | 0.8638 | 0.7606 | 0.387 | 0.8431 | 0.5305 |

## Cell2Cell -> BankChurners Transfer
| direction | method | roc_auc | accuracy | precision | recall | f1 | inverted_auc |
|---|---|---|---|---|---|---|---|
| Cell2Cell -> BankChurners | raw | 0.5 | 0.8396 | 0.0 | 0.0 | 0.0 | 0.5 |
| Cell2Cell -> BankChurners | rank | 0.4476 | 0.5607 | 0.1401 | 0.3385 | 0.1982 | 0.5524 |
| Cell2Cell -> BankChurners | coral | 0.4551 | 0.3944 | 0.1562 | 0.6308 | 0.2505 | 0.5449 |

## BankChurners -> Cell2Cell Transfer
| direction | method | roc_auc | accuracy | precision | recall | f1 | inverted_auc |
|---|---|---|---|---|---|---|---|
| BankChurners -> Cell2Cell | raw | 0.5 | 0.2881 | 0.2881 | 1.0 | 0.4474 | 0.5 |
| BankChurners -> Cell2Cell | rank | 0.4973 | 0.5638 | 0.2844 | 0.3389 | 0.3092 | 0.5027 |
| BankChurners -> Cell2Cell | coral | 0.5087 | 0.4803 | 0.2924 | 0.5659 | 0.3856 | 0.4913 |

## Cell2Cell -> BankChurners Threshold Sensitivity
| direction | method | best_threshold | best_f1 | roc_auc | accuracy | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|
| Cell2Cell -> BankChurners | raw | 0.05 | 0.2765 | 0.5 | 0.1604 | 0.1604 | 1.0 | 0.2765 |
| Cell2Cell -> BankChurners | rank | 0.24 | 0.277 | 0.4476 | 0.1703 | 0.161 | 0.9908 | 0.277 |
| Cell2Cell -> BankChurners | coral | 0.05 | 0.2765 | 0.4551 | 0.1604 | 0.1604 | 1.0 | 0.2765 |

## BankChurners -> Cell2Cell Threshold Sensitivity
| direction | method | best_threshold | best_f1 | roc_auc | accuracy | precision | recall | f1 |
|---|---|---|---|---|---|---|---|---|
| BankChurners -> Cell2Cell | raw | 0.05 | 0.4474 | 0.5 | 0.2881 | 0.2881 | 1.0 | 0.4474 |
| BankChurners -> Cell2Cell | rank | 0.05 | 0.4066 | 0.4973 | 0.4187 | 0.288 | 0.691 | 0.4066 |
| BankChurners -> Cell2Cell | coral | 0.05 | 0.4233 | 0.5087 | 0.3635 | 0.2864 | 0.8107 | 0.4233 |

## Domain Separability
| method | domain_auc | domain_accuracy |
|---|---|---|
| raw | 1.0 | 1.0 |
| rank | 0.5026 | 0.5067 |
| coral | 0.447 | 0.5106 |

## Interpretation
- `billing2` is still too small to carry over cleanly to BankChurners.
- If CORAL helps only weakly, the problem is not just scale mismatch; the feature meaning itself is drifting.
- If AUC stays below 0.5, the portable representation is not yet truly general across domains.
- This bank retest therefore checks portability, but it does not yet confirm a fully general model.