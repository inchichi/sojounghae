# Cluster Router Experiment on abstract_shared without tenure

## Goal
- Check whether clustering on the shared abstract representation helps cross-domain churn transfer.
- Source domains: Cell2Cell and BankChurners.
- Target domain: IBM Telco.
- Methods: baseline pooled XGBoost, cluster-augmented XGBoost, and cluster router (mixture of experts).

## Baseline pooled model
| split | roc_auc | accuracy | precision | recall | f1 |
|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6117 | 0.5497 | 0.3488 | 0.6496 | 0.4539 |
| BankChurners holdout | 0.9828 | 0.9482 | 0.8235 | 0.8615 | 0.8421 |
| IBM holdout | 0.5869 | 0.7055 | 0.3048 | 0.0856 | 0.1336 |

### IBM best-threshold check for baseline
- best_threshold: 0.110
- best_f1: 0.4529

## K sweep diagnostics
| k | n_clusters | cluster_min_size | cluster_max_size | domain_ari | domain_nmi | domain_purity | churn_ari | churn_nmi | churn_purity | silhouette | aug_ibm_auc | aug_ibm_f1 | router_ibm_auc | router_ibm_f1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.0 | 2.0 | 8185.0 | 40753.0 | 0.9728 | 0.9287 | 0.9945 | -0.0417 | 0.0112 | 0.7329 | 0.3383 | 0.6021 | 0.0936 | 0.5788 | 0.1171 |
| 3.0 | 3.0 | 8063.0 | 32520.0 | 0.5272 | 0.6262 | 0.9938 | -0.0253 | 0.0088 | 0.7329 | 0.2558 | 0.5777 | 0.0314 | 0.6133 | 0.4302 |
| 4.0 | 4.0 | 11.0 | 32143.0 | 0.5154 | 0.6205 | 0.9938 | -0.0246 | 0.0089 | 0.733 | 0.2499 | 0.5592 | 0.018 | 0.5562 | 0.1411 |
| 5.0 | 5.0 | 11.0 | 31955.0 | 0.5045 | 0.6054 | 0.995 | -0.0159 | 0.0126 | 0.7355 | 0.2639 | 0.6069 | 0.0531 | 0.5771 | 0.1396 |
| 6.0 | 6.0 | 16.0 | 24797.0 | 0.3035 | 0.4563 | 0.9867 | -0.0072 | 0.0122 | 0.7351 | 0.1674 | 0.5481 | 0.1305 | 0.5303 | 0.1336 |
| 7.0 | 7.0 | 16.0 | 17321.0 | 0.1898 | 0.3966 | 0.9901 | -0.0001 | 0.0097 | 0.7351 | 0.1915 | 0.5454 | 0.1481 | 0.52 | 0.1458 |
| 8.0 | 8.0 | 10.0 | 17433.0 | 0.1526 | 0.3118 | 0.9696 | -0.0067 | 0.0105 | 0.7351 | 0.2077 | 0.548 | 0.0043 | 0.5424 | 0.1551 |

## Best cluster-augmented model: k=5
| split | roc_auc | accuracy | precision | recall | f1 |
|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6143 | 0.5507 | 0.3484 | 0.6424 | 0.4518 |
| BankChurners holdout | 0.9832 | 0.9477 | 0.8269 | 0.8523 | 0.8394 |
| IBM holdout | 0.6069 | 0.7218 | 0.275 | 0.0294 | 0.0531 |

## Best cluster-router model: k=3
| split | roc_auc | accuracy | precision | recall | f1 |
|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6056 | 0.5905 | 0.3577 | 0.5292 | 0.4269 |
| BankChurners holdout | 0.9874 | 0.9477 | 0.7905 | 0.9169 | 0.849 |
| IBM holdout | 0.6133 | 0.5337 | 0.3184 | 0.6631 | 0.4302 |

## Cluster composition for best cluster-augmented k=5
 cluster_id  BankChurners  Cell2Cell  total  purity  churn_rate
          0           177      31778  31955  0.9945      0.2859
          1          7924         67   7991  0.9916      0.1561
          2             0       8358   8358  1.0000      0.2761
          3             0         11     11  1.0000      0.7273
          4             0        623    623  1.0000      0.5971

### IBM cluster composition for best cluster-augmented k=5
 cluster_id  count  churn_rate
        0.0      5      0.0000
        1.0      3      0.0000
        2.0    232      0.4054
        3.0   1169      0.2523

## Cluster composition for best router k=3
 cluster_id  BankChurners  Cell2Cell  total  purity  churn_rate
          0             0       8355   8355  1.0000      0.2770
          1           171      32349  32520  0.9947      0.2912
          2          7930        133   8063  0.9835      0.1596

### IBM cluster composition for best router k=3
 cluster_id  count  churn_rate
        0.0   1403      0.2741
        1.0      4      0.0000
        2.0      2      0.0000

## Interpretation
- If cluster purity is high but IBM AUC does not improve, clustering is mostly acting as a domain separator rather than a shared representation learner.
- If the router beats the baseline on IBM, then cluster-based routing is a viable way to handle the domain mismatch.
- If neither the augmented model nor the router improves IBM, then clustering is not solving the meaning drift across domains.