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
    unsafe_allow_html=True
)


st.title("Switzerland's Hospital System: Between Performance and Bottleneck")
st.subheader("Did you know that despite demographic change and the resulting increase in demand for staff in our healthcare system, the number of hospitals and beds has decreased in recent years? "
             "That there are significant regional differences in the efficiency of medical device usage? ")

st.write("In our Streamlit web app, we focus on two main areas of content: "
         "Under *Swiss Hospital Data*, you will find visualizations and statistical tools designed to shed light on Swiss hospitals in retrospect.  The data set is based on data provided by the Federal Statistical Office and covers the years 2010–2023. "
         "Secondly, we have used a *dashboard* to simulate a Swiss hospital, illustrating the most important key figures and implementing some resulting diagrams. "
         "Although the content of this dashboard cannot be interpreted, it is intended to highlight mechanisms that would make it easier for hospitals to plan for the future in order to save costs.")

# Buttons
col8, col9 = st.columns(2)

with col8:
    btn_data = st.button("➡️ Explore Facts and Figures about Swiss Hospitals")

with col8:
    btn_dash = st.button("➡️ Explore Dashboard for Sample Hospital")

if btn_data:
    st.switch_page("pages/Facts_and_Figures.py")

if btn_dash:
    st.switch_page("pages/Dashboard_for_Sample_Hospital.py")

# About us
st.subheader("About us")
st.markdown("We are Jeremy and Jelena, economics students at UZH. As a part of a module in our bachelors degree program, we examined "
            "health data from Swiss hospitals over the last decade. We are both completely newbies in programming and data analysis but this project is just "
            "the start of some further projects. Hopefully : )")
