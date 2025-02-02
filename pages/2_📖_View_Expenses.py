import streamlit as st
from utils.expenseTracker import Account  
import time

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in first.")
    st.stop()

user_email = st.session_state.user_email
db_name = f"{user_email}.db"  

account = Account(db_name=db_name)

st.title("Your Transactions")

# Expenses Section
st.subheader("📉 Expenses")
expenses_df = account.expenseList()
if expenses_df.empty:
    st.write("No expenses added yet.")
else:
    st.dataframe(expenses_df)

# Delete Expense
with st.expander("🗑️ Delete Expense"):
    with st.form("delete_expense_form"):
        expense_id = st.number_input("Enter Expense ID to Delete", min_value=0, step=1)
        if st.form_submit_button("Delete Expense"):
            account.deleteExpense(expense_id)
            st.toast("✅ Expense Deleted Successfully!")
            time.sleep(1.5)
            st.rerun()

# Income Section
st.subheader("📈 Income")
income_df = account.incomeList()
if income_df.empty:
    st.write("No income data added.")
else:
    st.dataframe(income_df)

# Delete Income
with st.expander("🗑️ Delete Income"):
    with st.form("delete_income_form"):
        income_id = st.number_input("Enter Income ID to Delete", min_value=0, step=1)
        if st.form_submit_button("Delete Income"):
            account.deleteIncome(income_id)
            st.toast("✅ Income Deleted Successfully!")
            time.sleep(1.5)
            st.rerun()
