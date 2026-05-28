# Cluster Router Experiment on abstract_shared

## Goal
- Check whether clustering on the shared abstract representation helps cross-domain churn transfer.
- Source domains: Cell2Cell and BankChurners.
- Target domain: IBM Telco.
- Methods: baseline pooled XGBoost, cluster-augmented XGBoost, and cluster router (mixture of experts).

## Baseline pooled model
| split | roc_auc | accuracy | precision | recall | f1 |
|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6533 | 0.5609 | 0.3659 | 0.7148 | 0.4841 |
| BankChurners holdout | 0.9817 | 0.9472 | 0.8283 | 0.8462 | 0.8371 |
| IBM holdout | 0.5518 | 0.6473 | 0.197 | 0.107 | 0.1386 |

### IBM best-threshold check for baseline
- best_threshold: 0.160
- best_f1: 0.4466

## K sweep diagnostics
| k | n_clusters | cluster_min_size | cluster_max_size | domain_ari | domain_nmi | domain_purity | churn_ari | churn_nmi | churn_purity | silhouette | aug_ibm_auc | aug_ibm_f1 | router_ibm_auc | router_ibm_f1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.0 | 2.0 | 8226.0 | 40712.0 | 0.98 | 0.9464 | 0.996 | -0.042 | 0.0114 | 0.7329 | 0.3453 | 0.5982 | 0.0964 | 0.535 | 0.3781 |
| 3.0 | 3.0 | 6324.0 | 34434.0 | 0.6089 | 0.6788 | 0.9963 | -0.0329 | 0.0092 | 0.7329 | 0.2982 | 0.5666 | 0.0748 | 0.7131 | 0.494 |
| 4.0 | 4.0 | 5343.0 | 28548.0 | 0.3977 | 0.5397 | 0.9963 | -0.0149 | 0.0077 | 0.7329 | 0.1897 | 0.537 | 0.0611 | 0.6708 | 0.462 |
| 5.0 | 5.0 | 961.0 | 28426.0 | 0.388 | 0.5155 | 0.9951 | -0.0172 | 0.0072 | 0.7329 | 0.2001 | 0.566 | 0.1142 | 0.7125 | 0.5198 |
| 6.0 | 6.0 | 961.0 | 25784.0 | 0.3232 | 0.4755 | 0.9952 | -0.0155 | 0.0069 | 0.7329 | 0.1982 | 0.5515 | 0.1171 | 0.6267 | 0.4556 |
| 7.0 | 7.0 | 961.0 | 19861.0 | 0.2163 | 0.4134 | 0.9953 | -0.0052 | 0.0062 | 0.7329 | 0.1554 | 0.5951 | 0.0887 | 0.7126 | 0.5206 |
| 8.0 | 8.0 | 929.0 | 14284.0 | 0.1512 | 0.369 | 0.995 | -0.0023 | 0.0056 | 0.7329 | 0.1774 | 0.5331 | 0.0683 | 0.6883 | 0.5167 |

## Best cluster-augmented model: k=2
| split | roc_auc | accuracy | precision | recall | f1 |
|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6539 | 0.5646 | 0.3678 | 0.7104 | 0.4846 |
| BankChurners holdout | 0.9811 | 0.9452 | 0.8185 | 0.8462 | 0.8321 |
| IBM holdout | 0.5982 | 0.6806 | 0.1935 | 0.0642 | 0.0964 |

## Best cluster-router model: k=3
| split | roc_auc | accuracy | precision | recall | f1 |
|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6488 | 0.608 | 0.3859 | 0.6094 | 0.4726 |
| BankChurners holdout | 0.9871 | 0.9531 | 0.8159 | 0.9138 | 0.8621 |
| IBM holdout | 0.7131 | 0.5493 | 0.3519 | 0.8289 | 0.494 |

## Cluster composition for best cluster-augmented k=2
 cluster_id  BankChurners  Cell2Cell  total  purity  churn_rate
          0            36      40676  40712  0.9991      0.2879
          1          8065        161   8226  0.9804      0.1644

### IBM cluster composition for best cluster-augmented k=2
 cluster_id  count  churn_rate
        0.0   1048      0.2800
        1.0    361      0.2459

## Cluster composition for best router k=3
 cluster_id  BankChurners  Cell2Cell  total  purity  churn_rate
          0            50      34384  34434  0.9985      0.2937
          1          8051        129   8180  0.9842      0.1633
          2             0       6324   6324  1.0000      0.2566

### IBM cluster composition for best router k=3
 cluster_id  count  churn_rate
        0.0    830      0.2788
        1.0    356      0.2500
        2.0    223      0.2778

## Interpretation
- If cluster purity is high but IBM AUC does not improve, clustering is mostly acting as a domain separator rather than a shared representation learner.
- If the router beats the baseline on IBM, then cluster-based routing is a viable way to handle the domain mismatch.
- If neither the augmented model nor the router improves IBM, then clustering is not solving the meaning drift across domains.