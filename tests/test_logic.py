"""Tests for pure data logic."""

import pandas as pd

from monitoring.logic import add_latency_flag


def test_flags_slow_models():
    df = pd.DataFrame({"latency_ms": [150.0]})
    result = add_latency_flag(df)
    assert result["latency_flag"].iloc[0] == "Slow"


def test_flags_fast_models():
    df = pd.DataFrame({"latency_ms": [80.0]})
    result = add_latency_flag(df)
    assert result["latency_flag"].iloc[0] == "OK"


def test_boundary_is_not_slow():
    df = pd.DataFrame({"latency_ms": [120.0]})
    result = add_latency_flag(df)
    assert result["latency_flag"].iloc[0] == "OK"


def test_does_not_mutate_input():
    df = pd.DataFrame({"latency_ms": [150.0]})
    add_latency_flag(df)
    assert "latency_flag" not in df.columns
