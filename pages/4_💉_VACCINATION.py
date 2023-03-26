import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
import pandas as pd
import plotly.express as px
import streamlit as st 
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import database as db

def interactive_df(data):
   gb = GridOptionsBuilder.from_dataframe(data)
   gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
   gb.configure_side_bar() #Add a sidebar
   #gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
   gridOptions = gb.build()
   grid_response = AgGrid(
    data,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=False,
    theme='streamlit', #Add theme color to the table
    enable_enterprise_modules=True,
    height=350, 
    width='100%',
    reload_data=True
    )

# -------------- SETTINGS --------------
currency = "৳"
page_title = "Al-Barakah Tracker"
page_icon = ":octocat:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)


# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["টিকা এন্ট্রি", "টিকার রিপোর্ট"],
    icons=["", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)