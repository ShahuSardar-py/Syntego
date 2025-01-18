import streamlit as st
from Home import manager
import matplotlib.pyplot as plt
import pandas as pd


def report():
    st.title("Summary")
    expenses = manager.viewExpenses()
    total = manager.expenses["Amount"].sum()
    if not expenses.empty:
        category_summary = expenses.groupby("Category")["Amount"].sum()
        st.bar_chart(category_summary)
        st.metric(label="total spent", value=total, delta="1.2 °F")
        #total=expenses[("Amount")].sum()
        #col1= st.columns(1)
        #col1.metric(label="total spent", value=total, delta=1000)

    else:
        st.write("No data available for summary.")


report()