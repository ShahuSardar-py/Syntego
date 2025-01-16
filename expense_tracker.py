import streamlit as st
import pandas as pd

#expense class 
class Expense:
    def __init__(self, Name, Amount, Description, Date, Category): #the attributes 
        self.Name= Name
        self.Amount=Amount
        self.Description=Description
        self.Date=Date
        self.Category=Category

class ExpenseTracker:
    def __init__(self):
        self.expenses=[] #empty list to add the expenses
    
    def add(self,expense):
        self.expenses.append(expense)
        #append the expense into the list
    def deleteEx(self,index):
        if 0<= index < len(self.expenses):
            del self.expenses[index]
            st.warning('expense deleted', icon="⚠️")
        else:
            st.warning('invalid indesxx')

tracker=ExpenseTracker()

st.header("testing- works")





st.header("Add New Expense")
with st.form("expense_form", clear_on_submit=True):
    expense_name = st.text_input("Name")
    expense_amount = st.number_input("Amount", min_value=0.01, step=0.01)
    expense_description = st.text_area("Description")
    expense_date = st.date_input("Date")
    expense_category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Shopping", "Other"])
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        # Create an Expense object and add it to the tracker
        new_expense = Expense(expense_name, expense_amount, expense_description, expense_date, expense_category)
        tracker.add(new_expense)
        st.success("Expense added successfully!")

# Section for displaying expenses
st.header("Expenses Summary")
if tracker.expenses:
    # Convert expenses to a DataFrame for display
    expenses_data = [{
        "Name": e.Name,
        "Amount": e.Amount,
        "Description": e.Description,
        "Date": e.Date,
        "Category": e.Category
    } for e in tracker.expenses]
    expenses_df = pd.DataFrame(expenses_data)

    st.table(expenses_df)

    # Option to delete an expense
    st.subheader("Delete an Expense")
    expense_index = st.number_input("Enter the index of the expense to delete:", min_value=0, max_value=len(tracker.expenses) - 1, step=1)
    if st.button("Delete Expense"):
        tracker.delete_ex(expense_index)
else:
    st.write("No expenses added yet!")

