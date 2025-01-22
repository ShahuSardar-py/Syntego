import streamlit as st
from utils.test import Account

st.title("Transaction Entry")
st.subheader("Log Your Expenses Or Income")

#  Get user identifier from the user
user_id = st.text_input("Enter a unique user identifier (Probably your name with DOB or email):", key="user_id")

# Initialize account and current_balance only if user_id is provided
if user_id:
    db_name = f"{user_id}.db"  

    # Initialize the Account object with the dynamically created db_name
    account = Account(db_name=db_name)

    # Get the current balance for the user
    current_balance = account.getBalance()
    st.markdown(f'Your Current Balance is: :red[{current_balance}]')
else:
    st.warning("Please enter a valid user identifier to proceed.")
    account = None
    current_balance = None  # Default if no user_id is entered

st.divider()

# Add Expense
with st.expander("Add New Expense ⬆"):
    if account:  # Ensure operations work only when account is initialized
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
                # Update the current balance
                current_balance = account.getBalance()
                st.markdown(f'Updated Balance: :red[{current_balance}]')
    else:
        st.info("Please enter a user ID to add an expense.")

# Add Income
with st.expander("Add New Income ⬇"):
    if account:  # Ensure operations work only when account is initialized
        with st.form("income_form"):
            InName = st.text_input("Income Title")
            InDate = st.date_input("Income Date")
            InAmount = st.number_input("Amount Received", min_value=0.0)
            InDes = st.text_area("Description")
            InSource = st.selectbox("Source Of Income", ("-", "Salary 💳", "Family 👨", "Investment 💱", "Other"))

            submit2 = st.form_submit_button("Add Income ➕")
            if submit2:
                account.addIncome(InDate, InName, InAmount, InSource, InDes)
                st.toast("Added Income! 🎉")
                # Update the current balance
                current_balance = account.getBalance()
                st.markdown(f'Updated Balance: :red[{current_balance}]')
    else:
        st.info("Please enter a user ID to add income.")

# Calculator
with st.sidebar:
    with st.expander("Calculator 🧮"):
        input_calc = st.text_input("Enter calculation")
        calculate = st.button("Calculate")
        if calculate:
            try:
                answer = eval(input_calc)
                st.success(answer)
            except Exception as e:
                st.error(f"Invalid input: {e}")
