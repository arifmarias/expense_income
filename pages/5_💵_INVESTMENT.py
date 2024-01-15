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
    options=["ইনভেস্টমেন্ট এন্ট্রি", "ইনভেস্টমেন্ট রিপোর্ট"],
    icons=["", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

if selected == "ইনভেস্টমেন্ট এন্ট্রি":
    # --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
    years = [datetime.today().year, datetime.today().year + 1]
    months = list(calendar.month_name[1:])
    d = st.date_input("তারিখ")
    year = d.year
    month = d.month
    day = d.day
    "---"
    with st.form("entry_form", clear_on_submit=True):
        with st.expander("ইনভেস্টমেন্ট"):
            invest_area = st.selectbox("খাত", options=("মাছ", "ছাগল", "জমি"))
            invest_amount = st.number_input("টাকার (৳) পরিমান")
        with st.expander("বিবরণ"):
            comment = st.text_area("", placeholder="Enter a comment here ...")
        
        "---"
        submitted = st.form_submit_button("Save Data")
    if submitted:
        input_date = str(day) + "/" + str(month) + "/" +str(year)
        year_month = str(year) + "_" + str(month)
        period = str(year)
        db.insert_period_invest(str(datetime.utcnow()), input_date, period, year_month,invest_area, invest_amount, comment)
        st.success("Data saved!")

if selected == "ইনভেস্টমেন্ট রিপোর্ট":
    with st.form("saved_periods"):
        items = db.fetch_all_periods_invest()
        df_invest = pd.DataFrame(items)
        # ----- SEARCHBOX ------------
        period = df_invest["period"].drop_duplicates().sort_values(ascending=False)
        year = st.selectbox("সাল সিলেক্ট করুন", period)
        left_column, right_column = st.columns(2)
        submitted = left_column.form_submit_button("রিপোর্ট")
        full_report = right_column.form_submit_button("ডিটেইল রিপোর্ট")
        if submitted:
            # ----- KPI ------------
            st.markdown("""---""")
            total_fish_invest = df_invest[(df_invest["period"] == year) & (df_invest["cat_investment"] == "মাছ") ]["amount"].sum()
            total_goat_invest = df_invest[(df_invest["period"] == year) & (df_invest["cat_investment"] == "ছাগল") ]["amount"].sum()
            total_land_invest = df_invest[(df_invest["period"] == year) & (df_invest["cat_investment"] == "জমি") ]["amount"].sum()
            left_column, middle_column, right_column = st.columns(3)
            with left_column:
                st.subheader("মাছ 🐠")
                st.subheader(f"৳ {total_fish_invest:,}")
            with middle_column:
                st.subheader("ছাগল 🐐")
                st.subheader(f"৳ {total_goat_invest:,}")
            with right_column:
                st.subheader("জমি 🌆")
                st.subheader(f"৳ {total_land_invest:,}")
            st.markdown("""---""")
            investment_by_categories = df_invest[(df_invest["period"] == year)].groupby(by=["cat_investment"]).sum()[['amount']].sort_values(by="amount", ascending = False)
            fig_invest = px.pie(investment_by_categories, values='amount', names=investment_by_categories.index, title="খাত অনুযায়ী ইনভেস্টমেন্ট")
            st.plotly_chart(fig_invest, use_container_width=True)
        
        if full_report:
            st.markdown("""---""")
            st.write(year + "- সালের ইনভেস্টমেন্টের ডিটেইল রিপোর্ট")
            df_invest_detail = df_invest[(df_invest["period"] == year)][["input_date", "cat_investment","amount","comment"]]
            df_invest_detail_rename = df_invest_detail.rename(columns= {"input_date": "তারিখ", "cat_investment":"ইনভেস্টমেন্টের খাত", "amount":"মোট টাকা", "comment":"বিবরণ"})
            interactive_df(df_invest_detail_rename)
            

        
