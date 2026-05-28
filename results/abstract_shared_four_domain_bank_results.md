# Abstract Shared Four-Domain Results

## Goal
- Fix `abstract_shared` as the common concept layer.
- Train on pooled `Cell2Cell + BankChurners + IBM` source domains.
- Test transfer on the unused `BankChurn` domain.
- Use a cluster-router mixture of experts instead of one global model.

## Concept Mapping
| concept | Cell2Cell | BankChurners | IBM | BankChurn |
| --- | --- | --- | --- | --- |
| tenure | MonthsInService | Months_on_book | tenure | Tenure |
| age | AgeHH1 | Customer_Age | SeniorCitizen | Age |
| partner_flag | MaritalStatus == Yes | Marital_Status == Married | Partner == Yes | (missing -> 0) |
| children_flag | ChildrenInHH == Yes | Dependent_count > 0 | Dependents == Yes | (missing -> 0) |
| relationship_depth | ActiveSubs + UniqueSubs + partner + children | Total_Relationship_Count + partner + children | partner + children + contract_strength | NumOfProducts + HasCrCard + IsActiveMember |
| activity_volume | MonthlyMinutes + received/outbound/inbound calls | Total_Trans_Ct | MonthlyCharges | Balance |
| monetary_volume | MonthlyRevenue + TotalRecurringCharge | Total_Trans_Amt | TotalCharges | EstimatedSalary |
| capacity | CreditRating (inverse ordinal) | Credit_Limit | Contract strength ordinal | CreditScore |
| pressure_ratio | OverageMinutes / MonthlyRevenue | Avg_Utilization_Ratio | MonthlyCharges / tenure | Balance / EstimatedSalary |
| change_intensity | PercChangeMinutes + PercChangeRevenues | Amt change + count change | abs(MonthlyCharges - avg_monthly_charges) | abs(Balance - EstimatedSalary) / EstimatedSalary |
| support_intensity | CustomerCareCalls + RetentionCalls + MadeCallToRetentionTeam | Contacts_Count_12_mon | support add-on count | HasCrCard + IsActiveMember |

## Dataset Splits
| split | rows | churn_rate |
| --- | --- | --- |
| Cell2Cell train | 40837 | 0.2882 |
| BankChurners train | 8101 | 0.1607 |
| IBM train | 5634 | 0.2654 |
| BankChurn train | 8000 | 0.2037 |
| Cell2Cell holdout | 10210 | 0.2881 |
| BankChurners holdout | 2026 | 0.1604 |
| IBM holdout | 1409 | 0.2654 |
| BankChurn holdout | 2000 | 0.2035 |

## Source Holdout Results
| roc_auc | accuracy | precision | recall | f1 | best_threshold | best_accuracy | best_precision | best_recall | best_f1 | domain | model |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.5659 | 0.4446 | 0.3106 | 0.7607 | 0.4411 | 0.4865 | 0.4099 | 0.3098 | 0.8532 | 0.4545 | Cell2Cell | pooled_global |
| 0.6606 | 0.8228 | 0.3111 | 0.0862 | 0.1349 | 0.3670 | 0.6782 | 0.2922 | 0.7077 | 0.4137 | BankChurners | pooled_global |
| 0.7880 | 0.6132 | 0.3948 | 0.8583 | 0.5409 | 0.6007 | 0.7410 | 0.5089 | 0.6898 | 0.5857 | IBM | pooled_global |
| 0.5734 | 0.4940 | 0.3217 | 0.6822 | 0.4373 | 0.4412 | 0.3747 | 0.3036 | 0.9041 | 0.4545 | Cell2Cell | router_k=2 |
| 0.6841 | 0.8322 | 0.4176 | 0.1169 | 0.1827 | 0.3737 | 0.6950 | 0.3007 | 0.6800 | 0.4170 | BankChurners | router_k=2 |
| 0.7881 | 0.6082 | 0.3917 | 0.8610 | 0.5385 | 0.5963 | 0.7161 | 0.4776 | 0.7406 | 0.5807 | IBM | router_k=2 |
| 0.5726 | 0.4807 | 0.3198 | 0.7121 | 0.4414 | 0.4495 | 0.3843 | 0.3053 | 0.8909 | 0.4547 | Cell2Cell | router_k=3 |
| 0.6843 | 0.8258 | 0.3814 | 0.1385 | 0.2032 | 0.3735 | 0.6856 | 0.2958 | 0.6954 | 0.4151 | BankChurners | router_k=3 |
| 0.7070 | 0.5947 | 0.3719 | 0.7647 | 0.5004 | 0.5407 | 0.6437 | 0.4027 | 0.7086 | 0.5136 | IBM | router_k=3 |
| 0.5791 | 0.4823 | 0.3226 | 0.7247 | 0.4465 | 0.4544 | 0.3940 | 0.3076 | 0.8817 | 0.4561 | Cell2Cell | router_k=4 |
| 0.6861 | 0.8144 | 0.3526 | 0.1877 | 0.2450 | 0.3940 | 0.7024 | 0.3069 | 0.6800 | 0.4230 | BankChurners | router_k=4 |
| 0.7329 | 0.6508 | 0.4145 | 0.7647 | 0.5376 | 0.4656 | 0.6288 | 0.4024 | 0.8209 | 0.5400 | IBM | router_k=4 |
| 0.5861 | 0.5042 | 0.3295 | 0.6961 | 0.4473 | 0.4483 | 0.4078 | 0.3126 | 0.8800 | 0.4613 | Cell2Cell | router_k=5 |
| 0.7051 | 0.8159 | 0.3983 | 0.2892 | 0.3351 | 0.4275 | 0.7369 | 0.3289 | 0.6154 | 0.4287 | BankChurners | router_k=5 |
| 0.7268 | 0.6352 | 0.4025 | 0.7727 | 0.5293 | 0.5186 | 0.6522 | 0.4150 | 0.7567 | 0.5360 | IBM | router_k=5 |
| 0.5895 | 0.5052 | 0.3292 | 0.6910 | 0.4459 | 0.4637 | 0.4381 | 0.3188 | 0.8358 | 0.4616 | Cell2Cell | router_k=6 |
| 0.7714 | 0.7986 | 0.3707 | 0.3662 | 0.3684 | 0.3909 | 0.7231 | 0.3392 | 0.7662 | 0.4703 | BankChurners | router_k=6 |
| 0.7282 | 0.6458 | 0.4090 | 0.7513 | 0.5297 | 0.4757 | 0.6324 | 0.4037 | 0.8075 | 0.5383 | IBM | router_k=6 |

