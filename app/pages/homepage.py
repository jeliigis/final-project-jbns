import streamlit as st
import pandas as pd


# content

st.title("Switzerland's Hospital System: Between Performance and Bottleneck.")
st.subheader("Discover how Swiss hospitals have evolved over the past decade — where resources are optimally used, where inefficiencies occur, and how data-driven planning can shape the future of healthcare.")
st.markdown("This dashboard provides an analytical view of the Swiss hospital landscape.  It highlights efficiency trends, capacity imbalances, and regional differences —  helping healthcare planners make better, data-driven decisions for the future")
st.set_page_config(
    page_title="Swiss Hospital Dashboard",
    page_icon="🏥",  # ← das ist dein favicon!
    layout="wide")

# first attempt of heatmapping: 10.11.25

# for col in ["Examinations_per_Device", "Beds_per_Nurse", "Beds_per_Doctor"]:
# df[col + "_norm"] = (
# (df[col] - df[col].min()) / (df[col].max() - df[col].min())
# ) * 100  # normiert auf 0–100
