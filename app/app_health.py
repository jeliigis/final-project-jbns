import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

homepage = st.Page("pages/homepage.py")
data_page = st.Page("pages/data_overview.py")

user_pages = [homepage, data_page]

pg = st.navigation(user_pages, position="sidebar", expanded=True)
pg.run()
