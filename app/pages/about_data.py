import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from pathlib import Path

st.header("About the Data")
st.markdown(
    "For our project, we used available datasets from the Federal Statistic Office Switzerland.")

HERE = Path(__file__).resolve().parent          # = app/pages
DATA_PATH = HERE.parent / "data" / "df_health.xlsx"  # = app/data/df_health.xlsx

df_health = pd.read_excel(DATA_PATH, na_values=["x"])
st.title("Swiss Hospital Data over the last decade")
st.dataframe(df_health)
