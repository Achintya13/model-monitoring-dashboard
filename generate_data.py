
"""Generate synthetic model monitoring data."""

from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

MODELS = [
    ("CR001", "Retail Credit Scorecard", "Retail Banking", "Risk"),
    ("CR002", "SME Default PD", "Business Banking", "Risk"),
    ("FR001", "Card Fraud Detection", "Payments", "Financial Crime"),
    ("FR002", "AML Transaction Monitor", "Payments", "Financial Crime"),
    ("MK001", "Churn Propensity", "Wealth", "Marketing"),
    ("MK002", "Next Best Product", "Wealth", "Marketing"),
    ("OP001", "Complaint Volume Forecast", "Operations", "COO"),
    ("OP002", "Branch Footfall", "Operations", "COO"),
]

DAYS = 120


def build_daily_metrics() -> pd.DataFrame:
    """One row per model per day, with some models drifting on purpose."""
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=DAYS)
    rows = []

    for model_id, _, _, _ in MODELS:
        base_auc = rng.uniform(0.72, 0.88)
        drift_rate = rng.choice([0.0, 0.0, 0.0002, 0.0008])

        for day_index, date in enumerate(dates):
            decay = drift_rate * day_index
            rows.append(
                {
                    "model_id": model_id,
                    "date": date,
                    "auc": base_auc - decay + rng.normal(0, 0.008),
                    "psi": abs(rng.normal(0.05 + decay * 20, 0.02)),
                    "volume": int(rng.normal(50_000, 6_000)),
                    "latency_ms": abs(rng.normal(85, 20)),
                    "null_rate": abs(rng.normal(0.01, 0.004)),
                }
            )

    return pd.DataFrame(rows)


def classify(row: pd.Series) -> str:
    """Simple RAG rules — red beats amber beats green."""
    if row["psi"] > 0.6 or row["auc"] < 0.70 or row["days_since_retrain"] > 365:
        return "Red"
    if row["psi"] > 0.10 or row["auc"] < 0.75 or row["days_since_retrain"] > 180:
        return "Amber"
    return "Green"


def build_model_summary(daily: pd.DataFrame) -> pd.DataFrame:
    """Latest snapshot per model, plus a RAG status."""
    catalogue = pd.DataFrame(
        MODELS, columns=["model_id", "model_name", "business_area", "owner_team"]
    )

    latest = daily.sort_values("date").groupby("model_id").last().reset_index()
    summary = catalogue.merge(latest, on="model_id")

    summary["days_since_retrain"] = rng.integers(5, 400, size=len(summary))
    summary["status"] = summary.apply(classify, axis=1)

    return summary


if __name__ == "__main__":
    Path("data").mkdir(exist_ok=True)

    daily = build_daily_metrics()
    summary = build_model_summary(daily)

    daily.to_csv("data/metrics_daily.csv", index=False)
    summary.to_csv("data/model_summary.csv", index=False)

    print(f"Wrote {len(daily)} daily rows and {len(summary)} models.")
