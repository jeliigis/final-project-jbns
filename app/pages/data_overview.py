import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from pathlib import Path


HERE = Path(__file__).resolve().parent          # = app/pages
DATA_PATH = HERE.parent / "data" / "df_health.xlsx"  # = app/data/df_health.xlsx

df_health = pd.read_excel(DATA_PATH, na_values=["x"])
st.dataframe(df_health)


# ROOT = Path(__file__).parent
# df_health = pd.read_excel(ROOT / "data" / "df_health.xlsx")

df_health.info()
df_health["Kost_Total"] = df_health["KostAmbA"] + df_health["KostStatA"]
df_health.head()

# generating a histogram for the total cost in switzerland
df_ch_cost = df_health[df_health["Region"] == "Schweiz"]
st.header("Kostenentwicklung der Akutbehandlung in Schweizer Spitälern (2010-2023)")
df_cost_ch_indexed = df_ch_cost.set_index('Jahr')
st.bar_chart(df_cost_ch_indexed['Kost_Total'])

# generating a bar plot for the total staff trend
df_health["Personal_Total"] = df_health[['MedTechPersonal_Anz_GrVe', 'MedTechPersonal_Anz_ZeVe', 'MedTechPersonal_Anz_AllgKr', 'MedTheraPersonal_Anz_GrVe',	'MedTheraPersonal_Anz_ZeVe',
                                         'MedTheraPersonal_Anz_AllgKr', 'Pflegepersonal_Anz_GrVe', 'Pflegepersonal_Anz_ZeVe', 'Pflegepersonal_Anz_AllgKr',	'Ärzteschaft_Anz_GrVe',	'Ärzteschaft_Anz_ZeVe',	'Ärzteschaft_Anz_AllgKr']].sum(axis=1)

df_ch_staff = df_health[df_health["Region"] == "Schweiz"]
st.header("Personalentwicklung in Schweizer Spitälern (2010-2023) ")
df_staff_ch_indexed = df_ch_staff.set_index("Jahr")
st.bar_chart(df_staff_ch_indexed["Personal_Total"])


# generating a bar plot for the total infrastructure trend over the years
df_health["Infrastructure_Total"] = df_health[['ANGIOGRAPHIE_Geräte', 'CT_SCANNER_Geräte', 'DIALYSE_Geräte', 'GAMMA_CAMERA_Geräte',	'LINEARBESCHLEUNIGER_Geräte', 'LITHOTRIPTOR_Geräte',	'MRI_Geräte', 'PET_SCANNER_Geräte', 'ANGIOGRAPHIE_Untersuchungen',
                                               'CT_SCANNER_Untersuchungen', 'DIALYSE_Untersuchungen', 'GAMMA_CAMERA_Untersuchungen',	'LINEARBESCHLEUNIGER_Untersuchungen', 'LITHOTRIPTOR_Untersuchungen', 'MRI_Untersuchungen', 'PET_SCANNER_Untersuchungen']].sum(axis=1)
df_ch_infrastructure = df_health[df_health["Region"] == "Schweiz"]
st.header("Infrastructure Development in Swiss Hospitals in 2010-2023")
df_infrastructure_ch_indexed = df_ch_infrastructure.set_index("Jahr")
st.bar_chart(df_infrastructure_ch_indexed["Infrastructure_Total"])


# generating a line plot for the examinations per device
column_devices = ["ANGIOGRAPHIE_Geräte", "CT_SCANNER_Geräte", "DIALYSE_Geräte", "GAMMA_CAMERA_Geräte",
                  "LINEARBESCHLEUNIGER_Geräte",	"LITHOTRIPTOR_Geräte", "MRI_Geräte", "PET_SCANNER_Geräte"]
df_health["Total Devices"] = df_health[column_devices].sum(axis=1)

column_examination = ["ANGIOGRAPHIE_Untersuchungen", "CT_SCANNER_Untersuchungen", "DIALYSE_Untersuchungen", "GAMMA_CAMERA_Untersuchungen",
                      "LINEARBESCHLEUNIGER_Untersuchungen", "LITHOTRIPTOR_Untersuchungen", "MRI_Untersuchungen", "PET_SCANNER_Untersuchungen"]
df_health["Total Examinations"] = df_health[column_examination].sum(axis=1)

df_health["Examinations per Device"] = (
    df_health["Total Examinations"] / df_health["Total Devices"])


df_ch_ExPerDe = df_health[df_health['Region'] == 'Schweiz']


# for this line chart we used the help of ai but made sure to understand what he is doing

st.header("Examinations per Device – Trend by Regions")

# Verfügbare Regionen (inkl. Schweiz)
regionen = sorted(df_health['Region'].dropna().unique().tolist())

# Auswahl-UI (Standard: Schweiz)
selection = st.multiselect("Choose region(S):", regionen, default=["Schweiz"])

if selection:
    fig, ax = plt.subplots(figsize=(9, 6))

    for r in selection:
        s = (df_health[df_health['Region'] == r]
             .sort_values('Jahr'))
        ax.plot(s['Jahr'], s['Examinations per Device'], marker='o', label=r)

    ax.set_xlabel("Jahr")
    ax.set_ylabel("Examinations per Device")
    ax.set_title("Examinations per Device - Trend by Regions")
    ax.grid(True)
    ax.legend(title="Region")
    st.pyplot(fig)
else:
    st.info("Please choose at least one region.")

# generating a bar plot for the bed/nurse development over the last decade
# new key-number
st.header("Beds per Nurse - Trend by Regions")
charge_nurse = "Beds per Nurse"
df_health[charge_nurse] = df_health["Betten_Total_AllgKr"] / \
    df_health["Pflegepersonal_Anz_AllgKr"]

if selection:
    fig, ax = plt.subplots(figsize=(9, 6))
    for r in selection:
        s = df_health[df_health["Region"] == r].sort_values("Jahr")
        ax.plot(s["Jahr"], s[charge_nurse], marker="o", label=r)
    ax.set_xlabel("Jahr")
    ax.set_ylabel(charge_nurse)
    ax.set_title("Beds per Nurse – Trend by Regions")
    ax.grid(True)
    ax.legend(title="Region")
    st.pyplot(fig)
else:
    st.info("Please choose at least one region.")

# generating a bar plot for the bed/doc development over the last decade
# new key humber

st.header("Beds per Doctor - Trend by Regions")
charge_doc = "Beds per Doctor"
df_health[charge_doc] = df_health["Betten_Total_AllgKr"] / \
    df_health["Ärzteschaft_Anz_AllgKr"]

if selection:
    fig, ax = plt.subplots(figsize=(9, 6))
    for r in selection:
        s = df_health[df_health["Region"] == r].sort_values("Jahr")
        ax.plot(s["Jahr"], s[charge_doc], marker="o", label=r)
    ax.set_xlabel("Jahr")
    ax.set_ylabel(charge_doc)
    ax.set_title("Beds per Docs – Trend by Regions")
    ax.grid(True)
    ax.legend(title="Region")
    st.pyplot(fig)
else:
    st.info("Please choose at least one region.")

# fig, ax = plt.subplots(figsize=(9, 6))
# s = df_health[df_health["Region"] == "Schweiz"].sort_values("Jahr")
# ax.plot(s["Jahr"], s["Betten_Total_AllgKr"], marker="o", label="Total Beds")
# ax.plot(s["Jahr"], s["Pflegepersonal_Anz_AllgKr"],
#        marker="o", label="Total Nurses")
# ax.set_title("Development of Beds vs Nurses (Switzerland)")
# ax.legend()
# st.pyplot(fig)
