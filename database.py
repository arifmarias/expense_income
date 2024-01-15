import os 
import streamlit as st  # pip install streamlit
from deta import Deta  # pip install deta
from dotenv import load_dotenv
from datetime import datetime



# Load the environment variables
load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")
# DETA_KEY = st.secrets["DETA_KEY"]

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db_f = deta.Base("monthly_reports_fish")
db_g = deta.Base("monthly_reports_goat")
db_in = deta.Base("investment")
db_vaccine = deta.Base("vaccination")
db_goat = deta.Base("goat_info")
db_self_cal = deta.Base("hero_calc")


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

# ---- GOAT INFO DB ----- 
# db.insert_period_invest(str(datetime.utcnow()), input_date, period, year_month, goat_number, breed,gender,color,purchase_or_birth,age,weight,purchase_price,comment)
def insert_new_animal(current, input_date, period, year_month, goat_number, breed, gender, color, purchase_or_birth, age, weight, purchase_price, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db_goat.put({"key": current, "input_date": input_date, "period": period, "year_month": year_month, "goat_number": goat_number, "breed": breed, "gender":gender, "color":color, "purchase_or_birth":purchase_or_birth, "age":age, "weight":weight, "purchase_price":purchase_price, "comment": comment})

def fetch_all_periods_animal():
    """Returns a dict of all periods"""
    res = db_goat.fetch()
    return res.items

# ---- VACCINATION DB ----- 
# db.insert_new_vaccination(str(datetime.utcnow()), input_date, period, year_month, gt, reason, med, med_measure,comment)
def insert_new_vaccination(current, input_date, period, year_month, goat_number, reason, med, med_measure, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db_vaccine.put({"key": current, "input_date": input_date, "period": period, "year_month": year_month, "goat_number": goat_number, "reason": reason, "med":med, "med_measure":med_measure, "comment": comment})

def fetch_all_periods_vaccination():
    """Returns a dict of all periods"""
    res = db_vaccine.fetch()
    return res.items

# ---- HERO DB ----- 
# db.insert_period_invest(str(datetime.utcnow()), input_date, period, year_month, invest_amount, total_investment, spend_amount, total_spend, total_balance, comment)
def insert_period_hero(current, input_date, period, year_month, invest_amount, total_investment, spend_amount, total_spend, total_balance, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db_self_cal.put({"key": current, "input_date": input_date, "period": period, "year_month": year_month, "invest_amount": invest_amount,"total_investment": total_investment, "spend_amount": spend_amount,"total_spend": total_spend, "total_balance":total_balance, "comment": comment})


def fetch_all_periods_hero():
    """Returns a dict of all periods"""
    res = db_self_cal.fetch()
    return res.items