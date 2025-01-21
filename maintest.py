import streamlit as st
import pandas as pd
import sqlite3

from utils.test import ExpenseManager
from utils.test import IncomeManager
from utils.test import Account
st.set_page_config(page_title="Syntego",
                   page_icon="💲")


st.title(" hello world-syntego 👋")

ExManager = ExpenseManager()
InManager= IncomeManager()
account=Account()

# Establish SQLite database connection
conn = sqlite3.connect('expenses.db')  
c = conn.cursor()
st.toast("EVERYTHING GOOD HERE!")

conn.close()
