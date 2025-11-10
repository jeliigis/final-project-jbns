import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

homepage = st.Page("pages/homepage.py")
data_page = st.Page("pages/data_overview.py")
about_us = st.Page("pages/about_us.py")
about_data = st.Page("pages/about_data.py")

user_pages = [homepage, data_page, about_data, about_us]

pg = st.navigation(user_pages, position="sidebar", expanded=True)
pg.run()
