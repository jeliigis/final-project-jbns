import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Home = st.Page("pages/Home.py")
Facts_and_Figures = st.Page(
    "pages/Facts_and_Figures.py")
Dashboard_for_Sample_Hospital = st.Page(
    "pages/Dashboard_for_Sample_Hospital.py")
About_Us = st.Page("pages/About_Us.py")


user_pages = [Home, Facts_and_Figures,
              Dashboard_for_Sample_Hospital, About_Us]

pg = st.navigation(user_pages, position="sidebar", expanded=True)
pg.run()
