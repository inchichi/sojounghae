# Abstract Shared Schema vs IBM Telco

## Setup
- Goal: check whether the abstract shared schema can explain IBM Telco as well.
- Source domains: Cell2Cell and BankChurners.
- Target domain: IBM Telco.
- Methods: source-only transfer with `raw`, `rank normalization`, `CORAL`; pooled multi-source training with `raw`, `rank`.

## Reference Baseline: billing2 on IBM
                            Setting  roc_auc  accuracy  precision  recall     f1
Cell2Cell -> IBM (billing2 + CORAL)   0.6885    0.5855     0.3604  0.7246 0.4813
           IBM in-domain (billing2)   0.8011    0.7119     0.4728  0.7433 0.5780

## Cell2Cell -> IBM Transfer
       direction method  roc_auc  accuracy  precision   recall       f1  inverted_auc
Cell2Cell -> IBM    raw 0.365321  0.298084   0.219690 0.644385 0.327668      0.634679
IBM -> Cell2Cell    raw 0.486104  0.514691   0.287613 0.463290 0.354902      0.513896
Cell2Cell -> IBM   rank 0.495258  0.577715   0.263383 0.328877 0.292509      0.504742
IBM -> Cell2Cell   rank 0.518335  0.612341   0.316075 0.296737 0.306101      0.481665
Cell2Cell -> IBM  coral 0.549638  0.593329   0.299799 0.398396 0.342135      0.450362
IBM -> Cell2Cell  coral 0.478341  0.581391   0.260948 0.247111 0.253841      0.521659

## BankChurners -> IBM Transfer
          direction method  roc_auc  accuracy  precision   recall       f1  inverted_auc
BankChurners -> IBM    raw 0.492729  0.733144   0.000000 0.000000 0.000000      0.507271
IBM -> BankChurners    raw 0.603804  0.839092   0.333333 0.003077 0.006098      0.396196
BankChurners -> IBM   rank 0.306656  0.689141   0.029412 0.005348 0.009050      0.693344
IBM -> BankChurners   rank 0.382271  0.648569   0.074725 0.104615 0.087179      0.617729
BankChurners -> IBM  coral 0.339876  0.477644   0.129098 0.168449 0.146172      0.660124
IBM -> BankChurners  coral 0.415312  0.715202   0.093548 0.089231 0.091339      0.584688

## IBM In-Domain
method  roc_auc  accuracy  precision  recall     f1
   raw   0.8335     0.741     0.5081  0.7594 0.6088
  rank   0.8331     0.741     0.5081  0.7540 0.6071

## Pooled Multi-Source Training
            split      method  roc_auc  accuracy  precision  recall     f1
Cell2Cell holdout  pooled_raw   0.6533    0.5609     0.3659  0.7148 0.4841
      IBM holdout  pooled_raw   0.5518    0.6473     0.1970  0.1070 0.1386
Cell2Cell holdout pooled_rank   0.6540    0.5636     0.3668  0.7084 0.4833
      IBM holdout pooled_rank   0.5608    0.6863     0.1222  0.0294 0.0474

## Domain Separability
                          pair  domain_auc  domain_accuracy
              Cell2Cell vs IBM      1.0000           0.9998
           BankChurners vs IBM      1.0000           1.0000
Pooled (Cell2Cell+Bank) vs IBM      0.9999           0.9998

## Interpretation
- If abstract shared features transfer to IBM better than the billing2 baseline, then the abstraction is capturing a more general churn pattern.
- If BankChurners -> IBM beats Cell2Cell -> IBM, the shared representation is likely closer to the financial churn structure than to the telecom-only structure.
- If pooled training improves IBM holdout while keeping source holdouts reasonable, the model is learning a genuinely shared representation rather than a source-specific shortcut.