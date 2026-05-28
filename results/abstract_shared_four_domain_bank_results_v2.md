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
| relationship_depth | ActiveSubs + UniqueSubs + partner + children | Total_Relationship_Count + partner + children | partner + children + contract_strength | NumOfProducts |
| activity_volume | MonthlyMinutes + received/outbound/inbound calls | Total_Trans_Ct | MonthlyCharges | NumOfProducts |
| monetary_volume | MonthlyRevenue + TotalRecurringCharge | Total_Trans_Amt | TotalCharges | Balance |
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
| 0.5657 | 0.4451 | 0.3111 | 0.7624 | 0.4419 | 0.4861 | 0.4083 | 0.3094 | 0.8549 | 0.4543 | Cell2Cell | pooled_global |
| 0.6608 | 0.8228 | 0.3152 | 0.0892 | 0.1391 | 0.3669 | 0.6782 | 0.2922 | 0.7077 | 0.4137 | BankChurners | pooled_global |
| 0.7881 | 0.6125 | 0.3943 | 0.8583 | 0.5404 | 0.5996 | 0.7388 | 0.5058 | 0.6952 | 0.5856 | IBM | pooled_global |
| 0.5850 | 0.6200 | 0.3626 | 0.4208 | 0.3896 | 0.3880 | 0.3926 | 0.3086 | 0.8929 | 0.4586 | Cell2Cell | router_k=2 |
| 0.7499 | 0.7359 | 0.3232 | 0.5908 | 0.4178 | 0.4804 | 0.7226 | 0.3196 | 0.6462 | 0.4277 | BankChurners | router_k=2 |
| 0.7593 | 0.6444 | 0.4152 | 0.8316 | 0.5539 | 0.5195 | 0.6636 | 0.4298 | 0.8182 | 0.5635 | IBM | router_k=2 |
| 0.5910 | 0.6365 | 0.3655 | 0.3552 | 0.3603 | 0.4086 | 0.4283 | 0.3173 | 0.8542 | 0.4627 | Cell2Cell | router_k=3 |
| 0.7559 | 0.7330 | 0.3188 | 0.5846 | 0.4126 | 0.4723 | 0.7147 | 0.3131 | 0.6523 | 0.4232 | BankChurners | router_k=3 |
| 0.7635 | 0.6324 | 0.4072 | 0.8449 | 0.5496 | 0.5392 | 0.6664 | 0.4318 | 0.8128 | 0.5640 | IBM | router_k=3 |
| 0.5961 | 0.6245 | 0.3630 | 0.4018 | 0.3814 | 0.4215 | 0.4196 | 0.3161 | 0.8715 | 0.4639 | Cell2Cell | router_k=4 |
| 0.8033 | 0.7878 | 0.3831 | 0.5292 | 0.4444 | 0.4660 | 0.7690 | 0.3735 | 0.6492 | 0.4742 | BankChurners | router_k=4 |
| 0.7804 | 0.6522 | 0.4185 | 0.7968 | 0.5488 | 0.5430 | 0.7133 | 0.4726 | 0.6925 | 0.5618 | IBM | router_k=4 |
| 0.5970 | 0.6212 | 0.3598 | 0.4038 | 0.3805 | 0.4360 | 0.4399 | 0.3198 | 0.8375 | 0.4629 | Cell2Cell | router_k=5 |
| 0.8276 | 0.8124 | 0.4398 | 0.6185 | 0.5141 | 0.4952 | 0.8110 | 0.4383 | 0.6338 | 0.5182 | BankChurners | router_k=5 |
| 0.8015 | 0.7026 | 0.4652 | 0.8048 | 0.5896 | 0.5178 | 0.7168 | 0.4794 | 0.7781 | 0.5933 | IBM | router_k=5 |
| 0.5972 | 0.6086 | 0.3579 | 0.4511 | 0.3991 | 0.4234 | 0.4119 | 0.3154 | 0.8889 | 0.4656 | Cell2Cell | router_k=6 |
| 0.8271 | 0.8100 | 0.4351 | 0.6185 | 0.5108 | 0.5044 | 0.8134 | 0.4418 | 0.6185 | 0.5154 | BankChurners | router_k=6 |
| 0.7611 | 0.6906 | 0.4478 | 0.7112 | 0.5496 | 0.4811 | 0.6771 | 0.4374 | 0.7567 | 0.5544 | IBM | router_k=6 |

## Router k Sweep
| k | mean_source_auc | mean_source_f1 | bank_auc | bank_f1 | bank_best_threshold | bank_best_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| 5.0000 | 0.7420 | 0.4947 | 0.5691 | 0.3426 | 0.8143 | 0.3581 |
| 2.0000 | 0.6981 | 0.4538 | 0.5581 | 0.3496 | 0.8521 | 0.3591 |
| 4.0000 | 0.7266 | 0.4582 | 0.5383 | 0.3411 | 0.6204 | 0.3515 |
| 6.0000 | 0.7285 | 0.4865 | 0.5380 | 0.3418 | 0.6960 | 0.3535 |
| 3.0000 | 0.7035 | 0.4408 | 0.5358 | 0.3422 | 0.7308 | 0.3587 |

## Best Router
- Best k by mean source AUC: `5`
- Best k by BankChurn AUC: `5`

## BankChurn External Test
| domain | model | roc_auc | accuracy | precision | recall | f1 | best_threshold | best_accuracy | best_precision | best_recall | best_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BankChurn | Cell2Cell_only_transfer | 0.4198 | 0.5405 | 0.1474 | 0.2629 | 0.1889 | 0.0000 | 0.2035 | 0.2035 | 1.0000 | 0.3382 |
| BankChurn | pooled_global | 0.5588 | 0.3835 | 0.2144 | 0.7617 | 0.3346 | 0.7072 | 0.5425 | 0.2480 | 0.6143 | 0.3534 |
| BankChurn | router_k=5 | 0.5691 | 0.2785 | 0.2103 | 0.9238 | 0.3426 | 0.8143 | 0.4640 | 0.2367 | 0.7346 | 0.3581 |
| BankChurn | bank_in_domain | 0.7620 | 0.6935 | 0.3669 | 0.6978 | 0.4809 | 0.5592 | 0.7500 | 0.4224 | 0.6216 | 0.5030 |

## Concept Coefficients
| concept | coefficient |
| --- | --- |
| tenure | -0.2714 |
| relationship_per_tenure | -0.1747 |
| relationship_depth | 0.1698 |
| partner_flag | -0.0959 |
| change_intensity | 0.0928 |
| activity_volume | -0.0820 |
| activity_per_tenure | -0.0685 |
| pressure_ratio | 0.0637 |
| monetary_volume | -0.0593 |
| monetary_per_tenure | 0.0431 |

## Interpretation
- If the pooled global model already lifts BankChurn above the Cell2Cell-only transfer, the shared concept layer is carrying some signal.
- If the router beats the pooled global model on BankChurn, the concept layer plus domain-aware routing is doing useful work.
- If BankChurn in-domain stays much higher than transfer, the new bank domain still needs its own calibration even after abstraction.