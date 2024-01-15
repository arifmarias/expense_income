import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
import pandas as pd
import numpy as np
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from streamlit_extras.switch_page_button import switch_page
import database as db  # local import

# -------------- SETTINGS --------------
currency = "৳"
page_title = "Hero's Self Tracker"
page_icon = ":moneybag:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
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
    options=["বিনিয়োগ-ব্যায় এন্ট্রি", "বিনিয়োগ-ব্যায় রিপোর্ট"],
    icons=["", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

if selected == "বিনিয়োগ-ব্যায় এন্ট্রি":
    # --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
    years = [datetime.today().year, datetime.today().year + 1]
    months = list(calendar.month_name[1:])
    d = st.date_input("তারিখ")
    year = d.year
    month = d.month
    day = d.day
    total_investment = 0
    total_spend = 0
    "---"
    with st.form("entry_form", clear_on_submit=True):
        with st.expander("বিনিয়োগ / পেয়েছি"):
            invest_cat = st.selectbox("কিভাবে পেয়েছি",('বিকাশ','ব্যাঙ্ক','ব্যবসা হতে'))
            invest_amount = st.number_input("টাকার (৳) পরিমান", key="1")
        
        with st.expander("ব্যায় / দিয়েছি"):
            spend_cat = st.selectbox("ব্যায়ের খাত",('জমি কিনা', 'মাছ', 'মিল', 'নিজ', 'দান','ছাগল','মামাকে দেয়া'))
            spend_amount = st.number_input("টাকার (৳) পরিমান", key="2")

        with st.expander("বিবরণ"):
            comment = st.text_area("", placeholder="Enter a comment here ...")
        
        "---"
        submitted = st.form_submit_button("Save Data")
        if submitted:
            input_date = str(day) + "/" + str(month) + "/" +str(year)
            year_month = str(year) + "_" + str(month)
            period = str(year)
            hero = db.fetch_all_periods_hero()
            df_hero = pd.DataFrame(hero)
            if df_hero.empty:
                if invest_amount >0:
                    total_investment = invest_amount
                if spend_amount >0:
                    total_spend = spend_amount
                total_balance = total_investment - total_spend
                db.insert_period_hero(str(datetime.utcnow()), input_date, period, year_month, invest_cat,invest_amount, total_investment, spend_cat,spend_amount, total_spend, total_balance, comment)
                st.success("Data saved!")
            else:
                if invest_amount>0:
                    total_investment = df_hero['invest_amount'].sum() + invest_amount
                    total_spend = df_hero['spend_amount'].sum() + spend_amount
                    total_balance = total_investment - total_spend
                    db.insert_period_hero(str(datetime.utcnow()), input_date, period, year_month, invest_cat,invest_amount, total_investment, "-",spend_amount, total_spend, total_balance, comment)
                    st.success("Data saved!")
                if spend_amount>0:
                    total_investment = df_hero['invest_amount'].sum() + invest_amount
                    total_spend = df_hero['spend_amount'].sum() + spend_amount
                    total_balance = total_investment - total_spend
                    db.insert_period_hero(str(datetime.utcnow()), input_date, period, year_month, "-",invest_amount, total_investment, spend_cat,spend_amount, total_spend, total_balance, comment)
                    st.success("Data saved!")
            # update = db.fetch_all_periods_hero()
            # update_df = pd.DataFrame(update)
            # update_df = update_df[["input_date","comment","invest_amount","total_investment","spend_amount","total_spend","total_balance"]]
            # update_df_rename = update_df.rename(columns={"input_date": "তারিখ","comment":"বিবরণ","invest_amount":"পেয়েছি", "total_investment":"মোট পেয়েছি/বিনিয়োগ","spend_amount":"দিয়েছি","total_spend":"মোট দিয়েছি/ব্যায়","total_balance":"ব্যালান্স/অবশিষ্ট" })
            # st.table(update_df_rename)

if selected == "বিনিয়োগ-ব্যায় রিপোর্ট":
    items = db.fetch_all_periods_hero()
    df_hero = pd.DataFrame(items)
    st.markdown("""---""")
    #st.subheader(year + "- সালের রিপোর্ট")
    if not df_hero.empty:
        df_hero_report = df_hero[["key","input_date","comment","invest_cat","invest_amount","total_investment","spend_cat","spend_amount","total_spend","total_balance"]]
        # df_hero_report["input_date"] = pd.to_datetime(df_hero_report["input_date"], dayfirst=True)
        # df_hero_report = df_hero_report.sort_values("input_date", ascending=False)
        df_hero_report = df_hero_report.sort_values("key", ascending=False)
        # df_hero_report["input_date"] = df_hero_report["input_date"].dt.strftime('%d/%m/%Y')
        df_hero_report = df_hero_report[["input_date","comment","invest_cat","invest_amount","total_investment","spend_cat","spend_amount","total_spend","total_balance"]]
        df_hero_select = df_hero_report[["input_date","comment","invest_cat","invest_amount","spend_cat","spend_amount","total_balance"]]
        df_hero_report_rename = df_hero_select.rename(columns={"input_date": "তারিখ","comment":"বিবরণ","invest_cat":"কিভাবে পেয়েছি","invest_amount":"পেয়েছি", "spend_cat":"কোথায় দিয়েছি","spend_amount":"দিয়েছি","total_balance":"ব্যালান্স/অবশিষ্ট" })
        col1, col2, col3 = st.columns(3)
        tti = df_hero_report["total_investment"].values[0]
        tte = df_hero_report["total_spend"].values[0]
        ttb = df_hero_report["total_balance"].values[0]
        col1.metric("মোট পেয়েছি ",f"৳ {tti:,}")
        col2.metric("মোট দিয়েছি ",f"৳ {tte:,}")
        col3.metric("অবশিষ্ট আছে ",f"৳ {ttb:,}")
        st.markdown("""---""")
        st.write(":sunglasses: :blue[ডিটেইল রিপোর্ট]")
        st.table(df_hero_report_rename)
    # with st.form("saved_periods"):
        
        # ----- SEARCHBOX ------------
        # period = df_hero["period"].drop_duplicates().sort_values(ascending=False)
        # year = st.selectbox("সাল সিলেক্ট করুন", period)
        # left_column, right_column = st.columns(2)
        # submitted = left_column.form_submit_button("রিপোর্ট")
        # if submitted:
            
