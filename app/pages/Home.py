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
crop_fraction = 0.35      
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

st.title("Behind the Numbers: A Data Story About Swiss Hospitals")

st.subheader(
    "Switzerland’s healthcare landscape is changing: "
    "fewer hospitals, rising costs, "
    "and significant regional differences. ")

st.markdown("Our analysis explores what Swiss Hospital Data from over a decade reveals "
            "about capacity, efficiency, and the pressures shaping today’s hospital system.")

st.write("")  # small space

# creating to boxes
col_left, col_right = st.columns(2, gap="large")

# Box 1: Research Questions
with col_left:
    with st.container(border=True):
        st.subheader("🔍 Our Guiding Questions")

        # 5 guiding questions

        st.markdown("**Quick Insights:**")

        with st.expander("1) How have hospitals and beds changed?"):
            st.write(
                "In our data, the **number of hospitals decreases over time**, "
                "while the **total number of beds declines more moderately**. "
                "This points to consolidation of hospital sites with slightly higher "
                "bed capacity per remaining hospital."
            )

        with st.expander("2) What drives rising hospital costs?"):
            st.write(
                "Costs correlate strongly with **higher staff expenses** "
                "In the regression graph, it is shown that as the number of nursing staff per bed increases, the costs per patient day also increase. "

            )

        with st.expander("3) How do the regions differ structurally?"):
            st.write(
                "The regional comparison shows clear **differences in examinations/device-rate, "
                "and beds/staff-rate**. "
                "We visualize that **regional differences** exist in terms of **costs per patient day"
                " despite the same nurse-to-bed ratio**."
            )

        with st.expander("4) What impact had the 2020 global pandemic?"):
            st.write(
                "In 2020, contrary to the trend, we are seeing a slight **increase in hospital locations**. "
                "We also have a **high acquisition rate** for medical equipment. "
                "The costs are in line with the upward trend."
            )

        with st.expander("5) Which key indicators improve hospital planning?"):
            st.write(
                "The sample hospital dashboard highlights key indices such as **bed occupancy per department**, "
                "**employment growth**, **patient composition** and **average treatment cost per patient**. "
                "Together, these indicators may support more resource-efficient planning and capacity management."
            )

# Box: Overview
with col_right:
    with st.container(border=True):

        st.subheader("🧭 How to Navigate This WebApp")

        st.markdown("""
**Swiss Hospital Data:**
Explore national trends from 2010–2023: beds & staff-occupancy, costs and regional differences.
        """)

        if st.button("➡️ Explore Facts and Figures about Swiss Hospitals", key="btn_data"):
            st.switch_page("pages/Facts_and_Figures.py")

        st.markdown("---")   # Trenner für optische Klarheit

        st.markdown("""
**Sample Hospital Dashboard:**
A simulated hospital overview with internal key indices: bed occupancy, staffing mix, patient composition and cost metrics.
        """)

        if st.button("➡️ Explore Dashboard for Sample Hospital", key="btn_dash"):
            st.switch_page("pages/Dashboard_for_Sample_Hospital.py")
