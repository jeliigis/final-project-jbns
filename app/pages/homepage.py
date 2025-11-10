import streamlit as st
import pandas as pd


# content

st.title("Switzerland's Hospital System: Between Performance and Bottleneck.")
st.subheader("Discover how Swiss hospitals have evolved over the past decade — where resources are optimally used, where inefficiencies occur, and how data-driven planning can shape the future of healthcare.")
st.markdown("This dashboard provides an analytical view of the Swiss hospital landscape.  It highlights efficiency trends, capacity imbalances, and regional differences —  helping healthcare planners make better, data-driven decisions for the future")
st.set_page_config(
    page_title="Swiss Hospital Dashboard",
    page_icon="🏥",  # ← das ist dein favicon!
    layout="wide"
)
