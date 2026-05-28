# Tri-domain pooled experiment (no_tenure)

## Setup
- Train on pooled Cell2Cell + BankChurners + IBM holdout splits.
- Evaluate holdout performance on all three domains.
- Methods: pooled baseline, cluster-augmented XGBoost, cluster-router, top-k gating mixture.

## Baseline pooled model
| split | roc_auc | accuracy | precision | recall | f1 | mean_auc | mean_f1 |
|---|---|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6119 | 0.5452 | 0.3462 | 0.6509 | 0.452 | 0.8123 | 0.6366 |
| BankChurners holdout | 0.9828 | 0.9427 | 0.8047 | 0.8492 | 0.8263 | 0.8123 | 0.6366 |
| IBM holdout | 0.8422 | 0.748 | 0.5161 | 0.8128 | 0.6314 | 0.8123 | 0.6366 |

### Best-threshold check for baseline
- cell: threshold=0.465, best_f1=0.4666, best_auc=0.6119
- bank: threshold=0.545, best_f1=0.8354, best_auc=0.9828
- ibm: threshold=0.540, best_f1=0.6389, best_auc=0.8422

## K sweep summary
| k | domain_purity | cluster_min_size | cluster_max_size | aug_mean_auc | aug_mean_f1 | router_mean_auc | router_mean_f1 | cell_router_auc | bank_router_auc | ibm_router_auc |
|---|---|---|---|---|---|---|---|---|---|---|
| 2.0 | 0.8444 | 10463.0 | 44109.0 | 0.8123 | 0.6335 | 0.8132 | 0.6343 | 0.6154 | 0.9868 | 0.8376 |
| 3.0 | 0.9627 | 2871.0 | 43478.0 | 0.8112 | 0.6354 | 0.8117 | 0.6375 | 0.6142 | 0.9871 | 0.8338 |
| 4.0 | 0.9723 | 2789.0 | 35560.0 | 0.8112 | 0.6351 | 0.8082 | 0.6319 | 0.6048 | 0.9871 | 0.8328 |
| 5.0 | 0.9486 | 2615.0 | 26488.0 | 0.8124 | 0.6342 | 0.8052 | 0.6286 | 0.5976 | 0.9868 | 0.8314 |
| 6.0 | 0.9582 | 623.0 | 26238.0 | 0.8117 | 0.6361 | 0.8044 | 0.6288 | 0.5953 | 0.9868 | 0.8311 |
| 7.0 | 0.931 | 623.0 | 26327.0 | 0.8112 | 0.6346 | 0.8033 | 0.6269 | 0.5948 | 0.9802 | 0.8347 |
| 8.0 | 0.9515 | 327.0 | 19023.0 | 0.8119 | 0.638 | 0.8036 | 0.6282 | 0.5949 | 0.9835 | 0.8325 |

