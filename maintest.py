import streamlit as st
import pandas as pd
import sqlite3

from utils.test import ExpenseManager
from utils.test import IncomeManager
from utils.test import Account

# Set up the page configuration for Streamlit
st.set_page_config(page_title="Syntego", page_icon="💲")

st.title("Hello World - Syntego 👋")

# Dynamically set the database name
db_name = "expenses.db"

# Initialize the managers with the database name
ExManager = ExpenseManager(db_name=db_name)
InManager = IncomeManager(db_name=db_name)
account = Account(db_name=db_name)

# Establish SQLite database connection for testing
conn = sqlite3.connect(db_name)
c = conn.cursor()

# Toast notification
st.toast("EVERYTHING GOOD HERE!")


# Close the connection
conn.close()
