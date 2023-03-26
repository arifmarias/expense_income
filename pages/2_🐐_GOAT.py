import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
import pandas as pd
import numpy as np

import plotly.graph_objects as go  # pip install plotly
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_extras.switch_page_button import switch_page

import database as db  # local import


incomes_g = ["ছাগল বিক্রি", "অন্যানো"]
expenses_g = ["নতুন ছাগল কিনা", "ঘর ও পরিবেশ উন্নয়ন", "ছাগলের খাবার", "লেবার বিল", "অন্যানো খরচ(টিকা ও ডাক্তার)"]

currency = "৳"
page_title = "Al-Barakah Tracker"
page_icon = ":goat:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
home = st.button("HOME 🏠")
if home:
    switch_page("HOME")
st.title(page_title + " " + page_icon)


# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])
d = st.date_input("তারিখ")
year = d.year
month = d.month
day = d.day

# --- DATABASE INTERFACE ---
def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods

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
    options=["ছাগলের হিসাব"],
    icons=["pencil-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)



# --- INPUT & SAVE PERIODS GOAT ---
if selected == "ছাগলের হিসাব":
    "---"
    st.cache_data.clear()
    st.session_state.load_state = False
    with st.form("entry_form", clear_on_submit=True):
        with st.expander("আয়"):
            for income in incomes_g:
                st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income)
        with st.expander("ব্যায়"):
            for expense in expenses_g:
                st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)
        with st.expander("বিবরণ"):
            comment = st.text_area("", placeholder="Enter a comment here ...")
        
        "---"
        submitted = st.form_submit_button("Save Data")
        if submitted:
            input_date = str(day) + "/" + str(month) + "/" +str(year)
            year_month = str(year) + "_" + str(month)
            period = str(year)
            incomes = {income: st.session_state[income] for income in incomes_g }
            expenses = {expense: st.session_state[expense] for expense in expenses_g}
            
            # ---- Add to Database GOAT Income -------
            for key,val in incomes.items():
                if val>0:
                    my_income = val
                    # (current, period, year_month, cat_income, incomes, cat_expenses, expenses, comment)
                    db.insert_period_goat(str(datetime.utcnow()), input_date, period, year_month, key, val, "null", 0, comment)
            
            # ---- Add to Database GOAT Expense -------
            for key,val in expenses.items():
                if val>0:
                    my_expense = val
                    # (current, period, year_month,  cat_income, incomes, cat_expenses, expenses, comment)
                    db.insert_period_goat(str(datetime.utcnow()), input_date, period, year_month, "null", 0, key, val, comment)
            items = db.fetch_all_periods_goat()
            df = pd.DataFrame(items)         
            st.table(df)
            # st.session_state["goat"] = df
            # st.table(df2)
            st.success("Data saved!")