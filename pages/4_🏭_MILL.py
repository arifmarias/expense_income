import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
import pandas as pd
import plotly.express as px
import streamlit as st 
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import database as db
from streamlit_extras.switch_page_button import switch_page


# -------------- SETTINGS --------------
currency = "৳"
page_title = "Al-Barakah Tracker"
page_icon = ":factory:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
home = st.button("HOME 🏠")
if home:
    switch_page("HOME")
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

# --- INCOME and EXPENSE ---
incomes = ["দৈনিক বিক্রি", "অন্যানো"]
expenses = ["ঘর ও পরিবেশ উন্নয়ন", "কাঁচামাল ক্রয়"]
expenses_daily_monthly = ["দৈনিক খরচ","লেবার বিল", "বিদ্যুৎ বিল"]
expenses_mill = ["লাইসেন্স ", "মেশিন ক্রয় ", "মেশিনের যন্ত্রপাতি ক্রয় ", "প্রাতিষ্ঠানিক খরচ - অন্যানো"]
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

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["মিলের হিসাব"],
    icons=["bag-check-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# --- INPUT & SAVE PERIODS FISH ---
if selected == "মিলের হিসাব":
    "---"
    with st.form("entry_form", clear_on_submit=True):
        with st.expander("আয়"):
            for income in incomes:
                st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income)
        with st.expander("ব্যায় (কাঁচামাল ও ঘর উন্নয়ন )"):
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)
        with st.expander("দৈনিক ও মাসিক ব্যায়"):
            for expense in expenses_daily_monthly:
                st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)
        with st.expander("প্রাতিষ্ঠানিক ব্যায়"):
            for expense in expenses_mill:
                st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)
        with st.expander("বিবরণ"):
            comment = st.text_area("", placeholder="Enter a comment here ...")
        
        "---"
        submitted = st.form_submit_button("Save Data")
        if submitted:
            input_date = str(day) + "/" + str(month) + "/" +str(year)
            year_month = str(year) + "_" + str(month)
            period = str(year)
            incomes = {income: st.session_state[income] for income in incomes }
            expenses = {expense: st.session_state[expense] for expense in expenses}
            expenses_daily_monthly = {expense: st.session_state[expense] for expense in expenses_daily_monthly}
            expenses_mill = {expense: st.session_state[expense] for expense in expenses_mill}
            # ---- Add to Database MILL Income -------
            for key,val in incomes.items():
                if val>0:
                    my_income = val
                    # (current, period, year_month,  cat_income, incomes, cat_expenses, expenses, comment)
                    db.insert_period_mill(str(datetime.utcnow()), input_date, period, year_month, key, val, "null", 0, comment)
                    #del st.session_state[income]
            
            # ---- Add to Database MILL Expense -------
            for key,val in expenses.items():
                if val>0:
                    my_expense = val
                    # (current, period, year_month,  cat_income, incomes, cat_expenses, expenses, comment)
                    db.insert_period_mill(str(datetime.utcnow()), input_date, period, year_month, "null", 0, key, val, comment)
            
            for key,val in expenses_daily_monthly.items():
                if val>0:
                    my_expense = val
                    # (current, period, year_month,  cat_income, incomes, cat_expenses, expenses, comment)
                    db.insert_period_mill(str(datetime.utcnow()), input_date, period, year_month, "null", 0, key, val, comment)
            
            for key,val in expenses_mill.items():
                if val>0:
                    my_expense = val
                    # (current, period, year_month,  cat_income, incomes, cat_expenses, expenses, comment)
                    db.insert_period_mill(str(datetime.utcnow()), input_date, period, year_month, "null", 0, key, val, comment)
            items = db.fetch_all_periods_mill()
            df = pd.DataFrame(items)     
            # st.table(df)
            # st.session_state["fish"] = df
            st.success("Data saved!")