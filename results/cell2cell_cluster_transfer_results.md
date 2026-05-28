# Cell2Cell-only Cluster Transfer

## Goal
- Train clusters only on Cell2Cell.
- Test the learned cluster structure on BankChurners and IBM Telco separately.
- Compare a plain baseline, a cluster-augmented model, and a cluster-router model.

## Cell2Cell baseline transfer
| setting | roc_auc | accuracy | precision | recall | f1 |
|---|---|---|---|---|---|
| Cell2Cell holdout | 0.6551 | 0.6009 | 0.3837 | 0.6349 | 0.4783 |
| BankChurners holdout | 0.4961 | 0.1693 | 0.1619 | 1.0 | 0.2786 |
| IBM holdout | 0.3661 | 0.2995 | 0.2201 | 0.6444 | 0.3281 |

## K sweep
| k | n_clusters | cluster_min_size | cluster_max_size | churn_ari | churn_nmi | churn_purity | silhouette | cell_baseline_auc | bank_baseline_auc | ibm_baseline_auc | cell_aug_auc | bank_aug_auc | ibm_aug_auc | cell_router_auc | bank_router_auc | ibm_router_auc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.0 | 2.0 | 7532.0 | 33305.0 | -0.0113 | 0.0008 | 0.7118 | 0.3117 | 0.6551 | 0.4961 | 0.3661 | 0.6554 | 0.513 | 0.3468 | 0.6493 | 0.441 | 0.5285 |
| 3.0 | 3.0 | 6618.0 | 27314.0 | -0.0016 | 0.0008 | 0.7118 | 0.159 | 0.6551 | 0.4961 | 0.3661 | 0.654 | 0.5167 | 0.4179 | 0.646 | 0.394 | 0.5997 |
| 4.0 | 4.0 | 2424.0 | 20769.0 | -0.0026 | 0.0009 | 0.7118 | 0.141 | 0.6551 | 0.4961 | 0.3661 | 0.6558 | 0.5383 | 0.329 | 0.6387 | 0.4235 | 0.4746 |
| 5.0 | 5.0 | 63.0 | 21223.0 | -0.0021 | 0.0013 | 0.7122 | 0.1459 | 0.6551 | 0.4961 | 0.3661 | 0.655 | 0.4808 | 0.3834 | 0.6373 | 0.515 | 0.4344 |
| 6.0 | 6.0 | 1073.0 | 12681.0 | -0.0017 | 0.0004 | 0.7118 | 0.1433 | 0.6551 | 0.4961 | 0.3661 | 0.6538 | 0.5182 | 0.3867 | 0.63 | 0.5726 | 0.542 |
| 7.0 | 7.0 | 48.0 | 12693.0 | -0.0012 | 0.0007 | 0.7122 | 0.1436 | 0.6551 | 0.4961 | 0.3661 | 0.6548 | 0.5117 | 0.3616 | 0.6307 | 0.4714 | 0.5503 |
| 8.0 | 8.0 | 14.0 | 15998.0 | -0.002 | 0.001 | 0.7123 | 0.159 | 0.6551 | 0.4961 | 0.3661 | 0.6564 | 0.5425 | 0.4485 | 0.6347 | 0.5074 | 0.5216 |

## Best external-average router k=6
                 setting  roc_auc  accuracy  precision  recall     f1  best_threshold  best_f1  best_auc
      Cell2Cell baseline   0.6551    0.6009     0.3837  0.6349 0.4783           0.435   0.4892    0.6551
   Cell2Cell cluster-aug   0.6538    0.6033     0.3852  0.6315 0.4785           0.440   0.4889    0.6538
Cell2Cell cluster-router   0.6300    0.6036     0.3741  0.5581 0.4480           0.400   0.4781    0.6300

                    setting  roc_auc  accuracy  precision  recall     f1  best_threshold  best_f1  best_auc
      BankChurners baseline   0.4961    0.1693     0.1619  1.0000 0.2786           0.565   0.2811    0.4961
   BankChurners cluster-aug   0.5182    0.1841     0.1636  0.9938 0.2810           0.545   0.2841    0.5182
BankChurners cluster-router   0.5726    0.4107     0.1681  0.6769 0.2693           0.340   0.2949    0.5726

           setting  roc_auc  accuracy  precision  recall     f1  best_threshold  best_f1  best_auc
      IBM baseline   0.3661    0.2995     0.2201  0.6444 0.3281            0.05   0.4195    0.3661
   IBM cluster-aug   0.3867    0.3307     0.2368  0.6845 0.3519            0.19   0.4205    0.3867
IBM cluster-router   0.5420    0.2747     0.2604  0.9412 0.4079            0.05   0.4195    0.5420

## Interpretation
- If the router improves IBM more than BankChurners, then the Cell2Cell cluster structure is telecom-specific.
- If BankChurners remains weak, then Cell2Cell clusters do not transfer cleanly into the financial domain.
- The best k is selected by the average external AUC on IBM and BankChurners.