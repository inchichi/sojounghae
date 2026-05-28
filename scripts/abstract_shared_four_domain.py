#!/usr/bin/env python3
"""Four-domain abstract shared experiment with BankChurn as an unseen test set."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data"
RESULTS_ROOT = ROOT / "results"
SEED = 42

FEATURES = [
    "tenure",
    "age",
    "partner_flag",
    "children_flag",
    "relationship_depth",
    "activity_volume",
    "monetary_volume",
    "capacity",
    "pressure_ratio",
    "change_intensity",
    "support_intensity",
    "volume_to_capacity",
    "activity_per_tenure",
    "monetary_per_tenure",
    "support_per_tenure",
    "relationship_per_tenure",
    "support_to_activity",
]

CREDIT_RATING_MAP = {
    "1-Highest": 7.0,
    "2-High": 6.0,
    "3-Good": 5.0,
    "4-Medium": 4.0,
    "5-Low": 3.0,
    "6-VeryLow": 2.0,
    "7-Lowest": 1.0,
}

CONTRACT_MAP = {
    "Month-to-month": 1.0,
    "One year": 2.0,
    "Two year": 3.0,
}


@dataclass
class FitResult:
    name: str
    model: object
    preprocessor_fit: pd.DataFrame


class StandardLogitModel:
    def __init__(self, random_state: int = SEED):
        self.random_state = random_state
        self.imputer = SimpleImputer(strategy="median")
        self.scaler = RobustScaler()
        self.model = LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            solver="liblinear",
            random_state=random_state,
        )

    def fit(
        self,
        X: pd.DataFrame,
        y: np.ndarray,
        sample_weight: np.ndarray | None = None,
        preprocessor_fit: pd.DataFrame | None = None,
    ) -> "StandardLogitModel":
        fit_X = X if preprocessor_fit is None else preprocessor_fit
        self.imputer.fit(fit_X)
        self.scaler.fit(self.imputer.transform(fit_X))
        Xt = self.transform(X)
        self.model.fit(Xt, y, sample_weight=sample_weight)
        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        return self.scaler.transform(self.imputer.transform(X))

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        Xt = self.transform(X)
        return self.model.predict_proba(Xt)[:, 1]

    @property
    def coef_(self) -> np.ndarray:
        return self.model.coef_[0]


class ClusterRouter:
    def __init__(self, n_clusters: int, random_state: int = SEED):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.imputer = SimpleImputer(strategy="median")
        self.scaler = StandardScaler()
        self.kmeans: KMeans | None = None
        self.global_model = StandardLogitModel(random_state=random_state)
        self.experts: list[object] = []

    def fit(
        self,
        X: pd.DataFrame,
        y: np.ndarray,
        preprocessor_fit: pd.DataFrame | None = None,
        cluster_fit: pd.DataFrame | None = None,
        sample_weight: np.ndarray | None = None,
    ) -> "ClusterRouter":
        fit_X = X if preprocessor_fit is None else preprocessor_fit
        self.imputer.fit(fit_X)
        self.scaler.fit(self.imputer.transform(fit_X))

        X_scaled = self.transform(X)
        cluster_source = X if cluster_fit is None else cluster_fit
        cluster_scaled = self.transform(cluster_source)

        self.kmeans = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=20,
        )
        self.kmeans.fit(cluster_scaled)

        self.global_model.fit(X, y, sample_weight=sample_weight, preprocessor_fit=fit_X)

        labels = self.kmeans.predict(X_scaled)
        self.experts = []
        for cluster_id in range(self.n_clusters):
            mask = labels == cluster_id
            if mask.sum() == 0:
                expert = DummyClassifier(strategy="most_frequent")
                expert.fit(X_scaled[:1], y[:1])
            elif np.unique(y[mask]).size < 2:
                expert = DummyClassifier(strategy="constant", constant=int(y[mask][0]))
                expert.fit(X_scaled[mask], y[mask])
            else:
                expert = StandardLogitModel(random_state=self.random_state)
                expert.fit(X.iloc[mask], y[mask], preprocessor_fit=fit_X)
            self.experts.append(expert)
        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        return self.scaler.transform(self.imputer.transform(X))

    def predict_proba(self, X: pd.DataFrame, temperature: float = 1.0) -> np.ndarray:
        if self.kmeans is None:
            raise RuntimeError("Router has not been fit.")
        X_scaled = self.transform(X)
        distances = self.kmeans.transform(X_scaled)
        logits = -distances / max(temperature, 1e-6)
        logits = logits - logits.max(axis=1, keepdims=True)
        weights = np.exp(logits)
        weights = weights / weights.sum(axis=1, keepdims=True)

        expert_probs = []
        for expert in self.experts:
            if hasattr(expert, "predict_proba"):
                probs = expert.predict_proba(X if isinstance(expert, StandardLogitModel) else X_scaled)
                if probs.ndim == 2:
                    probs = probs[:, 1]
            else:
                probs = np.full(X.shape[0], 0.5)
            expert_probs.append(np.asarray(probs, dtype=float))
        expert_probs = np.column_stack(expert_probs)
        mixed = (weights * expert_probs).sum(axis=1)
        return mixed


def lower_str(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower()


def to_num(series: pd.Series) -> np.ndarray:
    return pd.to_numeric(series, errors="coerce").fillna(0.0).to_numpy(dtype=float)


def yes_flag(series: pd.Series) -> np.ndarray:
    return lower_str(series).isin({"yes", "married", "existing customer", "attrited customer"}).to_numpy(dtype=float)


def safe_div(num: Iterable[float], den: Iterable[float]) -> np.ndarray:
    num_arr = np.asarray(num, dtype=float)
    den_arr = np.asarray(den, dtype=float)
    out = np.zeros_like(num_arr, dtype=float)
    mask = np.isfinite(num_arr) & np.isfinite(den_arr) & (den_arr != 0)
    out[mask] = num_arr[mask] / den_arr[mask]
    return out


def build_cell2cell_features(df: pd.DataFrame) -> pd.DataFrame:
    tenure = to_num(df["MonthsInService"])
    age = to_num(df["AgeHH1"])
    partner = yes_flag(df["MaritalStatus"])
    children = yes_flag(df["ChildrenInHH"])
    active_subs = to_num(df["ActiveSubs"])
    unique_subs = to_num(df["UniqueSubs"])
    monthly_minutes = to_num(df["MonthlyMinutes"])
    received_calls = to_num(df["ReceivedCalls"])
    outbound_calls = to_num(df["OutboundCalls"])
    inbound_calls = to_num(df["InboundCalls"])
    monthly_revenue = to_num(df["MonthlyRevenue"])
    total_recurring = to_num(df["TotalRecurringCharge"])
    overage_minutes = to_num(df["OverageMinutes"])
    perc_minutes = to_num(df["PercChangeMinutes"])
    perc_revenues = to_num(df["PercChangeRevenues"])
    customer_care = to_num(df["CustomerCareCalls"])
    retention_calls = to_num(df["RetentionCalls"])
    retention_team = yes_flag(df["MadeCallToRetentionTeam"])
    credit_capacity = np.asarray(
        [CREDIT_RATING_MAP.get(str(v).strip(), 0.0) for v in df["CreditRating"].astype(str)],
        dtype=float,
    )

    relationship_depth = active_subs + unique_subs + partner + children
    activity_volume = monthly_minutes + received_calls + outbound_calls + inbound_calls
    monetary_volume = monthly_revenue + total_recurring
    capacity = credit_capacity
    pressure_ratio = safe_div(overage_minutes, monthly_revenue + 1.0)
    change_intensity = np.abs(perc_minutes) + np.abs(perc_revenues)
    support_intensity = customer_care + retention_calls + retention_team

    return pd.DataFrame(
        {
            "tenure": tenure,
            "age": age,
            "partner_flag": partner,
            "children_flag": children,
            "relationship_depth": relationship_depth,
            "activity_volume": activity_volume,
            "monetary_volume": monetary_volume,
            "capacity": capacity,
            "pressure_ratio": pressure_ratio,
            "change_intensity": change_intensity,
            "support_intensity": support_intensity,
            "volume_to_capacity": safe_div(monetary_volume, capacity + 1.0),
            "activity_per_tenure": safe_div(activity_volume, tenure + 1.0),
            "monetary_per_tenure": safe_div(monetary_volume, tenure + 1.0),
            "support_per_tenure": safe_div(support_intensity, tenure + 1.0),
            "relationship_per_tenure": safe_div(relationship_depth, tenure + 1.0),
            "support_to_activity": safe_div(support_intensity, activity_volume + 1.0),
        }
    )


def build_bankchurners_features(df: pd.DataFrame) -> pd.DataFrame:
    tenure = to_num(df["Months_on_book"])
    age = to_num(df["Customer_Age"])
    partner = lower_str(df["Marital_Status"]).eq("married").to_numpy(dtype=float)
    children = (to_num(df["Dependent_count"]) > 0).astype(float)
    relationship_depth = to_num(df["Total_Relationship_Count"]) + partner + children
    activity_volume = to_num(df["Total_Trans_Ct"])
    monetary_volume = to_num(df["Total_Trans_Amt"])
    capacity = to_num(df["Credit_Limit"])
    pressure_ratio = to_num(df["Avg_Utilization_Ratio"])
    change_intensity = to_num(df["Total_Amt_Chng_Q4_Q1"]) + to_num(df["Total_Ct_Chng_Q4_Q1"])
    support_intensity = to_num(df["Contacts_Count_12_mon"])

    return pd.DataFrame(
        {
            "tenure": tenure,
            "age": age,
            "partner_flag": partner,
            "children_flag": children,
            "relationship_depth": relationship_depth,
            "activity_volume": activity_volume,
            "monetary_volume": monetary_volume,
            "capacity": capacity,
            "pressure_ratio": pressure_ratio,
            "change_intensity": change_intensity,
            "support_intensity": support_intensity,
            "volume_to_capacity": safe_div(monetary_volume, capacity + 1.0),
            "activity_per_tenure": safe_div(activity_volume, tenure + 1.0),
            "monetary_per_tenure": safe_div(monetary_volume, tenure + 1.0),
            "support_per_tenure": safe_div(support_intensity, tenure + 1.0),
            "relationship_per_tenure": safe_div(relationship_depth, tenure + 1.0),
            "support_to_activity": safe_div(support_intensity, activity_volume + 1.0),
        }
    )


def build_ibm_features(df: pd.DataFrame) -> pd.DataFrame:
    tenure = to_num(df["tenure"])
    age = to_num(df["SeniorCitizen"])
    partner = yes_flag(df["Partner"])
    children = yes_flag(df["Dependents"])
    contract_strength = np.asarray(
        [CONTRACT_MAP.get(str(v).strip(), 0.0) for v in df["Contract"].astype(str)],
        dtype=float,
    )
    support_cols = ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport"]
    support_intensity = sum(yes_flag(df[col]) for col in support_cols)
    monthly_charges = to_num(df["MonthlyCharges"])
    total_charges = pd.to_numeric(df["TotalCharges"].astype(str).str.strip(), errors="coerce").fillna(0.0).to_numpy(dtype=float)

    relationship_depth = partner + children + contract_strength
    activity_volume = monthly_charges
    monetary_volume = total_charges
    capacity = contract_strength
    pressure_ratio = safe_div(monthly_charges, tenure + 1.0)
    avg_charges = safe_div(total_charges, tenure + 1.0)
    change_intensity = np.abs(monthly_charges - avg_charges)

    return pd.DataFrame(
        {
            "tenure": tenure,
            "age": age,
            "partner_flag": partner,
            "children_flag": children,
            "relationship_depth": relationship_depth,
            "activity_volume": activity_volume,
            "monetary_volume": monetary_volume,
            "capacity": capacity,
            "pressure_ratio": pressure_ratio,
            "change_intensity": change_intensity,
            "support_intensity": support_intensity,
            "volume_to_capacity": safe_div(monetary_volume, capacity + 1.0),
            "activity_per_tenure": safe_div(activity_volume, tenure + 1.0),
            "monetary_per_tenure": safe_div(monetary_volume, tenure + 1.0),
            "support_per_tenure": safe_div(support_intensity, tenure + 1.0),
            "relationship_per_tenure": safe_div(relationship_depth, tenure + 1.0),
            "support_to_activity": safe_div(support_intensity, activity_volume + 1.0),
        }
    )


def build_bank_features(df: pd.DataFrame) -> pd.DataFrame:
    tenure = to_num(df["Tenure"])
    age = to_num(df["Age"])
    partner = np.zeros(len(df), dtype=float)
    children = np.zeros(len(df), dtype=float)
    relationship_depth = to_num(df["NumOfProducts"])
    activity_volume = to_num(df["NumOfProducts"])
    monetary_volume = to_num(df["Balance"])
    capacity = to_num(df["CreditScore"])
    pressure_ratio = safe_div(monetary_volume, to_num(df["EstimatedSalary"]) + 1.0)
    change_intensity = safe_div(np.abs(monetary_volume - to_num(df["EstimatedSalary"])), to_num(df["EstimatedSalary"]) + 1.0)
    support_intensity = to_num(df["HasCrCard"]) + to_num(df["IsActiveMember"])

    return pd.DataFrame(
        {
            "tenure": tenure,
            "age": age,
            "partner_flag": partner,
            "children_flag": children,
            "relationship_depth": relationship_depth,
            "activity_volume": activity_volume,
            "monetary_volume": monetary_volume,
            "capacity": capacity,
            "pressure_ratio": pressure_ratio,
            "change_intensity": change_intensity,
            "support_intensity": support_intensity,
            "volume_to_capacity": safe_div(monetary_volume, capacity + 1.0),
            "activity_per_tenure": safe_div(activity_volume, tenure + 1.0),
            "monetary_per_tenure": safe_div(monetary_volume, tenure + 1.0),
            "support_per_tenure": safe_div(support_intensity, tenure + 1.0),
            "relationship_per_tenure": safe_div(relationship_depth, tenure + 1.0),
            "support_to_activity": safe_div(support_intensity, activity_volume + 1.0),
        }
    )


def target_cell2cell(df: pd.DataFrame) -> np.ndarray:
    return lower_str(df["Churn"]).eq("yes").to_numpy(dtype=int)


def target_bankchurners(df: pd.DataFrame) -> np.ndarray:
    return lower_str(df["Attrition_Flag"]).eq("attrited customer").to_numpy(dtype=int)


def target_ibm(df: pd.DataFrame) -> np.ndarray:
    return lower_str(df["Churn"]).eq("yes").to_numpy(dtype=int)


def target_bank(df: pd.DataFrame) -> np.ndarray:
    return df["Exited"].astype(int).to_numpy()


def prepare_domain(
    name: str,
    raw_df: pd.DataFrame,
    feature_builder: Callable[[pd.DataFrame], pd.DataFrame],
    target_builder: Callable[[pd.DataFrame], np.ndarray],
    seed: int = SEED,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    y = target_builder(raw_df)
    train_idx, test_idx = train_test_split(
        raw_df.index,
        test_size=0.2,
        random_state=seed,
        stratify=y,
    )
    train_raw = raw_df.loc[train_idx].copy()
    test_raw = raw_df.loc[test_idx].copy()
    train = feature_builder(train_raw)
    test = feature_builder(test_raw)
    train["y"] = target_builder(train_raw)
    test["y"] = target_builder(test_raw)
    train["domain"] = name
    test["domain"] = name
    return train, test


def stratified_sample(frame: pd.DataFrame, max_rows: int, seed: int = SEED) -> pd.DataFrame:
    if len(frame) <= max_rows:
        return frame.copy()
    frac = max_rows / len(frame)
    parts = []
    for _, group in frame.groupby("y"):
        n = max(1, int(round(len(group) * frac)))
        n = min(n, len(group))
        parts.append(group.sample(n=n, random_state=seed))
    sampled = pd.concat(parts, axis=0)
    if len(sampled) > max_rows:
        sampled = sampled.sample(n=max_rows, random_state=seed)
    return sampled


def domain_weights(frames: dict[str, pd.DataFrame]) -> dict[str, float]:
    total = len(frames)
    return {name: 1.0 / total for name in frames}


def make_pooled_frames(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return pd.concat(frames.values(), axis=0, ignore_index=True)


def fit_pooled_model(
    train_frames: dict[str, pd.DataFrame],
    balanced_fit_rows: int = 6000,
) -> tuple[StandardLogitModel, pd.DataFrame]:
    pooled_train = make_pooled_frames(train_frames)
    weights = domain_weights(train_frames)
    sample_weight = pooled_train["domain"].map(weights).to_numpy(dtype=float)
    model = StandardLogitModel(random_state=SEED)
    model.fit(
        pooled_train[FEATURES],
        pooled_train["y"].to_numpy(dtype=int),
        sample_weight=sample_weight,
        preprocessor_fit=pooled_train[FEATURES],
    )
    return model, pooled_train


def fit_cell_only_model(train_frame: pd.DataFrame) -> StandardLogitModel:
    model = StandardLogitModel(random_state=SEED)
    model.fit(
        train_frame[FEATURES],
        train_frame["y"].to_numpy(dtype=int),
        preprocessor_fit=train_frame[FEATURES],
    )
    return model


def fit_bank_in_domain(train_frame: pd.DataFrame) -> StandardLogitModel:
    return fit_cell_only_model(train_frame)


def threshold_metrics(y_true: np.ndarray, probs: np.ndarray, threshold: float) -> dict[str, float]:
    pred = (probs >= threshold).astype(int)
    return {
        "roc_auc": roc_auc_score(y_true, probs),
        "accuracy": accuracy_score(y_true, pred),
        "precision": precision_score(y_true, pred, zero_division=0),
        "recall": recall_score(y_true, pred, zero_division=0),
        "f1": f1_score(y_true, pred, zero_division=0),
    }


def best_threshold(y_true: np.ndarray, probs: np.ndarray) -> tuple[float, float]:
    precision, recall, thresholds = precision_recall_curve(y_true, probs)
    if thresholds.size == 0:
        return 0.5, 0.0
    f1 = (2 * precision[:-1] * recall[:-1]) / np.clip(precision[:-1] + recall[:-1], 1e-12, None)
    best_idx = int(np.argmax(f1))
    return float(thresholds[best_idx]), float(f1[best_idx])


def evaluate_model(y_true: np.ndarray, probs: np.ndarray) -> dict[str, float]:
    default = threshold_metrics(y_true, probs, 0.5)
    thr, best_f1 = best_threshold(y_true, probs)
    best = threshold_metrics(y_true, probs, thr)
    return {
        "roc_auc": default["roc_auc"],
        "accuracy": default["accuracy"],
        "precision": default["precision"],
        "recall": default["recall"],
        "f1": default["f1"],
        "best_threshold": thr,
        "best_accuracy": best["accuracy"],
        "best_precision": best["precision"],
        "best_recall": best["recall"],
        "best_f1": best_f1,
    }


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


def domain_rows(raw: pd.DataFrame, name: str, builder: Callable[[pd.DataFrame], pd.DataFrame]) -> tuple[int, float]:
    y = raw["y"].to_numpy(dtype=int)
    return len(raw), float(y.mean())


def coef_snapshot(model: StandardLogitModel, top_n: int = 10) -> pd.DataFrame:
    coef = model.coef_
    frame = pd.DataFrame({"concept": FEATURES, "coefficient": coef})
    frame["abs_coefficient"] = frame["coefficient"].abs()
    frame = frame.sort_values("abs_coefficient", ascending=False).head(top_n)
    return frame[["concept", "coefficient"]]


def main() -> None:
    cell_raw = pd.read_csv(DATA_ROOT / "raw" / "cell2celltrain.csv")
    bankchurners_raw = pd.read_csv(DATA_ROOT / "external" / "credit_card_churn" / "BankChurners.csv")
    ibm_raw = pd.read_csv(DATA_ROOT / "external" / "ibm_telco" / "Telco-Customer-Churn.csv")
    bank_raw = pd.read_csv(DATA_ROOT / "external" / "bank_customer_churn" / "BankChurn.csv")

    cell_train, cell_test = prepare_domain("Cell2Cell", cell_raw, build_cell2cell_features, target_cell2cell)
    bankchurners_train, bankchurners_test = prepare_domain(
        "BankChurners", bankchurners_raw, build_bankchurners_features, target_bankchurners
    )
    ibm_train, ibm_test = prepare_domain("IBM", ibm_raw, build_ibm_features, target_ibm)
    bank_train, bank_test = prepare_domain("BankChurn", bank_raw, build_bank_features, target_bank)

    source_frames = {
        "Cell2Cell": cell_train,
        "BankChurners": bankchurners_train,
        "IBM": ibm_train,
    }

    pooled_global, pooled_train = fit_pooled_model(source_frames, balanced_fit_rows=5000)

    source_results = []
    for name, test_frame in [
        ("Cell2Cell", cell_test),
        ("BankChurners", bankchurners_test),
        ("IBM", ibm_test),
    ]:
        probs = pooled_global.predict_proba(test_frame[FEATURES])
        result = evaluate_model(test_frame["y"].to_numpy(dtype=int), probs)
        result.update({"domain": name, "model": "pooled_global"})
        source_results.append(result)

    # Router sweep
    router_results = []
    bank_transfer_sweeps = []
    router_candidates: dict[int, ClusterRouter] = {}

    for k in range(2, 7):
        router = ClusterRouter(n_clusters=k, random_state=SEED)
        router.fit(
            pooled_train[FEATURES],
            pooled_train["y"].to_numpy(dtype=int),
            preprocessor_fit=pooled_train[FEATURES],
            cluster_fit=pooled_train[FEATURES],
            sample_weight=pooled_train["domain"].map(domain_weights(source_frames)).to_numpy(dtype=float),
        )
        router_candidates[k] = router

        src_metrics = []
        for name, test_frame in [
            ("Cell2Cell", cell_test),
            ("BankChurners", bankchurners_test),
            ("IBM", ibm_test),
        ]:
            probs = router.predict_proba(test_frame[FEATURES])
            result = evaluate_model(test_frame["y"].to_numpy(dtype=int), probs)
            result.update({"domain": name, "model": f"router_k={k}"})
            router_results.append(result)
            src_metrics.append((result["roc_auc"], result["f1"]))

        mean_auc = float(np.mean([m[0] for m in src_metrics]))
        mean_f1 = float(np.mean([m[1] for m in src_metrics]))
        bank_probs = router.predict_proba(bank_test[FEATURES])
        bank_eval = evaluate_model(bank_test["y"].to_numpy(dtype=int), bank_probs)
        bank_transfer_sweeps.append(
            {
                "k": k,
                "mean_source_auc": mean_auc,
                "mean_source_f1": mean_f1,
                "bank_auc": bank_eval["roc_auc"],
                "bank_f1": bank_eval["f1"],
                "bank_best_threshold": bank_eval["best_threshold"],
                "bank_best_f1": bank_eval["best_f1"],
            }
        )

    bank_transfer_df = pd.DataFrame(bank_transfer_sweeps)
    best_k_source = int(bank_transfer_df.sort_values(["mean_source_auc", "bank_auc"], ascending=False).iloc[0]["k"])
    best_k_bank = int(bank_transfer_df.sort_values(["bank_auc", "mean_source_auc"], ascending=False).iloc[0]["k"])
    best_router = router_candidates[best_k_bank]

    bank_only_transfer = fit_cell_only_model(cell_train)
    bank_only_probs = bank_only_transfer.predict_proba(bank_test[FEATURES])
    bank_only_eval = evaluate_model(bank_test["y"].to_numpy(dtype=int), bank_only_probs)

    bank_in_domain = fit_bank_in_domain(bank_train)
    bank_in_probs = bank_in_domain.predict_proba(bank_test[FEATURES])
    bank_in_eval = evaluate_model(bank_test["y"].to_numpy(dtype=int), bank_in_probs)

    pooled_bank_probs = pooled_global.predict_proba(bank_test[FEATURES])
    pooled_bank_eval = evaluate_model(bank_test["y"].to_numpy(dtype=int), pooled_bank_probs)
    router_bank_probs = best_router.predict_proba(bank_test[FEATURES])
    router_bank_eval = evaluate_model(bank_test["y"].to_numpy(dtype=int), router_bank_probs)

    source_only_bank_result = {
        "domain": "BankChurn",
        "model": "Cell2Cell_only_transfer",
        **bank_only_eval,
    }
    pooled_bank_result = {
        "domain": "BankChurn",
        "model": "pooled_global",
        **pooled_bank_eval,
    }
    router_bank_result = {
        "domain": "BankChurn",
        "model": f"router_k={best_k_bank}",
        **router_bank_eval,
    }
    in_domain_bank_result = {
        "domain": "BankChurn",
        "model": "bank_in_domain",
        **bank_in_eval,
    }

    source_df = pd.DataFrame(source_results + router_results)
    bank_df = pd.DataFrame(
        [
            source_only_bank_result,
            pooled_bank_result,
            router_bank_result,
            in_domain_bank_result,
        ]
    )
    coef_df = coef_snapshot(pooled_global, top_n=10)

    concept_mapping = pd.DataFrame(
        [
            {
                "concept": "tenure",
                "Cell2Cell": "MonthsInService",
                "BankChurners": "Months_on_book",
                "IBM": "tenure",
                "BankChurn": "Tenure",
            },
            {
                "concept": "age",
                "Cell2Cell": "AgeHH1",
                "BankChurners": "Customer_Age",
                "IBM": "SeniorCitizen",
                "BankChurn": "Age",
            },
            {
                "concept": "partner_flag",
                "Cell2Cell": "MaritalStatus == Yes",
                "BankChurners": "Marital_Status == Married",
                "IBM": "Partner == Yes",
                "BankChurn": "(missing -> 0)",
            },
            {
                "concept": "children_flag",
                "Cell2Cell": "ChildrenInHH == Yes",
                "BankChurners": "Dependent_count > 0",
                "IBM": "Dependents == Yes",
                "BankChurn": "(missing -> 0)",
            },
            {
                "concept": "relationship_depth",
                "Cell2Cell": "ActiveSubs + UniqueSubs + partner + children",
                "BankChurners": "Total_Relationship_Count + partner + children",
                "IBM": "partner + children + contract_strength",
                "BankChurn": "NumOfProducts",
            },
            {
                "concept": "activity_volume",
                "Cell2Cell": "MonthlyMinutes + received/outbound/inbound calls",
                "BankChurners": "Total_Trans_Ct",
                "IBM": "MonthlyCharges",
                "BankChurn": "NumOfProducts",
            },
            {
                "concept": "monetary_volume",
                "Cell2Cell": "MonthlyRevenue + TotalRecurringCharge",
                "BankChurners": "Total_Trans_Amt",
                "IBM": "TotalCharges",
                "BankChurn": "Balance",
            },
            {
                "concept": "capacity",
                "Cell2Cell": "CreditRating (inverse ordinal)",
                "BankChurners": "Credit_Limit",
                "IBM": "Contract strength ordinal",
                "BankChurn": "CreditScore",
            },
            {
                "concept": "pressure_ratio",
                "Cell2Cell": "OverageMinutes / MonthlyRevenue",
                "BankChurners": "Avg_Utilization_Ratio",
                "IBM": "MonthlyCharges / tenure",
                "BankChurn": "Balance / EstimatedSalary",
            },
            {
                "concept": "change_intensity",
                "Cell2Cell": "PercChangeMinutes + PercChangeRevenues",
                "BankChurners": "Amt change + count change",
                "IBM": "abs(MonthlyCharges - avg_monthly_charges)",
                "BankChurn": "abs(Balance - EstimatedSalary) / EstimatedSalary",
            },
            {
                "concept": "support_intensity",
                "Cell2Cell": "CustomerCareCalls + RetentionCalls + MadeCallToRetentionTeam",
                "BankChurners": "Contacts_Count_12_mon",
                "IBM": "support add-on count",
                "BankChurn": "HasCrCard + IsActiveMember",
            },
        ]
    )

    out_path = RESULTS_ROOT / "abstract_shared_four_domain_bank_results_v2.md"
    RESULT_LINES = []
    RESULT_LINES.append("# Abstract Shared Four-Domain Results")
    RESULT_LINES.append("")
    RESULT_LINES.append("## Goal")
    RESULT_LINES.append("- Fix `abstract_shared` as the common concept layer.")
    RESULT_LINES.append("- Train on pooled `Cell2Cell + BankChurners + IBM` source domains.")
    RESULT_LINES.append("- Test transfer on the unused `BankChurn` domain.")
    RESULT_LINES.append("- Use a cluster-router mixture of experts instead of one global model.")
    RESULT_LINES.append("")
    RESULT_LINES.append("## Concept Mapping")
    RESULT_LINES.append(render_table(concept_mapping))
    RESULT_LINES.append("")
    RESULT_LINES.append("## Dataset Splits")
    split_rows = []
    for name, frame in [
        ("Cell2Cell", cell_train),
        ("BankChurners", bankchurners_train),
        ("IBM", ibm_train),
        ("BankChurn", bank_train),
    ]:
        split_rows.append(
            {
                "split": f"{name} train",
                "rows": len(frame),
                "churn_rate": float(frame["y"].mean()),
            }
        )
    for name, frame in [
        ("Cell2Cell", cell_test),
        ("BankChurners", bankchurners_test),
        ("IBM", ibm_test),
        ("BankChurn", bank_test),
    ]:
        split_rows.append(
            {
                "split": f"{name} holdout",
                "rows": len(frame),
                "churn_rate": float(frame["y"].mean()),
            }
        )
    RESULT_LINES.append(render_table(pd.DataFrame(split_rows)))
    RESULT_LINES.append("")
    RESULT_LINES.append("## Source Holdout Results")
    RESULT_LINES.append(render_table(source_df))
    RESULT_LINES.append("")
    RESULT_LINES.append("## Router k Sweep")
    RESULT_LINES.append(render_table(bank_transfer_df.sort_values(["bank_auc", "mean_source_auc"], ascending=False)))
    RESULT_LINES.append("")
    RESULT_LINES.append(f"## Best Router")
    RESULT_LINES.append(f"- Best k by mean source AUC: `{best_k_source}`")
    RESULT_LINES.append(f"- Best k by BankChurn AUC: `{best_k_bank}`")
    RESULT_LINES.append("")
    RESULT_LINES.append("## BankChurn External Test")
    RESULT_LINES.append(render_table(bank_df))
    RESULT_LINES.append("")
    RESULT_LINES.append("## Concept Coefficients")
    RESULT_LINES.append(render_table(coef_df))
    RESULT_LINES.append("")
    RESULT_LINES.append("## Interpretation")
    RESULT_LINES.append(
        "- If the pooled global model already lifts BankChurn above the Cell2Cell-only transfer, the shared concept layer is carrying some signal."
    )
    RESULT_LINES.append(
        "- If the router beats the pooled global model on BankChurn, the concept layer plus domain-aware routing is doing useful work."
    )
    RESULT_LINES.append(
        "- If BankChurn in-domain stays much higher than transfer, the new bank domain still needs its own calibration even after abstraction."
    )
    out_path.write_text("\n".join(RESULT_LINES), encoding="utf-8")

    print(f"Wrote {out_path}")
    print(f"Best router k by source AUC: {best_k_source}")
    print(f"Best router k by BankChurn AUC: {best_k_bank}")
    print(bank_df.to_string(index=False))


if __name__ == "__main__":
    main()
