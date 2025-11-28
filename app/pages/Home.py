import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image

st.set_page_config(
    page_title="Swiss Hospital Analysis",
    page_icon="🏥",
    layout="wide")


HERE = Path(__file__).resolve().parent
HERO_IMG = HERE.parent.parent / "images" / "hospital.jpg"

original_img = Image.open(HERO_IMG)
w, h = original_img.size
crop_fraction = 0.35      # << hier ändern nach Wunsch
crop_height = int(h * crop_fraction)
top = (h - crop_height) // 2
bottom = top + crop_height
cropped_img = original_img.crop((0, top, w, bottom))
st.image(cropped_img, use_container_width=True)

st.markdown(
    """
    <div style="text-align:left; font-size:11px; opacity:0.7;">
        Source:
        <a href="https://www.nytimes.com/2017/02/22/well/live/bad-hospital-design-is-making-us-sicker.html"
           target="_blank"
           style="color:inherit; text-decoration:none;">
            NYTimes
        </a>
    </div>
    """,
    unsafe_allow_html=True)


# Text

st.title("Behind the Numbers: A Data Story About Switzerland’s Hospitals")

st.markdown(
    "Switzerland’s healthcare landscape is changing — fewer hospitals, rising costs, "
    "and significant regional differences. Our analysis explores what the data reveals "
    "about capacity, efficiency, and the pressures shaping today’s hospital system.")

st.write("")  # small space

# creating to boxes
col_left, col_right = st.columns(2, gap="large")

# Box 1: Research Questions
with col_left:
    with st.container(border=True):
        st.subheader("🔍 Our Guiding Questions")
        st.write(
            """
1. **How have the number of hospitals and beds changed** in light of demographic developments?  
2. **What drives rising costs** in the Swiss hospital system?  
   • How do **staffing levels** and **bed occupancy** influence efficiency?  
3. **How do the major regions differ** in their hospital structures and capacities?  
4. **What impact did the 2020 pandemic** have on the hospital system?  
5. **Which key indicators can help hospitals** plan resources more efficiently?  
            """
        )

# Box 2: Overview
with col_right:
    with st.container(border=True):
        st.subheader("🧭 How to Navigate This App")
        st.write(
            """
**Swiss Hospital Data**  
Explore national trends from 2010–2023: beds, staff, occupancy, costs and regional differences.

**Sample Hospital Dashboard**  
A simulated hospital view with internal key indices: bed occupancy, staffing mix, patient composition and cost metrics.
The data for this Dashboard was synthetically generated and therefore not inteded as a numerical interpretation.
            """)

st.write("")  # space

# Box 3: Navigation
with st.container(border=True):
    st.subheader("🚀 Start Exploring")

    col8, col9 = st.columns(2)

    with col8:
        btn_data = st.button(
            "➡️ Explore Facts and Figures about Swiss Hospitals")

    with col9:
        btn_dash = st.button("➡️ Explore Dashboard for Sample Hospital")

    if btn_data:
        st.switch_page("pages/Facts_and_Figures.py")

    if btn_dash:
        st.switch_page("pages/Dashboard_for_Sample_Hospital.py")
