import streamlit as st
from Home import manager
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_icon='📊',
                   page_title="Financial Report")

st.title("Your Expense Report 📄")
st.write("Explore & understand your expenses using cool graphs")
st.divider()

#METRICS
col1, col2, col3 = st.columns(3)
expenses = manager.viewExpenses()

total_spent=manager.expenses['Amount'].sum()
with col1:
    st.metric(label="total spent", value=total_spent)
with col2:
    st.metric(label="total spent", value=total_spent)
with col3:
    st.metric(label="total spent", value=total_spent)



#def report():
    #st.title("Summary")
    #expenses = manager.viewExpenses()
    #total = manager.expenses["Amount"].sum()
    #if not expenses.empty:
        #category_summary = expenses.groupby("Category")["Amount"].sum()
        #st.bar_chart(category_summary)
        #st.metric(label="total spent", value=total)

        #NOT WOKRING YET
        #total=expenses[("Amount")].sum()
        #col1= st.columns(1)
        #col1.metric(label="total spent", value=total, delta=1000)

    #else:
        #st.write("No data available for summary.")

