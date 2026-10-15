"""Pure data logic — no Streamlit imports allowed in here."""

import numpy as np
import pandas as pd

LATENCY_THRESHOLD_MS = 120


def add_latency_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with a latency_flag column added."""
    out = df.copy()
    out["latency_flag"] = np.where(
        out["latency_ms"] > LATENCY_THRESHOLD_MS, "Slow", "OK"
    )
    return out
