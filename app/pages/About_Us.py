import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image


st.subheader("About us")
st.markdown("We are Jeremy and Jelena, economics students at UZH. As a part of a module in our bachelors degree program, we examined "
            "health data from Swiss hospitals over the last decade. We are both completely newbies in programming and data analysis but this project is just "
            "the start of some further projects. Hopefully : )")

if st.button("Jeremy's GitHub"):
    st.markdown("[Open GitHub](https://github.com/jeriigis)")

if st.button("Jelena's GitHub"):
    st.markdown("[Open GitHub](https://github.com/jeliigis)")
