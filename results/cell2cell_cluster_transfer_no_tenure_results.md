# Cell2Cell-only Cluster Transfer Without Tenure

## Goal
- Train clusters only on Cell2Cell without tenure.
- Test the learned cluster structure on BankChurners and IBM Telco separately.
- Compare a plain baseline, a cluster-augmented model, and a cluster-router model.

## Cell2Cell baseline transfer
| setting | roc_auc | accuracy | precision | recall | f1 |
|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6119 | 0.593 | 0.3629 | 0.5455 | 0.4358 |
| BankChurners holdout | 0.5883 | 0.1821 | 0.164 | 1.0 | 0.2818 |
| IBM holdout | 0.4836 | 0.6629 | 0.1418 | 0.0535 | 0.0777 |

## K sweep
| k | n_clusters | cluster_min_size | cluster_max_size | churn_ari | churn_nmi | churn_purity | silhouette | cell_baseline_auc | bank_baseline_auc | ibm_baseline_auc | cell_aug_auc | bank_aug_auc | ibm_aug_auc | cell_router_auc | bank_router_auc | ibm_router_auc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.0 | 2.0 | 8756.0 | 32081.0 | -0.0058 | 0.0002 | 0.7118 | 0.2883 | 0.6119 | 0.5883 | 0.4836 | 0.6113 | 0.5341 | 0.3998 | 0.605 | 0.344 | 0.5315 |
| 3.0 | 3.0 | 11.0 | 31800.0 | -0.0062 | 0.0005 | 0.7119 | 0.2804 | 0.6119 | 0.5883 | 0.4836 | 0.6114 | 0.5414 | 0.3824 | 0.6034 | 0.4071 | 0.491 |
| 4.0 | 4.0 | 11.0 | 24766.0 | -0.0019 | 0.0003 | 0.7119 | 0.1742 | 0.6119 | 0.5883 | 0.4836 | 0.611 | 0.5537 | 0.4474 | 0.6021 | 0.3444 | 0.5554 |
| 5.0 | 5.0 | 16.0 | 24704.0 | -0.0013 | 0.0008 | 0.7123 | 0.1759 | 0.6119 | 0.5883 | 0.4836 | 0.6131 | 0.6009 | 0.4343 | 0.6006 | 0.4132 | 0.5072 |
| 6.0 | 6.0 | 16.0 | 18370.0 | -0.0 | 0.0029 | 0.7145 | 0.1883 | 0.6119 | 0.5883 | 0.4836 | 0.6118 | 0.5386 | 0.4125 | 0.5902 | 0.5558 | 0.4732 |
| 7.0 | 7.0 | 10.0 | 15656.0 | 0.0064 | 0.0037 | 0.7149 | 0.1616 | 0.6119 | 0.5883 | 0.4836 | 0.6135 | 0.5136 | 0.3702 | 0.5915 | 0.4076 | 0.5481 |
| 8.0 | 8.0 | 11.0 | 10065.0 | 0.0029 | 0.0033 | 0.7149 | 0.1833 | 0.6119 | 0.5883 | 0.4836 | 0.6107 | 0.5574 | 0.489 | 0.5815 | 0.5474 | 0.4789 |

## Best external-average router k=6
                 setting  roc_auc  accuracy  precision  recall     f1  best_threshold  best_f1  best_auc
      Cell2Cell baseline   0.6119    0.5930     0.3629  0.5455 0.4358           0.425   0.4649    0.6119
   Cell2Cell cluster-aug   0.6118    0.5924     0.3617  0.5425 0.4340           0.425   0.4652    0.6118
Cell2Cell cluster-router   0.5902    0.5886     0.3515  0.5061 0.4149           0.370   0.4565    0.5902

                    setting  roc_auc  accuracy  precision  recall     f1  best_threshold  best_f1  best_auc
      BankChurners baseline   0.5883    0.1821     0.1640  1.0000 0.2818            0.74   0.3012    0.5883
   BankChurners cluster-aug   0.5386    0.1728     0.1624  1.0000 0.2794            0.66   0.2907    0.5386
BankChurners cluster-router   0.5558    0.8026     0.1739  0.0615 0.0909            0.27   0.3008    0.5558

           setting  roc_auc  accuracy  precision  recall     f1  best_threshold  best_f1  best_auc
      IBM baseline   0.4836    0.6629     0.1418  0.0535 0.0777            0.05   0.4195    0.4836
   IBM cluster-aug   0.4125    0.6189     0.1378  0.0829 0.1035            0.05   0.4195    0.4125
IBM cluster-router   0.4732    0.6437     0.1322  0.0615 0.0839            0.05   0.4195    0.4732

## Interpretation
- If the router improves IBM more than BankChurners, then the Cell2Cell cluster structure is telecom-specific.
- If BankChurners remains weak, then Cell2Cell clusters do not transfer cleanly into the financial domain.
- The best k is selected by the average external AUC on IBM and BankChurners.