## Top-k gating sweep summary
| n_clusters | gate_k | domain_purity | cluster_min_size | cluster_max_size | mean_auc | mean_f1 | cell_auc | bank_auc | ibm_auc | avg_top1_weight | avg_gate_entropy |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.0 | 2.0 | 0.8444 | 10463.0 | 44109.0 | 0.8091 | 0.6357 | 0.6063 | 0.9849 | 0.8362 | 0.7828 | 0.486 |
| 3.0 | 2.0 | 0.9627 | 2871.0 | 43478.0 | 0.8087 | 0.639 | 0.6088 | 0.9848 | 0.8326 | 0.8452 | 0.3851 |
| 3.0 | 3.0 | 0.9627 | 2871.0 | 43478.0 | 0.8078 | 0.6392 | 0.6083 | 0.9845 | 0.8305 | 0.8146 | 0.5164 |
| 4.0 | 2.0 | 0.9723 | 2789.0 | 35560.0 | 0.8067 | 0.6266 | 0.6029 | 0.9863 | 0.831 | 0.807 | 0.442 |
| 4.0 | 3.0 | 0.9723 | 2789.0 | 35560.0 | 0.8046 | 0.6321 | 0.6024 | 0.986 | 0.8254 | 0.752 | 0.6462 |
| 5.0 | 2.0 | 0.9486 | 2615.0 | 26488.0 | 0.8072 | 0.6306 | 0.6048 | 0.9851 | 0.8316 | 0.7709 | 0.4941 |
| 5.0 | 3.0 | 0.9486 | 2615.0 | 26488.0 | 0.8061 | 0.6241 | 0.604 | 0.9842 | 0.83 | 0.6954 | 0.7504 |
| 6.0 | 2.0 | 0.9582 | 623.0 | 26238.0 | 0.8061 | 0.6305 | 0.6031 | 0.984 | 0.831 | 0.7726 | 0.4916 |
| 6.0 | 3.0 | 0.9582 | 623.0 | 26238.0 | 0.8048 | 0.6277 | 0.6027 | 0.9835 | 0.8281 | 0.6977 | 0.7462 |
| 7.0 | 2.0 | 0.931 | 623.0 | 26327.0 | 0.8064 | 0.6258 | 0.5991 | 0.9827 | 0.8374 | 0.77 | 0.48 |
| 7.0 | 3.0 | 0.931 | 623.0 | 26327.0 | 0.8055 | 0.6249 | 0.5991 | 0.9831 | 0.8343 | 0.6957 | 0.7302 |
| 8.0 | 2.0 | 0.9515 | 327.0 | 19023.0 | 0.8047 | 0.6321 | 0.5993 | 0.9832 | 0.8316 | 0.7557 | 0.4982 |
| 8.0 | 3.0 | 0.9515 | 327.0 | 19023.0 | 0.806 | 0.6287 | 0.602 | 0.9825 | 0.8334 | 0.6683 | 0.7776 |

## Best cluster-augmented model: k=5
| split | roc_auc | accuracy | precision | recall | f1 | mean_auc | mean_f1 |
|---|---|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6121 | 0.5446 | 0.345 | 0.6462 | 0.4498 | 0.8124 | 0.6342 |
| BankChurners holdout | 0.9827 | 0.9442 | 0.8064 | 0.8585 | 0.8316 | 0.8124 | 0.6342 |
| IBM holdout | 0.8425 | 0.7367 | 0.5025 | 0.8128 | 0.621 | 0.8124 | 0.6342 |

## Best cluster-router model: k=2
| split | roc_auc | accuracy | precision | recall | f1 | mean_auc | mean_f1 |
|---|---|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6154 | 0.5968 | 0.3651 | 0.5404 | 0.4358 | 0.8132 | 0.6343 |
| BankChurners holdout | 0.9868 | 0.9497 | 0.7973 | 0.92 | 0.8543 | 0.8132 | 0.6343 |
| IBM holdout | 0.8376 | 0.7275 | 0.4919 | 0.8128 | 0.6129 | 0.8132 | 0.6343 |

## Best top-k gating model: k=2, gate_k=2
| split | roc_auc | accuracy | precision | recall | f1 | mean_auc | mean_f1 |
|---|---|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6063 | 0.5857 | 0.3558 | 0.5401 | 0.429 | 0.8091 | 0.6357 |
| BankChurners holdout | 0.9849 | 0.9506 | 0.8032 | 0.9169 | 0.8563 | 0.8091 | 0.6357 |
| IBM holdout | 0.8362 | 0.7253 | 0.49 | 0.8503 | 0.6217 | 0.8091 | 0.6357 |

## Interpretation
- Compare mean AUC across the three holdouts to judge the final pooled representation.
- If router > baseline, the shared representation plus routing is doing useful domain separation.
- If top-k gating beats hard routing, the cluster boundaries are soft enough that blending multiple experts helps.
- If top-k gating does not beat hard routing, the routing problem is already close to hard domain separation.