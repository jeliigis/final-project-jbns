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
st.write("_based on Federal Statistical Office, 2025_")
tab1, tab2, tab3, tab4 = st.tabs(
    ["Development Visualisation", "Regional Structure Trend ", "Linear Regression", "Overview Dataset"])
# st.dataframe(df_health)


# ROOT = Path(__file__).parent
# df_health = pd.read_excel(ROOT / "data" / "df_health.xlsx")

with tab1:
    st.header("Development Visualisation")
    st.write("Development of Swiss Hospitals captured in bar plots")

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

    fig, ax = plt.subplots(figsize=(9, 6))
    s = df_health[df_health["Region"] == "Schweiz"].sort_values("Year")
    ax.plot(s["Year"], s["Beds_Total_General"],
            marker="o", label="Total Beds")
    ax.plot(s["Year"], s["Nurses_Amount_General"],
            marker="o", label="Total Nurses")
    ax.set_title("Development of Beds vs Nurses (Switzerland)")
    ax.legend()
    # st.pyplot(fig)
    # st.caption("_x-axis = Year, y-axis= Total Beds and Nurses_")
    # st.write("While nurses numbers have steadily increased in recent years, the number of beds requiring care has fallen in parallel. "
    # "This development has eased the burden on nursing staff, although it should be noted that individual treatments may have become more intensive as a result. ")

with tab2:
    st.subheader("Regional Structure Trend")
    st.write("Overview of regional differences in infrastrutural and staff trend")
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
        st.header("Examinations per Device – Trend by Regions")
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


# doing a regression