## Router k Sweep
| k | mean_source_auc | mean_source_f1 | bank_auc | bank_f1 | bank_best_threshold | bank_best_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| 6.0000 | 0.6964 | 0.4480 | 0.5429 | 0.3308 | 0.9607 | 0.3500 |
| 2.0000 | 0.6819 | 0.3861 | 0.4787 | 0.3330 | 0.0000 | 0.3382 |
| 5.0000 | 0.6727 | 0.4372 | 0.5305 | 0.3267 | 0.9029 | 0.3440 |
| 4.0000 | 0.6660 | 0.4097 | 0.4628 | 0.2819 | 0.0000 | 0.3387 |
| 3.0000 | 0.6546 | 0.3817 | 0.4277 | 0.1941 | 0.0000 | 0.3383 |

## Best Router
- Best k by mean source AUC: `6`

## BankChurn External Test
| domain | model | roc_auc | accuracy | precision | recall | f1 | best_threshold | best_accuracy | best_precision | best_recall | best_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BankChurn | Cell2Cell_only_transfer | 0.5319 | 0.7840 | 0.2449 | 0.0295 | 0.0526 | 0.0000 | 0.2035 | 0.2035 | 1.0000 | 0.3382 |
| BankChurn | pooled_global | 0.4608 | 0.5600 | 0.1868 | 0.3464 | 0.2427 | 0.0000 | 0.2035 | 0.2035 | 1.0000 | 0.3382 |
| BankChurn | router_k=6 | 0.5429 | 0.2190 | 0.2003 | 0.9484 | 0.3308 | 0.9607 | 0.4745 | 0.2339 | 0.6953 | 0.3500 |
| BankChurn | bank_in_domain | 0.7564 | 0.6940 | 0.3674 | 0.6978 | 0.4814 | 0.5622 | 0.7520 | 0.4242 | 0.6118 | 0.5010 |

## Concept Coefficients
| concept | coefficient |
| --- | --- |
| monetary_volume | -1.1836 |
| tenure | -0.3664 |
| monetary_per_tenure | 0.1920 |
| relationship_depth | 0.1737 |
| relationship_per_tenure | -0.1607 |
| pressure_ratio | 0.1085 |
| partner_flag | -0.0938 |
| volume_to_capacity | 0.0855 |
| support_to_activity | 0.0630 |
| support_intensity | 0.0430 |

## Interpretation
- If the pooled global model already lifts BankChurn above the Cell2Cell-only transfer, the shared concept layer is carrying some signal.
- If the router beats the pooled global model on BankChurn, the concept layer plus domain-aware routing is doing useful work.
- If BankChurn in-domain stays much higher than transfer, the new bank domain still needs its own calibration even after abstraction.