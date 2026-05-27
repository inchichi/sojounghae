# Portable Billing + Credit Extension Diagnosis

## Setup
- Base portable model fixed as `billing2 + CORAL`.
- `billing2 = monthly_billing + total_billing`.
- Credit extension tests whether a generalizable financial axis can be added on top of billing.
- Methods: `raw`, `rank normalization`, `CORAL`.
- Source domain: Cell2Cell. Target domain: IBM Telco.

## Credit Proxies
- Cell2Cell: `credit_score = CreditRating` ordinalized from low to high, `credit_access = HasCreditCard`.
- IBM Telco: `credit_score = PaymentMethod` ordinalized from low to high trust, `credit_access = automatic payment method`.

## Dataset Size
- Cell2Cell rows: `51,047`; churn rate `0.2882`
- IBM Telco rows: `7,043`; churn rate `0.2654`

## billing2
### Transfer at threshold 0.5
| Direction | Method | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|---:|
| Cell2Cell -> IBM | raw | 0.6061 | 0.7331 | 0.4737 | 0.0481 | 0.0874 |
| IBM -> Cell2Cell | raw | 0.5000 | 0.3204 | 0.2863 | 0.9103 | 0.4356 |
| Cell2Cell -> IBM | rank | 0.6396 | 0.6615 | 0.3597 | 0.3529 | 0.3563 |
| IBM -> Cell2Cell | rank | 0.5243 | 0.6113 | 0.3199 | 0.3100 | 0.3149 |
| Cell2Cell -> IBM | coral | 0.6837 | 0.5735 | 0.3528 | 0.7273 | 0.4751 |
| IBM -> Cell2Cell | coral | 0.5256 | 0.5881 | 0.3159 | 0.3685 | 0.3402 |

### Best-threshold F1
| Direction | Method | Best Threshold | Best F1 |
|---|---|---:|---:|
| Cell2Cell -> IBM | raw | 0.3100 | 0.4418 |
| IBM -> Cell2Cell | raw | 0.1350 | 0.4474 |
| Cell2Cell -> IBM | rank | 0.4250 | 0.4709 |
| IBM -> Cell2Cell | rank | 0.0500 | 0.4475 |
| Cell2Cell -> IBM | coral | 0.5600 | 0.4823 |
| IBM -> Cell2Cell | coral | 0.1050 | 0.4476 |

### Domain separability
| Method | Domain AUC | Domain Accuracy |
|---|---:|---:|
| raw | 0.9940 | 0.9692 |
| rank | 0.9540 | 0.8674 |
| coral | 0.8902 | 0.8072 |

## billing2_credit_score
### Transfer at threshold 0.5
| Direction | Method | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|---:|
| Cell2Cell -> IBM | raw | 0.3727 | 0.5316 | 0.1217 | 0.1230 | 0.1223 |
| IBM -> Cell2Cell | raw | 0.4946 | 0.3228 | 0.2872 | 0.9109 | 0.4367 |
| Cell2Cell -> IBM | rank | 0.4972 | 0.5280 | 0.2619 | 0.4278 | 0.3249 |
| IBM -> Cell2Cell | rank | 0.5178 | 0.5982 | 0.3000 | 0.2957 | 0.2978 |
| Cell2Cell -> IBM | coral | 0.4796 | 0.4457 | 0.2731 | 0.6551 | 0.3855 |
| IBM -> Cell2Cell | coral | 0.5267 | 0.5927 | 0.3057 | 0.3253 | 0.3152 |

### Best-threshold F1
| Direction | Method | Best Threshold | Best F1 |
|---|---|---:|---:|
| Cell2Cell -> IBM | raw | 0.0500 | 0.4195 |
| IBM -> Cell2Cell | raw | 0.0500 | 0.4470 |
| Cell2Cell -> IBM | rank | 0.4100 | 0.4305 |
| IBM -> Cell2Cell | rank | 0.0500 | 0.4444 |
| Cell2Cell -> IBM | coral | 0.3100 | 0.4227 |
| IBM -> Cell2Cell | coral | 0.0900 | 0.4479 |

### Domain separability
| Method | Domain AUC | Domain Accuracy |
|---|---:|---:|
| raw | 0.9992 | 0.9870 |
| rank | 1.0000 | 1.0000 |
| coral | 0.9993 | 0.9916 |

## billing2_credit_family
### Transfer at threshold 0.5
| Direction | Method | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|---:|
| Cell2Cell -> IBM | raw | 0.3651 | 0.5216 | 0.1445 | 0.1631 | 0.1533 |
| IBM -> Cell2Cell | raw | 0.4858 | 0.3226 | 0.2872 | 0.9113 | 0.4367 |
| Cell2Cell -> IBM | rank | 0.4799 | 0.5188 | 0.2500 | 0.4064 | 0.3096 |
| IBM -> Cell2Cell | rank | 0.5191 | 0.5961 | 0.2976 | 0.2954 | 0.2965 |
| Cell2Cell -> IBM | coral | 0.5108 | 0.4755 | 0.2804 | 0.6230 | 0.3867 |
| IBM -> Cell2Cell | coral | 0.5116 | 0.6246 | 0.3016 | 0.2301 | 0.2610 |

### Best-threshold F1
| Direction | Method | Best Threshold | Best F1 |
|---|---|---:|---:|
| Cell2Cell -> IBM | raw | 0.0500 | 0.4195 |
| IBM -> Cell2Cell | raw | 0.0750 | 0.4470 |
| Cell2Cell -> IBM | rank | 0.3750 | 0.4209 |
| IBM -> Cell2Cell | rank | 0.0500 | 0.4448 |
| Cell2Cell -> IBM | coral | 0.3100 | 0.4221 |
| IBM -> Cell2Cell | coral | 0.0800 | 0.4476 |

### Domain separability
| Method | Domain AUC | Domain Accuracy |
|---|---:|---:|
| raw | 0.9995 | 0.9888 |
| rank | 1.0000 | 1.0000 |
| coral | 1.0000 | 0.9988 |

## Cross-schema comparison
- Compare the CORAL rows first, since `billing2 + CORAL` is the fixed portable baseline.
- If adding credit features improves Cell2Cell -> IBM but hurts IBM -> Cell2Cell or increases domain separability, the credit axis is only partially generalizable.
- If the credit extension does not beat `billing2 + CORAL`, then the portable schema should remain `billing2` only.
