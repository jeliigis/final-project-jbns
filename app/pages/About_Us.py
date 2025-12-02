import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image


st.subheader("About us")
st.markdown("We are Jeremy and Jelena, economic students at UZH. As a part of a module in our bachelors degree, we examined "
            "health data from Swiss hospitals over the last decade.")

if st.button("Jeremy's GitHub"):
    st.markdown("[Open GitHub](https://github.com/jeriigis)")

if st.button("Jelena's GitHub"):
    st.markdown("[Open GitHub](https://github.com/jeliigis)")
