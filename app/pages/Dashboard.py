import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Wichtig: Page Config möglichst früh
st.set_page_config(
    page_title="Swiss Hospital Dashboard",
    page_icon="🏥",
    layout="wide")

# content
st.title("Switzerland's Hospital System: Between Performance and Bottleneck")
st.markdown(
    "🔎 Discover how a figurative Swiss hospital could potentially look like and its kpi's development.")
st.write("This dashboard was created to display various measurements and illustrations relating to a hospital. "
         "The data was generated synthetically and is not intended to be interpreted in terms of content. The aim would be to use data for a real hospital in Switzerland. ")

# BI-Diagram Dashboard

HERE = Path(__file__).resolve().parent
DATA_PATH = HERE.parent / "data" / "bi_diagramm_data.xlsx"

df_sim = pd.read_excel(DATA_PATH, na_values=["x"])
st.title("Swiss Hospital Data")

# KPI Dashboard

# available years: 2024 and 2025
years = sorted(df_sim["Year"].unique())  # numpy array
default_year_index = len(years) - 1  # create default

selected_year = st.selectbox("Select year", years, index=default_year_index)

# available months
month_options = df_sim[df_sim["Year"] == selected_year]["Month"].unique()
selected_month = st.selectbox("Select month", month_options)

# row for the chosen month and year
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


# KPI-Box Functions


def metric_chart(label: str, value, delta=None):
    """Creates a KPI metric box wrapped in a bordered container."""
    with st.container(border=True):  # creates boxes
        st.metric(
            label=label,
            value=f"{value:,}",
            delta=f"{delta:.2f}%" if delta is not None else None)

# Previous Month


month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"]

current_idx = month_order.index(selected_month)

if current_idx == 0:
    prev_month_name = "December"
    prev_year = selected_year - 1
else:
    prev_month_name = month_order[current_idx - 1]
    prev_year = selected_year

# Get Pre-Rows
pre_row = df_sim[
    (df_sim["Year"] == prev_year) &
    (df_sim["Month"] == prev_month_name)]


def pct_change(current, previous):
    if previous is None or previous == 0:
        return None
    return (current - previous) / previous * 100

# Deltas and KPI from the previous month


if not pre_row.empty:
    pre_row = pre_row.iloc[0]

    # Previous Month: Total Patients
    prev_total_patients = int(pre_row["Total Patient"])

    # Previous Month: Total Staff
    prev_total_staff = int(
        pre_row[["Nurses", "Doctors", "MedTech", "Cleaning"]].sum())

    # Previous Month: Total Cost
    prev_total_cost = float(pre_row["Treatment Cost"])

    # Previous Month: Avg Treatment Cost
    prev_avg_treat_cost = round(prev_total_cost / prev_total_patients, 2)

    # Change in %
    delta_patients = pct_change(total_patients, prev_total_patients)
    delta_staff = pct_change(total_staff, prev_total_staff)
    delta_cost = pct_change(avg_treat_cost, prev_avg_treat_cost)
else:
    # In case there is no previous month (december 2024!)
    delta_patients = delta_staff = delta_cost = None

# Donut-Chart Function


def donut_card(row, columns, title, col):
    """Create a Donut-Chart in a Card inside a column."""
    values = row[columns]

    df_pie = pd.DataFrame({"Category": values.index, "Value": values.values})

    fig = px.pie(
        df_pie,
        names="Category",
        values="Value",
        hole=0.50)

    # Exclude numbers in chart, show in hover only
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
            st.markdown(f"**{title}**")
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False})

# Radar-Chart Function


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

    ratio = occ / beds  # warning message

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
        title="",
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, 1.05])),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.35,
            xanchor="left",
            x=0.0,
            font=dict(size=10)),
        margin=dict(l=40, r=40, t=60, b=60),
        height=380)

    with col:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False})

    # warn message
    threshold = 0.91  # randomly chosen
    critical = ratio >= threshold
    if critical.any():
        overloaded = [labels[i] for i, v in enumerate(critical) if v]
        st.error("⚠️ Critical occupancy in: " + ", ".join(overloaded))

# Area Chart for Staff


