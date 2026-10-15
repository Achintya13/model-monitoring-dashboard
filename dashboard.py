"""Model monitoring dashboard — high and mid level views."""

from monitoring.views import render_model_detail, render_portfolio

import streamlit as st

from monitoring.data import load_daily, load_summary

st.set_page_config(page_title="Model Monitoring", layout="wide")

COLOURS = {
    "Red": "background-color: #d13b3b; color: white",
    "Amber": "background-color: #e0a020; color: black",
    "Green": "background-color: #2e8b47; color: white",
    "Slow": "background-color: #b8860b; color: white",
    "OK": "background-color: #3a6b8a; color: white",
}

summary = load_summary()
daily = load_daily()

if "selected_model" not in st.session_state:
    st.session_state.selected_model = summary["model_id"].iloc[0]

st.title("Model Monitoring")

view = st.sidebar.radio("View", ["Portfolio", "Model detail"])

if view == "Portfolio":
    render_portfolio(summary)
else:
    render_model_detail(summary)
