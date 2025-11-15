import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
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


# available years: 2024 and 2025
years = sorted(df_sim["Year"].unique())  # num-py array
default_year_index = len(years)-1  # create default

selected_year = st.selectbox("Select year", years, index=default_year_index)

# available months
month_options = df_sim[df_sim["Year"] == selected_year]["Month"].unique()

selected_month = st.selectbox("Select month", month_options)

# row for the chosen month and year
selected_row = df_sim[
    (df_sim["Year"] == selected_year) &
    # iloc = slects data based on integer position
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
# round to not get too many decimal digits
avg_treat_cost = round(total_cost / total_patients, 2)

# In order to create a data dashboard for different months we need to define our own functions which access then to de chosen data

# definition for KPI at the top


def metric_chart(label: str, value):
    """Creates a KPI metric box wrapped in a bordered container."""
    with st.container(border=True):  # creates boxes
        st.metric(label=label, value=f"{value:,}")

# definition for the donut chart
# used plotly.express --> AI suggestion


def donut_card(row, columns, title, col):
    """Create a Donut-Chart in a Chard inside a column."""
    values = row[columns]

    df_pie = pd.DataFrame({"Category": values.index, "Value": values.values})

    fig = px.pie(
        df_pie,
        names="Category",
        values="Value",
        hole=0.50)

    # Wanted to exclude numbers in the graphic due to space issues --> asked AI
    fig.update_traces(
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{value} meals<br>%{percent}")

    # Legend as a Caption
    fig.update_layout(
        title=None,
        margin=dict(l=0, r=0, t=0, b=40),
        height=260,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(size=13)))

    with col:
        with st.container(border=True):
            st.markdown(f"### {title}")
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False})

# definition for radar chart


def radar_chart(row, title, col):
    """Bed Capacity vs. Occupancy as a Radar-Chart in a Card."""
    # Departments (Labels)
    labels = ["Oncology", "Emergency", "Palliative", "Surgery",
              "Internal", "Gynecology", "Neonatology", "Geriatrics"]

    beds_cols = ["Beds_Onc", "Beds_Emer", "Beds_Pall", "Beds_Sur",
                 "Beds_Int", "Beds_Gyn", "Beds_Neo", "Beds_Ger"]
    occ_cols = ["Beds_Onc_Occ", "Beds_Emer_Occ", "Beds_Pall_Occ", "Beds_Sur_Occ",
                "Beds_Int_Occ", "Beds_Gyn_Occ", "Beds_Neo_Occ", "Beds_Ger_Occ"]

    beds = row[beds_cols].to_numpy(dtype=float)
    occ = row[occ_cols].to_numpy(dtype=float)

    ratio = occ / beds  # für warning message

    # normalize
    max_val = beds.max()  # = 30
    beds_norm = beds / max_val
    occ_norm = occ / max_val

    df_radar = pd.DataFrame({
        "Department": labels * 2,
        "Value": list(beds_norm) + list(occ_norm),
        "Metric": ["Capacity"] * len(labels) + ["Occupancy"] * len(labels)})

    fig = px.line_polar(
        df_radar,
        r="Value",
        theta="Department",
        color="Metric",
        line_close=True,
        color_discrete_map={
            "Capacity": "#27ae60",
            "Occupancy": "#7f8c8d"})

    fig.update_traces(fill="toself", opacity=0.4)

    fig.update_layout(
        title=None,
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, 1.05])),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=10)),
        margin=dict(l=40, r=40, t=60, b=60),
        height=380)

    with col:
        with st.container(border=True):
            st.markdown(f"### {title}")
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False})

    # warn message --> used AI as a inspiration
    threshold = 0.85  # randomly chosen
    critical = ratio >= threshold
    if critical.any():
        overloaded = [labels[i] for i, v in enumerate(critical) if v]
        st.error("⚠️ Critical occupancy in: " + ", ".join(overloaded))

# Illustration


col1, col2, col3 = st.columns((3, 6, 3), gap="medium")

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

# Donut-Pie
diet_cols = [
    "Raw_diet",
    "Soft_diet",
    "Normal_diet",
    "Diabetic_diet",
    "Vegetarian/Vegan"]

with col1:
    donut_card(
        row=selected_row,
        columns=diet_cols,
        title=f"Diet Distribution — {selected_month} {selected_year}",
        col=col1)
# Radar-Chart
with col2:
    radar_chart(
        row=selected_row,
        title=f"Bed Capacity vs. Occupancy — {selected_month} {selected_year}",
        col=col2)
