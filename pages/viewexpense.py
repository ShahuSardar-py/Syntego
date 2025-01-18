import streamlit as st
from Home import manager

def View():
    st.title("Your Expenses")
    st.caption("View all expenses here")
    expenses= manager.viewExpenses()
    if expenses.empty:
        st.write("Looks like no expenses added yet! ")
    else:
        st.table(expenses)


View()

        
