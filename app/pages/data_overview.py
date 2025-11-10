import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Swiss Hospital Dashboard",
    page_icon="🏥",
    layout="centered"
)

HERE = Path(__file__).resolve().parent          # = app/pages
DATA_PATH = HERE.parent / "data" / "df_health.xlsx"  # = app/data/df_health.xlsx

df_health = pd.read_excel(DATA_PATH, na_values=["x"])
st.title("Swiss Hospital Data")
st.subheader("Data Overview")
tab1, tab2, tab3 = st.tabs(
    ["Development Statistics", "Occupancy Statistics", "Regression"])
# st.dataframe(df_health)


# ROOT = Path(__file__).parent
# df_health = pd.read_excel(ROOT / "data" / "df_health.xlsx")

with tab1:
    st.header("Development Statistics")

    # generating a bar plot for the total of hospitals trend over the years
    df_ch_hospitals = df_health[df_health["Region"] == "Schweiz"]
    st. subheader("Hospital development in Swiss Hospitals in 2010 - 2023")
    df_hospitals_ch_indexed = df_ch_hospitals.set_index('Year')
    st.bar_chart(df_hospitals_ch_indexed["Amount_Hospitals_General"])
    st.caption("_x-axis = Year, y-axis = number of hospitals_")
    st.write("This graphic illustrates the development of the number of hospitals in Switzerland from 2010 to 2023. "
             "The data show a gradual decline in the total number of hospitals over the observed period, suggesting a trend toward consolidation or centralization within the Swiss healthcare system. "
             "While the decrease is not abrupt, it reflects a steady structural adjustment in hospital availability nationwide. Regarding the year 2023, there has been a decrease of -19.8% since the year 2010.")

# generating a histogram for the total cost in switzerland

    df_health.info()
    df_health["Cost_Total"] = df_health["Cost_AcuteCare_Amb"] + \
        df_health["Cost_AcuteCare_Stat"]
    df_health.head()
    df_ch_cost = df_health[df_health["Region"] == "Schweiz"]
    st.subheader(
        "Cost development of acute treatment in Swiss hospitals in 2010–2023")
    df_cost_ch_indexed = df_ch_cost.set_index('Year')
    st.bar_chart(df_cost_ch_indexed['Cost_Total'])
    st.caption("_x-axis = Year, y-axis = Total Cost in CHF (Billion)_")
    st.write("This graphic illustrates how total costs of acute treatment in Swiss hospitals have developed from 2010 - 2023. "
             "A continous upward trend can be observed, indicating a steady increase in healthcare costs over the examined period. "
             "The growth may reflect multiple underlying factors such as demographic changes, advances in medical technology, and rising service intensity in hospitals. "
             "Overall, the data highlight the increasing financial burden on the Swiss health system. ")


# generating a bar plot for the total staff trend
    df_health["Staff_Total"] = df_health[['MedTec_Amount_Basic', 'MedTec_Amount_Central', 'MedTec_Amount_General', 'MedThe_Amount_Basic', 'MedThe_Amount_Central',
                                          'MedThe_Amount_General', 'Nurses_Amount_Basic', 'Nurses_Amount_Central', 'Nurses_Amount_General',	'Doctors_Amount_Basic',	'Doctors_Amount_Central', 'Doctors_Amount_General']].sum(axis=1)

    df_ch_staff = df_health[df_health["Region"] == "Schweiz"]
    st.subheader(
        "Staff development of acute treatment in Swiss hospitals in 2010-2023")
    df_staff_ch_indexed = df_ch_staff.set_index('Year')
    st.bar_chart(df_staff_ch_indexed["Staff_Total"])
    st.caption("_x-axis = Year, y-axis = Numbers of full-time-equivalent staff_")
    st.write("The graphic shows the development of staff employed in acute treatment in Swiss hospitals between 2010 and 2023. "
             "The number of full-time equivalent positions has increased steadly over the period, reflecting a growth of about + 30.9 %. "
             "The data highlight the expansion of hospital services and the growing demand for healthcare professionals. ")

    # generating a bar plot for the total infrastructure trend over the years
    df_health["Infrastructure_Total"] = df_health[["Angiographie_Device", "CT_Scanner_Device", "Dialyse_Device", "Gamma_Camera_Device",
                                                   "Linear_Accelerator_Device",	"Lithotriptor_Device", "MRI_Device", "Pet_Scanner_Device"]].sum(axis=1)
    df_ch_infrastructure = df_health[df_health["Region"] == "Schweiz"]
    df_ch_infrastructure = df_ch_infrastructure[df_ch_infrastructure['Year'] >= 2013]
    st.subheader("Infrastructure development in Swiss Hospitals in 2013-2023")
    df_infrastructure_ch_indexed = df_ch_infrastructure.set_index('Year')
    st.bar_chart(df_infrastructure_ch_indexed["Infrastructure_Total"])
    st.caption("_x-axis = Year, y-axis = Number of Medical Devices_")
    st.caption("List of relevant Devices: Angiographie, CT Scanner, Dialyse, Gamma Camera, Linear Accelerator,Lithotriptor, MRI,Pet_Scanner")
    st.write("This graphic presents the development of numbers of available medical devices in acute treatment in Swiss hospitals between 2010 and 2023."
             "The lates number of total medical devices in Switzerland in 2023 has increased by + 20% since 2013. There were comparatively large increases in 2016 to 2017 and 2017 to 2018. "
             "The highest acquisition rate is evident in the available data for 2020. While 23 new devices were purchased in the previous year, the corresponding figure for 2020 was 85. "
             "This can be linked to the global pandemic. A year later, the number of new devices purchased fell to a low of 14. ")
    # generating a bar plot for the total of hospital beds trend over the years
    df_ch_beds = df_health[df_health["Region"] == "Schweiz"]
    st. subheader(
        "Hospital Beds development in Swiss Hospitals in 2010 - 2023")
    df_beds_ch_indexed = df_ch_beds.set_index('Year')
    st.bar_chart(df_beds_ch_indexed["Beds_Total_General"])
    st.caption("_x-axis = Year, y-axis = number of hospital beds_")
    st.write("The graphic shows the development of total beds in Swiss hospitals between 2010 and 2023. "
             "The data demonstrate that Switzerland has reduced its total number of beds in acute treatment hospitals by -12.4% over the last 13 years.")


