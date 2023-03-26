import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
import pandas as pd
import numpy as np

import plotly.express as px
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_extras.switch_page_button import switch_page
import database as db  # local import

# -------------- SETTINGS --------------
currency = "৳"
page_title = "Al-Barakah Tracker"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

customized_button = st.markdown("""
    <style >
    div.stButton > button:first-child {
        background-color: #578a00;
        color:#ffffff;
    }
    div.stButton > button:hover {
        background-color: #00128a;
        color:#ffffff;
        }
    </style>""", unsafe_allow_html=True)

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown("""---""")
with st.container(): 
    left_column, right_column = st.columns(2)
    fish = left_column.button("FISH 🐠")
    goat = right_column.button("GOAT 🐐")
    if fish:
        switch_page("FISH")
    if goat:
        switch_page("GOAT")

with st.container(): 
    left_column, right_column = st.columns(2)
    vac = left_column.button("VACCINATION 💉")
    inv = right_column.button("INVESTMENT 💵")
    if vac:
        switch_page("VACCINATION")
    if inv:
        switch_page("INVESTMENT")

with st.container(): 
    left_column,right_column = st.columns(2)
    rep = left_column.button("REPORT ✨")
    if rep:
        switch_page("REPORT")
st.markdown("""---""")