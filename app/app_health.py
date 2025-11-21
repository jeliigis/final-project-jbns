import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Home = st.Page("pages/Home.py")
Swiss_Hospital_Data = st.Page("pages/Swiss_Hospital_Data.py")
Dashboard = st.Page("pages/Dashboard.py")
user_pages = [Home, Swiss_Hospital_Data, Dashboard]

pg = st.navigation(user_pages, position="sidebar", expanded=True)
pg.run()
