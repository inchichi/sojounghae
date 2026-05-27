# Common-Core Diagnosis: Cell2Cell vs IBM Telco

## Experimental Setup
- Goal: test whether a strictly shared telecom feature core transfers better than the full Cell2Cell feature space.
- Models: XGBoost with the same tuned family used in the Cell2Cell baseline, trained separately on each source domain.
- Variants: `core5`, `core6`, `core8`.
- `core5`: `tenure`, `is_senior`, `partner`, `dependents`, `monthly_billing`
- `core6`: `core5` + `total_billing`
- `core8`: `core6` + `commitment_band`, `payment_card`

## Dataset Size
- Cell2Cell: `51,047` rows, churn rate `0.2882`
- IBM Telco: `7,043` rows, churn rate `0.2654`

## core5
| Setting | ROC-AUC | Inverted AUC | Accuracy | Precision | Recall | F1 | Train sec |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cell2Cell in-domain | 0.6146 | 0.6146 | 0.5493 | 0.3475 | 0.6431 | 0.4512 | 0.4 |
| IBM in-domain | 0.8223 | 0.8223 | 0.7275 | 0.4912 | 0.7487 | 0.5932 | 0.1 |
| Cell2Cell -> IBM | 0.3425 | 0.6575 | 0.5046 | 0.1124 | 0.1257 | 0.1187 | nan |
| IBM -> Cell2Cell | 0.4813 | 0.5187 | 0.5044 | 0.2759 | 0.4432 | 0.3401 | nan |
- Domain classifier AUC: `0.9670`; accuracy: `0.8899`

### Top Drift Features
| feature | cell_missing | ibm_missing | cell_mean | ibm_mean | smd | ks |
|---|---:|---:|---:|---:|---:|---:|
| tenure | 0.000 | 0.000 | 18.7563 | 32.3711 | -0.7282 | 0.3689 |
| monthly_billing | 0.003 | 0.000 | 58.8345 | 64.7617 | -0.1560 | 0.2696 |
| is_senior | 0.290 | 0.000 | 0.0478 | 0.1621 | -0.3795 | 0.1143 |
| partner | 0.386 | 0.000 | 0.5950 | 0.4830 | 0.2260 | 0.1120 |
| dependents | 0.000 | 0.000 | 0.2423 | 0.2996 | -0.1292 | 0.0573 |

### Top Target-Association Gaps
| feature | cell_corr | ibm_corr | corr_gap |
|---|---:|---:|---:|
| tenure | 0.0396 | -0.3671 | 0.4067 |
| monthly_billing | -0.0237 | 0.1847 | 0.2084 |
| dependents | 0.0096 | -0.1642 | 0.1738 |
| is_senior | -0.0169 | 0.1509 | 0.1677 |
| partner | 0.0157 | -0.1504 | 0.1662 |

## core6
| Setting | ROC-AUC | Inverted AUC | Accuracy | Precision | Recall | F1 | Train sec |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cell2Cell in-domain | 0.6237 | 0.6237 | 0.5650 | 0.3570 | 0.6363 | 0.4574 | 0.1 |
| IBM in-domain | 0.8264 | 0.8264 | 0.7367 | 0.5027 | 0.7567 | 0.6041 | 0.1 |
| Cell2Cell -> IBM | 0.3040 | 0.6960 | 0.4351 | 0.1019 | 0.1444 | 0.1195 | nan |
| IBM -> Cell2Cell | 0.4830 | 0.5170 | 0.4931 | 0.2762 | 0.4684 | 0.3475 | nan |
- Domain classifier AUC: `1.0000`; accuracy: `0.9999`

### Top Drift Features
| feature | cell_missing | ibm_missing | cell_mean | ibm_mean | smd | ks |
|---|---:|---:|---:|---:|---:|---:|
| total_billing | 0.003 | 0.002 | 46.8301 | 2283.3004 | -1.3952 | 0.8665 |
| tenure | 0.000 | 0.000 | 18.7563 | 32.3711 | -0.7282 | 0.3689 |
| monthly_billing | 0.003 | 0.000 | 58.8345 | 64.7617 | -0.1560 | 0.2696 |
| is_senior | 0.290 | 0.000 | 0.0478 | 0.1621 | -0.3795 | 0.1143 |
| partner | 0.386 | 0.000 | 0.5950 | 0.4830 | 0.2260 | 0.1120 |
| dependents | 0.000 | 0.000 | 0.2423 | 0.2996 | -0.1292 | 0.0573 |

