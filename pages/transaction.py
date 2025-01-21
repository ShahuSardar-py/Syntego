import streamlit as st
from utils.test import Account

# Initialize the Account object
account = Account()

st.title("Transaction Entry")
st.subheader("Log Your Expenses Or Income")

CurrentBalance = account.getBalance()
st.markdown(f'Your Current Balance is: :red[{CurrentBalance}]')

st.divider()


# Add Expense
with st.expander("Add New Expense ⬆"):
    with st.form("expense_form"):
        exName = st.text_input("Expense Title")
        exDate = st.date_input("Date Of Expense")
        exAmount = st.number_input("Amount Spent", min_value=0.0)
        exDes = st.text_area("Description")
        exCategory = st.selectbox("Category of expense", ("-", "Food 🍕", "Personal 👨", "Transport 🚌", "Investment 💱"))

        submit1 = st.form_submit_button("Add Expense ➕")
        if submit1:
            account.addExpense(exDate, exName, exAmount, exCategory, exDes)
            st.toast("Added Expense! 🎉")
    CurrentBalance = account.getBalance()
    st.markdown(f'Updated Balance: :red[{CurrentBalance}]')


# Add Income
with st.expander("Add New Income ⬇"):
    with st.form("income_form"):
        InName = st.text_input("Income Title")
        InDate = st.date_input("Income Date")
        InAmount = st.number_input("Amount Spent", min_value=0.0)
        InDes = st.text_area("Description")
        InSource = st.selectbox("Source Of Income", ("-", "Salary 💳", "Family 👨", "Investment 💱", "Other"))

        submit2 = st.form_submit_button("Add Income ➕")
        if submit2:
            account.addIncome(InDate, InName, InAmount, InSource, InDes)
            st.toast("Added income! 🎉")
    CurrentBalance = account.getBalance()
    st.markdown(f'Updated Balance: :red[{CurrentBalance}]')

# Calculator
with st.sidebar:
    with st.expander("Calculator 🧮"):
        input = st.text_input("Enter calculation")
        calculate = st.button("Calculate")
        if calculate:
            answer = eval(input)
            st.success(answer)



