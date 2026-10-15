"""Loading and caching the monitoring data."""

import pandas as pd
import streamlit as st


@st.cache_data(ttl=10)
def load_summary() -> pd.DataFrame:
    return pd.read_csv("data/model_summary.csv", parse_dates=["date"])


@st.cache_data
def load_daily() -> pd.DataFrame:
    return pd.read_csv("data/metrics_daily.csv", parse_dates=["date"])
