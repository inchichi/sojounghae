# Portable Billing/Payment Transfer Diagnosis

## Setup
- Goal: test whether a smaller portable schema centered on billing/payment transfers better than the wider portable schemas.
- Source domain: Cell2Cell.
- Target domain: IBM Telco.
- Transfer methods: raw, rank normalization, CORAL alignment.
- Models: XGBoost with the tuned Cell2Cell family, trained only on the source domain for transfer experiments.
- Rank normalization uses an empirical CDF fit on each domain train split separately for the billing features.

## Portable Schema Candidates
- `billing2`: `monthly_billing`, `total_billing`
- `billing3`: `billing2` + `payment_card`

## Dataset Size
- Cell2Cell rows: `51,047`; churn rate `0.2882`
- IBM Telco rows: `7,043`; churn rate `0.2654`

## billing2
### In-domain baselines
| Dataset | Method | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|---:|
| Cell2Cell | raw | 0.5601 | 0.5558 | 0.3288 | 0.5201 | 0.4029 |
| IBM Telco | raw | 0.8190 | 0.7381 | 0.5045 | 0.7567 | 0.6053 |
| Cell2Cell | rank | 0.5601 | 0.5558 | 0.3288 | 0.5201 | 0.4029 |
| IBM Telco | rank | 0.8190 | 0.7381 | 0.5045 | 0.7567 | 0.6053 |

### Transfer results at threshold 0.5
| Direction | Method | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|---:|
| Cell2Cell -> IBM | raw | 0.6061 | 0.7331 | 0.4737 | 0.0481 | 0.0874 |
| IBM -> Cell2Cell | raw | 0.5000 | 0.3204 | 0.2863 | 0.9103 | 0.4356 |
| Cell2Cell -> IBM | rank | 0.6396 | 0.6615 | 0.3597 | 0.3529 | 0.3563 |
| IBM -> Cell2Cell | rank | 0.5243 | 0.6113 | 0.3199 | 0.3100 | 0.3149 |
| Cell2Cell -> IBM | coral | 0.6837 | 0.5735 | 0.3528 | 0.7273 | 0.4751 |
| IBM -> Cell2Cell | coral | 0.5256 | 0.5881 | 0.3159 | 0.3685 | 0.3402 |

### Transfer threshold sensitivity
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

### Interpretation
- `billing2` isolates the pure billing signal and removes the payment proxy.
- If rank normalization or CORAL helps here, then scale mismatch is part of the failure mode.

## billing3
### In-domain baselines
| Dataset | Method | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|---:|
| Cell2Cell | raw | 0.5630 | 0.5584 | 0.3303 | 0.5184 | 0.4035 |
| IBM Telco | raw | 0.8207 | 0.7339 | 0.4991 | 0.7487 | 0.5989 |
| Cell2Cell | rank | 0.5630 | 0.5584 | 0.3303 | 0.5184 | 0.4035 |
| IBM Telco | rank | 0.8207 | 0.7339 | 0.4991 | 0.7487 | 0.5989 |

### Transfer results at threshold 0.5
| Direction | Method | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|---:|
| Cell2Cell -> IBM | raw | 0.3327 | 0.4102 | 0.1759 | 0.3316 | 0.2298 |
| IBM -> Cell2Cell | raw | 0.4931 | 0.3211 | 0.2869 | 0.9126 | 0.4365 |
| Cell2Cell -> IBM | rank | 0.5771 | 0.5813 | 0.3138 | 0.4866 | 0.3816 |
| IBM -> Cell2Cell | rank | 0.5254 | 0.6310 | 0.3179 | 0.2451 | 0.2768 |
| Cell2Cell -> IBM | coral | 0.5820 | 0.5252 | 0.3092 | 0.6390 | 0.4167 |
| IBM -> Cell2Cell | coral | 0.5139 | 0.4568 | 0.2889 | 0.6057 | 0.3912 |

### Transfer threshold sensitivity
| Direction | Method | Best Threshold | Best F1 |
|---|---|---:|---:|
| Cell2Cell -> IBM | raw | 0.0500 | 0.4195 |
| IBM -> Cell2Cell | raw | 0.0500 | 0.4475 |
| Cell2Cell -> IBM | rank | 0.4550 | 0.4530 |
| IBM -> Cell2Cell | rank | 0.0500 | 0.4424 |
| Cell2Cell -> IBM | coral | 0.4550 | 0.4435 |
| IBM -> Cell2Cell | coral | 0.0500 | 0.4474 |

### Domain separability
| Method | Domain AUC | Domain Accuracy |
|---|---:|---:|
| raw | 0.9975 | 0.9781 |
| rank | 0.9695 | 0.9023 |
| coral | 1.0000 | 1.0000 |

### Interpretation
- `billing3` adds the payment proxy on top of pure billing.
- If `billing3` underperforms `billing2`, payment-card information is adding domain-specific noise rather than stable signal.

## Cross-schema comparison
- Compare `billing2` and `billing3` before deciding the final portable schema.
- Prefer the schema that keeps transfer AUC above chance and does not require an aggressive threshold shift.
- If CORAL improves transfer more than rank normalization, the mismatch is mostly covariance/scale; if not, the problem is semantic drift.