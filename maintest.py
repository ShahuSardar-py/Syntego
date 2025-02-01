import streamlit as st
import pandas as pd
import sqlite3
import time

from utils.test import ExpenseManager
from utils.test import IncomeManager
from utils.test import Account
from auth import AuthManager

st.set_page_config(page_title="Syntego", page_icon="💲")

st.title("💰 Personal Finance Manager")

auth = AuthManager()

# Session state for tracking login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

with tab1:
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if auth.login_user(email, password):
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success("Login successful! Redirecting...")
            time.sleep(1.5)
            st.rerun()

        else:
            st.error("Invalid email or password.")

with tab2:
    st.subheader("Register")
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    register_btn = st.button("Register")

    if register_btn:
        if auth.register_user(new_email, new_password):
            st.success("Registration successful! Please log in.")
        else:
            st.error("Email already exists.")

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


