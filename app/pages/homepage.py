import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
# content

st.title("Switzerland's Hospital System: Between Performance and Bottleneck.")
st.subheader("Discover how Swiss hospitals have evolved over the past decade — where resources are optimally used, where inefficiencies occur, and how data-driven planning can shape the future of healthcare.")
st.markdown("This dashboard provides an analytical view of the Swiss hospital landscape.  It highlights efficiency trends, capacity imbalances, and regional differences —  helping healthcare planners make better, data-driven decisions for the future")
st.set_page_config(
    page_title="Swiss Hospital Dashboard",
    page_icon="🏥",
    layout="wide")

# BI-Diagram Dashboard

HERE = Path(__file__).resolve().parent
DATA_PATH = HERE.parent / "data" / "bi_diagramm_data.xlsx"

df_sim = pd.read_excel(DATA_PATH, na_values=["x"])
st.title("Swiss Hospital Data")
st.subheader("Data Overview")

# st.dataframe(df_sim)

# KPI Dashboard


# verfügbare Jahre (sortiert)
years = sorted(df_sim["Year"].unique())
# Standard: letztes Jahr (also das aktuellste)
default_year_index = len(years) - 1

selected_year = st.selectbox(
    "Select year",
    years,
    index=default_year_index)

# verfügbare Monate für das ausgewählte Jahr
month_options = df_sim[df_sim["Year"] == selected_year]["Month"].unique()

selected_month = st.selectbox(
    "Select month",
    month_options)

# Zeile für ausgewählte Kombination Jahr + Monat holen
selected_row = df_sim[
    (df_sim["Year"] == selected_year) &
    (df_sim["Month"] == selected_month)].iloc[0]

# KPI Calculation

st.subheader(f"Key Figures {selected_month} {selected_year}")
# Total Patients
total_patients = int(selected_row["Total Patient"])

# Total Staff
total_staff = int(
    selected_row[["Nurses", "Doctors", "MedTech", "Cleaning"]].sum())

# Total Cost
total_cost = float(selected_row["Treatment Cost"])

# Average Treatment Cost

avg_treat_cost = round(total_cost / total_patients, 2)


def metric_chart(label: str, value):
    """Creates a KPI metric box wrapped in a bordered container."""
    with st.container(border=True):
        st.metric(label=label, value=f"{value:,}")

# Illustration


col1, col2, col3 = st.columns((3, 3, 3), gap="medium")

with col1:
    metric_chart(
        f"Total Patient {selected_month} {selected_year}",
        total_patients)

with col2:
    metric_chart(
        f"Total Staff {selected_month} {selected_year}",
        total_staff)

with col3:
    metric_chart(
        f"Avg. Treatment Cost per Patient ({selected_month} {selected_year})",
        avg_treat_cost)


# Pie Diagram

# row_pie = df_sim[(df_sim["Year"] == 2025) & (
    # df_sim["Month"] == "November")].iloc[0]
# diet_values = row_pie[["Raw_diet", "Soft_diet",
    # "Normal_diet", "Diabetic_diet", "Vegetarian/Vegan"]]

# fig, ax = plt.subplots(figsize=(2, 2), dpi=200)   # scharf + klein

# diet_values.plot.pie(
    # autopct="%1.1f%%",
   # ylabel="",
    # ax=ax,
   # textprops={'fontsize': 3}
# )

# ax.set_title("Diet Distribution — November 2025", fontsize=6)
# plt.tight_layout(pad=0)

# st.pyplot(fig, clear_figure=True)