def staff_area_chart(df_sim):
    """Stacked Area Chart für Staff-Kategorien über alle Monate (Dec 2024 – Dec 2025)."""
    # Reihenfolge der Monate definieren
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"]

    # nur die relevanten Spalten
    staff_cols = ["Doctors", "Nurses", "MedTech", "Cleaning"]

    df_staff = df_sim.copy()

    # Monat numerisch für Sortierung
    month_map = {m: i+1 for i, m in enumerate(month_order)}
    df_staff["Month_num"] = df_staff["Month"].map(month_map)

    # sortieren: erst Jahr, dann Monat
    df_staff = df_staff.sort_values(["Year", "Month_num"])

    # Label für x-Achse, z.B. "Dec 2024"
    df_staff["Month_label"] = df_staff["Month"].str[:3] + \
        " " + df_staff["Year"].astype(str)

    # Long-Format für Plotly
    df_long = df_staff.melt(
        id_vars=["Year", "Month", "Month_num", "Month_label"],
        value_vars=staff_cols,
        var_name="Staff_Type",
        value_name="Count")

    # Reihenfolge der x-Achse fixieren (sonst sortiert Plotly alphabetisch)
    month_label_order = df_staff["Month_label"].tolist()

    fig = px.area(
        df_long,
        x="Month_label",
        y="Count",
        color="Staff_Type",
        category_orders={
            "Month_label": month_label_order,
            "Staff_Type": staff_cols},
        labels={
            "Month_label": "Month",
            "Count": "Number of Staff",
            "Staff_Type": "Staff Category"})

    fig.update_layout(
        title="",
        yaxis=dict(
            range=[0, 900],
            dtick=50,
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="left",
            x=0.0,
            font=dict(size=10)),
        margin=dict(l=40, r=40, t=40, b=120),
        height=380)

    return fig


