import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
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

st.subheader("Key Figures November 2025")

nov_row = df_sim[(df_sim["Year"] == 2025) & (
    df_sim["Month"] == "November")].iloc[0]

# KPI Calculation
# Total Patients
total_patients_nov = int(nov_row["Total Patient"])

# Total Staff
total_staff_nov = int(
    nov_row[["Nurses", "Doctors", "MedTech", "Cleaning"]].sum())

# Total Cost
total_cost_nov = float(nov_row["Treatment Cost"])

# Average Treatment Cost

avg_treat_cost_nov = round(total_cost_nov / total_patients_nov, 2)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Patient November 2025",
              value=f"{total_patients_nov:,}")

with col2:
    st.metric(label="Total Staff November 2025", value=f"{total_staff_nov:,}")

with col3:
    st.metric(
        label="Avg. Treatment Cost per Patient (Nov 2025)",
        value=f"{avg_treat_cost_nov:,}")


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


# Spider Diagram
