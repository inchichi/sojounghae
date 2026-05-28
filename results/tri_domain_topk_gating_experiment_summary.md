# Tri-domain top-k gating experiment summary

| variant | best_router_k | best_router_mean_auc | best_router_mean_f1 | best_topk_k | best_topk_gate_k | best_topk_mean_auc | best_topk_mean_f1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| with_tenure | 2 | 0.8232 | 0.6448 | 2 | 2 | 0.8186 | 0.6359 |
| no_tenure | 2 | 0.8132 | 0.6343 | 2 | 2 | 0.8091 | 0.6357 |

## Interpretation

- Top-k gating did not beat hard router in either variant.
- The weights were not fully sharp, but the clusters were already sufficiently separable that blending multiple experts did not help.
- The best top-k setting was still `k=2, gate_k=2`, which is effectively a soft two-expert mixture rather than a broad universal gate.