with tab3:
    from sklearn.linear_model import LinearRegression
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import statsmodels.api as sm

    # --- Vorbereitung
    # first i rename some columns because the description is wrong/misleading
    df_health = df_health.rename(columns={"Bed_OccupancyDays_Basic": "Bed_CapacityDays_Basic",
                                 "Bed_OccupancyDays_Central": "Bed_CapacityDays_Central", "Bed_OccupancyDays_General": "Bed_CapacityDays_General"})
    req = ["Region", "Year", "Cost_Total", "Staff_Total", "Beds_Total_General", "Bed_Occupancy_General",
           "Total Devices", "Total Examinations", "Nurses_Amount_General"]

    df_health_reg = df_health.dropna(subset=req).copy()
    # drop Switzerland as it is not a region to avoid multicollinearity (dont know if its multicollinearity, but switzerland just exists through the values of the other regions)
    df_health_reg = df_health_reg[df_health_reg["Region"] != "Schweiz"]

    # generating some new variables for the regressions
    df_health_reg["Bed_OccupancyDays_General"] = df_health_reg["Bed_CapacityDays_General"] * \
        (df_health_reg["Bed_Occupancy_General"] / 100)
    df_health_reg["Avg_Days_Occ"] = df_health_reg["Bed_OccupancyDays_General"] / \
        df_health_reg["Beds_Total_General"]

    df_health_reg["cost_per_bedday"] = df_health_reg["Cost_Total"] / \
        df_health_reg["Bed_OccupancyDays_General"]
    df_health_reg["nurses_per_bed"] = df_health_reg["Nurses_Amount_General"] / \
        df_health_reg["Beds_Total_General"]
    df_health_reg["examinations_per_device"] = df_health_reg["Total Examinations"] / \
        df_health_reg["Total Devices"]

    # nur sinnvolle Zeilen behalten / with the help of AI
    df_health_reg = df_health_reg.replace([np.inf, -np.inf], np.nan).dropna()
    df_health_reg = df_health_reg[df_health_reg["cost_per_bedday"] != 0]

    st.subheader("Linear Regressions")
    st.write("Statistical Measurement with OLS")

    # 1) cost_per_bed ~ nurses_per_bed
    st.header("Linear Regression: Cost per Bed Day on Beds per Nurse")
    X1 = df_health_reg[["nurses_per_bed"]]   # 2D
    y1 = df_health_reg["cost_per_bedday"]       # 1D

    model_1 = LinearRegression().fit(X1, y1)
    df_health_reg["Regression_nurses"] = model_1.predict(X1)

    plt.figure()
    plt.scatter(df_health_reg["nurses_per_bed"],
                df_health_reg["cost_per_bedday"], label="Data")
    plt.plot(df_health_reg["nurses_per_bed"],
             df_health_reg["Regression_nurses"], label="Regression", color="magenta")
    plt.xlabel("Nurses per bed")
    plt.ylabel("Cost per bedday")
    plt.legend()
    st.pyplot(plt)

    # 1.2) adding some statistical key figures
    X1 = sm.add_constant(X1)
    model_1_2 = sm.OLS(y1, X1).fit()

    st.write("Slope:", round(model_1_2.params["nurses_per_bed"], 2))
    st.write("Std. Error:", round(model_1_2.bse["nurses_per_bed"], 2))
    st.write("P-value:", round(model_1_2.pvalues[1], 2))
    st.write("R^2:", round(model_1_2.rsquared, 2))

    # 2) cost per beddays - nurses per bed (with two way FE)
    st.header(
        "Two-Way Fixed Effects: Cost per Bedday on Beds per Nurse (Region + Year)")

    # generate a new dataset were we have the demeaned data to have a bit more overview
    df_fe = df_health_reg.copy()

    # calculate the mean in general
    mean_nurses = df_fe["nurses_per_bed"].mean()
    mean_cost = df_fe["cost_per_bedday"].mean()

    # demean year and regions / used a bit help of AI with .transform
    region_mean_nurses = df_fe.groupby(
        "Region")["nurses_per_bed"].transform("mean")
    year_mean_nurses = df_fe.groupby(
        "Year")["nurses_per_bed"].transform("mean")

    region_mean_cost = df_fe.groupby(
        "Region")["cost_per_bedday"].transform("mean")
    year_mean_cost = df_fe.groupby("Year")["cost_per_bedday"].transform("mean")

    # generate the new datapoints by using double demeaning (thanks to ronak jain and intermediate econometrics)
    df_fe["nurses_dd"] = (df_fe["nurses_per_bed"] -
                          region_mean_nurses - year_mean_nurses + mean_nurses)
    df_fe["cost_dd"] = (df_fe["cost_per_bedday"] -
                        region_mean_cost - year_mean_cost + mean_cost)

    # removing influential datapoints in retrospect as the regression had some influential datapoints by looking at the cooks distance
    # (used AI for the Code, Intution done by ourselves)
    X2 = sm.add_constant(df_fe[["nurses_dd"]])
    y2 = df_fe["cost_dd"]
    model_fe_1 = sm.OLS(y2, X2).fit()
    influence = model_fe_1.get_influence()
    df_fe["cooks_d1"] = influence.cooks_distance[0]
    # using just the 4/n rule for the definition of outliers
    threshold = 4 / len(df_fe)
    df_fe_clean_1 = df_fe[df_fe["cooks_d1"] < threshold]

    Xc1 = sm.add_constant(df_fe_clean_1[["nurses_dd"]])
    yc1 = df_fe_clean_1["cost_dd"]
    model_fe_clean_1 = LinearRegression().fit(Xc1, yc1)
    df_fe_clean_1["regline_dd"] = model_fe_clean_1.predict(Xc1)

    plt.figure()
    plt.scatter(df_fe_clean_1["nurses_dd"], df_fe_clean_1["cost_dd"],
                label="Data (within Region & Year)")
    plt.plot(df_fe_clean_1["nurses_dd"], df_fe_clean_1["regline_dd"],
             label="Two-Way FE Regression", color="magenta")
    plt.xlabel("Nurses per Bed (within Region & Year)")
    plt.ylabel("Cost per Bedday (within Region & Year)")
    plt.legend()

    st.pyplot(plt)

    # 2.2) adding some statistical key figures
    X2 = sm.add_constant(X2)
    model_fe_clean_1 = sm.OLS(y2, X2).fit()

    st.write("Slope:", round(model_fe_clean_1.params["nurses_dd"], 2))
    st.write("Std. Error:", round(model_fe_clean_1.bse["nurses_dd"], 2))
    st.write("P-value:", round(model_fe_clean_1.pvalues[1], 2))
    st.write("R^2:", round(model_fe_clean_1.rsquared, 2))

    # 3) cost_per_bed ~ Bed_Occupancy_General
    st.header("Linear Regression: Cost per Bedday on Average occupied Beddays")

    # WICHTIG: X als 2D-DataFrame
    X3 = df_health_reg[["Avg_Days_Occ"]]
    y3 = df_health_reg["cost_per_bedday"]

    model_2 = LinearRegression().fit(X3, y3)
    df_health_reg["Regression_occupancy"] = model_2.predict(X3)

    plt.figure()
    plt.scatter(df_health_reg["Avg_Days_Occ"],
                df_health_reg["cost_per_bedday"], label="Data")
    plt.plot(df_health_reg["Avg_Days_Occ"],
             df_health_reg["Regression_occupancy"], label="Regression", color="magenta")
    plt.xlabel("Avg. Days Occ")
    plt.ylabel("Cost per bedday")
    plt.legend()
    st.pyplot(plt)

    # 3.2) adding some statistical key figures
    X3 = sm.add_constant(X3)
    model_3_2 = sm.OLS(y3, X3).fit()

    st.write("Slope:", round(model_3_2.params["Avg_Days_Occ"], 2))
    st.write("Std. Error:", round(model_3_2.bse["Avg_Days_Occ"], 2))
    st.write("P-value:", round(model_3_2.pvalues[1], 2))
    st.write("R^2:", round(model_3_2.rsquared, 2))

    # 4) cost per beddays - nurses per bed (with two way FE)
    st.header(
        "Two-Way Fixed Effects: Cost per Bedday on Average occupied Beddays (Region + Year)")

    # generate a new dataset were we have the demeaned data to have a bit more overview
    df_fe_2 = df_health_reg.copy()

    # calculate the mean in general
    mean_days_occ = df_fe_2["Avg_Days_Occ"].mean()
    mean_cost = df_fe_2["cost_per_bedday"].mean()

    # demean year and regions / used a bit help of AI with .transform
    region_mean_days_occ = df_fe_2.groupby(
        "Region")["Avg_Days_Occ"].transform("mean")
    year_mean_days_occ = df_fe_2.groupby(
        "Year")["Avg_Days_Occ"].transform("mean")

    region_mean_cost = df_fe_2.groupby(
        "Region")["cost_per_bedday"].transform("mean")
    year_mean_cost = df_fe_2.groupby(
        "Year")["cost_per_bedday"].transform("mean")

    # generate the new datapoints by using double demeaning (thanks to ronak jain and intermediate econometrics)
    df_fe_2["days_dd"] = (df_fe_2["Avg_Days_Occ"] -
                          region_mean_days_occ - year_mean_days_occ + mean_days_occ)
    df_fe_2["cost_dd"] = (df_fe_2["cost_per_bedday"] -
                          region_mean_cost - year_mean_cost + mean_cost)

    # #regress and plot as used to above
    # X4 = df_fe_2[["days_dd"]]
    # y4 = df_fe_2["cost_dd"]

    # removing influential datapoints in retrospect as the regression had some influential datapoints by looking at the cooks distance
    # (used AI for the Code, Intution done by ourselves)
    X4 = sm.add_constant(df_fe_2[["days_dd"]])
    y4 = df_fe_2["cost_dd"]
    model_fe_2 = sm.OLS(y4, X4).fit()
    influence = model_fe_2.get_influence()
    df_fe_2["cooks_d2"] = influence.cooks_distance[0]
    # using just the 4/n rule for the definition of outliers
    threshold = 4 / len(df_fe_2)
    df_fe_clean_2 = df_fe_2[df_fe_2["cooks_d2"] < threshold]

    Xc2 = sm.add_constant(df_fe_clean_2[["days_dd"]])
    yc2 = df_fe_clean_2["cost_dd"]
    model_fe_clean_2 = LinearRegression().fit(Xc2, yc2)
    df_fe_clean_2["regline_dd"] = model_fe_clean_2.predict(Xc2)

    plt.figure()
    plt.scatter(df_fe_clean_2["days_dd"], df_fe_clean_2["cost_dd"],
                label="Data (within Region & Year)")
    plt.plot(df_fe_clean_2["days_dd"], df_fe_clean_2["regline_dd"],
             label="Two-Way FE Regression", color="magenta")
    plt.xlabel("Avg. Beddays (within Region & Year)")
    plt.ylabel("Cost per Bedday (within Region & Year)")
    plt.legend()

    st.pyplot(plt)

    # 4.2) adding some statistical key figures
    Xc2 = sm.add_constant(Xc2)
    model_fe_clean_2 = sm.OLS(yc2, Xc2).fit()

    st.write("Slope:", round(model_fe_clean_2.params["days_dd"], 2))
    st.write("Std. Error:", round(model_fe_clean_2.bse["days_dd"], 2))
    st.write("P-value:", round(model_fe_clean_2.pvalues[1], 2))
    st.write("R^2:", round(model_fe_clean_2.rsquared, 2))


with tab4:
    import matplotlib.pyplot as plt
    st.subheader("Overview merged Dataset")
    st.write("For our project, we used available datasets from the Federal Statistic Office Switzerland and merged them into one main dataset. "
             "Feel free to look at the it and make use of the filter option if you are interested in specific variables, regions or years.")

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