with tab2:
    st.subheader("Occupancy Statistics")
    # generating a line plot for the examinations per device
    column_devices = ["Angiographie_Device", "CT_Scanner_Device", "Dialyse_Device", "Gamma_Camera_Device",
                      "Linear_Accelerator_Device",	"Lithotriptor_Device", "MRI_Device", "Pet_Scanner_Device"]
    df_health["Total Devices"] = df_health[column_devices].sum(axis=1)

    column_examination = ["Angiographie_Examination", "CT_Scanner_Examination", "Dialyse_Examination", "Gamma_Camera_Examination",
                          "Linear_Accelerator_Examination", "Lithotriptor_Examination", "MRI_Examination", "Pet_Scanner_Examination"]
    df_health["Total Examinations"] = df_health[column_examination].sum(axis=1)

    df_health["Examinations per Device"] = (
        df_health["Total Examinations"] / df_health["Total Devices"])

    df_ch_ExPerDe = df_health[df_health['Region'] == 'Schweiz']

    # for this line chart we used the help of ai but made sure to understand what he is doing

    st.header("Examinations per Device – Trend by Regions")

    # Verfügbare Regionen (inkl. Schweiz)
    regionen = sorted(df_health['Region'].dropna().unique().tolist())

    # Auswahl-UI (Standard: Schweiz)
    selection = st.multiselect(
        "Choose region(S):", regionen, default=["Schweiz"])

    if selection:
        fig, ax = plt.subplots(figsize=(9, 6))

        for r in selection:
            s = (df_health[df_health['Region'] == r]
                 .sort_values('Year'))
            ax.plot(s['Year'], s['Examinations per Device'],
                    marker='o', label=r)

        ax.set_xlabel('Year')
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
    df_health[charge_nurse] = df_health["Beds_Total_General"] / \
        df_health["Nurses_Amount_General"]

    if selection:
        fig, ax = plt.subplots(figsize=(9, 6))
        for r in selection:
            s = df_health[df_health["Region"] == r].sort_values("Year")
            ax.plot(s['Year'], s[charge_nurse], marker="o", label=r)
        ax.set_xlabel('Year')
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
    df_health[charge_doc] = df_health["Beds_Total_General"] / \
        df_health["Doctors_Amount_General"]

    if selection:
        fig, ax = plt.subplots(figsize=(9, 6))
        for r in selection:
            s = df_health[df_health["Region"] == r].sort_values("Year")
            ax.plot(s["Year"], s[charge_doc], marker="o", label=r)
        ax.set_xlabel("Year")
        ax.set_ylabel(charge_doc)
        ax.set_title("Beds per Docs – Trend by Regions")
        ax.grid(True)
        ax.legend(title="Region")
        st.pyplot(fig)
    else:
        st.info("Please choose at least one region.")

    fig, ax = plt.subplots(figsize=(9, 6))
    s = df_health[df_health["Region"] == "Schweiz"].sort_values("Year")
    ax.plot(s["Year"], s["Beds_Total_General"],
            marker="o", label="Total Beds")
    ax.plot(s["Year"], s["Nurses_Amount_General"],
            marker="o", label="Total Nurses")
    ax.set_title("Development of Beds vs Nurses (Switzerland)")
    ax.legend()
    st.pyplot(fig)


# doing a regression
with tab3:  # install scikit: pip3 install scikit-learn
    from sklearn.linear_model import LinearRegression
    df_health_reg = df_health.dropna(
        subset=["Cost_Total", "Staff_Total", "Beds_Total_General"])

    df_health_reg["cost_per_bed"] = df_health_reg["Cost_Total"] / \
        df_health_reg["Beds_Total_General"]
    df_health_reg["nurses_per_bed"] = df_health_reg["Nurses_Amount_General"] / \
        df_health_reg["Beds_Total_General"]

    st.title("Linear Regressions")
    st.header("Linear Regression: Cost per Bed on Beds per Nurse")

    X = df_health_reg[["nurses_per_bed"]]
    y = df_health_reg["cost_per_bed"]

    df_health_reg = df_health_reg[df_health_reg["cost_per_bed"] != 0]

    model = LinearRegression().fit(X, y)
    df_health_reg["Regression"] = model.predict(X)

    st.write(f"Intercept: {model.intercept_:.2f}")  # used AI for help
    st.write(f"Slope: {model.coef_[0]:.2f}")

    plt.scatter(df_health_reg["nurses_per_bed"],
                df_health_reg["cost_per_bed"], label="Data")
    plt.plot(df_health_reg["nurses_per_bed"],
             df_health_reg["Regression"], label="Regression")
    plt.xlabel("Nurses per bed")
    plt.ylabel("Cost per bed")
    plt.legend()

    plt.xlim(0, 4)
    plt.ylim(0, 2_000_000)

    st.pyplot(plt)

    st.write(df_health_reg[["cost_per_bed", "nurses_per_bed"]].head(112))