def patient_area_chart(df_sim):
    """Stacked Area Chart für Patienten-Kategorien über alle Monate (Dec 2024 – Dec 2025)."""
    # Reihenfolge der Monate definieren
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"]

    # 👉 HIER ggf. an deine echten Spaltennamen anpassen
    patient_cols = ["Newborn", "Children/Teen", "Adult", "Elderly"]

    df_pat = df_sim.copy()

    # Monat numerisch für Sortierung
    month_map = {m: i + 1 for i, m in enumerate(month_order)}
    df_pat["Month_num"] = df_pat["Month"].map(month_map)

    # sortieren: erst Jahr, dann Monat
    df_pat = df_pat.sort_values(["Year", "Month_num"])

    # Label für x-Achse, z.B. "Dec 2024"
    df_pat["Month_label"] = df_pat["Month"].str[:3] + \
        " " + df_pat["Year"].astype(str)

    # Long-Format für Plotly
    df_long = df_pat.melt(
        id_vars=["Year", "Month", "Month_num", "Month_label"],
        value_vars=patient_cols,
        var_name="Patient_Type",
        value_name="Count",)

    # Reihenfolge der x-Achse fixieren
    month_label_order = df_pat["Month_label"].tolist()

    fig = px.area(
        df_long,
        x="Month_label",
        y="Count",
        color="Patient_Type",
        category_orders={
            "Month_label": month_label_order,
            "Patient_Type": patient_cols, },
        labels={
            "Month_label": "Month",
            "Count": "Number of Patients",
            "Patient_Type": "Patient Category", },)

    # Y-Achse dynamisch aufrunden (Schritte à 50)
    max_count = df_long["Count"].max()
    if pd.isna(max_count):
        max_count = 0
    upper = ((int(max_count) // 50) + 1) * 50 if max_count > 0 else 50

    fig.update_layout(
        title="",
        yaxis=dict(
            range=[0, 250],
            dtick=50,
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="left",
            x=0.0,
            font=dict(size=10),),
        margin=dict(l=40, r=40, t=40, b=120),
        height=380,)

    return fig


def total_bed_occupancy(row):
    """Berechnet die gesamte Betten-Auslastung in % über alle Departments."""
    beds_cols = ["Beds_Onc", "Beds_Emer", "Beds_Pall", "Beds_Sur",
                 "Beds_Int", "Beds_Gyn", "Beds_Neo", "Beds_Ger"]
    occ_cols = ["Beds_Onc_Occ", "Beds_Emer_Occ", "Beds_Pall_Occ", "Beds_Sur_Occ",
                "Beds_Int_Occ", "Beds_Gyn_Occ", "Beds_Neo_Occ", "Beds_Ger_Occ"]

    total_beds = row[beds_cols].sum()
    total_occ = row[occ_cols].sum()

    if total_beds == 0:
        return 0.0

    return float(total_occ / total_beds * 100)


bed_occupancy_pct = total_bed_occupancy(selected_row)


def bed_occupancy_gauge(value_pct: float):
    """
    Vertikales Gauge ohne Zahlen.
    Drei gleich große Zonen (optisch Drittel):
      < 80%  = Low capacity utilization
      80–90% = Optimal
      > 90%  = High capacity utilization

    Nur die Zone, in der value_pct liegt, wird kräftig eingefärbt,
    die anderen sind blass/hinterlegt.
    """
    fig = go.Figure()

    # 1) bestimmen, in welcher Zone wir sind (nach deinen Schwellen)
    if value_pct < 80:
        active_zone = "low"
    elif value_pct <= 95:
        active_zone = "optimal"
    else:
        active_zone = "high"

    colors_base = {
        "high":    "rgba(231, 76, 60, 0.25)",   # #E74C3C blass
        "optimal": "rgba(82, 179, 174, 0.25)",  # F5B7B1 blass
        "low":     "rgba(245, 183, 177, 0.25)",  # #52B3AE blass
    }
    colors_high = {
        "high":    "rgba(231, 76, 60, 1)",      # High full red
        "optimal": "rgba(82, 179, 174, 1)",    # Optimal full rosé
        "low":     "rgba(245, 183, 177, 1)",     # Low full teal
    }
    # 3) Drei optisch gleich große Segmente (Drittel)
    segments = [
        ("high",    66.67, 100),   # oben
        ("optimal", 33.33, 66.67),  # Mitte
        ("low",      0.0, 33.33),  # unten
    ]

    for name, y0, y1 in segments:
        fig.add_shape(
            type="rect",
            x0=0, x1=1,
            y0=y0, y1=y1,
            fillcolor=colors_high[name] if name == active_zone else colors_base[name],
            line=dict(width=0),
        )

    # 4) Labels mittig in die Blöcke schreiben
    fig.add_annotation(
        x=0.5, y=(0 + 33.33) / 2,  # Mitte vom unteren Drittel
        text="Low capacity\nutilization",
        showarrow=False,
        font=dict(size=10, color="black"),
        align="center"
    )
    fig.add_annotation(
        x=0.5, y=(33.33 + 66.67) / 2,
        text="Optimal",
        showarrow=False,
        font=dict(size=10, color="black"),
        align="center"
    )
    fig.add_annotation(
        x=0.5, y=(66.67 + 100) / 2,
        text="High capacity\nutilization",
        showarrow=False,
        font=dict(size=10, color="black"),
        align="center"
    )

    # 5) Achsen komplett ausblenden (keine Zahlen)
    fig.update_xaxes(visible=False, range=[0, 1])
    fig.update_yaxes(visible=False, range=[0, 100])

    fig.update_layout(
        title="",
        margin=dict(l=40, r=40, t=10, b=10),
        height=380,
        width=160,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


# Layout: KPIs + Charts
col1, col2, col3 = st.columns((3, 6, 3), gap="medium")

with col1:
    metric_chart(
        f"**Total Patient {selected_month} {selected_year}**",
        total_patients,
        delta_patients)

with col3:
    metric_chart(
        f"**Total Staff {selected_month} {selected_year}**",
        total_staff,
        delta_staff)

with col2:
    metric_chart(
        f"**Avg.Treat.Cost/Patient({selected_month} {selected_year}**)",
        avg_treat_cost,
        delta_cost)

# Donut-Pie
diet_cols = [
    "Raw Diet",
    "Soft Diet",
    "Normal Diet",
    "Diabetic Diet",
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

st.markdown("**Staff Composition over Time (Dec 2024 – Dec 2025)**")

with st.container(border=True):
    fig_staff = staff_area_chart(df_sim)
    st.plotly_chart(
        fig_staff,
        use_container_width=True,
        config={"displayModeBar": False})


st.markdown("**Patient Composition over Time (Dec 2024 – Dec 2025)**")
with st.container(border=True):
    fig_pat = patient_area_chart(df_sim)
    st.plotly_chart(fig_pat, use_container_width=True,
                    config={"displayModeBar": False})

with col3:
    with st.container(border=True):
        st.markdown(
            f"**Total Bed Occupancy — {selected_month} {selected_year}**")
        fig_gauge = bed_occupancy_gauge(bed_occupancy_pct)
        st.plotly_chart(
            fig_gauge,
            use_container_width=True,
            config={"displayModeBar": False})
