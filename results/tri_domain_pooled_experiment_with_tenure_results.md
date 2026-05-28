# Tri-domain pooled experiment (with_tenure)

## Setup
- Train on pooled Cell2Cell + BankChurners + IBM holdout splits.
- Evaluate holdout performance on all three domains.
- Methods: pooled baseline, cluster-augmented XGBoost, cluster-router.

## Baseline pooled model
| split | roc_auc | accuracy | precision | recall | f1 | mean_auc | mean_f1 |
|---|---|---|---|---|---|---|---|
| Cell2Cell holdout | 0.653 | 0.5546 | 0.3616 | 0.7135 | 0.48 | 0.8247 | 0.6436 |
| BankChurners holdout | 0.9799 | 0.9413 | 0.8121 | 0.8246 | 0.8183 | 0.8247 | 0.6436 |
| IBM holdout | 0.8412 | 0.7516 | 0.5208 | 0.8048 | 0.6324 | 0.8247 | 0.6436 |

### Best-threshold check for baseline
- cell: threshold=0.470, best_f1=0.4886, best_auc=0.6530
- bank: threshold=0.565, best_f1=0.8256, best_auc=0.9799
- ibm: threshold=0.525, best_f1=0.6328, best_auc=0.8412

## K sweep summary
| k | domain_purity | cluster_min_size | cluster_max_size | aug_mean_auc | aug_mean_f1 | router_mean_auc | router_mean_f1 | cell_router_auc | bank_router_auc | ibm_router_auc |
|---|---|---|---|---|---|---|---|---|---|---|
| 2.0 | 0.8531 | 10269.0 | 44303.0 | 0.8255 | 0.6469 | 0.8232 | 0.6448 | 0.6544 | 0.9859 | 0.8294 |
| 3.0 | 0.8994 | 6710.0 | 37768.0 | 0.825 | 0.6474 | 0.8218 | 0.6448 | 0.649 | 0.9861 | 0.8304 |
| 4.0 | 0.975 | 2569.0 | 37195.0 | 0.8249 | 0.6482 | 0.8227 | 0.6441 | 0.6505 | 0.9869 | 0.8306 |
| 5.0 | 0.979 | 869.0 | 37128.0 | 0.8255 | 0.6493 | 0.8221 | 0.643 | 0.651 | 0.9864 | 0.8289 |
| 6.0 | 0.9659 | 869.0 | 35909.0 | 0.8249 | 0.6458 | 0.8096 | 0.6249 | 0.6499 | 0.9855 | 0.7933 |
| 7.0 | 0.9709 | 865.0 | 32438.0 | 0.8253 | 0.651 | 0.8103 | 0.6271 | 0.6432 | 0.9858 | 0.8019 |
| 8.0 | 0.9679 | 625.0 | 22778.0 | 0.8256 | 0.6451 | 0.8141 | 0.6415 | 0.6338 | 0.9863 | 0.8222 |

## Best cluster-augmented model: k=8
| split | roc_auc | accuracy | precision | recall | f1 | mean_auc | mean_f1 |
|---|---|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6538 | 0.5561 | 0.364 | 0.723 | 0.4842 | 0.8256 | 0.6451 |
| BankChurners holdout | 0.9809 | 0.9442 | 0.8252 | 0.8277 | 0.8264 | 0.8256 | 0.6451 |
| IBM holdout | 0.842 | 0.7459 | 0.5138 | 0.7968 | 0.6247 | 0.8256 | 0.6451 |

## Best cluster-router model: k=2
| split | roc_auc | accuracy | precision | recall | f1 | mean_auc | mean_f1 |
|---|---|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6544 | 0.6063 | 0.3864 | 0.623 | 0.477 | 0.8232 | 0.6448 |
| BankChurners holdout | 0.9859 | 0.9472 | 0.7868 | 0.92 | 0.8482 | 0.8232 | 0.6448 |
| IBM holdout | 0.8294 | 0.7324 | 0.4975 | 0.7861 | 0.6093 | 0.8232 | 0.6448 |

## Interpretation
- Compare mean AUC across the three holdouts to judge the final pooled representation.
- If router > baseline, the shared representation plus routing is doing useful domain separation.
- If tenure-inclusive and tenure-free variants diverge, tenure is acting more like a routing cue than a universal core feature.