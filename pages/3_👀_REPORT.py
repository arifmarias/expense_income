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

def interactive_df(data):
   gb = GridOptionsBuilder.from_dataframe(data)
   gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10) #Add pagination
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
    # height=350, 
    width='100%',
    reload_data=True
    )
   data = grid_response['data']
   # AgGrid(data)


# -------------- SETTINGS --------------
currency = "৳"
page_title = "Al-Barakah Tracker"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
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
# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["মাছের হিসাব", "ছাগলের হিসাব"],
    icons=["bar-chart-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# ----- Visualization for FISH ------------
with st.form("saved_periods"):
   if selected == "মাছের হিসাব":
    # ----- GET ALL FISH DATA FROM DATABASE------------
    items = db.fetch_all_periods()
    df_fish = pd.DataFrame(items)
    # ----- SEARCHBOX ------------
    period = df_fish["period"].drop_duplicates().sort_values(ascending=False)
    year = st.selectbox("সাল সিলেক্ট করুন", period)
    # ----- REPORT TYPE ------------
    left_column, right_column = st.columns(2)
    submitted = left_column.form_submit_button("রিপোর্ট")
    full_report = right_column.form_submit_button("ডিটেইল রিপোর্ট")
    if submitted:
        items_1 = db.fetch_all_periods_invest()
        df_invest = pd.DataFrame(items_1)
        total_investment = df_invest[(df_invest["cat_investment"]=="মাছ") & (df_invest["period"]==year) ]["amount"].sum()
        # ----- KPI ------------
        st.markdown("""---""")
        total_income = df_fish[df_fish["period"] == year]["incomes"].sum()
        total_expense = df_fish[df_fish["period"] == year]["expenses"].sum()
        left_column, middle_column, right_column = st.columns(3)
        with left_column:
            st.subheader("মোট আয়")
            st.subheader(f"৳ {total_income:,}")
        with middle_column:
            st.subheader("মোট ব্যায়")
            st.subheader(f"৳ {total_expense:,}")
        with right_column:
            st.subheader("মোট বিনিয়োগ")
            st.subheader(f"৳ {total_investment:,}")
        st.markdown("""---""")

        # ----- GROUPWISE TOTAL EXPENSE ------------
        df_fish_expense = df_fish[(df_fish["period"] == year) & (df_fish["expenses_cat"]!='null')]
        expense_by_categories = df_fish_expense.groupby(by=["expenses_cat"]).sum()[['expenses']].sort_values(by="expenses", ascending = False)
        fig_expense = px.pie(expense_by_categories, values='expenses', names=expense_by_categories.index, title="খাত অনুযায়ী ব্যায়")
        expense_by_month = df_fish_expense.groupby(by=["year_month"]).sum()[['expenses']].sort_values(by="expenses", ascending = False)
        fig_expense_month = px.bar(expense_by_month, x=expense_by_month.index, y='expenses', title="মাস অনুযায়ী ব্যায়", labels={'year_month':'মাস', 'expenses':'খরচ'})

        # ----- GROUPWISE TOTAL INCOME ------------
        df_fish_income = df_fish[(df_fish["period"] == year) & (df_fish["incomes_cat"]!='null')]
        income_by_categories = df_fish_income.groupby(by=["incomes_cat"]).sum()[['incomes']].sort_values(by="incomes", ascending = False)
        fig_income = px.pie(income_by_categories, values='incomes', names=income_by_categories.index, title="খাত অনুযায়ী আয়")


        # ----- TABLE VIZ FOR INCOME AND EXPENSE ------------
        left_column, right_column = st.columns(2)
        left_column.table(expense_by_categories.reset_index().rename(columns={'expenses_cat':'ব্যায়র খাত','expenses':'মোট টাকা'}))
        right_column.table(income_by_categories.reset_index().rename(columns={'incomes_cat':'আয়ের খাত','incomes':'মোট টাকা'}))

        # ----- PIE-CHART VIZ FOR INCOME AND EXPENSE ------------
        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_expense, use_container_width=True)
        right_column.plotly_chart(fig_income, use_container_width=True)
        
        # ----- BAR-CHART VIZ FOR INCOME AND EXPENSE ------------
        #left_column, right_column = st.columns(2)
        st.plotly_chart(fig_expense_month, use_container_width=True)
        
    
    if full_report:
       # ----- DETAILS EXPENSE ------------
       st.markdown("""---""")
       st.write(year + "- সালের ব্যায়র ডিটেইল রিপোর্ট")
       df_fish_expense_detail = df_fish[(df_fish["period"] == year) & (df_fish["expenses_cat"]!='null')]
       df_fish_expense_detail = df_fish_expense_detail[["input_date", "expenses_cat","expenses","comment"]]
       df_fish_expense_detail["input_date"] = pd.to_datetime(df_fish_expense_detail["input_date"], dayfirst=True)
       df_fish_expense_detail = df_fish_expense_detail.sort_values("input_date", ascending=False)
       df_fish_expense_detail["input_date"] = df_fish_expense_detail["input_date"].dt.strftime('%d/%m/%Y')
       df_fish_expense_detail_rename = df_fish_expense_detail.rename(columns= {"input_date": "তারিখ", "expenses_cat":"ব্যায়র খাত", "expenses":"মোট টাকা", "comment":"বিবরণ"})
       interactive_df(df_fish_expense_detail_rename)

       # ----- DETAILS INCOME ------------
       st.markdown("""---""")
       st.write(year + "- সালের আয়ের ডিটেইল রিপোর্ট")
       df_fish_income_detail = df_fish[(df_fish["period"] == year) & (df_fish["incomes_cat"]!='null')]
       df_fish_income_detail = df_fish_income_detail[["input_date", "incomes_cat","incomes","comment"]]
       df_fish_income_detail["input_date"] = pd.to_datetime(df_fish_income_detail["input_date"], dayfirst=True)
       df_fish_income_detail = df_fish_income_detail.sort_values("input_date", ascending=False)
       df_fish_income_detail["input_date"] = df_fish_income_detail["input_date"].dt.strftime('%d/%m/%Y')
       df_fish_income_detail_rename = df_fish_income_detail.rename(columns= {"input_date": "তারিখ", "incomes_cat":"ব্যায়র খাত", "incomes":"মোট টাকা", "comment":"বিবরণ"})
       interactive_df(df_fish_income_detail_rename)

       

