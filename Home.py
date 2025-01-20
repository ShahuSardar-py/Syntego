import streamlit as st
import pandas as pd

from utils.expenseTracker import ExpenseManager
from utils.expenseTracker import IncomeManager
from utils.expenseTracker import Account
st.set_page_config(page_title="Syntego",
                   page_icon="💲")


st.title(" hello world-syntego 👋")

ExManager = ExpenseManager()
InManager= IncomeManager()
account=Account()

st.toast("EVERYTHIN GOOD HERE!")

