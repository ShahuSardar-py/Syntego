import streamlit as st
from Home import manager

def Add():
    st.title("Add New Expense")
    st.caption("Add your expenses here.")

    with st.form("expesne_form"):
        exName= st.text_input("Enter Expense Title")
        exDate= st.date_input("Expense Date")
        exAmount= st.number_input("Amount Spent", min_value=0)
        exDes= st.text_area("Description")
        exCategory= st.selectbox("Category of expense", ("Food 🍕", "Personal 👨 ", "Transport 🚌", "Investment 💱"))

        submitted = st.form_submit_button("Add ➕")
        if submitted:
            manager.addExpense(exDate,exName,exAmount,exCategory, exDes)
            st.toast("Added Expense! 🎉")

def calculator():
    with st.sidebar:
        with st.expander("Simple Calculator"):
            input=st.text_input("enter calculation")
            calculate=st.button("Calculate")
            if calculate:
                answer=eval(input)
                st.success(answer)
            


Add()
calculator()