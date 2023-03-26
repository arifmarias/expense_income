import os 
import streamlit as st  # pip install streamlit
from deta import Deta  # pip install deta
from dotenv import load_dotenv
from datetime import datetime



# Load the environment variables
# load_dotenv(".env")
# DETA_KEY = os.getenv("DETA_KEY")
DETA_KEY = st.secrets["DETA_KEY"]

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db_f = deta.Base("monthly_reports_fish")
db_g = deta.Base("monthly_reports_goat")
db_in = deta.Base("investment")


# ---- Fish DB ----- 
def insert_period(current, input_date, period, year_month, cat_income, incomes, cat_expenses, expenses, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db_f.put({"key": current, "input_date": input_date, "period": period, "year_month": year_month, "incomes_cat": cat_income,"incomes": incomes, "expenses_cat": cat_expenses,"expenses": expenses, "comment": comment})


def fetch_all_periods():
    """Returns a dict of all periods"""
    res = db_f.fetch()
    return res.items

def get_period(period):
    """If not found, the function will return None"""
    return db_f.get(period)

# ---- Goat DB ----- 

def insert_period_goat(current, input_date, period, year_month, cat_income, incomes, cat_expenses, expenses, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db_g.put({"key": current, "input_date": input_date, "period": period, "year_month": year_month, "incomes_cat": cat_income,"incomes": incomes, "expenses_cat": cat_expenses,"expenses": expenses, "comment": comment})


def fetch_all_periods_goat():
    """Returns a dict of all periods"""
    res = db_g.fetch()
    return res.items

def get_period_goat(period):
    """If not found, the function will return None"""
    return db_g.get(period)

# ---- Investment DB ----- 
def insert_period_invest(current, input_date, period, year_month, cat_investment, amount, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db_in.put({"key": current, "input_date": input_date, "period": period, "year_month": year_month, "cat_investment": cat_investment,"amount": amount, "comment": comment})


def fetch_all_periods_invest():
    """Returns a dict of all periods"""
    res = db_in.fetch()
    return res.items

