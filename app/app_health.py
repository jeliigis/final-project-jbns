import pandas as pd
import streamlit as st
st.title('Final Project Team igis')
st.header("Welcome to our Dashboard!")
st.markdown("With our Data Analysis we want to show where bottlenecks occur, where there is potential overcapacities and how hospitals and planners can work with that.")
st.markdown("Test")

df_health = pd.read_excel("./data/df_health.xlsx", na_values=["X"])
st.dataframe(df_health)

df_health.info()
df_health["Kost_Total"] = df_health["KostAmbA"] + df_health["KostStatA"]
df_health.head()

###generating a histogram for the total cost in switzerland
df_ch_cost = df_health[df_health["Region"] == "Schweiz"]
st.header("Kostenentwicklung der Akutbehandlung in Schweizer Spitälern (2010-2023)")
df_cost_ch_indexed = df_ch_cost.set_index('Jahr')
st.bar_chart(df_cost_ch_indexed['Kost_Total'])

#generating a bar plot for the total staff trend
df_health["Personal_Total"] = df_health[['MedTechPersonal_Anz_GrVe','MedTechPersonal_Anz_ZeVe','MedTechPersonal_Anz_AllgKr','MedTheraPersonal_Anz_GrVe',	'MedTheraPersonal_Anz_ZeVe','MedTheraPersonal_Anz_AllgKr','Pflegepersonal_Anz_GrVe','Pflegepersonal_Anz_ZeVe','Pflegepersonal_Anz_AllgKr',	'Ärzteschaft_Anz_GrVe',	'Ärzteschaft_Anz_ZeVe',	'Ärzteschaft_Anz_AllgKr']].sum(axis=1)

df_ch_staff = df_health[df_health["Region"]== "Schweiz"]
st.header("Personalentwicklung in Schweizer Spitälern (2010-2023) ")
df_staff_ch_indexed = df_ch_staff.set_index("Jahr")
st.bar_chart(df_staff_ch_indexed["Personal_Total"])


#generating a bar plot for the total infrastructure trend over the years
df_health["Infrastructure_Total"]= df_health[['ANGIOGRAPHIE_Geräte','CT_SCANNER_Geräte','DIALYSE_Geräte','GAMMA_CAMERA_Geräte',	'LINEARBESCHLEUNIGER_Geräte','LITHOTRIPTOR_Geräte',	'MRI_Geräte','PET_SCANNER_Geräte','ANGIOGRAPHIE_Untersuchungen','CT_SCANNER_Untersuchungen','DIALYSE_Untersuchungen','GAMMA_CAMERA_Untersuchungen',	'LINEARBESCHLEUNIGER_Untersuchungen','LITHOTRIPTOR_Untersuchungen','MRI_Untersuchungen','PET_SCANNER_Untersuchungen']].sum(axis=1)
df_ch_infrastructure = df_health[df_health["Region"]== "Schweiz"]
st.header("Infrastructure Development in Swiss Hospitals in 2010-2023")
df_infrastructure_ch_indexed = df_ch_infrastructure.set_index("Jahr")
st.bar_chart(df_infrastructure_ch_indexed["Infrastructure_Total"])