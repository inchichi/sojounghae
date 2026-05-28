# Abstract Shared Schema and Multi-Source Training

## Setup
- Source domain: Cell2Cell
- Target domain: BankChurners
- Reference baseline: `billing2 = monthly_billing + total_billing`
- New schema: `abstract_shared`
- Multi-source training: pooled Cell2Cell + BankChurners
- Methods: `raw`, `rank normalization`, `CORAL` for transfer; pooled `raw`, `rank` for multi-source

## Dataset Size
- Cell2Cell rows: `51,047`; churn rate `0.2882`
- BankChurners rows: `10,127`; attrition rate `0.1607`

## Reference Baseline
- `billing2 + CORAL` Cell2Cell -> BankChurners: `AUC 0.4551`, `F1 0.2505`
- `billing2 + CORAL` BankChurners -> Cell2Cell: `AUC 0.5087`, `F1 0.3856`

## Abstract Shared Schema
- tenure
- age
- partner_flag
- children_flag
- relationship_depth
- activity_volume
- monetary_volume
- capacity
- pressure_ratio
- change_intensity
- support_intensity
- volume_to_capacity
- activity_per_tenure
- monetary_per_tenure
- support_per_tenure
- relationship_per_tenure
- support_to_activity

## Source-Only Transfer
                direction method  roc_auc  accuracy  precision   recall       f1  inverted_auc
Cell2Cell -> BankChurners    raw 0.603066  0.217177   0.167983 0.981538 0.286871      0.396934
BankChurners -> Cell2Cell    raw 0.500414  0.694613   0.349829 0.069680 0.116213      0.499586
Cell2Cell -> BankChurners   rank 0.587413  0.823297   0.348624 0.116923 0.175115      0.412587
BankChurners -> Cell2Cell   rank 0.482656  0.712537   0.612903 0.006458 0.012782      0.517344
Cell2Cell -> BankChurners  coral 0.467307  0.433366   0.153328 0.560000 0.240741      0.532693
BankChurners -> Cell2Cell  coral 0.531578  0.605583   0.323921 0.339225 0.331396      0.468422

## In-Domain Holdout
               split method  roc_auc  accuracy  precision   recall       f1
   Cell2Cell holdout    raw 0.654023  0.599021   0.381286 0.628824 0.474724
BankChurners holdout    raw 0.987511  0.952122   0.813187 0.910769 0.859216
   Cell2Cell holdout   rank 0.655324  0.602938   0.386484 0.643440 0.482908
BankChurners holdout   rank 0.987311  0.952122   0.816667 0.904615 0.858394
   Cell2Cell holdout  coral 0.617316  0.584917   0.364208 0.590755 0.450609
BankChurners holdout  coral 0.961000  0.911155   0.675545 0.858462 0.756098

## Threshold Sensitivity
                direction method  best_threshold  best_f1  roc_auc  accuracy  precision   recall       f1
Cell2Cell -> BankChurners    raw           0.845 0.308824 0.603066  0.628825   0.220183 0.516923 0.308824
BankChurners -> Cell2Cell    raw           0.050 0.216130 0.500414  0.663957   0.329617 0.160775 0.216130
Cell2Cell -> BankChurners   rank           0.255 0.305720 0.587413  0.652517   0.224964 0.476923 0.305720
BankChurners -> Cell2Cell   rank           0.050 0.051399 0.482656  0.714398   0.598485 0.026852 0.051399
Cell2Cell -> BankChurners  coral           0.195 0.277160 0.467307  0.165844   0.160954 0.996923 0.277160
BankChurners -> Cell2Cell  coral           0.050 0.414175 0.531578  0.439765   0.296394 0.687288 0.414175

## Multi-Source Pooled Training
               split      method  roc_auc  accuracy  precision   recall       f1
   Cell2Cell holdout  pooled_raw 0.647375  0.552204   0.361300 0.721618 0.481515
BankChurners holdout  pooled_raw 0.985589  0.953603   0.844776 0.870769 0.857576
   Cell2Cell holdout pooled_rank 0.646993  0.551028   0.361458 0.728076 0.483085
BankChurners holdout pooled_rank 0.985786  0.954590   0.839650 0.886154 0.862275

## Domain Separability
method  domain_auc  domain_accuracy
   raw     1.00000         1.000000
  rank     1.00000         1.000000
 coral     0.48197         0.555374

## Interpretation
- If the abstract schema were truly more universal, Cell2Cell -> BankChurners AUC should rise above the `billing2` baseline.
- If pooled multi-source training improves both holdouts, then the common representation is being learned rather than merely transferred.
- If domain AUC stays far from 0.5, the two domains are still easy to separate even after abstraction.
