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
page_icon = ":poodle:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
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
    options=["টিকা এন্ট্রি", "টিকার রিপোর্ট", "নতুন ছাগল এন্ট্রি"],
    icons=["", "bar-chart-fill", "pencil-fill", ],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

if selected == "নতুন ছাগল এন্ট্রি":
    # --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
    years = [datetime.today().year, datetime.today().year + 1]
    months = list(calendar.month_name[1:])
    
    "---"
    with st.expander("এন্ট্রি ফর্ম"):
        with st.form("entry_form", clear_on_submit=True):
            g_all = db.fetch_all_periods_animal()
            df_vaccine = pd.DataFrame(g_all)
            if df_vaccine.empty:
                goat_num = 1
                goat_num = int(1)
            else:
                goat_num = df_vaccine["goat_number"].max()
                goat_num = goat_num + 1
                goat_num = int(goat_num)
            
            st.subheader("ছাগল নম্বর : AB-" + str(goat_num) )
            breed = st.selectbox("জাত", options=("ব্ল্যাক বেঙ্গল ছাগল", "যমুনাপারি ছাগল", "বিটল ছাগল", "বোয়ার ছাগল", "বারবারি ছাগল"))
            gender = st.selectbox("জেন্ডার", options=("পুরুষ ছাগল", "মহিলা ছাগল"))
            color = st.text_input("রঙ")
            purchase_or_birth = st.selectbox("কেনা নাকি জন্ম?", options=("কেনা", "জন্ম"))
            d = st.date_input("কেনা বা জন্মের তারিখ")
            year = d.year
            month = d.month
            day = d.day
            age = st.number_input("বর্তমান বয়স (মাস)")
            weight = st.number_input("প্রাথমিক ওজন (কেজি ও গ্রাম)")
            purchase_price = st.number_input("দাম (কেনা হলে)")
            comment = st.text_area("", placeholder="বিবরণ")        
            "---"
            submitted = st.form_submit_button("Save Data")
        
        if submitted:
            input_date = str(day) + "/" + str(month) + "/" +str(year)
            year_month = str(year) + "_" + str(month)
            period = str(year)
            db.insert_new_animal(str(datetime.utcnow()), input_date, period, year_month, goat_num, breed,gender,color,purchase_or_birth,age,weight,purchase_price,comment)

            st.success("Data saved!")
            

if selected == "টিকা এন্ট্রি":
    with st.form("entry_form2", clear_on_submit=True):
        # ----- GET ALL GOAT INFO FROM DATABASE------------
        items = db.fetch_all_periods_animal()
        df_vaccine = pd.DataFrame(items)
        gt_num = "AB-" + df_vaccine["goat_number"].astype(str) + "-" + df_vaccine["color"] + "-" + df_vaccine["breed"]
        gt = st.selectbox("ছাগল সিলেক্ট করুন", gt_num)
        gt = int(gt.split("-")[1])
        "---"
        d = st.date_input("ভেকসিন/মেডিসিন দেয়ার তারিখ")
        year = d.year
        month = d.month
        day = d.day
        reason = st.text_input("ভেকসিন/মেডিসিন দেয়ার কারণ (উপসর্গ)")
        med = st.text_input("ভেকসিন/মেডিসিন")
        med_measure = st.text_input("ভেকসিন/মেডিসিন-এর পরিমান")
        comment = st.text_area(label="বিবরণ", value="", placeholder="বিবরণ")
        "---"
        submitted = st.form_submit_button("Save Data")
    
    if submitted:
            input_date = str(day) + "/" + str(month) + "/" +str(year)
            year_month = str(year) + "_" + str(month)
            period = str(year)
            db.insert_new_vaccination(str(datetime.utcnow()), input_date, period, year_month, gt, reason, med, med_measure,comment)

            st.success("Data saved!")

if selected == "টিকার রিপোর্ট":
    with st.form("entry_form3", clear_on_submit=True):
        # ----- GET ALL GOAT INFO FROM DATABASE------------
        items = db.fetch_all_periods_animal()
        df_animal = pd.DataFrame(items)
        gt_num = "AB-" + df_animal["goat_number"].astype(str) + "-" + df_animal["color"] + "-" + df_animal["breed"]
        gt = st.selectbox("ছাগল সিলেক্ট করুন", gt_num)
        gt = int(gt.split("-")[1])
        left_column, right_column = st.columns(2)
        submitted = left_column.form_submit_button("রিপোর্ট")
        # full_report = right_column.form_submit_button("ডিটেইল রিপোর্ট")
        if submitted:
            st.markdown("""---""")
            st.write("ছাগল নম্বর  AB- " + str(gt) + " -এর ভেকসিন/মেডিসিন ডিটেইল রিপোর্ট")
            vacc = db.fetch_all_periods_vaccination()
            df_vacc = pd.DataFrame(vacc)
            df_vacc_goat = df_vacc[df_vacc["goat_number"] == gt][["input_date", "reason", "med","med_measure","comment"]]
            df_vacc_goat["input_date"] = pd.to_datetime(df_vacc_goat["input_date"], dayfirst=True)
            df_vacc_goat = df_vacc_goat.sort_values("input_date", ascending=False)
            df_vacc_goat["input_date"] = df_vacc_goat["input_date"].dt.strftime('%d/%m/%Y')
            df_vacc_goat_rename = df_vacc_goat.rename(columns= {"input_date": "তারিখ", "reason":"উপসর্গ", "med":"ভেকসিন/মেডিসিন", "med_measure":"ভেকসিন/মেডিসিন-এর পরিমান", "comment":"বিবরণ"})
            interactive_df(df_vacc_goat_rename)