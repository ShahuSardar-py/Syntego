import streamlit as st
import pandas as pd

from utils.expenseTracker import ExpenseManager
st.set_page_config(page_title="Syntego",
                   page_icon="💲")


st.title(" hello world-syntego 👋")

manager = ExpenseManager()