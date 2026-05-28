#!/usr/bin/env python3
"""Build a concise dashboard of the main churn experiments.

The dashboard is a curated summary of representative milestones, not a full
dump of every parameter sweep in the repository.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
RESULTS = ROOT / "results"

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update(
    {
        "figure.dpi": 160,
        "savefig.dpi": 160,
        "axes.titlesize": 12,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
    }
)


def render_table(df: pd.DataFrame, float_fmt: str = "{:.4f}") -> str:
    def fmt(value: object) -> str:
        if isinstance(value, (float, np.floating)):
            return float_fmt.format(float(value))
        if isinstance(value, (int, np.integer)):
            return str(int(value))
        return str(value)

    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |"]
    lines.append("| " + " | ".join(["---"] * len(cols)) + " |")
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(fmt(row[c]) for c in cols) + " |")
    return "\n".join(lines)


def grouped_bar(ax, df: pd.DataFrame, title: str, value_cols: tuple[str, str] = ("roc_auc", "f1")) -> None:
    x = np.arange(len(df))
    width = 0.36
    colors = ["#4C78A8", "#F58518"]
    bars1 = ax.bar(x - width / 2, df[value_cols[0]], width, label=value_cols[0].upper(), color=colors[0])
    bars2 = ax.bar(x + width / 2, df[value_cols[1]], width, label=value_cols[1].upper(), color=colors[1])

    ax.set_title(title)
    ax.set_ylim(0, 1.05)
    ax.set_xticks(x)
    ax.set_xticklabels(df["label"], rotation=20, ha="right")
    ax.set_ylabel("Score")
    ax.legend(frameon=False, ncol=2, loc="upper left")
    ax.bar_label(bars1, fmt="%.3f", padding=2, fontsize=8)
    ax.bar_label(bars2, fmt="%.3f", padding=2, fontsize=8)


def save_figure(path: Path, fig: plt.Figure) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def build_data() -> dict[str, pd.DataFrame]:
    internal_family = pd.DataFrame(
        [
            {"label": "LogReg", "roc_auc": 0.6084, "f1": 0.4464},
            {"label": "RF", "roc_auc": 0.6676, "f1": 0.1843},
            {"label": "XGB", "roc_auc": 0.6820, "f1": 0.4955},
            {"label": "Tuned XGB", "roc_auc": 0.6805, "f1": 0.5070},
        ]
    )

    internal_xgb = pd.DataFrame(
        [
            {"label": "Baseline", "roc_auc": 0.6820, "f1": 0.4955},
            {"label": "Engineered", "roc_auc": 0.6794, "f1": 0.4917},
            {"label": "Selected", "roc_auc": 0.6741, "f1": 0.4931},
            {"label": "No CED", "roc_auc": 0.6763, "f1": 0.4881},
            {"label": "Tuned", "roc_auc": 0.6805, "f1": 0.5070},
        ]
    )

    bankchurners_transfer = pd.DataFrame(
        [
            {"label": "Full", "roc_auc": 0.5732, "f1": 0.2926},
            {"label": "Portable", "roc_auc": 0.5663, "f1": 0.2764},
            {"label": "Abstract", "roc_auc": 0.6031, "f1": 0.2869},
        ]
    )

    ibm_transfer = pd.DataFrame(
        [
            {"label": "billing2+CORAL", "roc_auc": 0.6885, "f1": 0.4813},
            {"label": "Abstract+CORAL", "roc_auc": 0.5496, "f1": 0.3421},
            {"label": "core5", "roc_auc": 0.3425, "f1": 0.1187},
        ]
    )

    bankchurn_stress = pd.DataFrame(
        [
            {"label": "Cell2Cell only", "roc_auc": 0.5319, "f1": 0.0526},
            {"label": "Pooled global", "roc_auc": 0.4608, "f1": 0.2427},
            {"label": "Router k=6", "roc_auc": 0.5429, "f1": 0.3308},
            {"label": "Bank in-domain", "roc_auc": 0.7564, "f1": 0.4809},
        ]
    )

    bankchurn_retest = pd.DataFrame(
        [
            {"label": "Cell2Cell only", "roc_auc": 0.4198, "f1": 0.1889},
            {"label": "Pooled global", "roc_auc": 0.5588, "f1": 0.3346},
            {"label": "Router k=5", "roc_auc": 0.5691, "f1": 0.3426},
            {"label": "Bank in-domain", "roc_auc": 0.7620, "f1": 0.4809},
        ]
    )

    tri_domain = pd.DataFrame(
        [
            {"label": "Pooled", "roc_auc": 0.8232, "f1": 0.6448},
            {"label": "Router k=2", "roc_auc": 0.8232, "f1": 0.6448},
            {"label": "Top-k", "roc_auc": 0.8186, "f1": 0.6359},
        ]
    )

    pooled_2domain = pd.DataFrame(
        [
            {"label": "Pooled raw mean", "roc_auc": 0.8165, "f1": 0.6695},
            {"label": "Pooled rank mean", "roc_auc": 0.8164, "f1": 0.6727},
        ]
    )

    return {
        "internal_family": internal_family,
        "internal_xgb": internal_xgb,
        "bankchurners_transfer": bankchurners_transfer,
        "ibm_transfer": ibm_transfer,
        "bankchurn_stress": bankchurn_stress,
        "bankchurn_retest": bankchurn_retest,
        "tri_domain": tri_domain,
        "pooled_2domain": pooled_2domain,
    }


def plot_internal(data: dict[str, pd.DataFrame]) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8))
    grouped_bar(axes[0], data["internal_family"], "Cell2Cell: model family comparison")
    grouped_bar(axes[1], data["internal_xgb"], "Cell2Cell: XGB stage progression")
    path = FIGURES / "experiment_dashboard_internal.png"
    save_figure(path, fig)
    return path


def plot_transfer(data: dict[str, pd.DataFrame]) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.8))
    grouped_bar(axes[0], data["bankchurners_transfer"], "Cell2Cell -> BankChurners")
    grouped_bar(axes[1], data["ibm_transfer"], "Cell2Cell -> IBM")
    path = FIGURES / "experiment_dashboard_transfer.png"
    save_figure(path, fig)
    return path


def plot_multisource(data: dict[str, pd.DataFrame]) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.8))
    grouped_bar(axes[0], data["pooled_2domain"], "2-domain pooled abstract_shared (mean)")
    grouped_bar(axes[1], data["tri_domain"], "3-domain pooled / routing")
    path = FIGURES / "experiment_dashboard_multisource.png"
    save_figure(path, fig)
    return path


def plot_bankchurn(data: dict[str, pd.DataFrame]) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.8))
    grouped_bar(axes[0], data["bankchurn_stress"], "BankChurn stress test")
    grouped_bar(axes[1], data["bankchurn_retest"], "BankChurn retest after concept redefinition")
    path = FIGURES / "experiment_dashboard_bankchurn.png"
    save_figure(path, fig)
    return path


def write_report(data: dict[str, pd.DataFrame], figure_paths: dict[str, Path]) -> Path:
    def report_rel(path: Path) -> str:
        return Path("..") / path.relative_to(ROOT)

    summary = pd.DataFrame(
        [
            {
                "phase": "Cell2Cell internal",
                "best setup": "Tuned XGBoost",
                "roc_auc": 0.6805,
                "f1": 0.5070,
                "message": "내부 기준선은 유지 기간/사용량 중심의 tuned XGBoost가 가장 안정적.",
            },
            {
                "phase": "Cell2Cell -> BankChurners",
                "best setup": "abstract_shared raw",
                "roc_auc": 0.6031,
                "f1": 0.2869,
                "message": "추상 개념층이 portable schema보다 전이를 더 잘 살렸다.",
            },
            {
                "phase": "Cell2Cell -> IBM",
                "best setup": "billing2 + CORAL",
                "roc_auc": 0.6885,
                "f1": 0.4813,
                "message": "IBM에는 billing 중심 축이 아직 가장 강했다.",
            },
            {
                "phase": "BankChurn stress v1",
                "best setup": "Router k=6",
                "roc_auc": 0.5429,
                "f1": 0.3308,
                "message": "새 은행 도메인은 꽤 거칠어서 routing만으로도 개선이 제한적이었다.",
            },
            {
                "phase": "BankChurn retest v2",
                "best setup": "Router k=5",
                "roc_auc": 0.5691,
                "f1": 0.3426,
                "message": "BankChurn 개념 재정의 후 pooled global과 router가 모두 개선됐다.",
            },
            {
                "phase": "3-domain pooled",
                "best setup": "Router k=2",
                "roc_auc": 0.8232,
                "f1": 0.6448,
                "message": "도메인-aware pooled training이 전체 평균 성능을 가장 안정적으로 유지했다.",
            },
        ]
    )

    internal_detail = pd.DataFrame(
        [
            {"model": "Logistic Regression", "roc_auc": 0.6084, "accuracy": 0.5848, "precision": 0.3625, "recall": 0.5809, "f1": 0.4464},
            {"model": "Random Forest", "roc_auc": 0.6676, "accuracy": 0.7200, "precision": 0.5737, "recall": 0.1098, "f1": 0.1843},
            {"model": "XGBoost", "roc_auc": 0.6820, "accuracy": 0.6309, "precision": 0.4087, "recall": 0.6292, "f1": 0.4955},
            {"model": "Engineered XGB", "roc_auc": 0.6794, "accuracy": 0.6305, "precision": 0.4073, "recall": 0.6203, "f1": 0.4917},
            {"model": "Selected XGB", "roc_auc": 0.6741, "accuracy": 0.6248, "precision": 0.4037, "recall": 0.6332, "f1": 0.4931},
            {"model": "No CurrentEquipmentDays", "roc_auc": 0.6763, "accuracy": 0.6347, "precision": 0.4093, "recall": 0.6044, "f1": 0.4881},
            {"model": "Tuned XGB", "roc_auc": 0.6805, "accuracy": 0.5897, "precision": 0.3878, "recall": 0.7322, "f1": 0.5070},
        ]
    )

    transfer_detail = pd.DataFrame(
        [
            {"task": "Cell2Cell -> BankChurners", "setup": "Full model", "roc_auc": 0.5732, "f1": 0.2926},
            {"task": "Cell2Cell -> BankChurners", "setup": "Portable model", "roc_auc": 0.5663, "f1": 0.2764},
            {"task": "Cell2Cell -> BankChurners", "setup": "abstract_shared raw", "roc_auc": 0.6031, "f1": 0.2869},
            {"task": "Cell2Cell -> IBM", "setup": "billing2 + CORAL", "roc_auc": 0.6885, "f1": 0.4813},
            {"task": "Cell2Cell -> IBM", "setup": "abstract_shared + CORAL", "roc_auc": 0.5496, "f1": 0.3421},
            {"task": "Cell2Cell -> IBM", "setup": "core5", "roc_auc": 0.3425, "f1": 0.1187},
        ]
    )

    multisource_detail = pd.DataFrame(
        [
            {"setting": "2-domain pooled", "setup": "Pooled raw mean", "roc_auc": 0.8165, "f1": 0.6695},
            {"setting": "2-domain pooled", "setup": "Pooled rank mean", "roc_auc": 0.8164, "f1": 0.6727},
            {"setting": "3-domain pooled", "setup": "Router k=2", "roc_auc": 0.8232, "f1": 0.6448},
            {"setting": "3-domain pooled", "setup": "Top-k gating", "roc_auc": 0.8186, "f1": 0.6359},
        ]
    )

    bank_detail = pd.DataFrame(
        [
            {"setting": "Original stress", "setup": "Cell2Cell only", "roc_auc": 0.5319, "f1": 0.0526},
            {"setting": "Original stress", "setup": "Pooled global", "roc_auc": 0.4608, "f1": 0.2427},
            {"setting": "Original stress", "setup": "Router k=6", "roc_auc": 0.5429, "f1": 0.3308},
            {"setting": "Original stress", "setup": "Bank in-domain", "roc_auc": 0.7564, "f1": 0.4809},
            {"setting": "Retest v2", "setup": "Cell2Cell only", "roc_auc": 0.4198, "f1": 0.1889},
            {"setting": "Retest v2", "setup": "Pooled global", "roc_auc": 0.5588, "f1": 0.3346},
            {"setting": "Retest v2", "setup": "Router k=5", "roc_auc": 0.5691, "f1": 0.3426},
            {"setting": "Retest v2", "setup": "Bank in-domain", "roc_auc": 0.7620, "f1": 0.4809},
        ]
    )

    report_lines: list[str] = []
    report_lines.append("# Experiment Dashboard")
    report_lines.append("")
    report_lines.append("이 문서는 지금까지의 대표 실험을 보기 쉽게 정리한 대시보드다. 모든 파라미터 탐색을 전부 나열한 것은 아니고, 흐름을 설명하는 데 중요한 대표 결과만 골랐다.")
    report_lines.append("")
    report_lines.append("## 1. 한눈에 보는 대표 결과")
    report_lines.append(render_table(summary))
    report_lines.append("")
    report_lines.append("## 2. Cell2Cell 내부 성능 진화")
    report_lines.append(render_table(internal_detail))
    report_lines.append("")
    report_lines.append(f"![Cell2Cell internal]({report_rel(figure_paths['internal']).as_posix()})")
    report_lines.append("")
    report_lines.append("## 3. 외부 전이 요약")
    report_lines.append(render_table(transfer_detail))
    report_lines.append("")
    report_lines.append(f"![Cross-domain transfer]({report_rel(figure_paths['transfer']).as_posix()})")
    report_lines.append("")
    report_lines.append("## 4. 다도메인 공동학습")
    report_lines.append(render_table(multisource_detail))
    report_lines.append("")
    report_lines.append("2-domain pooled는 두 홀드아웃의 평균값으로, 3-domain pooled는 대표 mean AUC/F1를 그대로 적었다.")
    report_lines.append("")
    report_lines.append(f"![Multisource]({report_rel(figure_paths['multisource']).as_posix()})")
    report_lines.append("")
    report_lines.append("## 5. BankChurn 스트레스 테스트")
    report_lines.append(render_table(bank_detail))
    report_lines.append("")
    report_lines.append(f"![BankChurn stress]({report_rel(figure_paths['bank']).as_posix()})")
    report_lines.append("")
    report_lines.append("## 읽는 법")
    report_lines.append("- AUC는 순위 분리력, F1은 실제 0/1 판정 품질을 본다.")
    report_lines.append("- 외부 전이에서는 AUC가 0.5를 넘는지, 그리고 threshold를 다시 잡았을 때 F1이 얼마나 회복되는지가 중요하다.")
    report_lines.append("- BankChurn은 unseen target이라, pooled global과 router가 올라가도 in-domain보다 낮다면 아직 정렬이 덜 된 것이다.")

    path = RESULTS / "experiment_dashboard.md"
    path.write_text("\n".join(report_lines), encoding="utf-8")
    return path


def main() -> None:
    data = build_data()
    figure_paths = {
        "internal": plot_internal(data),
        "transfer": plot_transfer(data),
        "multisource": plot_multisource(data),
        "bank": plot_bankchurn(data),
    }
    report_path = write_report(data, figure_paths)
    print(f"Wrote {report_path}")
    for key, value in figure_paths.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