with st.form("saved_periods_goat"):
   # ----- Visualization for GOAT ------------
   if selected == "ছাগলের হিসাব":
    # ----- GET ALL GOAT DATA FROM DATABASE------------
    items = db.fetch_all_periods_goat()
    df_goat = pd.DataFrame(items)

    # ----- SEARCHBOX ------------
    period = df_goat["period"].drop_duplicates().sort_values(ascending=False)
    year = st.selectbox("সাল সিলেক্ট করুন", period)

    # ----- REPORT TYPE ------------
    left_column, right_column = st.columns(2)
    submitted = left_column.form_submit_button("রিপোর্ট")
    full_report = right_column.form_submit_button("ডিটেইল রিপোর্ট")
    if submitted:
        items_1 = db.fetch_all_periods_invest()
        df_invest = pd.DataFrame(items_1)
        total_investment = df_invest[(df_invest["cat_investment"]=="ছাগল") & (df_invest["period"]==year)]["amount"].sum()
        # ----- KPI ------------
        st.markdown("""---""")
        total_income = df_goat[df_goat["period"] == year]["incomes"].sum()
        total_expense = df_goat[df_goat["period"] == year]["expenses"].sum()
        left_column, middle_column, right_column = st.columns(3)
        with left_column:
            st.subheader("মোট আয়:")
            st.subheader(f"৳ {total_income:,}")
        with middle_column:
            st.subheader("মোট ব্যায়")
            st.subheader(f"৳ {total_expense:,}")
        with right_column:
            st.subheader("মোট বিনিয়োগ")
            st.subheader(f"৳ {total_investment:,}")
        st.markdown("""---""")

        # ----- GROUPWISE TOTAL EXPENSE ------------
        df_goat_expense = df_goat[(df_goat["period"] == year) & (df_goat["expenses_cat"]!='null')]
        expense_by_categories = df_goat_expense.groupby(by=["expenses_cat"]).sum()[['expenses']].sort_values(by="expenses", ascending = False)
        fig_expense = px.pie(expense_by_categories, values='expenses', names=expense_by_categories.index, title="খাত অনুযায়ী ব্যায়")
        expense_by_month = df_goat_expense.groupby(by=["year_month"]).sum()[['expenses']].sort_values(by="expenses", ascending = False)
        fig_expense_month = px.bar(expense_by_month, x=expense_by_month.index, y='expenses', title="মাস অনুযায়ী ব্যায়", labels={'year_month':'মাস', 'expenses':'খরচ'})


        # ----- GROUPWISE TOTAL INCOME ------------
        df_goat_income = df_goat[(df_goat["period"] == year) & (df_goat["incomes_cat"]!='null')]
        income_by_categories = df_goat_income.groupby(by=["incomes_cat"]).sum()[['incomes']].sort_values(by="incomes", ascending = False)
        fig_income = px.pie(income_by_categories, values='incomes', names=income_by_categories.index, title="খাত অনুযায়ী আয়")


        # ----- TABLE VIZ FOR INCOME AND EXPENSE ------------
        left_column, right_column = st.columns(2)
        left_column.table(expense_by_categories.reset_index().rename(columns={'expenses_cat':'ব্যায়র খাত','expenses':'মোট টাকা'}))
        right_column.table(income_by_categories.reset_index().rename(columns={'incomes_cat':'আয়ের খাত','incomes':'মোট টাকা'}))

        # ----- PIE-CHART VIZ FOR INCOME AND EXPENSE ------------
        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_expense, use_container_width=True)
        right_column.plotly_chart(fig_income, use_container_width=True)

        # ----- BAR-CHART VIZ FOR INCOME AND EXPENSE ------------
        #left_column, right_column = st.columns(2)
        st.plotly_chart(fig_expense_month, use_container_width=True)
    
    if full_report:
       # ----- DETAILS EXPENSE ------------
       st.markdown("""---""")
       st.write(year + "- সালের ব্যায়র ডিটেইল রিপোর্ট")
       df_goat_expense_detail = df_goat[(df_goat["period"] == year) & (df_goat["expenses_cat"]!='null')]
       df_goat_expense_detail = df_goat_expense_detail[["input_date", "expenses_cat","expenses","comment"]]
       df_goat_expense_detail_rename = df_goat_expense_detail.rename(columns= {"input_date": "তারিখ", "expenses_cat":"ব্যায়র খাত", "expenses":"মোট টাকা", "comment":"বিবরণ"})
       interactive_df(df_goat_expense_detail_rename)


       # ----- DETAILS INCOME ------------
       st.markdown("""---""")
       st.write(year + "- সালের আয়ের ডিটেইল রিপোর্ট")
       df_goat_income_detail = df_goat[(df_goat["period"] == year) & (df_goat["incomes_cat"]!='null')]
       df_goat_income_detail = df_goat_income_detail[["input_date", "incomes_cat","incomes","comment"]]
       df_goat_income_detail_rename = df_goat_income_detail.rename(columns= {"input_date": "তারিখ", "incomes_cat":"ব্যায়র খাত", "incomes":"মোট টাকা", "comment":"বিবরণ"})
       interactive_df(df_goat_income_detail_rename)
