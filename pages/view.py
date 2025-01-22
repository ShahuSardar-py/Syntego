import streamlit as st
from utils.test import Account  

user_id = st.text_input("Enter a unique user identifier (e.g., your name with DOB or email):", key="user_id")

if user_id:
    db_name = f"{user_id}.db"  

    
    account = Account(db_name=db_name)

    # Function to show expenses table
    def show_expenses():
        st.title("Your Expense Record")
        st.caption("View all expenses here")
        expenses_df = account.expenseList()  
        if expenses_df.empty:
            st.write("Looks like no expenses added yet!")
        else:
            st.dataframe(expenses_df)  

    # Function to show income table
    def show_income():
        st.title("Your Income Record")
        st.caption("View all income records here")
        income_df = account.incomeList()
        if income_df.empty:
            st.write("Looks like no income records added yet!")
        else:
            st.dataframe(income_df) 

    # Delete an expense record
    def delete_expense():
        st.subheader("Delete An Expense Record")
        with st.form("delete_expense_form"):
            expense_id = st.number_input("Enter Expense ID to Delete", min_value=0, step=1)
            delete_button = st.form_submit_button("Delete Expense")
            if delete_button:
                account.deleteExpense(expense_id)  
                st.toast("Expense Deleted Successfully! 🎉")

    # Delete an income record
    def delete_income():
        st.subheader("Delete An Income Record")
        with st.form("delete_income_form"):
            income_id = st.number_input("Enter Income ID to Delete", min_value=0, step=1)
            delete_button = st.form_submit_button("Delete Income")
            if delete_button:
                account.deleteIncome(income_id) 
                st.toast("Income Deleted Successfully! 🎉")

    # Display the expense and income records
    with st.expander("View Expenses"):
        show_expenses()
        delete_expense()

    with st.expander("View Income"):
        show_income()
        delete_income()

else:
    st.warning("Please enter a valid user identifier to view or manage records.")
