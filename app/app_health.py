import pandas as pd
import streamlit as st
st.title('Final Project Team igis')
st.header("Welcome to our Dashboard!")
st.markdown("With our Data Analysis we want to show where bottlenecks occur, where there is potential overcapacities and how hospitals and planners can work with that.")
st.markdown("Test")

df_health = pd.read_excel("../data/df_health.xlsx")
st.dataframe(df_health)