### Top Target-Association Gaps
| feature | cell_corr | ibm_corr | corr_gap |
|---|---:|---:|---:|
| tenure | 0.0396 | -0.3671 | 0.4067 |
| monthly_billing | -0.0237 | 0.1847 | 0.2084 |
| dependents | 0.0096 | -0.1642 | 0.1738 |
| is_senior | -0.0169 | 0.1509 | 0.1677 |
| partner | 0.0157 | -0.1504 | 0.1662 |
| total_billing | -0.0671 | -0.2322 | 0.1650 |

## core8
| Setting | ROC-AUC | Inverted AUC | Accuracy | Precision | Recall | F1 | Train sec |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cell2Cell in-domain | 0.6245 | 0.6245 | 0.5673 | 0.3605 | 0.6485 | 0.4634 | 0.1 |
| IBM in-domain | 0.8274 | 0.8274 | 0.7367 | 0.5026 | 0.7727 | 0.6091 | 0.1 |
| Cell2Cell -> IBM | 0.2791 | 0.7209 | 0.4074 | 0.1019 | 0.1578 | 0.1238 | nan |
| IBM -> Cell2Cell | 0.4860 | 0.5140 | 0.4981 | 0.2776 | 0.4630 | 0.3471 | nan |
- Domain classifier AUC: `1.0000`; accuracy: `0.9998`

### Top Drift Features
| feature | cell_missing | ibm_missing | cell_mean | ibm_mean | smd | ks |
|---|---:|---:|---:|---:|---:|---:|
| total_billing | 0.003 | 0.002 | 46.8301 | 2283.3004 | -1.3952 | 0.8665 |
| payment_card | 0.000 | 0.000 | 0.6759 | 0.2161 | 1.0433 | 0.4598 |
| tenure | 0.000 | 0.000 | 18.7563 | 32.3711 | -0.7282 | 0.3689 |
| commitment_band | 0.000 | 0.000 | 0.7247 | 1.1157 | -0.5430 | 0.3689 |
| monthly_billing | 0.003 | 0.000 | 58.8345 | 64.7617 | -0.1560 | 0.2696 |
| is_senior | 0.290 | 0.000 | 0.0478 | 0.1621 | -0.3795 | 0.1143 |
| partner | 0.386 | 0.000 | 0.5950 | 0.4830 | 0.2260 | 0.1120 |
| dependents | 0.000 | 0.000 | 0.2423 | 0.2996 | -0.1292 | 0.0573 |

### Top Target-Association Gaps
| feature | cell_corr | ibm_corr | corr_gap |
|---|---:|---:|---:|
| tenure | 0.0396 | -0.3671 | 0.4067 |
| commitment_band | 0.0281 | -0.3363 | 0.3643 |
| monthly_billing | -0.0237 | 0.1847 | 0.2084 |
| dependents | 0.0096 | -0.1642 | 0.1738 |
| is_senior | -0.0169 | 0.1509 | 0.1677 |
| partner | 0.0157 | -0.1504 | 0.1662 |
| total_billing | -0.0671 | -0.2322 | 0.1650 |
| payment_card | -0.0086 | -0.1343 | 0.1257 |

## Leave-One-Group-Out Ablation on core8
| removed_group | n_features | C2I AUC | C2I F1 | I2C AUC | I2C F1 |
|---|---:|---:|---:|---:|---:|
| household | 5 | 0.3111 | 0.2337 | 0.4861 | 0.3115 |
| billing | 6 | 0.3607 | 0.1615 | 0.4899 | 0.3455 |
| commitment | 7 | 0.2696 | 0.1158 | 0.4838 | 0.3587 |
| payment | 7 | 0.2654 | 0.1151 | 0.4869 | 0.3697 |
| tenure | 7 | 0.3747 | 0.1284 | 0.4850 | 0.4337 |

## Interpretation
- If the strict common core improves transfer relative to the full Cell2Cell model, the main failure mode is feature mismatch rather than classifier capacity.
- If the `core8` extension worsens transfer or makes the domains easier to classify, then the abstracted commitment/payment features are adding domain-specific noise.
- Large correlation gaps between Cell2Cell and IBM for the same feature indicate that a feature with the same name or rough meaning still behaves differently across datasets.