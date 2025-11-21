import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from pathlib import Path

st.title("About the Data")
st.markdown(
    "For our project, we used available datasets from the Federal Statistic Office Switzerland.")

HERE = Path(__file__).resolve().parent  # path to app/pages
DATA_PATH = HERE.parent / "data" / "df_health.xlsx"  # path to app/data/df_health
df_health = pd.read_excel(DATA_PATH, na_values=["x"])

# displaying the data
# using placeholders because we want the table to be above the filters
title_placeholder = st.empty()
table_placeholder = st.empty()

# adding a filter for years and regions
st.subheader("Filter the data")
years = st.multiselect("Select years", sorted(
    df_health["Year"].unique()), default=sorted(df_health["Year"].unique()))
regions = st.multiselect("Select regions", sorted(
    df_health["Region"].unique()), default=sorted(df_health["Region"].unique()))

# adding a filter, which columns should be displayed
categories = st.multiselect(
    "Select columns", df_health.columns, default=df_health.columns)
df_health = df_health[df_health["Year"].isin(
    years) & df_health["Region"].isin(regions)][categories]


title_placeholder.header("Swiss Hospital Data over the last decade")
table_placeholder.dataframe(df_health)
