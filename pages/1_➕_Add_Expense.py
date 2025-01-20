import streamlit as st
from Home import account


def Expense():
    st.title("Add New Expense")
    st.caption("Add your expenses here.")
    CurrentBalance=account.getBalance()
    st.write(CurrentBalance)

    with st.form("expesne_form"):
        exName= st.text_input("Enter Expense Title")
        exDate= st.date_input("Expense Date")
        exAmount= st.number_input("Amount Spent", min_value=0)
        exDes= st.text_area("Description")
        exCategory= st.selectbox("Category of expense", ("Food 🍕", "Personal 👨 ", "Transport 🚌", "Investment 💱"))

        submit1 = st.form_submit_button("Add ➕")
        if submit1:
            account.addExpense(exDate,exName,exAmount,exCategory, exDes)
            st.toast("Added Expense! 🎉")


def Income():
    st.title("Add New income")
    st.caption("Add your expincomesenses here.")
    CurrentBalance=account.getBalance()
    st.write(CurrentBalance)

    with st.form("income_form"):
        InName= st.text_input("Enter income Title")
        InDate= st.date_input("income Date")
        InAmount= st.number_input("Amount Spent", min_value=0)
        InDes= st.text_area("Description")
        InSource= st.selectbox("Category of expense", ("Salary 🍕", "Family 👨 ", "Freinds 🚌", "Investment 💱"))

        submit2 = st.form_submit_button("Add ➕")
        if submit2:
            account.addIncome(InDate,InName,InAmount,InSource, InDes)
            st.toast("Added income! 🎉")

def calculator():
    with st.sidebar:
        with st.expander("Simple Calculator"):
            input=st.text_input("enter calculation")
            calculate=st.button("Calculate")
            if calculate:
                answer=eval(input)
                st.success(answer)
            

with st.expander("Add Expense"):
    Expense()
with st.expander("Add income"):
    Income()

calculator()