"""Rendering the dashboard views."""

import streamlit as st

from monitoring.logic import add_latency_flag

COLOURS = {
    "Red": "background-color: #d13b3b; color: white",
    "Amber": "background-color: #e0a020; color: black",
    "Green": "background-color: #2e8b47; color: white",
    "Slow": "background-color: #b8860b; color: white",
    "OK": "background-color: #3a6b8a; color: white",
}


def render_portfolio(summary):
    st.caption(f"{len(summary)} models — as at {summary['date'].max():%d %b %Y}")

    areas = sorted(summary["business_area"].unique())
    statuses = sorted(summary["status"].unique())
    chosen_areas = st.sidebar.multiselect("Business area", areas, default=areas)
    chosen_status = st.sidebar.multiselect("Status", statuses, default=statuses)

    filtered = summary[summary["business_area"].isin(chosen_areas)]
    filtered = filtered[filtered["status"].isin(chosen_status)]
    filtered = add_latency_flag(filtered)

    counts = filtered["status"].value_counts()
    cols = st.columns(4)
    cols[0].metric("Models", len(filtered))
    cols[1].metric("Red", int(counts.get("Red", 0)))
    cols[2].metric("Amber", int(counts.get("Amber", 0)))
    cols[3].metric("Green", int(counts.get("Green", 0)))

    st.subheader("Portfolio status")
    table = filtered[
        [
            "model_id",
            "model_name",
            "business_area",
            "auc",
            "psi",
            "days_since_retrain",
            "status",
            "latency_ms",
            "latency_flag",
        ]
    ].sort_values("status")

    styled = (
        table.style.map(lambda v: COLOURS.get(v, ""), subset=["status"])
        .map(lambda v: COLOURS.get(v, ""), subset=["latency_flag"])
        .format({"auc": "{:.3f}", "psi": "{:.3f}", "latency_ms": "{:.0f}"})
    )

    st.dataframe(styled, use_container_width=True, hide_index=True)

    st.subheader("Drill into a model")
    pick = st.selectbox("Model", filtered["model_id"])
    if st.button("Open model detail"):
        st.session_state.selected_model = pick
        st.rerun()


def render_model_detail(summary, daily):
    ids = list(summary["model_id"])
    current = st.session_state.selected_model
    chosen_id = st.sidebar.selectbox("Model", ids, index=ids.index(current))
    st.session_state.selected_model = chosen_id

    row = summary[summary["model_id"] == chosen_id].iloc[0]
    history = daily[daily["model_id"] == chosen_id].sort_values("date")

    st.subheader(f"{row['model_id']} — {row['model_name']}")
    st.caption(f"{row['business_area']} · owned by {row['owner_team']}")

    cols = st.columns(4)
    cols[0].metric("Status", row["status"])
    cols[1].metric("AUC", f"{row['auc']:.3f}")
    cols[2].metric("PSI", f"{row['psi']:.3f}")
    cols[3].metric("Days since retrain", int(row["days_since_retrain"]))

    window = st.slider("Days of history", 30, len(history), len(history))
    recent = history.tail(window).set_index("date")

    st.subheader("Discrimination (AUC)")
    st.line_chart(recent["auc"])

    st.subheader("Population stability (PSI)")
    st.line_chart(recent["psi"])

    left, right = st.columns(2)
    with left:
        st.subheader("Volume")
        st.bar_chart(recent["volume"])
    with right:
        st.subheader("Latency (ms)")
        st.line_chart(recent["latency_ms"])
