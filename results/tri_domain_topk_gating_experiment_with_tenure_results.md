# Tri-domain pooled experiment (with_tenure)

## Setup
- Train on pooled Cell2Cell + BankChurners + IBM holdout splits.
- Evaluate holdout performance on all three domains.
- Methods: pooled baseline, cluster-augmented XGBoost, cluster-router, top-k gating mixture.

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

## Top-k gating sweep summary
| n_clusters | gate_k | domain_purity | cluster_min_size | cluster_max_size | mean_auc | mean_f1 | cell_auc | bank_auc | ibm_auc | avg_top1_weight | avg_gate_entropy |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.0 | 2.0 | 0.8531 | 10269.0 | 44303.0 | 0.8186 | 0.6359 | 0.6512 | 0.9839 | 0.8205 | 0.8467 | 0.3794 |
| 3.0 | 2.0 | 0.8994 | 6710.0 | 37768.0 | 0.8175 | 0.6426 | 0.6466 | 0.9843 | 0.8215 | 0.8188 | 0.4231 |
| 3.0 | 3.0 | 0.8994 | 6710.0 | 37768.0 | 0.8154 | 0.6382 | 0.6472 | 0.9843 | 0.8149 | 0.7798 | 0.5836 |
| 4.0 | 2.0 | 0.975 | 2569.0 | 37195.0 | 0.8146 | 0.6418 | 0.6475 | 0.9852 | 0.8109 | 0.8577 | 0.3505 |
| 4.0 | 3.0 | 0.975 | 2569.0 | 37195.0 | 0.811 | 0.6265 | 0.6483 | 0.985 | 0.7996 | 0.823 | 0.492 |
| 5.0 | 2.0 | 0.979 | 869.0 | 37128.0 | 0.814 | 0.6348 | 0.6456 | 0.9838 | 0.8127 | 0.8523 | 0.3635 |
| 5.0 | 3.0 | 0.979 | 869.0 | 37128.0 | 0.8093 | 0.6238 | 0.6471 | 0.9834 | 0.7975 | 0.8128 | 0.5171 |
| 6.0 | 2.0 | 0.9659 | 869.0 | 35909.0 | 0.8088 | 0.6222 | 0.6462 | 0.983 | 0.7972 | 0.86 | 0.3457 |
| 6.0 | 3.0 | 0.9659 | 869.0 | 35909.0 | 0.8089 | 0.6178 | 0.6472 | 0.9826 | 0.7969 | 0.8254 | 0.4867 |
| 7.0 | 2.0 | 0.9709 | 865.0 | 32438.0 | 0.8102 | 0.6194 | 0.6392 | 0.9842 | 0.8071 | 0.8352 | 0.3863 |
| 7.0 | 3.0 | 0.9709 | 865.0 | 32438.0 | 0.8095 | 0.6091 | 0.6365 | 0.9838 | 0.8082 | 0.7927 | 0.5501 |
| 8.0 | 2.0 | 0.9679 | 625.0 | 22778.0 | 0.8139 | 0.6361 | 0.6366 | 0.9834 | 0.8217 | 0.778 | 0.4603 |
| 8.0 | 3.0 | 0.9679 | 625.0 | 22778.0 | 0.8135 | 0.6331 | 0.6378 | 0.9821 | 0.8208 | 0.7144 | 0.6847 |

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

## Best top-k gating model: k=2, gate_k=2
| split | roc_auc | accuracy | precision | recall | f1 | mean_auc | mean_f1 |
|---|---|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6512 | 0.6444 | 0.4069 | 0.5119 | 0.4534 | 0.8186 | 0.6359 |
| BankChurners holdout | 0.9839 | 0.9437 | 0.7712 | 0.9231 | 0.8403 | 0.8186 | 0.6359 |
| IBM holdout | 0.8205 | 0.7431 | 0.5106 | 0.7701 | 0.6141 | 0.8186 | 0.6359 |

## Interpretation
- Compare mean AUC across the three holdouts to judge the final pooled representation.
- If router > baseline, the shared representation plus routing is doing useful domain separation.
- If top-k gating beats hard routing, the cluster boundaries are soft enough that blending multiple experts helps.
- If top-k gating does not beat hard routing, the routing problem is already close to hard domain separation.