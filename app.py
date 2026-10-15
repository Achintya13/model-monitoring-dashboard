import pandas as pd
import streamlit as st

st.title("Hello from Python")

name = st.text_input("Your name", "Python")
st.write(f"Hello, {name}")

df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
st.dataframe(df)
st.line_chart(df, x="x", y="y")
